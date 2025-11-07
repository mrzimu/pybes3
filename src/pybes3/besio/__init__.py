from __future__ import annotations

from typing import Any
from warnings import warn

import uproot

from . import root_io  # noqa: F401
from .raw_io import RawBinaryReader
from .raw_io import concatenate as concatenate_raw


def open(file, **kwargs) -> Any:
    """
    Alias for `uproot.open`.

    Returns:
        The uproot file object.

    Warning:
        This function is deprecated and will be removed in future versions.
        Use `uproot.open` instread.
    """
    # TODO: Remove this in the future.
    warn(
        "`pybes3.open` is deprecated and will be removed in future versions. "
        "Use `uproot.open` instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return uproot.open(file, **kwargs)


def concatenate(files, expressions=None, cut=None, **kwargs) -> Any:
    """
    Alias for `uproot.concatenate`.

    Returns:
        The concatenated array.

    Warning:
        This function is deprecated and will be removed in future versions.
        Use `uproot.concatenate` instread.
    """
    # TODO: Remove this in the future.
    warn(
        "`pybes3.concatenate` is deprecated and will be removed in future versions. "
        "Use `uproot.concatenate` instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return uproot.concatenate(files, expressions, cut, **kwargs)


def open_raw(file: str) -> RawBinaryReader:
    """
    Open a raw binary file.

    Parameters:
        file (str): The file to open.

    Returns:
        (RawBinaryReader): The raw binary reader.
    """
    return RawBinaryReader(file)


__all__ = ["open", "concatenate", "open_raw", "concatenate_raw"]
