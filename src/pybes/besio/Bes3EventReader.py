import re
import awkward as ak
from pathlib import Path
from glob import glob
from typing import Union

from .IOEvent import IOEvent
from ._cpp_besio import _Bes3EventReader


class Bes3EventReader:
    def __init__(self, files: Union[str, Path, list[Union[str, Path]]]) -> None:
        """
        Initialize the Bes3EventReader object.

        Args:
            files (Union[str, Path, list[Union[str, Path]]]): The path(s) to the file(s) to be read.

        Raises:
            FileNotFoundError: If no files are provided or if any of the provided files are not found.
            ValueError: If no available fields are found in the provided files.
        """
        arg_files = files

        # Parse files
        parsed_files: list[Path] = [Path(f).resolve()
                                    for f in files] if isinstance(files, list) else [Path(files).resolve()]
        parsed_files: list[Path] = [Path(i) for i in sum([glob(str(f)) for f in parsed_files], [])]
        if len(parsed_files) == 0:
            raise FileNotFoundError(f"No files provided from {arg_files}.")

        # Check files existence
        for f in parsed_files:
            if not f.exists():
                raise FileNotFoundError(f"File {f} not found.")

        # Set files
        self.files = [str(f) for f in parsed_files]

        self.reader = _Bes3EventReader(self.files)
        self._available_fields: list[str] = self.reader.get_available_fields()

        if len(self._available_fields) == 0:
            raise ValueError(
                "You should only read BES3 rtraw/dst files!\nIf you want to read ordinary ROOT files, see https://uproot.readthedocs.io/en/stable/")

    @property
    def entries(self) -> int:
        return self.reader.get_entries()

    @property
    def available_fields(self) -> list[str]:
        return self._available_fields

    def arrays(self,
               entry_start: int = 0,
               entry_stop: int = -1,
               fields: Union[list[str], None] = None,
               return_dict: bool = False,
               optimize_res: bool = True
               ) -> Union[IOEvent, dict[str, ak.Array]]:
        """
        Retrieve arrays of data from the event file.

        Args:
            entry_start (int, optional): The starting entry index. Defaults to 0.
            entry_stop (int, optional): The stopping entry index. Defaults to -1, which means all entries.
            fields (list[str] or None, optional): The list of field names to retrieve. Defaults to None, which means all fields.
            return_dict (bool, optional): Whether to return the result as a dictionary. Defaults to False.
            optimize_res (bool, optional): Whether to optimize the result by removing empty fields. Defaults to True.

        Returns:
            Union[IOEvent, dict[str, ak.Array]]: The retrieved arrays as a dictionary or an IOEvent object.

        Raises:
            ValueError: If entry_start is greater than or equal to entry_stop.
            ValueError: If entry_stop is greater than the total number of entries.
            KeyError: If no field named `field` is available in the file.
        """
        if entry_stop < 0:
            entry_stop = self.entries

        if entry_start >= entry_stop:
            raise ValueError(f"entry_start ({entry_start}) should be smaller than entry_stop ({entry_stop}).")

        if entry_stop > self.entries:
            raise ValueError(
                f"entry_stop ({entry_stop}) should be smaller than the total number of entries ({self.entries}).")

        if fields is None:
            fields = self.available_fields

        arg_fields = []
        for field in fields:
            parse_field = field.replace("*", ".*").replace("?", ".")
            for available_field in self.available_fields:
                if re.match(parse_field, available_field):
                    arg_fields.append(available_field)

        if len(arg_fields) == 0:
            raise KeyError(f"No field named {field} available in the file.")

        res_dict = self.reader.arrays(entry_start, entry_stop, arg_fields)

        # Remove empty fields
        if optimize_res:
            optimized_dict = {}
            for k, res_arr in res_dict.items():
                if not isinstance(res_arr, ak.Array):
                    optimized_dict[k] = res_arr
                    continue

                for f in res_arr.fields:
                    hasElement = ak.any(res_arr[f])
                    hasElement = len(hasElement) > 0 if 'string' in res_arr[f].typestr else bool(hasElement)
                    if hasElement:
                        optimized_dict[k] = res_arr
                        break
            return optimized_dict if return_dict else IOEvent(self.files, entry_stop - entry_start, optimized_dict)

        else:
            return res_dict if return_dict else IOEvent(self.files, entry_stop - entry_start, res_dict)

    def __repr__(self) -> str:
        return f"Bes3EventReader(entries={self.entries}, files={self.files})"
