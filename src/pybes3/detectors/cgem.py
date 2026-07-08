from __future__ import annotations

from typing import Any

import awkward as ak
import numpy as np

import pybes3._kernels._ufuncs as _ufuncs
from pybes3._utils import _check_range
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


def _check_idx(idx: IntLike) -> None:
    _check_range(idx, 0, N_STRIPS, "idx")


def get_cgem_idx(
    layer: IntLike, sheet: IntLike, strip_type: IntLike, strip: IntLike
) -> IntLike:
    """
    Get the CGEM strip index for the given layer, sheet, strip_type and strip.

    Parameters:
        layer: The layer number, 0-2.
        sheet: The sheet number within the layer.
        strip_type: The strip type, 0 for x-strip and 1 for v-strip.
        strip: The strip number within the strip type.

    Returns:
        The strip index of the CGEM strip, ranging from 0 to 9896.
    """
    return _ufuncs.get_cgem_idx(layer, sheet, strip_type, strip)


def get_cgem_gid(
    layer: IntLike, sheet: IntLike, strip_type: IntLike, strip: IntLike
) -> IntLike:
    """
    !!! warning "Deprecated"
        This function is deprecated, use `get_cgem_idx` instead.
    """
    import warnings

    warnings.warn(
        "get_cgem_gid is deprecated, use get_cgem_idx instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return get_cgem_idx(layer, sheet, strip_type, strip)


def cgem_idx_to_layer(idx: IntLike) -> IntLike:
    """
    Convert CGEM strip index to layer.

    Parameters:
        idx: The index of the strip.

    Returns:
        The layer number of the strip.
    """
    _check_idx(idx)
    return _ufuncs.cgem_idx_to_layer(idx)


def cgem_gid_to_layer(gid: IntLike) -> IntLike:
    """
    !!! warning "Deprecated"
        This function is deprecated, use `cgem_idx_to_layer` instead.
    """
    import warnings

    warnings.warn(
        "cgem_gid_to_layer is deprecated, use cgem_idx_to_layer instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return cgem_idx_to_layer(gid)


def cgem_idx_to_sheet(idx: IntLike) -> IntLike:
    """
    Convert CGEM strip index to sheet.

    Parameters:
        idx: The index of the strip.

    Returns:
        The sheet number of the strip.
    """
    _check_idx(idx)
    return _ufuncs.cgem_idx_to_sheet(idx)


def cgem_gid_to_sheet(gid: IntLike) -> IntLike:
    """
    !!! warning "Deprecated"
        This function is deprecated, use `cgem_idx_to_sheet` instead.
    """
    import warnings

    warnings.warn(
        "cgem_gid_to_sheet is deprecated, use cgem_idx_to_sheet instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return cgem_idx_to_sheet(gid)


def cgem_idx_to_strip_type(idx: IntLike) -> IntLike:
    """
    Convert CGEM strip index to strip type.

    Parameters:
        idx: The index of the strip.

    Returns:
        The strip type of the strip, 0 for x-strip and 1 for v-strip.
    """
    _check_idx(idx)
    return _ufuncs.cgem_idx_to_strip_type(idx)


def cgem_gid_to_strip_type(gid: IntLike) -> IntLike:
    """
    !!! warning "Deprecated"
        This function is deprecated, use `cgem_idx_to_strip_type` instead.
    """
    import warnings

    warnings.warn(
        "cgem_gid_to_strip_type is deprecated, use cgem_idx_to_strip_type instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return cgem_idx_to_strip_type(gid)


def cgem_idx_to_strip(idx: IntLike) -> IntLike:
    """
    Convert CGEM strip index to strip number.

    Parameters:
        idx: The index of the strip.

    Returns:
        The strip number within the corresponding strip type.
    """
    _check_idx(idx)
    return _ufuncs.cgem_idx_to_strip(idx)


def cgem_gid_to_strip(gid: IntLike) -> IntLike:
    """
    !!! warning "Deprecated"
        This function is deprecated, use `cgem_idx_to_strip` instead.
    """
    import warnings

    warnings.warn(
        "cgem_gid_to_strip is deprecated, use cgem_idx_to_strip instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return cgem_idx_to_strip(gid)


def cgem_idx_to_is_xstrip(idx: IntLike) -> BoolLike:
    """
    Check whether a CGEM strip index corresponds to an x-strip.

    Parameters:
        idx: The index of the strip.

    Returns:
        True if the strip is an x-strip, otherwise False.
    """
    _check_idx(idx)
    return _ufuncs.cgem_idx_to_is_xstrip(idx)


def cgem_gid_to_is_xstrip(gid: IntLike) -> BoolLike:
    """
    !!! warning "Deprecated"
        This function is deprecated, use `cgem_idx_to_is_xstrip` instead.
    """
    import warnings

    warnings.warn(
        "cgem_gid_to_is_xstrip is deprecated, use cgem_idx_to_is_xstrip instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return cgem_idx_to_is_xstrip(gid)


def cgem_idx_to_is_vstrip(idx: IntLike) -> BoolLike:
    """
    Check whether a CGEM strip index corresponds to a v-strip.

    Parameters:
        idx: The index of the strip.

    Returns:
        True if the strip is a v-strip, otherwise False.
    """
    _check_idx(idx)
    return _ufuncs.cgem_idx_to_is_vstrip(idx)


def cgem_gid_to_is_vstrip(gid: IntLike) -> BoolLike:
    """
    !!! warning "Deprecated"
        This function is deprecated, use `cgem_idx_to_is_vstrip` instead.
    """
    import warnings

    warnings.warn(
        "cgem_gid_to_is_vstrip is deprecated, use cgem_idx_to_is_vstrip instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return cgem_idx_to_is_vstrip(gid)


def parse_cgem_idx(idx: IntLike) -> ak.Array | dict[str, Any]:
    """
    Parse CGEM strip index into layer, sheet, strip type and strip number.

    Parameters:
        idx: The index of the strip.

    Returns:
        If idx is a ak.Array, returns an ak.Array with fields "layer", "sheet", "strip_type",
        "strip", "is_xstrip" and "is_vstrip".
        Otherwise, returns a dictionary with keys "layer", "sheet", "strip_type", "strip",
        "is_xstrip" and "is_vstrip".
    """
    _check_idx(idx)
    layer = _ufuncs.cgem_idx_to_layer(idx)
    sheet = _ufuncs.cgem_idx_to_sheet(idx)
    strip_type = _ufuncs.cgem_idx_to_strip_type(idx)
    strip = _ufuncs.cgem_idx_to_strip(idx)
    is_xstrip = _ufuncs.cgem_idx_to_is_xstrip(idx)
    is_vstrip = _ufuncs.cgem_idx_to_is_vstrip(idx)

    res = {
        "layer": layer,
        "sheet": sheet,
        "strip_type": strip_type,
        "strip": strip,
        "is_xstrip": is_xstrip,
        "is_vstrip": is_vstrip,
    }

    if isinstance(idx, ak.Array):
        return ak.zip(res)
    else:
        return res


def parse_cgem_gid(gid: IntLike) -> ak.Array | dict[str, Any]:
    """
    !!! warning "Deprecated"
        This function is deprecated, use `parse_cgem_idx` instead.
    """
    import warnings

    warnings.warn(
        "parse_cgem_gid is deprecated, use parse_cgem_idx instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return parse_cgem_idx(gid)
