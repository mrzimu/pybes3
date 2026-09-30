from __future__ import annotations

from typing import Any, Literal

import awkward as ak
import numpy as np

import pybes3.kernels.ufuncs as _ufuncs
from pybes3.data import TOF_GEOM
from pybes3.typing import BoolLike, FloatLike, IntLike

N_PARTS = 5
N_LAYER_OR_MODULE = np.array([1, 2, 1, 36, 36])
N_PHI_OR_STRIP = np.array([48, 88, 48, 12, 12])
N_STRIPS = (N_LAYER_OR_MODULE * N_PHI_OR_STRIP).sum()

N_LAYER_OR_MODULE.setflags(write=False)
N_PHI_OR_STRIP.setflags(write=False)

with np.load(TOF_GEOM) as f:
    _tof_geom_table = dict(f)

for v in _tof_geom_table.values():
    v.setflags(write=False)


_part = _tof_geom_table["part"]
_layer_or_module = _tof_geom_table["layer_or_module"]
_phi_or_strip = _tof_geom_table["phi_or_strip"]
_points_x = _tof_geom_table["points_x"]
_points_y = _tof_geom_table["points_y"]
_points_z = _tof_geom_table["points_z"]

_ufuncs._init_tof_geom(
    _points_x,
    _points_y,
    _points_z,
)


def get_tof_geom_table(library: Literal["np", "ak", "pd"] = "np"):
    """
    Get TOF scintillator / MRPC position table.

    Parameters:
        library: The library to return the data in. Choose from 'ak', 'np', 'pd'.

    Returns:
        (ak.Array | dict[str, np.ndarray] | pd.DataFrame): The TOF scintillator / MRPC position table.

    Raises:
        ValueError: If the library is not 'ak', 'np', or 'pd'.
        ImportError: If the library is 'pd' but pandas is not installed.
    """
    cp: dict[str, np.ndarray] = {k: v.copy() for k, v in _tof_geom_table.items()}

    res: dict[str, np.ndarray] = {}
    for k in ["gid", "part", "layer_or_module", "phi_or_strip"]:
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


def get_tof_gid(part: IntLike, layer_or_module: IntLike, phi_or_strip: IntLike) -> IntLike:
    """
    Get TOF gid of given part, layer_or_module and phi_or_strip.

    Parameters:
        part: The part of the TOF, 0-2 for scintillator, 3-4 for MRPC.
        layer_or_module: The layer (for scintillator) or module (for MRPC) number, starting from 0.
        phi_or_strip: The phi (for scintillator) or strip (for MRPC) number, starting from 0.

    Returns:
        The strip global ID of the TOF strip, ranging from 0 to 1135.
    """
    return _ufuncs.get_tof_gid(part, layer_or_module, phi_or_strip)


def tof_gid_to_part(gid: IntLike) -> IntLike:
    """
    Get TOF part from gid.

    Parameters:
        gid: The strip global ID of the TOF strip, ranging from 0 to 1135.

    Returns:
        The part of the TOF strip.
    """
    return _ufuncs.tof_gid_to_part(gid)


def tof_gid_to_layer_or_module(gid: IntLike) -> IntLike:
    """
    Get TOF layer_or_module from gid.

    Parameters:
        gid: The strip global ID of the TOF strip, ranging from 0 to 1135.

    Returns:
        The layer (for scintillator) or module (for MRPC) number of the TOF strip.
    """
    return _ufuncs.tof_gid_to_layer_or_module(gid)


def tof_gid_to_phi_or_strip(gid: IntLike) -> IntLike:
    """
    Get TOF phi_or_strip from gid.

    Parameters:
        gid: The strip global ID of the TOF strip, ranging from 0 to 1135.

    Returns:
        The phi (for scintillator) or strip (for MRPC) number of the TOF strip.
    """
    return _ufuncs.tof_gid_to_phi_or_strip(gid)


def tof_gid_to_point_x(gid: IntLike, i: IntLike) -> FloatLike:
    """
    Get TOF point x coordinate from gid and index.

    Parameters:
        gid: The strip global ID of the TOF strip, ranging from 0 to 1135.
        i: The index of the point, ranging from 0 to 7.

    Returns:
        The x coordinate of the TOF point.
    """
    return _ufuncs.tof_gid_to_point_x(gid, i)


def tof_gid_to_point_y(gid: IntLike, i: IntLike) -> FloatLike:
    """
    Get TOF point y coordinate from gid and index.

    Parameters:
        gid: The strip global ID of the TOF strip, ranging from 0 to 1135.
        i: The index of the point, ranging from 0 to 7.

    Returns:
        The y coordinate of the TOF point.
    """
    return _ufuncs.tof_gid_to_point_y(gid, i)


def tof_gid_to_point_z(gid: IntLike, i: IntLike) -> FloatLike:
    """
    Get TOF point z coordinate from gid and index.

    Parameters:
        gid: The strip global ID of the TOF strip, ranging from 0 to 1135.
        i: The index of the point, ranging from 0 to 7.

    Returns:
        The z coordinate of the TOF point.
    """
    return _ufuncs.tof_gid_to_point_z(gid, i)


def parse_tof_gid(gid: IntLike) -> ak.Array | dict[str, Any]:
    """
    Parse TOF gid into part, layer_or_module and phi_or_strip.

    Parameters:
        gid: The strip global ID of the TOF strip, ranging from 0 to 1135.

    Returns:
        If gid is a ak.Array, returns an ak.Array with fields "part", "layer_or_module" and "phi_or_strip".
        Otherwise, returns a dictionary with keys "part", "layer_or_module" and "phi_or_strip".
    """
    part = _ufuncs.tof_gid_to_part(gid)
    layer_or_module = _ufuncs.tof_gid_to_layer_or_module(gid)
    phi_or_strip = _ufuncs.tof_gid_to_phi_or_strip(gid)

    res = {
        "part": part,
        "layer_or_module": layer_or_module,
        "phi_or_strip": phi_or_strip,
    }

    if isinstance(gid, ak.Array):
        return ak.zip(res)
    else:
        return res


def tof_hit_status_to_is_raw(status: IntLike) -> BoolLike:
    """Convert hit status to `is_raw`."""
    return _ufuncs.tof_hit_status_to_is_raw(status)


def tof_hit_status_to_is_readout(status: IntLike) -> BoolLike:
    """Convert hit status to `is_readout`."""
    return _ufuncs.tof_hit_status_to_is_readout(status)


def tof_hit_status_to_is_counter(status: IntLike) -> BoolLike:
    """Convert hit status to `is_counter`."""
    return _ufuncs.tof_hit_status_to_is_counter(status)


def tof_hit_status_to_is_cluster(status: IntLike) -> BoolLike:
    """Convert hit status to `is_cluster`."""
    return _ufuncs.tof_hit_status_to_is_cluster(status)


def tof_hit_status_to_is_barrel(status: IntLike) -> BoolLike:
    """Convert hit status to `is_barrel`."""
    return _ufuncs.tof_hit_status_to_is_barrel(status)


def tof_hit_status_to_is_east(status: IntLike) -> BoolLike:
    """Convert hit status to `is_east`."""
    return _ufuncs.tof_hit_status_to_is_east(status)


def tof_hit_status_to_layer(status: IntLike) -> IntLike:
    """Convert hit status to `layer`."""
    return _ufuncs.tof_hit_status_to_layer(status)


def tof_hit_status_to_is_overflow(status: IntLike) -> BoolLike:
    """Convert hit status to `is_overflow`."""
    return _ufuncs.tof_hit_status_to_is_overflow(status)


def tof_hit_status_to_is_multihit(status: IntLike) -> BoolLike:
    """Convert hit status to `is_multihit`."""
    return _ufuncs.tof_hit_status_to_is_multihit(status)


def tof_hit_status_to_n_counter(status: IntLike) -> IntLike:
    """Convert hit status to `n_counter`."""
    return _ufuncs.tof_hit_status_to_n_counter(status)


def tof_hit_status_to_n_east(status: IntLike) -> IntLike:
    """Convert hit status to `n_east`."""
    return _ufuncs.tof_hit_status_to_n_east(status)


def tof_hit_status_to_n_west(status: IntLike) -> IntLike:
    """Convert hit status to `n_west`."""
    return _ufuncs.tof_hit_status_to_n_west(status)


def tof_hit_status_to_is_mrpc(status: IntLike) -> BoolLike:
    """Convert hit status to `is_mrpc`."""
    return _ufuncs.tof_hit_status_to_is_mrpc(status)


def tof_hit_status_id_to_gid(status: IntLike, tof_id: IntLike) -> IntLike:
    """
    Convert the hit status and the `tofID` of a TOF hit into the `gid` of its strip.

    The hit status is used to know which part of the TOF the hit belongs to (see
    `tof_hit_status_to_is_barrel`, `tof_hit_status_to_is_east` and
    `tof_hit_status_to_is_mrpc`), and the `tofID` to know which strip it is. The `tofID` is
    not the raw digi ID: it is a compact index which enumerates the counters of that part,
    with the east and the west endcaps sharing a single index space (east first):

    - barrel: `tof_id = layer * 88 + phi`, and `gid = 48 + tof_id`;
    - scintillator endcaps: `tof_id = 48 * endcap + phi`, and `gid = tof_id` for the east
      endcap, `gid = tof_id + 176` for the west one;
    - MRPC endcaps: `tof_id = 432 * endcap + module * 12 + strip`, and `gid = 272 +
      tof_id` for both endcaps, since `tof_id` already distinguishes them.

    Both arguments must be filtered beforehand: a hit without a hit status
    (`status == 0`) carries the raw digi ID in its `tofID` field instead of the compact
    index, and a negative `tofID` is not a valid counter index.

    Parameters:
        status: The hit status of the TOF hit, encoded as an integer, must not be 0.
        tof_id: The `tofID` of the TOF hit, must not be negative.

    Returns:
        The global ID of the strip the hit belongs to, in the same shape as the input.

    Raises:
        ValueError: If any element of `status` is 0, or if any element of `tof_id` is
            negative.
    """
    m1 = status == 0
    if (isinstance(m1, (bool, np.bool)) and m1) or (
        not isinstance(m1, (bool, np.bool)) and ak.any(m1)
    ):
        raise ValueError(
            "TOF hit status cannot be zero, try to filter them out before calling this function"
        )

    m2 = tof_id < 0
    if (isinstance(m2, (bool, np.bool)) and m2) or (
        not isinstance(m2, (bool, np.bool)) and ak.any(m2)
    ):
        raise ValueError(
            "TOF ID cannot be negative, try to filter them out before calling this function"
        )

    return _ufuncs.tof_hit_status_id_to_gid(status, tof_id)


def parse_tof_hit_status(status: IntLike) -> ak.Array | dict[str, Any]:
    """
    Parse TOF hit status into its components.

    Parameters:
        status: The hit status of a TOF hit, encoded as an integer.

    Returns:
        If status is a ak.Array, returns an ak.Array with the parsed fields.
        Otherwise, returns a dictionary with the parsed fields.
    """
    res = {
        "is_raw": tof_hit_status_to_is_raw(status),
        "is_readout": tof_hit_status_to_is_readout(status),
        "is_counter": tof_hit_status_to_is_counter(status),
        "is_cluster": tof_hit_status_to_is_cluster(status),
        "is_barrel": tof_hit_status_to_is_barrel(status),
        "is_east": tof_hit_status_to_is_east(status),
        "is_overflow": tof_hit_status_to_is_overflow(status),
        "is_multihit": tof_hit_status_to_is_multihit(status),
        "is_mrpc": tof_hit_status_to_is_mrpc(status),
        "layer": tof_hit_status_to_layer(status),
        "n_counter": tof_hit_status_to_n_counter(status),
        "n_east": tof_hit_status_to_n_east(status),
        "n_west": tof_hit_status_to_n_west(status),
    }

    if isinstance(status, ak.Array):
        return ak.zip(res)
    else:
        return res
