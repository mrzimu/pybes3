from __future__ import annotations

import enum
import glob
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import awkward as ak
import awkward.contents
import awkward.index
import numpy as np
from numpy.typing import NDArray
from uproot._util import regularize_filter

from pybes3.data import CGEM_ELEC_TABLE
from pybes3.io import _reid
from pybes3.kernels._io import RawFileReader

_info_tables: dict[str, np.ndarray] | None = None

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
    """
    Sequential and random-access reader for a BES3 raw file.

    Instances are created by `pybes3.open_raw`. The file is opened on construction and
    must be released with `close()` or a `with` block.
    """

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
        self._reader = RawFileReader(self.path)

    @property
    def file_version(self) -> int:
        """
        Version of the file format.
        """
        return self._reader.file_version

    @property
    def file_number(self) -> int:
        """
        Number of the file in the run.
        """
        return self._reader.file_number

    @property
    def file_date(self) -> int:
        """
        Creation date of the file.
        """
        return self._reader.file_date

    @property
    def file_time(self) -> int:
        """
        Creation time of the file.
        """
        return self._reader.file_time

    @property
    def file_name(self) -> str:
        """
        Name stored in the file header.
        """
        return self._reader.file_name

    @property
    def file_tag(self) -> str:
        """
        Tag stored in the file header.
        """
        return self._reader.file_tag

    @property
    def run_number(self) -> int:
        """
        Run number.
        """
        return self._reader.run_number

    @property
    def max_events(self) -> int:
        """
        Maximum number of events the run can contain.
        """
        return self._reader.max_events

    @property
    def rec_enable(self) -> int:
        """
        Reconstruction flag of the run.
        """
        return self._reader.rec_enable

    @property
    def trigger_type(self) -> int:
        """
        Trigger type of the run.
        """
        return self._reader.trigger_type

    @property
    def detector_mask(self) -> int:
        """
        Detector mask of the run.
        """
        return self._reader.detector_mask

    @property
    def beam_type(self) -> int:
        """
        Beam type of the run.
        """
        return self._reader.beam_type

    @property
    def beam_energy(self) -> int:
        """
        Beam energy of the run.
        """
        return self._reader.beam_energy

    @property
    def entries(self) -> int:
        """
        Number of events in the file.
        """
        return self._reader.entries

    @property
    def size(self) -> int:
        """
        File size in bytes.
        """
        return self._reader.size

    @property
    def _data_start(self) -> int:
        """
        Byte offset of the first event.
        """
        return self._reader.data_start

    @property
    def _data_end(self) -> int:
        """
        Byte offset of the end of the data section.
        """
        return self._reader.data_end

    @property
    def closed(self) -> bool:
        """
        Whether the file is closed.
        """
        return self._reader.closed

    def close(self) -> None:
        """
        Close the file.
        """
        self._reader.close()

    @property
    def index_status(self) -> str:
        """
        Return the state of the in-memory entry index.

        The index is built lazily while reading: opening a file does not scan it,
        and reading from entry 0 never needs it.

        Returns:
            `"complete"`, `"partial"` or `"missing"`.
        """
        valid = self._reader.index_valid()
        if self.entries == 0 or valid >= self.entries:
            return "complete"
        return "partial" if valid > 0 else "missing"

    def arrays(
        self,
        *,
        entry_start: int = 0,
        entry_stop: int | None = None,
        filter_name: str | list | None = None,
    ) -> ak.Array:
        """
        Read and return arrays of data from the BES raw file.

        Parameters:
            entry_start (int, optional): The starting entry to read. Defaults to 0.
            entry_stop (int, optional): The stopping entry to read. Defaults to `None`, which means read all entries. `-1` is accepted as an alias of `None`.
            filter_name (Union[str, list, None], optional): A filter to select specific fields to read. Defaults to `None`, which means read all fields.

        Returns:
            An Awkward Array containing the read data.

        Raises:
            ValueError: If `entry_start` is negative or the file is closed.
        """
        start, stop = _normalize_range(self.entries, entry_start, entry_stop)
        fields = _select_fields(filter_name)

        org_dict = self._reader.read(start, stop - start, fields, _info_tables)
        return _raw_dict_to_ak(org_dict)

    def iterate(
        self,
        *,
        step_size: int = 5000,
        entry_start: int = 0,
        entry_stop: int | None = None,
        filter_name: str | list | None = None,
        report: bool = False,
    ) -> Iterator[ak.Array | tuple[int, int, ak.Array]]:
        """
        Iterate over the entries in batches.

        Parameters:
            step_size (int, optional): Number of entries per batch. Defaults to 5000.
            entry_start (int, optional): The first entry to read. Defaults to 0.
            entry_stop (int, optional): The entry to stop at. Defaults to `None`, which means read until the end.
            filter_name (Union[str, list, None], optional): A filter to select specific fields to read. Defaults to `None`, which means read all fields.
            report (bool, optional): If `True`, yield `(start, stop, array)` tuples. Defaults to `False`.

        Returns:
            An iterator of Awkward Arrays, or of `(start, stop, array)` tuples.

        Raises:
            ValueError: If `step_size` is not a positive integer.
        """
        if not isinstance(step_size, (int, np.integer)) or step_size <= 0:
            raise ValueError(f"step_size must be a positive integer, got {step_size!r}")

        start, stop = _normalize_range(self.entries, entry_start, entry_stop)
        fields = _select_fields(filter_name)

        return self._iterate(start, stop, int(step_size), fields, report)

    def _iterate(
        self,
        start: int,
        stop: int,
        step_size: int,
        fields: list[str],
        report: bool,
    ) -> Iterator[ak.Array | tuple[int, int, ak.Array]]:
        pos = start
        while pos < stop:
            count = min(step_size, stop - pos)
            array = _raw_dict_to_ak(self._reader.read(pos, count, fields, _info_tables))
            yield (pos, pos + count, array) if report else array
            pos += count

    @property
    def entry_byte_offsets(self) -> NDArray[np.int64]:
        """
        Return the byte offset of every entry, followed by the end of the data section.

        The first access scans the file once; the offsets are kept in the reader and
        reused by later reads.

        Raises:
            ValueError: If the file is closed.
        """
        if self.closed:
            raise ValueError("I/O operation on closed raw file")

        self._reader.build_entry_index()

        starts = np.asarray(self._reader.entry_starts(), dtype=np.int64)
        return np.append(starts, self._data_end)

    def read_block(self, n_blocks: int = -1) -> NDArray[np.uint32]:
        """
        Read raw 32-bit words from the data section.

        This method is designed for generating testing data.

        Parameters:
            n_blocks (int, optional): The number of data blocks to read. If negative, read the whole data section. Defaults to -1.

        Returns:
            The requested words of the data section.

        Raises:
            ValueError: If the file is closed.
        """
        return self._reader.read_block(n_blocks)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __repr__(self) -> str:
        file_name = Path(self.path).name
        size = int(self.size / 1024 / 1024)
        return f"<RawData filename='{file_name}' Entries={self.entries} Size='{size} MB'>"


def _is_raw(file: str | Path) -> bool:
    with open(file, "rb") as f:
        return int.from_bytes(f.read(4), "little") == BesFlag.FILE_START


def _normalize_range(
    entries: int,
    entry_start: int | None,
    entry_stop: int | None,
) -> tuple[int, int]:
    """
    Normalize an entry range against a total number of entries.
    """
    if entry_start is None:
        entry_start = 0
    entry_start = int(entry_start)
    if entry_start < 0:
        raise ValueError(f"entry_start must not be negative, got {entry_start}")

    if entry_stop is None or entry_stop == -1:
        stop = entries
    else:
        entry_stop = int(entry_stop)
        if entry_stop < -1:
            raise ValueError(
                f"entry_stop must be -1 or a non-negative integer, got {entry_stop}"
            )
        stop = min(entry_stop, entries)

    start = min(entry_start, entries)
    return start, max(start, stop)


def _select_fields(filter_name: str | list | None) -> list[str]:
    """
    Resolve `filter_name` into the list of fields to read.
    """
    filter_func = regularize_filter(filter_name)
    return [field for field in _RAW_FIELDS if filter_func(field)]


def _resolve_files(files: str | Path | list[str | Path]) -> list[str]:
    """
    Expand a glob and keep only valid raw files.
    """
    if not isinstance(files, list):
        files = glob.glob(files, recursive=True)

    return [str(Path(file).resolve()) for file in files if _is_raw(file)]


def _file_ranges(
    files: list[str],
    entry_start: int,
    entry_stop: int | None,
) -> list[tuple[str, int, int, int]]:
    """
    Split a global entry range into per-file local ranges.

    Returns:
        A list of `(path, local_start, local_stop, global_start)`, with empty files omitted.
    """
    entries_per_file = []
    total = 0
    for file in files:
        with RawBinaryReader(file) as reader:
            n_entries = reader.entries
        entries_per_file.append((file, n_entries))
        total += n_entries

    start, stop = _normalize_range(total, entry_start, entry_stop)

    ranges = []
    offset = 0
    for file, n_entries in entries_per_file:
        local_start = max(0, start - offset)
        local_stop = min(n_entries, stop - offset)
        if local_stop > local_start:
            ranges.append((file, local_start, local_stop, offset))
        offset += n_entries

    return ranges


def _read_range(
    item: tuple[str, int, int, int],
    filter_name: str | list | None,
) -> ak.Array:
    path, local_start, local_stop, _ = item
    with RawBinaryReader(path) as reader:
        return reader.arrays(
            entry_start=local_start,
            entry_stop=local_stop,
            filter_name=filter_name,
        )


def concatenate_raw(
    files: str | Path | list[str | Path],
    *,
    entry_start: int = 0,
    entry_stop: int | None = None,
    filter_name: str | list | None = None,
    workers: int = 1,
    verbose: bool = False,
) -> ak.Array:
    """
    Concatenate multiple raw binary files into `ak.Array`

    Parameters:
        files (str | Path | list[str | Path]): files to be read.
        entry_start (int, optional): The first entry to read across all files. Defaults to 0.
        entry_stop (int, optional): The entry to stop at across all files. Defaults to `None`, which means read until the end.
        filter_name (Union[str, list, None], optional): A filter to select specific fields to read. Defaults to `None`, which means read all fields.
        workers (int, optional): Number of files to read concurrently. Defaults to 1.
        verbose (bool, optional): Show reading process. Defaults to `False`.

    Returns:
        Concatenated raw data array.

    Raises:
        ValueError: If no valid raw file is found or `workers` is not positive.
    """
    if workers <= 0:
        raise ValueError(f"workers must be a positive integer, got {workers}")

    paths = _resolve_files(files)
    if len(paths) == 0:
        raise ValueError("No valid raw files found")

    ranges = _file_ranges(paths, entry_start, entry_stop)
    if len(ranges) == 0:
        return ak.Array([])

    res = []
    n_cum_read = 0

    if workers == 1:
        for item in ranges:
            n_read = item[2] - item[1]
            if verbose:
                print(
                    f"Reading file {item[0]}: {n_cum_read} -> {n_cum_read + n_read} entries ...",
                )
            res.append(_read_range(item, filter_name))
            n_cum_read += n_read
    else:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            for item, array in zip(
                ranges, executor.map(lambda it: _read_range(it, filter_name), ranges)
            ):
                n_read = item[2] - item[1]
                if verbose:
                    print(
                        f"Reading file {item[0]}: {n_cum_read} -> {n_cum_read + n_read} entries ...",
                    )
                res.append(array)
                n_cum_read += n_read

    return ak.concatenate(res)


def _iterate_files(
    ranges: list[tuple[str, int, int, int]],
    step_size: int,
    filter_name: str | list | None,
    report: bool,
    verbose: bool,
) -> Iterator[ak.Array | tuple[int, int, ak.Array]]:
    n_cum_read = 0
    for path, local_start, local_stop, global_start in ranges:
        with RawBinaryReader(path) as reader:
            if verbose:
                print(
                    f"Reading file {path}: {n_cum_read} -> {n_cum_read + local_stop - local_start} entries ...",
                )

            for start, stop, array in reader.iterate(
                step_size=step_size,
                entry_start=local_start,
                entry_stop=local_stop,
                filter_name=filter_name,
                report=True,
            ):
                yield (global_start + start, global_start + stop, array) if report else array

            n_cum_read += local_stop - local_start


def iterate_raw(
    files: str | Path | list[str | Path],
    *,
    step_size: int = 5000,
    entry_start: int = 0,
    entry_stop: int | None = None,
    filter_name: str | list | None = None,
    report: bool = False,
    verbose: bool = False,
) -> Iterator[ak.Array | tuple[int, int, ak.Array]]:
    """
    Iterate over multiple raw binary files in batches.

    Batches never span two files, so the last batch of a file may be smaller than `step_size`.

    Parameters:
        files (str | Path | list[str | Path]): files to be read.
        step_size (int, optional): Number of entries per batch. Defaults to 5000.
        entry_start (int, optional): The first entry to read across all files. Defaults to 0.
        entry_stop (int, optional): The entry to stop at across all files. Defaults to `None`, which means read until the end.
        filter_name (Union[str, list, None], optional): A filter to select specific fields to read. Defaults to `None`, which means read all fields.
        report (bool, optional): If `True`, yield `(start, stop, array)` tuples with global entry indices. Defaults to `False`.
        verbose (bool, optional): Show reading process. Defaults to `False`.

    Returns:
        An iterator of Awkward Arrays, or of `(start, stop, array)` tuples.

    Raises:
        ValueError: If `step_size` is not a positive integer or no valid raw file is found.
    """
    if not isinstance(step_size, (int, np.integer)) or step_size <= 0:
        raise ValueError(f"step_size must be a positive integer, got {step_size!r}")

    paths = _resolve_files(files)
    if len(paths) == 0:
        raise ValueError("No valid raw files found")

    ranges = _file_ranges(paths, entry_start, entry_stop)
    return _iterate_files(ranges, int(step_size), filter_name, report, verbose)
