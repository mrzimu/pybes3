from __future__ import annotations

from typing import Any

import awkward as ak
import numba as nb
import numpy as np

from pybes3.typing import IntLike, BoolLike

N_PARTS = 5
N_LAYER_OR_MODULE = np.array([1, 2, 1, 36, 36])
N_PHI_OR_STRIP = np.array([48, 88, 48, 12, 12])
N_STRIPS = (N_LAYER_OR_MODULE * N_PHI_OR_STRIP).sum()

N_LAYER_OR_MODULE.setflags(write=False)
N_PHI_OR_STRIP.setflags(write=False)


def _init():
    _part = np.empty(N_STRIPS, dtype=np.int64)
    _layer_or_module = np.empty(N_STRIPS, dtype=np.int64)
    _phi_or_strip = np.empty(N_STRIPS, dtype=np.int64)

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


@nb.vectorize(cache=True)
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
    gid = (N_LAYER_OR_MODULE[:part] * N_PHI_OR_STRIP[:part]).sum()
    gid += layer_or_module * N_PHI_OR_STRIP[part]
    gid += phi_or_strip
    return gid


@nb.vectorize(cache=True)
def tof_gid_to_part(gid: IntLike) -> IntLike:
    """Get TOF part from gid."""
    return _part[gid]


@nb.vectorize(cache=True)
def tof_gid_to_layer_or_module(gid: IntLike) -> IntLike:
    """Get TOF layer_or_module from gid."""
    return _layer_or_module[gid]


@nb.vectorize(cache=True)
def tof_gid_to_phi_or_strip(gid: IntLike) -> IntLike:
    """Get TOF phi_or_strip from gid."""
    return _phi_or_strip[gid]


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


RAW_IDX = np.int32(0)
RAW_MASK = np.int32(0x00000001)
READOUT_IDX = np.int32(1)
READOUT_MASK = np.int32(0x00000002)
COUNTER_IDX = np.int32(2)
COUNTER_MASK = np.int32(0x00000004)
CLUSTER_IDX = np.int32(3)
CLUSTER_MASK = np.int32(0x00000008)
BARREL_IDX = np.int32(4)
BARREL_MASK = np.int32(0x00000010)
EAST_IDX = np.int32(5)
EAST_MASK = np.int32(0x00000020)
LAYER_IDX = np.int32(6)
LAYER_MASK = np.int32(0x000000C0)
OVERFLOW_IDX = np.int32(8)
OVERFLOW_MASK = np.int32(0x00000100)
MULTIHIT_IDX = np.int32(9)
MULTIHIT_MASK = np.int32(0x00000200)
NCOUNTER_IDX = np.int32(12)
NCOUNTER_MASK = np.int32(0x0000F000)
NEAST_IDX = np.int32(16)
NEAST_MASK = np.int32(0x000F0000)
NWEST_IDX = np.int32(20)
NWEST_MASK = np.int32(0x00F00000)
N_MASK = np.int32(0x0000000F)
MRPC_IDX = np.int32(24)
MRPC_MASK = np.int32(0x01000000)
N_MRPC = np.int32(0x00000001)


@nb.vectorize(cache=True)
def tof_trk_status_to_is_raw(status: IntLike) -> BoolLike:
    return ((status & RAW_MASK) >> RAW_IDX) > 0


@nb.vectorize(cache=True)
def tof_trk_status_to_is_readout(status: IntLike) -> BoolLike:
    return ((status & READOUT_MASK) >> READOUT_IDX) > 0


@nb.vectorize(cache=True)
def tof_trk_status_to_is_counter(status: IntLike) -> BoolLike:
    return ((status & COUNTER_MASK) >> COUNTER_IDX) > 0


@nb.vectorize(cache=True)
def tof_trk_status_to_is_cluster(status: IntLike) -> BoolLike:
    return ((status & CLUSTER_MASK) >> CLUSTER_IDX) > 0


@nb.vectorize(cache=True)
def tof_trk_status_to_is_barrel(status: IntLike) -> BoolLike:
    return ((status & BARREL_MASK) >> BARREL_IDX) > 0


@nb.vectorize(cache=True)
def tof_trk_status_to_is_east(status: IntLike) -> BoolLike:
    return ((status & EAST_MASK) >> EAST_IDX) > 0


@nb.vectorize(cache=True)
def tof_trk_status_to_layer(status: IntLike) -> IntLike:
    return (status & LAYER_MASK) >> LAYER_IDX


@nb.vectorize(cache=True)
def tof_trk_status_to_is_overflow(status: IntLike) -> BoolLike:
    return ((status & OVERFLOW_MASK) >> OVERFLOW_IDX) > 0


@nb.vectorize(cache=True)
def tof_trk_status_to_is_multihit(status: IntLike) -> BoolLike:
    return ((status & MULTIHIT_MASK) >> MULTIHIT_IDX) > 0


@nb.vectorize(cache=True)
def tof_trk_status_to_n_counter(status: IntLike) -> IntLike:
    return (status >> NCOUNTER_IDX) & NCOUNTER_MASK


@nb.vectorize(cache=True)
def tof_trk_status_to_n_east(status: IntLike) -> IntLike:
    return (status >> NEAST_IDX) & NEAST_MASK


@nb.vectorize(cache=True)
def tof_trk_status_to_n_west(status: IntLike) -> IntLike:
    return (status >> NWEST_IDX) & NWEST_MASK


@nb.vectorize(cache=True)
def tof_trk_status_to_is_mrpc(status: IntLike) -> BoolLike:
    return ((status & MRPC_MASK) >> MRPC_IDX) > 0


def parse_tof_trk_status(status: IntLike) -> ak.Array | dict[str, Any]:
    res = {
        "is_raw": tof_trk_status_to_is_raw(status),
        "is_readout": tof_trk_status_to_is_readout(status),
        "is_counter": tof_trk_status_to_is_counter(status),
        "is_cluster": tof_trk_status_to_is_cluster(status),
        "is_barrel": tof_trk_status_to_is_barrel(status),
        "is_east": tof_trk_status_to_is_east(status),
        "is_overflow": tof_trk_status_to_is_overflow(status),
        "is_multihit": tof_trk_status_to_is_multihit(status),
        "is_mrpc": tof_trk_status_to_is_mrpc(status),
        "layer": tof_trk_status_to_layer(status),
        "n_counter": tof_trk_status_to_n_counter(status),
        "n_east": tof_trk_status_to_n_east(status),
        "n_west": tof_trk_status_to_n_west(status),
    }

    if isinstance(status, ak.Array):
        return ak.zip(res)
    else:
        return res
