from typing import Any

import uproot

from .raw_io import RawBinaryReader
from .raw_io import concatenate as concatenate_raw
from .root_io import wrap_uproot


def open(file, **kwargs) -> Any:
    """
    A wrapper around `uproot.open` that automatically calls `wrap_uproot` before opening the file.

    Parameters:
        file (str | Path | IO | dict[str | Path | IO, str]): The file to open.
        **kwargs (dict): Additional arguments to pass to `uproot.open`.

    Returns:
        The uproot file object.
    """
    wrap_uproot()
    return uproot.open(file, **kwargs)


def concatenate(files, branch: str, **kwargs) -> Any:
    """
    A wrapper around `uproot.concatenate` that automatically calls `wrap_uproot` before concatenating the files.

    Parameters:
        files (list[str | Path | IO, str]): The files to concatenate.
        branch (str): The branch to concatenate.
        **kwargs (dict): Additional arguments to pass to `uproot.concatenate`.

    Returns:
        The concatenated array.
    """
    wrap_uproot()
    return uproot.concatenate({str(f): branch for f in files}, **kwargs)


def open_raw(file: str) -> RawBinaryReader:
    """
    Open a raw binary file.

    Parameters:
        file (str): The file to open.

    Returns:
        (RawBinaryReader): The raw binary reader.
    """
    return RawBinaryReader(file)


__all__ = ["open", "concatenate", "open_raw", "concatenate_raw", "wrap_uproot"]
