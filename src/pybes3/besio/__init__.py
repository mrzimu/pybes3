from pathlib import Path
from typing import Union

import uproot

from .raw_io import RawBinaryReader
from .raw_io import concatenate as concatenate_raw
from .root_io import wrap_uproot


def open(file, **kwargs):
    wrap_uproot()
    return uproot.open(file, **kwargs)


def concatenate(files, branch: str, **kwargs):
    wrap_uproot()
    return uproot.concatenate({str(f): branch for f in files}, **kwargs)


def open_raw(file):
    return RawBinaryReader(file)


__all__ = ["open", "concatenate", "open_raw", "concatenate_raw", "wrap_uproot"]
