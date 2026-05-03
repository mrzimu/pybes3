from __future__ import annotations

from typing import Any

import awkward as ak
import numba as nb
import numpy as np

from pybes3.typing import IntLike

N_PARTS = 5
N_LAYER_OR_MODULE = np.array([1, 2, 1, 36, 36])
N_PHI_OR_STRIP = np.array([48, 88, 48, 12, 12])
N_STRIPS = (N_LAYER_OR_MODULE * N_PHI_OR_STRIP).sum()

N_LAYER_OR_MODULE.setflags(write=False)
N_PHI_OR_STRIP.setflags(write=False)


def _init():
    _part = np.empty(N_STRIPS, dtype=np.uint8)
    _layer_or_module = np.empty(N_STRIPS, dtype=np.uint8)
    _phi_or_strip = np.empty(N_STRIPS, dtype=np.uint8)

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
