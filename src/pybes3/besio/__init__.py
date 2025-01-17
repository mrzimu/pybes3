import uproot

from .raw_io import RawBinaryReader, _is_raw
from .root_io import wrap_uproot


def open(file, **kwargs):
    wrap_uproot()

    # check whether it's a RAW file
    if _is_raw(file):
        return RawBinaryReader(file)

    return uproot.open(file, **kwargs)


def concatenate(files, branch: str, **kwargs):
    wrap_uproot()
    return uproot.concatenate({str(f): branch for f in files}, **kwargs)
