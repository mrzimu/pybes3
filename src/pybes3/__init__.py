# fmt: off
from ._cache_numba import check_numba_cache
check_numba_cache()
# fmt: on

from . import besio, detectors, tracks
from ._version import __version__, version
from .besio import concatenate, concatenate_raw, open, open_raw, wrap_uproot
from .detectors import (
    emc_barrel_h1,
    emc_barrel_h2,
    emc_barrel_h3,
    emc_barrel_l,
    emc_barrel_offset_1,
    emc_barrel_offset_2,
    emc_barrel_r,
    emc_gid_to_center_x,
    emc_gid_to_center_y,
    emc_gid_to_center_z,
    emc_gid_to_front_center_x,
    emc_gid_to_front_center_y,
    emc_gid_to_front_center_z,
    emc_gid_to_part,
    emc_gid_to_phi,
    emc_gid_to_point_x,
    emc_gid_to_point_y,
    emc_gid_to_point_z,
    emc_gid_to_theta,
    get_emc_crystal_position,
    get_emc_gid,
    get_mdc_gid,
    get_mdc_wire_position,
    mdc_gid_to_east_x,
    mdc_gid_to_east_y,
    mdc_gid_to_east_z,
    mdc_gid_to_is_stereo,
    mdc_gid_to_layer,
    mdc_gid_to_stereo,
    mdc_gid_to_superlayer,
    mdc_gid_to_west_x,
    mdc_gid_to_west_y,
    mdc_gid_to_west_z,
    mdc_gid_to_wire,
    mdc_gid_z_to_x,
    mdc_gid_z_to_y,
    mdc_layer_to_is_stereo,
    mdc_layer_to_superlayer,
    parse_cgem_digi_id,
    parse_emc_digi,
    parse_emc_digi_id,
    parse_emc_gid,
    parse_mdc_digi,
    parse_mdc_digi_id,
    parse_mdc_gid,
    parse_muc_digi_id,
    parse_tof_digi_id,
)
from .tracks import compute_helix, helix_awk, helix_obj, parse_helix, regularize_helix
