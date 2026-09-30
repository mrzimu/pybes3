from __future__ import annotations

from typing import Any, Literal

import awkward as ak
import numpy as np

import pybes3.kernels.ufuncs as _ufuncs
from pybes3.data import CGEM_GEOM
from pybes3.typing import BoolLike, FloatLike, IntLike

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

STRIP_THICK = 0.0005
STRIP_WIDTH = np.array([0.058, 0.013])  # X, V
STRIP_RADIUS = np.array(
    [
        [9.0195, 9.0140],  # layer 0 -> X, V
        [13.2555, 13.2500],  # layer 1 -> X, V
        [17.5250, 17.5195],  # layer 2 -> X, V
    ]
)

with np.load(CGEM_GEOM) as f:
    _cgem_geom_table = dict(f)

for v in _cgem_geom_table.values():
    v.setflags(write=False)

_layer = _cgem_geom_table["layer"]
_sheet = _cgem_geom_table["sheet"]
_strip_type = _cgem_geom_table["strip_type"]
_strip = _cgem_geom_table["strip"]
_r = _cgem_geom_table["r"]
_phi0 = _cgem_geom_table["phi0"]
_dphi = _cgem_geom_table["dphi"]
_z0 = _cgem_geom_table["z0"]
_dz = _cgem_geom_table["dz"]
_width = _cgem_geom_table["width"]

_ufuncs._init_cgem_geom(_phi0, _dphi, _z0, _dz)


def get_cgem_geom_table(library: Literal["np", "ak", "pd"] = "np"):
    """
    Get CGEM strip geometry table.

    Parameters:
        library: The library to return the data in. Choose from 'ak', 'np', 'pd'.

    Returns:
        (ak.Array | dict[str, np.ndarray] | pd.DataFrame): The CGEM strip geometry table.

    Raises:
        ValueError: If the library is not 'ak', 'np', or 'pd'.
        ImportError: If the library is 'pd' but pandas is not installed.
    """
    cp: dict[str, np.ndarray] = {k: v.copy() for k, v in _cgem_geom_table.items()}

    if library == "ak":
        return ak.Array(cp)
    elif library == "np":
        return cp
    elif library == "pd":
        try:
            import pandas as pd  # type: ignore
        except ImportError:
            raise ImportError("Pandas is not installed. Run `pip install pandas`.")
        return pd.DataFrame(cp)
    else:
        raise ValueError(f"Invalid library {library}. Choose from 'ak', 'np', 'pd'.")


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


def cgem_gid_to_width(gid: IntLike) -> FloatLike:
    """
    Convert CGEM gid to the width of the strip.

    Parameters:
        gid: The strip global ID of the CGEM strip.

    Returns:
        The width (cm) of the strip, measured along the arc direction for an x-strip and
        perpendicular to the strip for a v-strip.
    """
    return _ufuncs.cgem_gid_to_width(gid)


def cgem_gid_to_radius(gid: IntLike) -> FloatLike:
    """
    Convert CGEM gid to the radius of the strip.

    Parameters:
        gid: The strip global ID of the CGEM strip.

    Returns:
        The radius (cm) of the strip, i.e. its distance from the beam axis.
    """
    return _ufuncs.cgem_gid_to_radius(gid)


def cgem_gid_to_phi0(gid: IntLike) -> FloatLike:
    """
    Convert CGEM gid to the azimuth of the strip at its most negative z end.

    Parameters:
        gid: The strip global ID of the CGEM strip.

    Returns:
        The azimuth (rad) of the centre line of the strip at its most negative z end.
    """
    return _ufuncs.cgem_gid_to_phi0(gid)


def cgem_gid_to_dphi(gid: IntLike) -> FloatLike:
    """
    Convert CGEM gid to the azimuth change of the strip along z.

    Parameters:
        gid: The strip global ID of the CGEM strip.

    Returns:
        The signed change of azimuth (rad) of the centre line from its most negative z end
        towards its most positive z end.
    """
    return _ufuncs.cgem_gid_to_dphi(gid)


def cgem_gid_to_z0(gid: IntLike) -> FloatLike:
    """
    Convert CGEM gid to the most negative z of the strip.

    Parameters:
        gid: The strip global ID of the CGEM strip.

    Returns:
        The most negative z (cm) of the centre line of the strip.
    """
    return _ufuncs.cgem_gid_to_z0(gid)


def cgem_gid_to_dz(gid: IntLike) -> FloatLike:
    """
    Convert CGEM gid to the length of the strip along z.

    Parameters:
        gid: The strip global ID of the CGEM strip.

    Returns:
        The length (cm) of the strip along z, i.e. the z difference between its two ends.
    """
    return _ufuncs.cgem_gid_to_dz(gid)


def cgem_gid_phi_to_z(gid: IntLike, phi: FloatLike) -> FloatLike:
    """
    Get the z (cm) position of a CGEM strip at the azimuth phi (rad).

    The z is obtained by linear interpolation between the two ends of the strip, without
    any range check, so a phi outside the strip is extrapolated. `phi` may be given in any
    period, i.e. it does not have to be wrapped into [-pi, pi].

    Parameters:
        gid: The strip global ID of the CGEM strip.
        phi: The azimuth (rad) of the point.

    Returns:
        The z (cm) position of the strip at phi (rad). It is NaN for an x-strip, whose phi
        does not give any z.
    """
    return _ufuncs.cgem_gid_phi_to_z(gid, phi)


def cgem_gid_z_to_phi(gid: IntLike, z: FloatLike) -> FloatLike:
    """
    Get the azimuth phi (rad) of a CGEM strip at the z (cm) position.

    The phi is obtained by linear interpolation between the two ends of the strip, without
    any range check, so a z outside the strip is extrapolated.

    Parameters:
        gid: The strip global ID of the CGEM strip.
        z: The z (cm) position.

    Returns:
        The azimuth (rad) of the strip at z (cm), which is `phi0 + (z - z0) / dz * dphi` and
        is therefore not wrapped into [-pi, pi]. It is always `phi0` for an x-strip, which
        runs along the z axis.
    """
    return _ufuncs.cgem_gid_z_to_phi(gid, z)


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
