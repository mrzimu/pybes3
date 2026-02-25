from __future__ import annotations

from pathlib import Path
from typing import Literal

import awkward as ak
import numba as nb
import numpy as np

from ...typing import FloatLike, IntLike

_cur_dir = Path(__file__).resolve().parent

ENDCAP_PHI_01 = 64
ENDCAP_PHI_23 = 80
ENDCAP_PHI_45 = 96
ENDCAP_CRYSTALS = 480

BARREL_PHI = 120
BARREL_CRYSTALS = 5280

# ---------------------------------------------------------------------------
# Lazy loading: geometry arrays are loaded from disk on first use.
# ---------------------------------------------------------------------------
_emc_geom = None
_part = None
_theta = None
_phi = None
_points_x = None
_points_y = None
_points_z = None
_center_x = None
_center_y = None
_center_z = None
_front_center_x = None
_front_center_y = None
_front_center_z = None
_loaded = False


def _ensure_loaded():
    """Load EMC geometry data from disk on first access."""
    global _loaded
    if _loaded:
        return

    global _emc_geom, _part, _theta, _phi
    global _points_x, _points_y, _points_z
    global _center_x, _center_y, _center_z
    global _front_center_x, _front_center_y, _front_center_z

    _emc_geom = dict(np.load(_cur_dir / "emc_geom.npz"))
    _part = _emc_geom["part"]
    _theta = _emc_geom["theta"]
    _phi = _emc_geom["phi"]
    _points_x = _emc_geom["points_x"]
    _points_y = _emc_geom["points_y"]
    _points_z = _emc_geom["points_z"]
    _center_x = _emc_geom["center_x"]
    _center_y = _emc_geom["center_y"]
    _center_z = _emc_geom["center_z"]
    _front_center_x = _emc_geom["front_center_x"]
    _front_center_y = _emc_geom["front_center_y"]
    _front_center_z = _emc_geom["front_center_z"]

    _loaded = True


emc_barrel_r = 94.2
emc_barrel_offset_1 = 2.5
emc_barrel_offset_2 = 5.0
emc_barrel_h1 = 5.1
emc_barrel_h2 = 5.2
emc_barrel_h3 = 5.2466
emc_barrel_l = 28.0


def get_emc_crystal_position(library: Literal["np", "ak", "pd"] = "np"):
    """
    Get EMC crystal position table.

    Parameters:
        library: The library to return the data in. Choose from 'ak', 'np', 'pd'.

    Returns:
        (ak.Array | dict[str, np.ndarray] | pd.DataFrame): The EMC crystal position table.

    Raises:
        ValueError: If the library is not 'ak', 'np', or 'pd'.
        ImportError: If the library is 'pd' but pandas is not installed.
    """
    _ensure_loaded()
    cp: dict[str, np.ndarray] = {k: v.copy() for k, v in _emc_geom.items()}

    res: dict[str, np.ndarray] = {}

    for k in [
        "gid",
        "center_x",
        "center_y",
        "center_z",
        "front_center_x",
        "front_center_y",
        "front_center_z",
    ]:
        res[k] = cp[k]

    # flatten crystal points
    for i in range(8):
        res[f"points_x_{i}"] = cp["points_x"][:, i]
        res[f"points_y_{i}"] = cp["points_y"][:, i]
        res[f"points_z_{i}"] = cp["points_z"][:, i]

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


@nb.vectorize(cache=True)
def get_emc_gid(part: IntLike, theta: IntLike, phi: IntLike) -> IntLike:
    """
    Get EMC gid of given part, theta, and phi.

    - part 0: 0-479
        - theta 0: 0-63
        - theta 1: 64-127
        - theta 2: 128-207
        - theta 3: 208-287
        - theta 4: 288-383
        - theta 5: 384-479
    - part 1: 480-5759 (theta 0-47)
    - part 2: 5760-6239
        - theta 5: 5760-5855 (96)
        - theta 4: 5856-5951 (96)
        - theta 3: 5952-6031 (80)
        - theta 2: 6032-6111 (80)
        - theta 1: 6112-6175 (64)
        - theta 0: 6176-6239 (64)

    Parameters:
        part: part number
        theta: theta number
        phi: phi number

    Returns:
        index: EMC index
    """
    if part == 0:
        res = 0
        if theta == 0 or theta == 1:
            return np.uint16(theta * ENDCAP_PHI_01 + phi)

        res += 2 * ENDCAP_PHI_01
        if theta == 2 or theta == 3:
            return np.uint16(res + (theta - 2) * ENDCAP_PHI_23 + phi)

        res += 2 * ENDCAP_PHI_23
        if theta == 4 or theta == 5:
            return np.uint16(res + (theta - 4) * ENDCAP_PHI_45 + phi)

    if part == 1:
        return np.uint16(ENDCAP_CRYSTALS + theta * BARREL_PHI + phi)

    if part == 2:
        res = ENDCAP_CRYSTALS + BARREL_CRYSTALS

        if theta == 4 or theta == 5:
            return np.uint16(res + (5 - theta) * ENDCAP_PHI_45 + phi)

        res += 2 * ENDCAP_PHI_45
        if theta == 2 or theta == 3:
            return np.uint16(res + (3 - theta) * ENDCAP_PHI_23 + phi)

        res += 2 * ENDCAP_PHI_23
        if theta == 0 or theta == 1:
            return np.uint16(res + (1 - theta) * ENDCAP_PHI_01 + phi)

    return np.uint16(65535)


@nb.vectorize(cache=True)
def emc_gid_to_part(gid: IntLike) -> IntLike:
    """
    Convert EMC gid to part.

    Parameters:
        gid: The gid of the crystal.

    Returns:
        The part number of the crystal.
    """
    return _part[gid]


@nb.vectorize(cache=True)
def emc_gid_to_theta(gid: IntLike) -> IntLike:
    """
    Convert EMC gid to theta.

    Parameters:
        gid: The gid of the crystal.

    Returns:
        The theta number of the crystal.
    """
    return _theta[gid]


@nb.vectorize(cache=True)
def emc_gid_to_phi(gid: IntLike) -> IntLike:
    """
    Convert EMC gid to phi.

    Parameters:
        gid: The gid of the crystal.

    Returns:
        The phi number of the crystal.
    """
    return _phi[gid]


@nb.vectorize(cache=True)
def emc_gid_to_point_x(gid: IntLike, point: IntLike) -> FloatLike:
    """
    Convert EMC gid to x coordinate of the point.

    Parameters:
        gid: The gid of the crystal.
        point: The point number, 0-7.

    Returns:
        The x coordinate of the point.
    """
    return _points_x[gid, point]


@nb.vectorize(cache=True)
def emc_gid_to_point_y(gid: IntLike, point: IntLike) -> FloatLike:
    """
    Convert EMC gid to y coordinate of the point.

    Parameters:
        gid: The gid of the crystal.
        point: The point number, 0-7.

    Returns:
        The y coordinate of the point.
    """
    return _points_y[gid, point]


@nb.vectorize(cache=True)
def emc_gid_to_point_z(gid: IntLike, point: IntLike) -> FloatLike:
    """
    Convert EMC gid to z coordinate of the point.

    Parameters:
        gid: The gid of the crystal.
        point: The point number, 0-7.

    Returns:
        The z coordinate of the point.
    """
    return _points_z[gid, point]


@nb.vectorize(cache=True)
def emc_gid_to_center_x(gid: IntLike) -> FloatLike:
    """
    Convert EMC gid to x coordinate of the crystal's center.

    Parameters:
        gid: The gid of the crystal.

    Returns:
        The x coordinate of the crystal's center.
    """
    return _center_x[gid]


@nb.vectorize(cache=True)
def emc_gid_to_center_y(gid: IntLike) -> FloatLike:
    """
    Convert EMC gid to y coordinate of the crystal's center.

    Parameters:
        gid: The gid of the crystal.

    Returns:
        The y coordinate of the crystal's center.
    """
    return _center_y[gid]


@nb.vectorize(cache=True)
def emc_gid_to_center_z(gid: IntLike) -> FloatLike:
    """
    Convert EMC gid to z coordinate of the crystal's center.

    Parameters:
        gid: The gid of the crystal.

    Returns:
        The z coordinate of the crystal's center.
    """
    return _center_z[gid]


@nb.vectorize(cache=True)
def emc_gid_to_front_center_x(gid: IntLike) -> FloatLike:
    """
    Convert EMC gid to x coordinate of the crystal's front center.

    Parameters:
        gid: The gid of the crystal.

    Returns:
        The x coordinate of the crystal's front center.
    """
    return _front_center_x[gid]


@nb.vectorize(cache=True)
def emc_gid_to_front_center_y(gid: IntLike) -> FloatLike:
    """
    Convert EMC gid to y coordinate of the crystal's front center.

    Parameters:
        gid: The gid of the crystal.

    Returns:
        The y coordinate of the crystal's front center.
    """
    return _front_center_y[gid]


@nb.vectorize(cache=True)
def emc_gid_to_front_center_z(gid: IntLike) -> FloatLike:
    """
    Convert EMC gid to z coordinate of the crystal's front center.

    Parameters:
        gid: The gid of the crystal.

    Returns:
        The z coordinate of the crystal's front center.
    """
    return _front_center_z[gid]


# ---------------------------------------------------------------------------
# Apply lazy-loading wrappers to all functions that access geometry data.
# ---------------------------------------------------------------------------
def _make_lazy(func):
    def wrapper(*args, **kwargs):
        _ensure_loaded()
        return func(*args, **kwargs)

    wrapper.__name__ = getattr(func, "__name__", str(func))
    wrapper.__doc__ = getattr(func, "__doc__", None)
    wrapper.__wrapped__ = func
    return wrapper


for _fn_name in [
    "emc_gid_to_part",
    "emc_gid_to_theta",
    "emc_gid_to_phi",
    "emc_gid_to_point_x",
    "emc_gid_to_point_y",
    "emc_gid_to_point_z",
    "emc_gid_to_center_x",
    "emc_gid_to_center_y",
    "emc_gid_to_center_z",
    "emc_gid_to_front_center_x",
    "emc_gid_to_front_center_y",
    "emc_gid_to_front_center_z",
]:
    globals()[_fn_name] = _make_lazy(globals()[_fn_name])
del _fn_name
