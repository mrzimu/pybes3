from __future__ import annotations

from typing import Any

import awkward as ak
import numpy as np

import pybes3.kernels.ufuncs as _ufuncs
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
        The strip global ID of the CGEM strip, ranging from 0 to 9896.
    """
    return _ufuncs.get_cgem_gid(layer, sheet, strip_type, strip)


def cgem_gid_to_layer(gid: IntLike) -> IntLike:
    """
    Convert CGEM gid to layer.

    Parameters:
        gid: The strip global ID of the CGEM strip.

    Returns:
        The layer number of the strip.
    """
    return _ufuncs.cgem_gid_to_layer(gid)


def cgem_gid_to_sheet(gid: IntLike) -> IntLike:
    """
    Convert CGEM gid to sheet.

    Parameters:
        gid: The strip global ID of the CGEM strip.

    Returns:
        The sheet number of the strip.
    """
    return _ufuncs.cgem_gid_to_sheet(gid)


def cgem_gid_to_strip_type(gid: IntLike) -> IntLike:
    """
    Convert CGEM gid to strip type.

    Parameters:
        gid: The strip global ID of the CGEM strip.

    Returns:
        The strip type of the strip, 0 for x-strip and 1 for v-strip.
    """
    return _ufuncs.cgem_gid_to_strip_type(gid)


def cgem_gid_to_strip(gid: IntLike) -> IntLike:
    """
    Convert CGEM gid to strip number.

    Parameters:
        gid: The strip global ID of the CGEM strip.

    Returns:
        The strip number within the corresponding strip type.
    """
    return _ufuncs.cgem_gid_to_strip(gid)


def cgem_gid_to_is_xstrip(gid: IntLike) -> BoolLike:
    """
    Check whether a CGEM gid corresponds to an x-strip.

    Parameters:
        gid: The strip global ID of the CGEM strip.

    Returns:
        True if the strip is an x-strip, otherwise False.
    """
    return _ufuncs.cgem_gid_to_is_xstrip(gid)


def cgem_gid_to_is_vstrip(gid: IntLike) -> BoolLike:
    """
    Check whether a CGEM gid corresponds to a v-strip.

    Parameters:
        gid: The strip global ID of the CGEM strip.

    Returns:
        True if the strip is a v-strip, otherwise False.
    """
    return _ufuncs.cgem_gid_to_is_vstrip(gid)


def parse_cgem_gid(gid: IntLike) -> ak.Array | dict[str, Any]:
    """
    Parse CGEM gid into layer, sheet, strip type and strip number.

    Parameters:
        gid: The strip global ID of the CGEM strip.

    Returns:
        If gid is a ak.Array, returns an ak.Array with fields "layer", "sheet", "strip_type",
        "strip", "is_xstrip" and "is_vstrip".
        Otherwise, returns a dictionary with keys "layer", "sheet", "strip_type", "strip",
        "is_xstrip" and "is_vstrip".
    """
    layer = _ufuncs.cgem_gid_to_layer(gid)
    sheet = _ufuncs.cgem_gid_to_sheet(gid)
    strip_type = _ufuncs.cgem_gid_to_strip_type(gid)
    strip = _ufuncs.cgem_gid_to_strip(gid)
    is_xstrip = _ufuncs.cgem_gid_to_is_xstrip(gid)
    is_vstrip = _ufuncs.cgem_gid_to_is_vstrip(gid)

    res = {
        "layer": layer,
        "sheet": sheet,
        "strip_type": strip_type,
        "strip": strip,
        "is_xstrip": is_xstrip,
        "is_vstrip": is_vstrip,
    }

    if isinstance(gid, ak.Array):
        return ak.zip(res)
    else:
        return res
