from __future__ import annotations

from typing import Any

import awkward as ak
import numpy as np

import pybes3._kernels._ufuncs as _ufuncs
from pybes3.typing import IntLike, BoolLike

N_PARTS = 5
N_LAYER_OR_MODULE = np.array([1, 2, 1, 36, 36])
N_PHI_OR_STRIP = np.array([48, 88, 48, 12, 12])
N_STRIPS = (N_LAYER_OR_MODULE * N_PHI_OR_STRIP).sum()

N_LAYER_OR_MODULE.setflags(write=False)
N_PHI_OR_STRIP.setflags(write=False)


def _init():
    _part = np.empty(N_STRIPS, dtype=np.int16)
    _layer_or_module = np.empty(N_STRIPS, dtype=np.int16)
    _phi_or_strip = np.empty(N_STRIPS, dtype=np.int32)

    gid = 0
    for part in range(5):
        n_layer_or_module = N_LAYER_OR_MODULE[part]
        n_phi_or_strip = N_PHI_OR_STRIP[part]

        for i in range(n_layer_or_module):
            for j in range(n_phi_or_strip):
                _part[gid] = part
                _layer_or_module[gid] = i
                _phi_or_strip[gid] = j
                gid += 1

    _part.setflags(write=False)
    _layer_or_module.setflags(write=False)
    _phi_or_strip.setflags(write=False)

    return _part, _layer_or_module, _phi_or_strip


_part, _layer_or_module, _phi_or_strip = _init()


def get_tof_gid(part: IntLike, layer_or_module: IntLike, phi_or_strip: IntLike) -> IntLike:
    """
    Get TOF gid of given part, layer_or_module and phi_or_strip.

    Parameters:
        part: The part of the TOF, 0-2 for scintillator, 3-4 for MRPC.
        layer_or_module: The layer (for scintillator) or module (for MRPC) number, starting from 0.
        phi_or_strip: The phi (for scintillator) or strip (for MRPC) number, starting from 0.

    Returns:
        The global strip ID of the TOF strip, ranging from 0 to 1135.
    """
    return _ufuncs.get_tof_idx(part, layer_or_module, phi_or_strip)


def tof_gid_to_part(gid: IntLike) -> IntLike:
    """Get TOF part from gid."""
    return _ufuncs.tof_idx_to_part(gid)


def tof_gid_to_layer_or_module(gid: IntLike) -> IntLike:
    """Get TOF layer_or_module from gid."""
    return _ufuncs.tof_idx_to_layer_or_module(gid)


def tof_gid_to_phi_or_strip(gid: IntLike) -> IntLike:
    """Get TOF phi_or_strip from gid."""
    return _ufuncs.tof_idx_to_phi_or_strip(gid)


def parse_tof_gid(gid: IntLike) -> ak.Array | dict[str, Any]:
    """
    Parse TOF gid into part, layer_or_module and phi_or_strip.

    Parameters:
        gid: The global strip ID of the TOF strip, ranging from 0 to 1135.

    Returns:
        If gid is a ak.Array, returns an ak.Array with fields "part", "layer_or_module" and "phi_or_strip".
        Otherwise, returns a dictionary with keys "part", "layer_or_module" and "phi_or_strip".
    """
    part = tof_gid_to_part(gid)
    layer_or_module = tof_gid_to_layer_or_module(gid)
    phi_or_strip = tof_gid_to_phi_or_strip(gid)

    res = {
        "part": part,
        "layer_or_module": layer_or_module,
        "phi_or_strip": phi_or_strip,
    }

    if isinstance(gid, ak.Array):
        return ak.zip(res)
    else:
        return res


def tof_hit_status_to_is_raw(status: IntLike) -> BoolLike:
    """Convert hit status to `is_raw`."""
    return _ufuncs.tof_hit_status_to_is_raw(status)


def tof_hit_status_to_is_readout(status: IntLike) -> BoolLike:
    """Convert hit status to `is_readout`."""
    return _ufuncs.tof_hit_status_to_is_readout(status)


def tof_hit_status_to_is_counter(status: IntLike) -> BoolLike:
    """Convert hit status to `is_counter`."""
    return _ufuncs.tof_hit_status_to_is_counter(status)


def tof_hit_status_to_is_cluster(status: IntLike) -> BoolLike:
    """Convert hit status to `is_cluster`."""
    return _ufuncs.tof_hit_status_to_is_cluster(status)


def tof_hit_status_to_is_barrel(status: IntLike) -> BoolLike:
    """Convert hit status to `is_barrel`."""
    return _ufuncs.tof_hit_status_to_is_barrel(status)


def tof_hit_status_to_is_east(status: IntLike) -> BoolLike:
    """Convert hit status to `is_east`."""
    return _ufuncs.tof_hit_status_to_is_east(status)


def tof_hit_status_to_layer(status: IntLike) -> IntLike:
    """Convert hit status to `layer`."""
    return _ufuncs.tof_hit_status_to_layer(status)


def tof_hit_status_to_is_overflow(status: IntLike) -> BoolLike:
    """Convert hit status to `is_overflow`."""
    return _ufuncs.tof_hit_status_to_is_overflow(status)


def tof_hit_status_to_is_multihit(status: IntLike) -> BoolLike:
    """Convert hit status to `is_multihit`."""
    return _ufuncs.tof_hit_status_to_is_multihit(status)


def tof_hit_status_to_n_counter(status: IntLike) -> IntLike:
    """Convert hit status to `n_counter`."""
    return _ufuncs.tof_hit_status_to_n_counter(status)


def tof_hit_status_to_n_east(status: IntLike) -> IntLike:
    """Convert hit status to `n_east`."""
    return _ufuncs.tof_hit_status_to_n_east(status)


def tof_hit_status_to_n_west(status: IntLike) -> IntLike:
    """Convert hit status to `n_west`."""
    return _ufuncs.tof_hit_status_to_n_west(status)


def tof_hit_status_to_is_mrpc(status: IntLike) -> BoolLike:
    """Convert hit status to `is_mrpc`."""
    return _ufuncs.tof_hit_status_to_is_mrpc(status)


def parse_tof_hit_status(status: IntLike) -> ak.Array | dict[str, Any]:
    """
    Parse TOF hit status into its components.

    Parameters:
        status: The hit status of a TOF hit, encoded as an integer.

    Returns:
        If status is a ak.Array, returns an ak.Array with the parsed fields.
        Otherwise, returns a dictionary with the parsed fields.
    """
    res = {
        "is_raw": tof_hit_status_to_is_raw(status),
        "is_readout": tof_hit_status_to_is_readout(status),
        "is_counter": tof_hit_status_to_is_counter(status),
        "is_cluster": tof_hit_status_to_is_cluster(status),
        "is_barrel": tof_hit_status_to_is_barrel(status),
        "is_east": tof_hit_status_to_is_east(status),
        "is_overflow": tof_hit_status_to_is_overflow(status),
        "is_multihit": tof_hit_status_to_is_multihit(status),
        "is_mrpc": tof_hit_status_to_is_mrpc(status),
        "layer": tof_hit_status_to_layer(status),
        "n_counter": tof_hit_status_to_n_counter(status),
        "n_east": tof_hit_status_to_n_east(status),
        "n_west": tof_hit_status_to_n_west(status),
    }

    if isinstance(status, ak.Array):
        return ak.zip(res)
    else:
        return res
