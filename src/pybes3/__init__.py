from . import besio, detectors
from ._version import __version__, version
from .besio import concatenate, concatenate_raw, open, open_raw, wrap_uproot
from .detectors import (
    # parse methods
    parse_mdc_gid,
    parse_mdc_digi,
    parse_cgem_digi_id,
    parse_emc_digi_id,
    parse_mdc_digi_id,
    parse_muc_digi_id,
    parse_tof_digi_id,
    # geometry
    get_mdc_gid,
)
from .tracks import parse_helix
