from __future__ import annotations

from typing import Any

import awkward as ak
import numba as nb
import numpy as np

from pybes3.typing import BoolLike, IntLike

N_LAYER = 3
N_STRIPS = 9897
X_STRIP_TYPE = 0
V_STRIP_TYPE = 1

N_SHEETS = np.array([1, 2, 2])
N_XSTRIPS = np.array([856, 630, 832])
N_VSTRIPS = np.array([1173, 1077, 1395])

N_SHEETS.setflags(write=False)
N_XSTRIPS.setflags(write=False)
N_VSTRIPS.setflags(write=False)


def _init():
    _layer = np.empty(N_STRIPS, dtype=np.uint8)
    _sheet = np.empty(N_STRIPS, dtype=np.uint8)
    _strip_type = np.empty(N_STRIPS, dtype=np.uint8)
    _strip = np.empty(N_STRIPS, dtype=np.uint16)

    gid = 0
    for layer in range(3):
        n_sheet = N_SHEETS[layer]
        n_xstrips = N_XSTRIPS[layer]
        n_vstrips = N_VSTRIPS[layer]

        for sheet in range(n_sheet):
            # x strips
            for strip in range(n_xstrips):
                _layer[gid] = layer
                _sheet[gid] = sheet
                _strip_type[gid] = 0
                _strip[gid] = strip
                gid += 1

            # v strips
            for strip in range(n_vstrips):
                _layer[gid] = layer
                _sheet[gid] = sheet
                _strip_type[gid] = 1
                _strip[gid] = strip
                gid += 1

    _layer.setflags(write=False)
    _sheet.setflags(write=False)
    _strip_type.setflags(write=False)
    _strip.setflags(write=False)

    return _layer, _sheet, _strip_type, _strip


_layer, _sheet, _strip_type, _strip = _init()


@nb.vectorize
def get_cgem_gid(
    layer: IntLike, sheet: IntLike, strip_type: IntLike, strip: IntLike
) -> IntLike:
    """
    Get CGEM gid of given layer, sheet, strip_type and strip.

    Parameters:
        layer: The layer number, 0-2.
        sheet: The sheet number within the layer.
        strip_type: The strip type, 0 for x-strip and 1 for v-strip.
        strip: The strip number within the strip type.

    Returns:
        The global strip ID of the CGEM strip, ranging from 0 to 9896.
    """
    gid = (N_SHEETS[:layer] * (N_XSTRIPS[:layer] + N_VSTRIPS[:layer])).sum()
    gid += sheet * (N_XSTRIPS[layer] + N_VSTRIPS[layer])
    gid += strip_type * N_XSTRIPS[layer]
    gid += strip
    return gid


@nb.vectorize
def cgem_gid_to_layer(gid: IntLike) -> IntLike:
    """
    Convert CGEM gid to layer.

    Parameters:
        gid: The gid of the strip.

    Returns:
        The layer number of the strip.
    """
    return _layer[gid]


@nb.vectorize
def cgem_gid_to_sheet(gid: IntLike) -> IntLike:
    """
    Convert CGEM gid to sheet.

    Parameters:
        gid: The gid of the strip.

    Returns:
        The sheet number of the strip.
    """
    return _sheet[gid]


@nb.vectorize
def cgem_gid_to_strip_type(gid: IntLike) -> IntLike:
    """
    Convert CGEM gid to strip type.

    Parameters:
        gid: The gid of the strip.

    Returns:
        The strip type of the strip, 0 for x-strip and 1 for v-strip.
    """
    return _strip_type[gid]


@nb.vectorize
def cgem_gid_to_strip(gid: IntLike) -> IntLike:
    """
    Convert CGEM gid to strip number.

    Parameters:
        gid: The gid of the strip.

    Returns:
        The strip number within the corresponding strip type.
    """
    return _strip[gid]


def cgem_gid_to_is_xstrip(gid: IntLike) -> BoolLike:
    """
    Check whether a CGEM gid corresponds to an x-strip.

    Parameters:
        gid: The gid of the strip.

    Returns:
        True if the strip is an x-strip, otherwise False.
    """
    return cgem_gid_to_strip_type(gid) == X_STRIP_TYPE


def cgem_gid_to_is_vstrip(gid: IntLike) -> BoolLike:
    """
    Check whether a CGEM gid corresponds to a v-strip.

    Parameters:
        gid: The gid of the strip.

    Returns:
        True if the strip is a v-strip, otherwise False.
    """
    return cgem_gid_to_strip_type(gid) == V_STRIP_TYPE


def parse_cgem_gid(gid: IntLike) -> ak.Array | dict[str, Any]:
    """
    Parse CGEM gid into layer, sheet, strip type and strip number.

    Parameters:
        gid: The gid of the strip.

    Returns:
        If gid is a ak.Array, returns an ak.Array with fields "layer", "sheet", "strip_type",
        "strip", "is_xstrip" and "is_vstrip".
        Otherwise, returns a dictionary with keys "layer", "sheet", "strip_type", "strip",
        "is_xstrip" and "is_vstrip".
    """
    layer = cgem_gid_to_layer(gid)
    sheet = cgem_gid_to_sheet(gid)
    strip_type = cgem_gid_to_strip_type(gid)
    strip = cgem_gid_to_strip(gid)

    res = {
        "layer": layer,
        "sheet": sheet,
        "strip_type": strip_type,
        "strip": strip,
        "is_xstrip": strip_type == X_STRIP_TYPE,
        "is_vstrip": strip_type == V_STRIP_TYPE,
    }

    if isinstance(gid, ak.Array):
        return ak.zip(res)
    else:
        return res
