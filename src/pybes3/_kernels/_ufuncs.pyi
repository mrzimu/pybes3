from __future__ import annotations

import numpy as np
from numpy._typing._ufunc import _UFunc_Nin1_Nout1, _UFunc_Nin2_Nout1

# detectors/cgem.cc
get_cgem_idx: np.ufunc
cgem_idx_to_layer: _UFunc_Nin1_Nout1
cgem_idx_to_sheet: _UFunc_Nin1_Nout1
cgem_idx_to_strip_type: _UFunc_Nin1_Nout1
cgem_idx_to_strip: _UFunc_Nin1_Nout1
cgem_idx_to_is_xstrip: _UFunc_Nin1_Nout1
cgem_idx_to_is_vstrip: _UFunc_Nin1_Nout1

# detectors/mdc.cc
def _init_mdc_geom(
    east_x: np.ndarray,
    east_y: np.ndarray,
    east_z: np.ndarray,
    west_x: np.ndarray,
    west_y: np.ndarray,
    west_z: np.ndarray,
    /,
): ...

get_mdc_idx: np.ufunc
mdc_idx_to_superlayer: _UFunc_Nin1_Nout1
mdc_layer_to_superlayer: _UFunc_Nin1_Nout1
mdc_idx_to_layer: _UFunc_Nin1_Nout1
mdc_idx_to_wire: _UFunc_Nin1_Nout1
mdc_idx_to_stereo: _UFunc_Nin1_Nout1
mdc_layer_to_is_stereo: _UFunc_Nin1_Nout1
mdc_idx_to_is_stereo: _UFunc_Nin1_Nout1
mdc_idx_to_west_x: _UFunc_Nin1_Nout1
mdc_idx_to_west_y: _UFunc_Nin1_Nout1
mdc_idx_to_west_z: _UFunc_Nin1_Nout1
mdc_idx_to_east_x: _UFunc_Nin1_Nout1
mdc_idx_to_east_y: _UFunc_Nin1_Nout1
mdc_idx_to_east_z: _UFunc_Nin1_Nout1
mdc_idx_z_to_x: _UFunc_Nin2_Nout1
mdc_idx_z_to_y: _UFunc_Nin2_Nout1

# detectors/tof.cc
get_tof_idx: np.ufunc
tof_idx_to_part: _UFunc_Nin1_Nout1
tof_idx_to_layer_or_module: _UFunc_Nin1_Nout1
tof_idx_to_phi_or_strip: _UFunc_Nin1_Nout1
tof_hit_status_to_is_raw: _UFunc_Nin1_Nout1
tof_hit_status_to_is_readout: _UFunc_Nin1_Nout1
tof_hit_status_to_is_counter: _UFunc_Nin1_Nout1
tof_hit_status_to_is_cluster: _UFunc_Nin1_Nout1
tof_hit_status_to_is_barrel: _UFunc_Nin1_Nout1
tof_hit_status_to_is_east: _UFunc_Nin1_Nout1
tof_hit_status_to_layer: _UFunc_Nin1_Nout1
tof_hit_status_to_is_overflow: _UFunc_Nin1_Nout1
tof_hit_status_to_is_multihit: _UFunc_Nin1_Nout1
tof_hit_status_to_n_counter: _UFunc_Nin1_Nout1
tof_hit_status_to_n_east: _UFunc_Nin1_Nout1
tof_hit_status_to_n_west: _UFunc_Nin1_Nout1
tof_hit_status_to_is_mrpc: _UFunc_Nin1_Nout1

# detectors/emc.cc
def _init_emc_geom(
    points_x: np.ndarray,
    points_y: np.ndarray,
    points_z: np.ndarray,
    center_x: np.ndarray,
    center_y: np.ndarray,
    center_z: np.ndarray,
    front_center_x: np.ndarray,
    front_center_y: np.ndarray,
    front_center_z: np.ndarray,
    /,
): ...

get_emc_idx: np.ufunc
emc_idx_to_part: _UFunc_Nin1_Nout1
emc_idx_to_theta: _UFunc_Nin1_Nout1
emc_idx_to_phi: _UFunc_Nin1_Nout1
emc_idx_to_center_x: _UFunc_Nin1_Nout1
emc_idx_to_center_y: _UFunc_Nin1_Nout1
emc_idx_to_center_z: _UFunc_Nin1_Nout1
emc_idx_to_front_center_x: _UFunc_Nin1_Nout1
emc_idx_to_front_center_y: _UFunc_Nin1_Nout1
emc_idx_to_front_center_z: _UFunc_Nin1_Nout1
emc_idx_to_point_x: _UFunc_Nin1_Nout1
emc_idx_to_point_y: _UFunc_Nin1_Nout1
emc_idx_to_point_z: _UFunc_Nin1_Nout1

# helix.cc
dr_phi0_to_x: _UFunc_Nin2_Nout1
dr_phi0_to_y: _UFunc_Nin2_Nout1
phi0_to_phi: _UFunc_Nin1_Nout1
kappa_to_pt: _UFunc_Nin1_Nout1
kappa_to_charge: _UFunc_Nin1_Nout1
kappa_to_radius: _UFunc_Nin1_Nout1
_fix_dr_sign: np.ufunc

# identifier.cc
## mdc
check_mdc_id: _UFunc_Nin1_Nout1
mdc_id_to_wire: _UFunc_Nin1_Nout1
mdc_id_to_layer: _UFunc_Nin1_Nout1
mdc_id_to_is_stereo: _UFunc_Nin1_Nout1
get_mdc_id: np.ufunc

## tof
check_tof_id: _UFunc_Nin1_Nout1
tof_id_to_part: _UFunc_Nin1_Nout1
tof_id_to_end: _UFunc_Nin1_Nout1
_tof_id_to_layer_or_module_1: _UFunc_Nin1_Nout1
_tof_id_to_layer_or_module_2: _UFunc_Nin2_Nout1
_tof_id_to_phi_or_strip_1: _UFunc_Nin1_Nout1
_tof_id_to_phi_or_strip_2: _UFunc_Nin2_Nout1
get_tof_id: np.ufunc

## emc
check_emc_id: _UFunc_Nin1_Nout1
emc_id_to_module: _UFunc_Nin1_Nout1
emc_id_to_theta: _UFunc_Nin1_Nout1
emc_id_to_phi: _UFunc_Nin1_Nout1
get_emc_id: np.ufunc

## muc
check_muc_id: _UFunc_Nin1_Nout1
muc_id_to_part: _UFunc_Nin1_Nout1
muc_id_to_segment: _UFunc_Nin1_Nout1
muc_id_to_layer: _UFunc_Nin1_Nout1
muc_id_to_channel: _UFunc_Nin1_Nout1
get_muc_id: np.ufunc

## cgem
check_cgem_id: _UFunc_Nin1_Nout1
cgem_id_to_layer: _UFunc_Nin1_Nout1
cgem_id_to_sheet: _UFunc_Nin1_Nout1
cgem_id_to_strip_type: _UFunc_Nin1_Nout1
cgem_id_to_strip: _UFunc_Nin1_Nout1
get_cgem_id: np.ufunc
