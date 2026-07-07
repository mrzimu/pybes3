from __future__ import annotations

from typing import Any, Literal

import awkward as ak
import numpy as np

import pybes3._kernels._ufuncs as _ufuncs
from pybes3.data import EMC_GEOM
from pybes3.typing import FloatLike, IntLike

N_CRYSTALS = 6240

ENDCAP_PHI_01 = 64
ENDCAP_PHI_23 = 80
ENDCAP_PHI_45 = 96
ENDCAP_CRYSTALS = 480
BARREL_PHI = 120
BARREL_CRYSTALS = 5280

BARREL_RADIUS = 94.2
BARREL_OFFSET_1 = 2.5
BARREL_OFFSET_2 = 5.0
BARREL_H1 = 5.1
BARREL_H2 = 5.2
BARREL_H3 = 5.2466
BARREL_L = 28.0

with np.load(EMC_GEOM) as f:
    _emc_geom = dict(f)

_emc_geom["part"] = _emc_geom["part"].astype(np.int16)
_emc_geom["theta"] = _emc_geom["theta"].astype(np.int32)
_emc_geom["phi"] = _emc_geom["phi"].astype(np.int32)


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

_ufuncs._init_emc_geom(
    _points_x,
    _points_y,
    _points_z,
    _center_x,
    _center_y,
    _center_z,
    _front_center_x,
    _front_center_y,
    _front_center_z,
)


def get_emc_geom_table(library: Literal["np", "ak", "pd"] = "np"):
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
    cp: dict[str, np.ndarray] = {k: v.copy() for k, v in _emc_geom.items()}

    res: dict[str, np.ndarray] = {}

    for k in [
        "gid",
        "part",
        "theta",
        "phi",
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


def get_emc_crystal_position(library: Literal["np", "ak", "pd"] = "np"):
    """
    !!! warning "Deprecated"
        This function is deprecated, use `get_emc_geom_table` instead.
    """
    import warnings

    warnings.warn(
        "get_emc_crystal_position is deprecated, use get_emc_geom_table instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    return get_emc_geom_table(library)


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
    return _ufuncs.get_emc_idx(part, theta, phi)


def emc_gid_to_part(gid: IntLike) -> IntLike:
    """
    Convert EMC gid to part.

    Parameters:
        gid: The gid of the crystal.

    Returns:
        The part number of the crystal.
    """
    return _ufuncs.emc_idx_to_part(gid)


def emc_gid_to_theta(gid: IntLike) -> IntLike:
    """
    Convert EMC gid to theta.

    Parameters:
        gid: The gid of the crystal.

    Returns:
        The theta number of the crystal.
    """
    return _ufuncs.emc_idx_to_theta(gid)


def emc_gid_to_phi(gid: IntLike) -> IntLike:
    """
    Convert EMC gid to phi.

    Parameters:
        gid: The gid of the crystal.

    Returns:
        The phi number of the crystal.
    """
    return _ufuncs.emc_idx_to_phi(gid)


def emc_gid_to_point_x(gid: IntLike, point: IntLike) -> FloatLike:
    """
    Convert EMC gid to x coordinate of the point.

    Parameters:
        gid: The gid of the crystal.
        point: The point number, 0-7.

    Returns:
        The x coordinate of the point.
    """
    return _ufuncs.emc_idx_to_point_x(gid, point)


def emc_gid_to_point_y(gid: IntLike, point: IntLike) -> FloatLike:
    """
    Convert EMC gid to y coordinate of the point.

    Parameters:
        gid: The gid of the crystal.
        point: The point number, 0-7.

    Returns:
        The y coordinate of the point.
    """
    return _ufuncs.emc_idx_to_point_y(gid, point)


def emc_gid_to_point_z(gid: IntLike, point: IntLike) -> FloatLike:
    """
    Convert EMC gid to z coordinate of the point.

    Parameters:
        gid: The gid of the crystal.
        point: The point number, 0-7.

    Returns:
        The z coordinate of the point.
    """
    return _ufuncs.emc_idx_to_point_z(gid, point)


def emc_gid_to_center_x(gid: IntLike) -> FloatLike:
    """
    Convert EMC gid to x coordinate of the crystal's center.

    Parameters:
        gid: The gid of the crystal.

    Returns:
        The x coordinate of the crystal's center.
    """
    return _ufuncs.emc_idx_to_center_x(gid)


def emc_gid_to_center_y(gid: IntLike) -> FloatLike:
    """
    Convert EMC gid to y coordinate of the crystal's center.

    Parameters:
        gid: The gid of the crystal.

    Returns:
        The y coordinate of the crystal's center.
    """
    return _ufuncs.emc_idx_to_center_y(gid)


def emc_gid_to_center_z(gid: IntLike) -> FloatLike:
    """
    Convert EMC gid to z coordinate of the crystal's center.

    Parameters:
        gid: The gid of the crystal.

    Returns:
        The z coordinate of the crystal's center.
    """
    return _ufuncs.emc_idx_to_center_z(gid)


def emc_gid_to_front_center_x(gid: IntLike) -> FloatLike:
    """
    Convert EMC gid to x coordinate of the crystal's front center.

    Parameters:
        gid: The gid of the crystal.

    Returns:
        The x coordinate of the crystal's front center.
    """
    return _ufuncs.emc_idx_to_front_center_x(gid)


def emc_gid_to_front_center_y(gid: IntLike) -> FloatLike:
    """
    Convert EMC gid to y coordinate of the crystal's front center.

    Parameters:
        gid: The gid of the crystal.

    Returns:
        The y coordinate of the crystal's front center.
    """
    return _ufuncs.emc_idx_to_front_center_y(gid)


def emc_gid_to_front_center_z(gid: IntLike) -> FloatLike:
    """
    Convert EMC gid to z coordinate of the crystal's front center.

    Parameters:
        gid: The gid of the crystal.

    Returns:
        The z coordinate of the crystal's front center.
    """
    return _ufuncs.emc_idx_to_front_center_z(gid)


def parse_emc_gid(gid: IntLike, geometry: bool = False) -> ak.Array | dict[str, Any]:
    """
    Parse the gid of EMC crystals. "gid" is the global ID of the crystal, ranges from 0 to 6239.
    When `gid` is an `ak.Array`, the result is an `ak.Array`, otherwise it is a `dict`.

    Keys of the output:

    - `gid`: Global ID of the crystal.
    - `part`: Part number, 0 for endcap0, 1 for barrel, 2 for endcap1.
    - `theta`: Theta number.
    - `phi`: Phi number.

    Optional keys of the output when `geometry` is `True`:

    - `front_center_x`: x position of the front center of the crystal.
    - `front_center_y`: y position of the front center of the crystal.
    - `front_center_z`: z position of the front center of the crystal.
    - `center_x`: x position of the center of the crystal.
    - `center_y`: y position of the center of the crystal.
    - `center_z`: z position of the center of the crystal.

    !!! info
        The 8 points of the crystal will not be returned here.
        If you need the 8 points of the crystal, use `emc_gid_to_point_x`, `emc_gid_to_point_y`
        and `emc_gid_to_point_z`.

    Parameters:
        gid: The gid of the crystal.
        geometry: Whether to include the geometry information.

    Returns:
        The parsed result.
    """
    part = emc_gid_to_part(gid)
    theta = emc_gid_to_theta(gid)
    phi = emc_gid_to_phi(gid)

    res = {"gid": gid, "part": part, "theta": theta, "phi": phi}

    if geometry:
        res["front_center_x"] = emc_gid_to_front_center_x(gid)
        res["front_center_y"] = emc_gid_to_front_center_y(gid)
        res["front_center_z"] = emc_gid_to_front_center_z(gid)
        res["center_x"] = emc_gid_to_center_x(gid)
        res["center_y"] = emc_gid_to_center_y(gid)
        res["center_z"] = emc_gid_to_center_z(gid)

    if isinstance(gid, ak.Array):
        return ak.zip(res)
    else:
        return res
