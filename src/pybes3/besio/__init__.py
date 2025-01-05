import uproot

from .uproot_wrappers import wrap_uproot


def open(file, **kwargs):
    wrap_uproot()
    return uproot.open(file, **kwargs)


def concatenate(files, branch: str, **kwargs):
    wrap_uproot()
    return uproot.concatenate({str(f): branch for f in files}, **kwargs)
