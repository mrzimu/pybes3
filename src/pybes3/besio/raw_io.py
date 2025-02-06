import glob
import mmap
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Union

import awkward as ak
import awkward.contents
import awkward.index
import numpy as np

from .besio_cpp import read_bes_raw


@dataclass
class BesFlag:
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


def _raw_dict_to_ak(raw_dict: dict):
    contents = {}

    for field_name, org_data in raw_dict.items():
        if field_name == "evt_header":
            contents[field_name] = awkward.contents.RecordArray(
                [awkward.contents.NumpyArray(i) for i in org_data.values()],
                list(org_data.keys()),
            )

        elif field_name in {"mdc", "tof", "emc", "muc"}:
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
    def __init__(
        self,
        file: str,
    ):
        self.file = str(Path(file).resolve())
        self._file = open(file, "rb")

        self.file_version: int = -1
        self.file_number: int = -1
        self.file_date: int = -1
        self.file_time: int = -1

        self.app_name: str = "None"
        self.app_tag: str = "None"

        self.run_number: int = -1
        self.max_events: int = -1
        self.rec_enable: int = -1
        self.trigger_type: int = -1
        self.detector_mask: int = -1
        self.beam_type: int = -1
        self.beam_energy: int = -1

        self.entries: int = -1

        self.data_start: int = 0  # in char
        self.data_end: int = 0  # in char
        self.file_size: int = 0  # in char
        self.data_size: int = 0  # in char

        self.event_starts: np.ndarray = np.empty(0, dtype=np.uint32)  # in char
        self.event_stops: np.ndarray = np.empty(0, dtype=np.uint32)  # in char
        self.max_event_offset: int = 0
        self.current_entry: int = -1

        self._preprocess_file()

    def arrays(
        self,
        n_blocks: int = -1,
        n_block_per_batch: int = 1000,
        sub_detectors: Union[list[str], None] = None,
        max_workers: Union[int, None] = None,
    ) -> ak.Array:
        """
        Read and return arrays of data from the BES raw file.

        Parameters:
            n_blocks (int, optional): The number of blocks to read. Defaults to -1, which means read all blocks.
            n_block_per_batch (int, optional): The number of blocks to read per batch. Defaults to 1000.
            sub_detectors (Union[list[str], None], optional): List of sub-detectors to read. Defaults to `None`, which means read all sub-detectors.
            max_workers (Union[int, None], optional): The maximum number of worker threads to use for reading the data. Defaults to `None`, which means use the default number of worker threads.

        Returns:
            An Awkward Array containing the read data.
        """

        self._reset_cursor()

        if sub_detectors is None:
            sub_detectors = []

        executor = ThreadPoolExecutor(max_workers=max_workers)

        n_total_blocks_read = 0

        futures: list[Future] = []
        while n_total_blocks_read < n_blocks or (
            n_blocks == -1 and self._file.tell() < self.data_end
        ):
            n_tlock_to_read = (
                min(n_blocks - n_total_blocks_read, n_block_per_batch)
                if n_blocks != -1
                else n_block_per_batch
            )

            batch_data, n_read = self._read_batch(n_tlock_to_read)
            futures.append(executor.submit(read_bes_raw, batch_data, sub_detectors))
            n_total_blocks_read += n_read

        res = []
        for future in futures:
            org_dict = future.result()
            res.append(_raw_dict_to_ak(org_dict))

        return ak.concatenate(res)

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
        self.data_start = self._file.tell()
        self._file.seek(0, 2)
        self.file_size = self._file.tell()
        self.data_end = self.file_size - 10 * 4
        self.data_size = self.data_end - self.data_start

        # read file tail
        self._file.seek(-10 * 4, 2)
        assert self._read() == BesFlag.FILE_TAIL_START, "Invalid file tail start flag"
        self._skip(3)
        self.entries = self._read()
        self._skip(4)
        assert self._read() == BesFlag.FILE_END, "Invalid file end flag"

        self._reset_cursor()

    def _reset_cursor(self):
        self._file.seek(self.data_start)
        self.current_entry = 0

    def _skip_event(self):
        flag = self._read()
        if flag == BesFlag.DATA_SEPERATOR:
            self._skip(3)
            flag = self._read()

        assert flag == BesFlag.FULL_EVENT_FRAGMENT, "Invalid event fragment flag"

        total_size = self._read()

        if self.current_entry > self.max_event_offset:
            self.event_starts[self.current_entry] = self._file.tell() - 4 * 2
            self.event_stops[self.current_entry] = (
                self.event_starts[self.current_entry] + total_size
            )

        self._skip(total_size - 2)
        self.current_entry += 1

    def _read_batch(self, n_blocks: int):
        pos_start = self._file.tell()
        block_counter = 0
        for _ in range(n_blocks):
            if self._file.tell() >= self.data_end:
                assert self._file.tell() == self.data_end, "Invalid data end"
                break

            assert self._read() == BesFlag.DATA_SEPERATOR, "Invalid data seperator flag"
            self._skip(2)
            block_size = self._read()
            self._skip(block_size // 4)
            block_counter += 1

        pos_end = self._file.tell()

        self._file.seek(pos_start, 0)
        batch_data = np.frombuffer(self._file.read(pos_end - pos_start), dtype=np.uint32)

        return batch_data, block_counter

    def __repr__(self) -> str:
        return (
            f"BesRawReader\n"
            f"- File: {self.file}\n"
            f"- Run Number: {self.run_number}\n"
            f"- Entries: {self.entries}\n"
            f"- File Size: {self.file_size//1024//1024} MB\n"
        )


def _is_raw(file):
    f = open(file, "rb")
    if int.from_bytes(f.read(4), "little") == BesFlag.FILE_START:
        f.close()
        return True
    return False


def concatenate(
    files: Union[Union[str, Path], list[Union[str, Path]]],
    n_block_per_batch: int = 10000,
    sub_detectors: Union[list[str], None] = None,
    max_workers: Union[int, None] = None,
    verbose: bool = False,
) -> ak.Array:
    """
    Concatenate multiple raw binary files into `ak.Array`

    Parameters:
        files (Union[Union[str, Path], list[Union[str, Path]]]): files to be read.
        n_block_per_batch (int, optional): The number of blocks to read per batch. Defaults to 1000.
        sub_detectors (Union[list[str], None], optional): List of sub-detectors to read. Defaults to `None`, which means read all sub-detectors.
        max_workers (Union[int, None], optional): The maximum number of worker threads to use for reading the data. Defaults to `None`, which means use the default number of worker threads.
        verbose (bool): Show reading process.

    Returns:
        Concatenated raw data array.
    """

    if not isinstance(files, list):
        files = glob.glob(files)

    files = [str(Path(file).resolve()) for file in files if _is_raw(file)]

    if len(files) == 0:
        raise ValueError("No valid raw files found")

    res = []
    for i, f in enumerate(files):
        if verbose:
            print(f"\rreading file {i+1}/{len(files)} ...", end="")

        res.append(
            RawBinaryReader(f).arrays(-1, n_block_per_batch, sub_detectors, max_workers)
        )

    if verbose:
        print()

    return ak.concatenate(res)
