from . import besio
from ._version import __version__, version
from .besio import concatenate, open, wrap_uproot
from ._check_latest_version import check_latest_version

check_latest_version()
