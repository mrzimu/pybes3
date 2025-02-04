from . import besio
from ._check_latest_version import check_new_version
from ._version import __version__, version
from .besio import concatenate, concatenate_raw, open, open_raw, wrap_uproot

check_new_version()
