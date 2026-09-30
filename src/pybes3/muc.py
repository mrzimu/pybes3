from __future__ import annotations

from typing import Any, Literal

import awkward as ak
import numpy as np

import pybes3.kernels.ufuncs as _ufuncs
from pybes3.data import MUC_GEOM
from pybes3.typing import FloatLike, IntLike

N_STRIPS = 9152

BARREL_SEGMENTS = 8
BARREL_LAYERS = 9
BARREL_STRIPS = 5056

ENDCAP_SEGMENTS = 4
ENDCAP_LAYERS = 8
ENDCAP_STRIPS = 2048

with np.load(MUC_GEOM) as f:
    _muc_geom_table: dict[str, np.ndarray] = dict(f)

for v in _muc_geom_table.values():
    v.setflags(write=False)

_part = _muc_geom_table["part"]
_segment = _muc_geom_table["segment"]
_layer = _muc_geom_table["layer"]
_strip = _muc_geom_table["strip"]
_points_x = _muc_geom_table["points_x"]
_points_y = _muc_geom_table["points_y"]
_points_z = _muc_geom_table["points_z"]
_center_x = _muc_geom_table["center_x"]
_center_y = _muc_geom_table["center_y"]
_center_z = _muc_geom_table["center_z"]
_dx = _muc_geom_table["dx"]
_dy = _muc_geom_table["dy"]
_dz = _muc_geom_table["dz"]

_ufuncs._init_muc_geom(
    _points_x,
    _points_y,
    _points_z,
    _center_x,
    _center_y,
    _center_z,
    _dx,
    _dy,
    _dz,
)


def get_muc_geom_table(library: Literal["np", "ak", "pd"] = "np"):
    """
    Get MUC strip position table.

    Parameters:
        library: The library to return the data in. Choose from 'ak', 'np', 'pd'.

    Returns:
        (ak.Array | dict[str, np.ndarray] | pd.DataFrame): The MUC strip position table.

    Raises:
        ValueError: If the library is not 'ak', 'np', or 'pd'.
        ImportError: If the library is 'pd' but pandas is not installed.
    """
    cp: dict[str, np.ndarray] = {k: v.copy() for k, v in _muc_geom_table.items()}

    res: dict[str, np.ndarray] = {}

    for k in [
        "gid",
        "part",
        "segment",
        "layer",
        "strip",
        "center_x",
        "center_y",
        "center_z",
        "dx",
        "dy",
        "dz",
    ]:
        res[k] = cp[k]

    # flatten strip points
    for i in range(8):
        res[f"x{i}"] = cp["points_x"][:, i]
        res[f"y{i}"] = cp["points_y"][:, i]
        res[f"z{i}"] = cp["points_z"][:, i]

    if library == "ak":
        return ak.Array(res)
    elif library == "np":
        return res
    elif library == "pd":
        try:
            import pandas as pd  # type: ignore
        except ImportError:
            raise ImportError("Pandas is not installed. Run `pip install pandas`.")
        return pd.DataFrame(res)
    else:
        raise ValueError(f"Invalid library {library}. Choose from 'ak', 'np', 'pd'.")


def get_muc_gid(part: IntLike, segment: IntLike, layer: IntLike, strip: IntLike) -> IntLike:
    """
    Get the MUC strip global ID (gid) with the given part, segment, layer, and strip.

    Parameters:
        part: part number
        segment: segment number
        layer: layer or gap number
        strip: strip or channel number

    Returns:
        The global ID of the MUC strip/channel.
    """
    return _ufuncs.get_muc_gid(part, segment, layer, strip)


def muc_gid_to_part(gid: IntLike) -> IntLike:
    """
    Convert MUC strip gid to part.

    Parameters:
        gid: The global ID of the strip, ranging from 0 to 9151.

    Returns:
        The part number of the strip, 0 and 2 for the endcaps, 1 for the barrel.
    """
    return _ufuncs.muc_gid_to_part(gid)


def muc_gid_to_segment(gid: IntLike) -> IntLike:
    """
    Convert MUC strip gid to segment.

    Parameters:
        gid: The global ID of the strip, ranging from 0 to 9151.

    Returns:
        The segment number of the strip.
    """
    return _ufuncs.muc_gid_to_segment(gid)


def muc_gid_to_layer(gid: IntLike) -> IntLike:
    """
    Convert MUC strip gid to layer (gap).

    Parameters:
        gid: The global ID of the strip, ranging from 0 to 9151.

    Returns:
        The layer (gap) number of the strip.
    """
    return _ufuncs.muc_gid_to_layer(gid)


def muc_gid_to_strip(gid: IntLike) -> IntLike:
    """
    Convert MUC strip gid to strip (channel) number within the layer.

    Parameters:
        gid: The global ID of the strip, ranging from 0 to 9151.

    Returns:
        The strip (channel) number of the strip.
    """
    return _ufuncs.muc_gid_to_strip(gid)


def muc_gid_to_point_x(gid: IntLike, point: IntLike) -> FloatLike:
    """
    Convert MUC strip gid to x coordinate of the point.

    Parameters:
        gid: The global ID of the strip.
        point: The point number, 0-7.

    Returns:
        The x coordinate of the point.
    """
    return _ufuncs.muc_gid_to_point_x(gid, point)


def muc_gid_to_point_y(gid: IntLike, point: IntLike) -> FloatLike:
    """
    Convert MUC strip gid to y coordinate of the point.

    Parameters:
        gid: The global ID of the strip.
        point: The point number, 0-7.

    Returns:
        The y coordinate of the point.
    """
    return _ufuncs.muc_gid_to_point_y(gid, point)


def muc_gid_to_point_z(gid: IntLike, point: IntLike) -> FloatLike:
    """
    Convert MUC strip gid to z coordinate of the point.

    Parameters:
        gid: The global ID of the strip.
        point: The point number, 0-7.

    Returns:
        The z coordinate of the point.
    """
    return _ufuncs.muc_gid_to_point_z(gid, point)


def muc_gid_to_center_x(gid: IntLike) -> FloatLike:
    """
    Convert MUC strip gid to x coordinate of the strip's center.

    Parameters:
        gid: The global ID of the strip.

    Returns:
        The x coordinate of the strip's center.
    """
    return _ufuncs.muc_gid_to_center_x(gid)


def muc_gid_to_center_y(gid: IntLike) -> FloatLike:
    """
    Convert MUC strip gid to y coordinate of the strip's center.

    Parameters:
        gid: The global ID of the strip.

    Returns:
        The y coordinate of the strip's center.
    """
    return _ufuncs.muc_gid_to_center_y(gid)


def muc_gid_to_center_z(gid: IntLike) -> FloatLike:
    """
    Convert MUC strip gid to z coordinate of the strip's center.

    Parameters:
        gid: The global ID of the strip.

    Returns:
        The z coordinate of the strip's center.
    """
    return _ufuncs.muc_gid_to_center_z(gid)


def muc_gid_to_dx(gid: IntLike) -> FloatLike:
    """
    Convert MUC strip gid to the half-length of the strip along x.

    Parameters:
        gid: The global ID of the strip.

    Returns:
        The half-length of the strip along x.
    """
    return _ufuncs.muc_gid_to_dx(gid)


def muc_gid_to_dy(gid: IntLike) -> FloatLike:
    """
    Convert MUC strip gid to the half-length of the strip along y.

    Parameters:
        gid: The global ID of the strip.

    Returns:
        The half-length of the strip along y.
    """
    return _ufuncs.muc_gid_to_dy(gid)


def muc_gid_to_dz(gid: IntLike) -> FloatLike:
    """
    Convert MUC strip gid to the half-length of the strip along z.

    Parameters:
        gid: The global ID of the strip.

    Returns:
        The half-length of the strip along z.
    """
    return _ufuncs.muc_gid_to_dz(gid)


def parse_muc_gid(gid: IntLike, geometry: bool = False) -> ak.Array | dict[str, Any]:
    """
    Parse the gid of MUC strips. "gid" is the global ID of the strip, ranges from 0 to 9151.
    When `gid` is an `ak.Array`, the result is an `ak.Array`, otherwise it is a `dict`.

    Keys of the output:

    - `gid`: Global ID of the strip.
    - `part`: Part number, 0 and 2 for the endcaps, 1 for the barrel.
    - `segment`: Segment number.
    - `layer`: Layer (gap) number.
    - `strip`: Strip (channel) number within the layer.

    Optional keys of the output when `geometry` is `True`:

    - `center_x`: x position of the center of the strip.
    - `center_y`: y position of the center of the strip.
    - `center_z`: z position of the center of the strip.
    - `dx`: Half-length of the strip along x.
    - `dy`: Half-length of the strip along y.
    - `dz`: Half-length of the strip along z.

    !!! info
        The 8 points of the strip will not be returned here.
        If you need the 8 points of the strip, use `muc_gid_to_point_x`, `muc_gid_to_point_y`
        and `muc_gid_to_point_z`.

    Parameters:
        gid: The global ID of the strip.
        geometry: Whether to include the geometry information.

    Returns:
        The parsed result.
    """
    part = _ufuncs.muc_gid_to_part(gid)
    segment = _ufuncs.muc_gid_to_segment(gid)
    layer = _ufuncs.muc_gid_to_layer(gid)
    strip = _ufuncs.muc_gid_to_strip(gid)

    res = {"gid": gid, "part": part, "segment": segment, "layer": layer, "strip": strip}

    if geometry:
        res["center_x"] = _ufuncs.muc_gid_to_center_x(gid)
        res["center_y"] = _ufuncs.muc_gid_to_center_y(gid)
        res["center_z"] = _ufuncs.muc_gid_to_center_z(gid)
        res["dx"] = _ufuncs.muc_gid_to_dx(gid)
        res["dy"] = _ufuncs.muc_gid_to_dy(gid)
        res["dz"] = _ufuncs.muc_gid_to_dz(gid)

    if isinstance(gid, ak.Array):
        return ak.zip(res)
    else:
        return res
