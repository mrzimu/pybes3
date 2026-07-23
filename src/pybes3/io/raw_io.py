from __future__ import annotations

import enum
import glob
from pathlib import Path
from typing import Union

import awkward as ak
import awkward.contents
import awkward.index
import numpy as np
from numpy.typing import NDArray
from uproot._util import regularize_filter

import pybes3.io._reid as _reid
from pybes3.data import CGEM_ELEC_TABLE
from pybes3.kernels._io import read_bes_raw

_info_tables: dict[str, np.ndarray] = None

_RAW_FIELDS = [
    "cgem",
    "mdc",
    "tof",
    "emc",
    "muc",
    "trigGTD",
]


class BesFlag(enum.IntEnum):
    FILE_START = 0x1234AAAA
    FILE_NAME = 0x1234AABB
    RUN_PARAMS = 0x1234BBBB
    DATA_SEPERATOR = 0x1234CCCC
    FILE_TAIL_START = 0x1234DDDD
    FILE_END = 0x1234EEEE

    FULL_EVENT_FRAGMENT = 0xAA1234AA
    SUB_DETECTOR = 0xBB1234BB
    ROS = 0xCC1234CC
    ROB = 0xDD1234DD
    ROD = 0xEE1234EE


def _raw_dict_to_ak(raw_dict: dict[str, object]) -> ak.Array:
    contents = {}

    for field_name in ["evt_header", "cgem", "mdc", "tof", "emc", "muc", "trigGTD"]:
        if field_name not in raw_dict:
            continue

        org_data = raw_dict[field_name]

        if field_name == "evt_header":
            contents[field_name] = awkward.contents.RecordArray(
                [awkward.contents.NumpyArray(i) for i in org_data.values()],
                list(org_data.keys()),
            )

        elif field_name in ["cgem", "mdc", "tof", "emc", "muc", "trigGTD"]:
            offsets, data_dict = org_data
            contents[field_name] = awkward.contents.ListOffsetArray(
                awkward.index.Index(offsets),
                awkward.contents.RecordArray(
                    [awkward.contents.NumpyArray(i) for i in data_dict.values()],
                    list(data_dict.keys()),
                ),
            )
        else:
            offsets, data = org_data
            contents[field_name] = awkward.contents.ListOffsetArray(
                awkward.index.Index(offsets),
                awkward.contents.NumpyArray(data),
            )

    return ak.Array(contents)


class RawBinaryReader:
    def __init__(self, file: str):
        # load cgem-elec-table
        global _info_tables
        if _info_tables is None:
            _info_tables = {}

            with np.load(CGEM_ELEC_TABLE) as f:
                cgem_elec_table = dict(f)

            for k, v in cgem_elec_table.items():
                _info_tables[f"cgem_{k}"] = v

            _info_tables["mdc_re2te"] = _reid.build_mdc_re2te()
            _info_tables["tof_re2te"] = _reid.build_tof_re2te()
            _info_tables["emc_re2te"] = _reid.build_emc_re2te()
            _info_tables["muc_re2te"] = _reid.build_muc_re2te()
            _info_tables["muc_strsqc"] = _reid.build_muc_strsqc()

        self.path = str(Path(file).resolve())
        self._file = open(file, "rb")

        self.file_version: int = -1
        self.file_number: int = -1
        self.file_date: int = -1
        self.file_time: int = -1

        self.app_name: str = None
        self.app_tag: str = None

        self.run_number: int = -1
        self.max_events: int = -1
        self.rec_enable: int = -1
        self.trigger_type: int = -1
        self.detector_mask: int = -1
        self.beam_type: int = -1
        self.beam_energy: int = -1

        self.entries: int = -1

        self._data_start: int = 0  # in char
        self._data_end: int = 0  # in char
        self.size: int = 0  # in char
        self._data_size: int = 0  # in char

        self._entry_starts: np.ndarray = None  # in char
        self._entry_stops: np.ndarray = None  # in char
        self._max_looped_entry: int = -1

        self._preprocess_file()

    def close(self) -> None:
        self._file.close()

    def arrays(
        self,
        *,
        entry_start: int = 0,
        entry_stop: int = -1,
        filter_name: Union[str, list, None] = None,
    ) -> ak.Array:
        """
        Read and return arrays of data from the BES raw file.

        Parameters:
            entry_start (int, optional): The starting entry to read. Defaults to 0.
            entry_stop (int, optional): The stopping entry to read. Defaults to -1, which means read all entries.
            filter_name (Union[str, list, None], optional): A filter to select specific fields to read. Defaults to `None`, which means read all fields.

        Returns:
            An Awkward Array containing the read data.
        """
        # process parameters
        if entry_stop == -1:
            entry_stop = self.entries
        entry_stop = min(entry_stop, self.entries)

        filter_func = regularize_filter(filter_name)
        fields = [field for field in _RAW_FIELDS if filter_func(field)]

        batch_data = self._read_event(entry_start, entry_stop)

        org_dict = read_bes_raw(batch_data, fields, _info_tables)
        return _raw_dict_to_ak(org_dict)

    def _read(self) -> int:
        return int.from_bytes(self._file.read(4), "little")

    def _skip(self, n: int = 1) -> None:
        self._file.seek(4 * n, 1)

    def _preprocess_file(self):
        # file header
        assert self._read() == BesFlag.FILE_START, "Invalid start flag"
        self._skip()

        self.file_version = self._read()
        self.file_number = self._read()
        self.file_date = self._read()
        self.file_time = self._read()
        self._skip(2)

        # file name
        assert self._read() == BesFlag.FILE_NAME, "Invalid file name flag"

        nchar_name = self._read()
        nbytes_name = np.ceil(nchar_name / 4).astype(int)
        self.file_name = self._file.read(nbytes_name * 4).decode("utf-8").strip()

        nchar_tag = self._read()
        nbytes_tag = np.ceil(nchar_tag / 4).astype(int)
        self.file_tag = self._file.read(nbytes_tag * 4).decode("utf-8").strip()

        # run parameters
        assert self._read() == BesFlag.RUN_PARAMS, "Invalid run params flag"
        self._skip()

        self.run_number = self._read()
        self.max_events = self._read()
        self.rec_enable = self._read()
        self.trigger_type = self._read()
        self.detector_mask = self._read()
        self.beam_type = self._read()
        self.beam_energy = self._read()

        # other information
        self._data_start = self._file.tell()
        self._file.seek(0, 2)
        self.size = self._file.tell()
        self._data_end = self.size - 10 * 4
        self._data_size = self._data_end - self._data_start

        # read file tail
        self._file.seek(-10 * 4, 2)
        assert self._read() == BesFlag.FILE_TAIL_START, "Invalid file tail start flag"
        self._skip(3)
        self.entries = self._read()
        self._skip(4)
        assert self._read() == BesFlag.FILE_END, "Invalid file end flag"

        # post process
        self._entry_starts = np.full(self.entries, -1, dtype=np.int64)
        self._entry_stops = np.full(self.entries, -1, dtype=np.int64)
        self._reset_cursor()

    def _reset_cursor(self) -> None:
        self._file.seek(self._data_start)

    def _skip_event(self) -> tuple[int, int]:
        flag = self._read()
        if flag == BesFlag.DATA_SEPERATOR:
            self._skip(3)
            flag = self._read()

        assert flag == BesFlag.FULL_EVENT_FRAGMENT, "Invalid event fragment flag"
        pos_start = self._file.tell() - 4

        total_size = self._read()
        self._skip(total_size - 2)
        pos_end = self._file.tell()

        return pos_start, pos_end

    def _read_block(self, n_blocks: int) -> NDArray[np.uint32]:
        """
        Read a batch of data with the specified number of blocks.
          - If n_blocks < 0, read all data.
          - If n_blocks >= 0, read n_blocks blocks of data. Each block is separated by a DATA_SEPERATOR flag.

        This method is designed for generating testing data.

        Parameters:
            n_blocks: The number of blocks to read. If negative, read all data.

        Returns:
            NDArray[np.uint32]: The batch of data read.
        """

        self._reset_cursor()
        if n_blocks < 0:
            return np.frombuffer(self._file.read(self._data_size), dtype=np.uint32)

        for _ in range(n_blocks):
            if self._file.tell() >= self._data_end:
                assert self._file.tell() == self._data_end, "Invalid data end"
                break

            assert self._read() == BesFlag.DATA_SEPERATOR, "Invalid data seperator flag"
            self._skip(2)
            block_size = self._read()
            self._skip(block_size // 4)

        pos_end = self._file.tell()

        self._file.seek(self._data_start)
        batch_data = np.frombuffer(
            self._file.read(pos_end - self._data_start), dtype=np.uint32
        )

        return batch_data

    def _read_event(self, entry_start: int, entry_stop: int) -> np.ndarray:
        if entry_start >= entry_stop or entry_start >= self.entries:
            return np.array([], dtype=np.uint32)

        pos_start = None
        pos_stop = None
        if entry_start == 0:
            pos_start = self._data_start
        if entry_stop == self.entries:
            pos_stop = self._data_end

        if pos_start is not None and pos_stop is not None:
            self._file.seek(self._data_start)
            return np.frombuffer(self._file.read(self._data_size), dtype=np.uint32)

        cur_entry = self._max_looped_entry

        # move cursor to the maximum position of the already looped events to avoid unnecessary skipping
        if cur_entry < 0:
            self._file.seek(self._data_start)
        else:
            self._file.seek(self._entry_stops[cur_entry])

        # loop until the entry_start-1 entry is reached, to record the start position of the entry_start entry
        if pos_start is None:
            while cur_entry < entry_start:
                cur_entry += 1
                self._entry_starts[cur_entry], self._entry_stops[cur_entry] = (
                    self._skip_event()
                )

            self._max_looped_entry = cur_entry
            pos_start = self._entry_starts[entry_start]

        # loop until the entry_stop-1 entry is reached, to record the stop position of the entry_stop entry
        if pos_stop is None:
            while cur_entry < entry_stop - 1:
                cur_entry += 1
                self._entry_starts[cur_entry], self._entry_stops[cur_entry] = (
                    self._skip_event()
                )

            self._max_looped_entry = cur_entry
            pos_stop = self._entry_stops[entry_stop - 1]

        # read the target entries
        self._file.seek(pos_start)
        return np.frombuffer(
            self._file.read(pos_stop - pos_start),
            dtype=np.uint32,
        )

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._file.close()

    def __repr__(self) -> str:
        file_name = Path(self.path).name
        size = int(self.size / 1024 / 1024)
        return f"<RawData filename='{file_name}' Entries={self.entries} Size='{size} MB'>"


def _is_raw(file: str | Path) -> bool:
    with open(file, "rb") as f:
        return int.from_bytes(f.read(4), "little") == BesFlag.FILE_START


def concatenate(
    files: str | Path | list[str | Path],
    *,
    entry_start: int = 0,
    entry_stop: int = -1,
    filter_name: Union[str, list, None] = None,
    verbose: bool = False,
) -> ak.Array:
    """
    Concatenate multiple raw binary files into `ak.Array`

    Parameters:
        files (str | Path | list[str | Path]): files to be read.
        entry_start (int, optional): The starting entry to read. Defaults to 0.
        entry_stop (int, optional): The stopping entry to read. Defaults to -1, which means read until the end.
        filter_name (Union[str, list, None], optional): A filter to select specific fields to read. Defaults to `None`, which means read all fields.
        verbose (bool, optional): Show reading process. Defaults to `False`.

    Returns:
        Concatenated raw data array.
    """
    if not isinstance(files, list):
        files = glob.glob(files, recursive=True)

    files = [str(Path(file).resolve()) for file in files if _is_raw(file)]

    if len(files) == 0:
        raise ValueError("No valid raw files found")

    n_cum_entries = 0
    readers_with_entry_range: list[tuple[RawBinaryReader, int, int]] = []
    for file in files:
        reader = RawBinaryReader(file)

        if n_cum_entries + reader.entries < entry_start:
            n_cum_entries += reader.entries
            continue

        entry_start_for_reader = None
        entry_stop_for_reader = None

        # entry_start for this reader
        if n_cum_entries < entry_start and n_cum_entries + reader.entries >= entry_start:
            entry_start_for_reader = entry_start - n_cum_entries
        else:
            entry_start_for_reader = 0

        # entry_stop for this reader
        if entry_stop < 0:
            entry_stop_for_reader = -1
        elif n_cum_entries <= entry_stop and n_cum_entries + reader.entries > entry_stop:
            entry_stop_for_reader = entry_stop - n_cum_entries
        else:
            entry_stop_for_reader = -1

        readers_with_entry_range.append(
            (reader, entry_start_for_reader, entry_stop_for_reader)
        )

        n_cum_entries += reader.entries
        if entry_stop >= 0 and n_cum_entries >= entry_stop:
            break

    try:
        res = []
        n_cum_read = 0
        for (
            reader,
            entry_start_for_reader,
            entry_stop_for_reader,
        ) in readers_with_entry_range:
            n_read = (
                entry_stop_for_reader - entry_start_for_reader
                if entry_stop_for_reader >= 0
                else reader.entries - entry_start_for_reader
            )

            if verbose:
                print(
                    f"Reading file {reader.path}: {n_cum_read} -> {n_cum_read + n_read} entries ...",
                )

            res.append(
                reader.arrays(
                    entry_start=entry_start_for_reader,
                    entry_stop=entry_stop_for_reader,
                    filter_name=filter_name,
                )
            )

            n_cum_read += n_read
    finally:
        for reader, _, _ in readers_with_entry_range:
            reader.close()

    if len(res) == 0:
        return ak.Array([])

    return ak.concatenate(res)
