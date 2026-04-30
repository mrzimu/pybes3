from __future__ import annotations

from typing import Any, overload

import awkward as ak
import numba as nb
import numpy as np

from pybes3._utils import _make_lazy
from pybes3.typing import ArrayLike, IntLike

N_LAYER = 3
N_STRIPS = 9897

N_SHEETS = np.array([1, 2, 2])
N_XSTRIPS = np.array([856, 630, 832])
N_VSTRIPS = np.array([1173, 1077, 1395])

X_STRIP_TYPE = 0
V_STRIP_TYPE = 1

# ---------------------------------------------------------------------------
# Lazy loading: gid arrays are loaded on first use.
# ---------------------------------------------------------------------------
_layer: np.ndarray = None
_sheet: np.ndarray = None
_strip_type: np.ndarray = None
_strip: np.ndarray = None
_loaded = False


def _ensure_loaded():
    """Load CGEM gid data on first access."""
    global _layer, _sheet, _strip_type, _strip, _loaded
    if _loaded:
        return

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

    _loaded = True


@overload
def get_cgem_gid(
    layer: ArrayLike,
    sheet: np.integer | ArrayLike,
    strip_type: np.integer | ArrayLike,
    strip: np.integer | ArrayLike,
) -> ArrayLike: ...
@overload
def get_cgem_gid(
    layer: np.integer | ArrayLike,
    sheet: ArrayLike,
    strip_type: np.integer | ArrayLike,
    strip: np.integer | ArrayLike,
) -> ArrayLike: ...
@overload
def get_cgem_gid(
    layer: np.integer | ArrayLike,
    sheet: np.integer | ArrayLike,
    strip_type: ArrayLike,
    strip: np.integer | ArrayLike,
) -> ArrayLike: ...
@overload
def get_cgem_gid(
    layer: np.integer | ArrayLike,
    sheet: np.integer | ArrayLike,
    strip_type: np.integer | ArrayLike,
    strip: ArrayLike,
) -> ArrayLike: ...
@overload
def get_cgem_gid(
    layer: np.integer, sheet: np.integer, strip_type: np.integer, strip: np.integer
) -> np.integer: ...


@nb.vectorize(cache=True)
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


@overload
def cgem_gid_to_layer(gid: ArrayLike) -> ArrayLike: ...
@overload
def cgem_gid_to_layer(gid: np.integer) -> np.integer: ...


@nb.vectorize(cache=True)
def cgem_gid_to_layer(gid: IntLike) -> IntLike:
    """
    Convert CGEM gid to layer.

    Parameters:
        gid: The gid of the strip.

    Returns:
        The layer number of the strip.
    """
    return _layer[gid]


@overload
def cgem_gid_to_sheet(gid: ArrayLike) -> ArrayLike: ...
@overload
def cgem_gid_to_sheet(gid: np.integer) -> np.integer: ...


@nb.vectorize(cache=True)
def cgem_gid_to_sheet(gid: IntLike) -> IntLike:
    """
    Convert CGEM gid to sheet.

    Parameters:
        gid: The gid of the strip.

    Returns:
        The sheet number of the strip.
    """
    return _sheet[gid]


@overload
def cgem_gid_to_strip_type(gid: ArrayLike) -> ArrayLike: ...
@overload
def cgem_gid_to_strip_type(gid: np.integer) -> np.integer: ...


@nb.vectorize(cache=True)
def cgem_gid_to_strip_type(gid: IntLike) -> IntLike:
    """
    Convert CGEM gid to strip type.

    Parameters:
        gid: The gid of the strip.

    Returns:
        The strip type of the strip, 0 for x-strip and 1 for v-strip.
    """
    return _strip_type[gid]


@overload
def cgem_gid_to_strip(gid: ArrayLike) -> ArrayLike: ...
@overload
def cgem_gid_to_strip(gid: np.integer) -> np.integer: ...


@nb.vectorize(cache=True)
def cgem_gid_to_strip(gid: IntLike) -> IntLike:
    """
    Convert CGEM gid to strip number.

    Parameters:
        gid: The gid of the strip.

    Returns:
        The strip number within the corresponding strip type.
    """
    return _strip[gid]


@overload
def cgem_gid_to_is_xstrip(gid: ArrayLike) -> ArrayLike: ...
@overload
def cgem_gid_to_is_xstrip(gid: np.integer) -> np.bool_: ...


def cgem_gid_to_is_xstrip(gid: IntLike) -> IntLike:
    """
    Check whether a CGEM gid corresponds to an x-strip.

    Parameters:
        gid: The gid of the strip.

    Returns:
        True if the strip is an x-strip, otherwise False.
    """
    return cgem_gid_to_strip_type(gid) == X_STRIP_TYPE


@overload
def cgem_gid_to_is_vstrip(gid: ArrayLike) -> ArrayLike: ...
@overload
def cgem_gid_to_is_vstrip(gid: np.integer) -> np.bool_: ...


def cgem_gid_to_is_vstrip(gid: IntLike) -> IntLike:
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


# ---------------------------------------------------------------------------
# Apply lazy-loading wrappers to all functions that access gid data.
# ---------------------------------------------------------------------------
for _fn_name in [
    "cgem_gid_to_layer",
    "cgem_gid_to_sheet",
    "cgem_gid_to_strip_type",
    "cgem_gid_to_strip",
    "cgem_gid_to_is_xstrip",
    "cgem_gid_to_is_vstrip",
]:
    globals()[_fn_name] = _make_lazy(globals()[_fn_name], _ensure_loaded)
del _fn_name
