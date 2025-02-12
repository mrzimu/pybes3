from . import besio, detectors
from ._check_latest_version import check_new_version
from ._version import __version__, version
from .besio import concatenate, concatenate_raw, open, open_raw, wrap_uproot
from .detectors import (
    get_cgem_id,
    get_emc_id,
    get_mdc_id,
    get_muc_id,
    get_tof_mrpc_id,
    get_tof_scint_id,
    parse_cgem_id,
    parse_emc_id,
    parse_mdc_id,
    parse_muc_id,
    parse_tof_id,
)

check_new_version()
