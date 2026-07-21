from __future__ import annotations

from typing import Any, Literal

import awkward as ak
import numpy as np

import pybes3._kernels._ufuncs as _ufuncs
from pybes3.data import MDC_GEOM
from pybes3.typing import BoolLike, FloatLike, IntLike

N_WIRES = 6796
N_LAYERS = 43
N_SUPERLAYERS = 12


with np.load(MDC_GEOM) as f:
    _mdc_geom_table = dict(f)

_mdc_geom_table["superlayer"] = _mdc_geom_table["superlayer"].astype(np.int16)
_mdc_geom_table["layer"] = _mdc_geom_table["layer"].astype(np.int16)
_mdc_geom_table["wire"] = _mdc_geom_table["wire"].astype(np.int32)
_mdc_geom_table["stereo"] = _mdc_geom_table["stereo"].astype(np.int8)

for v in _mdc_geom_table.values():
    v.setflags(write=False)

_ufuncs._init_mdc_geom(
    _mdc_geom_table["east_x"],
    _mdc_geom_table["east_y"],
    _mdc_geom_table["east_z"],
    _mdc_geom_table["west_x"],
    _mdc_geom_table["west_y"],
    _mdc_geom_table["west_z"],
)


def get_mdc_geom_table(library: Literal["np", "ak", "pd"] = "np"):
    """
    Get the MDC wire position table.

    Parameters:
        library: The library to return the data in. Choose from 'ak', 'np', 'pd'.

    Returns:
        (ak.Array | dict[str, np.ndarray] | pd.DataFrame): The MDC wire position table.

    Raises:
        ValueError: If the library is not 'ak', 'np', or 'pd'.
        ImportError: If the library is 'pd' but pandas is not installed.
    """
    if library == "ak":
        return ak.Array(_mdc_geom_table)
    elif library == "np":
        return {k: v for k, v in _mdc_geom_table.items()}
    elif library == "pd":
        try:
            import pandas as pd  # type: ignore
        except ImportError:
            raise ImportError("Pandas is not installed. Run `pip install pandas`.")
        return pd.DataFrame(_mdc_geom_table)
    else:
        raise ValueError(f"Invalid library {library}. Choose from 'ak', 'np', 'pd'.")


def get_mdc_wire_position(library: Literal["np", "ak", "pd"] = "np"):
    """
    !!! warning "Deprecated"
        This function is deprecated, use `get_mdc_geom_table` instead.
    """
    import warnings

    warnings.warn(
        "get_mdc_wire_position is deprecated, use get_mdc_geom_table instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    return get_mdc_geom_table(library)


def get_mdc_gid(layer: IntLike, wire: IntLike) -> IntLike:
    """
    Get the MDC wire global ID (gid) for the given layer and local wire number.

    Parameters:
        layer: The layer number.
        wire: The local wire number within the layer.

    Returns:
        The global ID of the wire.
    """
    return _ufuncs.get_mdc_gid(layer, wire)


def mdc_gid_to_superlayer(gid: IntLike) -> IntLike:
    """
    Convert gid to superlayer.

    Parameters:
        gid: The global ID of the wire.

    Returns:
        The superlayer number of the wire.
    """
    return _ufuncs.mdc_gid_to_superlayer(gid)


def mdc_layer_to_superlayer(layer: IntLike) -> IntLike:
    """
    Convert layer to superlayer.

    Parameters:
        layer: The layer number.

    Returns:
        The superlayer number of the layer.
    """
    return _ufuncs.mdc_layer_to_superlayer(layer)


def mdc_gid_to_layer(gid: IntLike) -> IntLike:
    """
    Convert gid to layer.

    Parameters:
        gid: The global ID of the wire.

    Returns:
        The layer number of the wire.
    """
    return _ufuncs.mdc_gid_to_layer(gid)


def mdc_gid_to_wire(gid: IntLike) -> IntLike:
    """
    Convert gid to wire.

    Parameters:
        gid: The global ID of the wire.

    Returns:
        The wire number of the wire.
    """
    return _ufuncs.mdc_gid_to_wire(gid)


def mdc_gid_to_stereo(gid: IntLike) -> IntLike:
    """
    Convert gid to stereo.
    `0` for `axial`,
    `-1` for stereo that `phi_west < phi_east`,
    `1` for stereo that `phi_west > phi_east`.

    Parameters:
        gid: The global ID of the wire.

    Returns:
        The stereo of the wire.
    """
    return _ufuncs.mdc_gid_to_stereo(gid)


def mdc_layer_to_is_stereo(layer: IntLike) -> BoolLike:
    """
    Convert layer to is_stereo.

    Parameters:
        layer: The layer number.

    Returns:
        The is_stereo of the layer.
    """
    return _ufuncs.mdc_layer_to_is_stereo(layer)


def mdc_gid_to_is_stereo(gid: IntLike) -> BoolLike:
    """
    Convert gid to is_stereo.

    Parameters:
        gid: The global ID of the wire.

    Returns:
        The is_stereo of the wire.
    """
    return _ufuncs.mdc_gid_to_is_stereo(gid)


def mdc_gid_to_west_x(gid: IntLike) -> FloatLike:
    """
    Convert gid to west_x (cm).

    Parameters:
        gid: The global ID of the wire.

    Returns:
        The west_x (cm) of the wire.
    """
    return _ufuncs.mdc_gid_to_west_x(gid)


def mdc_gid_to_west_y(gid: IntLike) -> FloatLike:
    """
    Convert gid to west_y (cm).

    Parameters:
        gid: The global ID of the wire.

    Returns:
        The west_y (cm) of the wire.
    """
    return _ufuncs.mdc_gid_to_west_y(gid)


def mdc_gid_to_west_z(gid: IntLike) -> FloatLike:
    """
    Convert gid to west_z (cm).

    Parameters:
        gid: The global ID of the wire.

    Returns:
        The west_z (cm) of the wire.
    """
    return _ufuncs.mdc_gid_to_west_z(gid)


def mdc_gid_to_east_x(gid: IntLike) -> FloatLike:
    """
    Convert gid to east_x (cm).

    Parameters:
        gid: The global ID of the wire.

    Returns:
        The east_x (cm) of the wire.
    """
    return _ufuncs.mdc_gid_to_east_x(gid)


def mdc_gid_to_east_y(gid: IntLike) -> FloatLike:
    """
    Convert gid to east_y (cm).

    Parameters:
        gid: The global ID of the wire.

    Returns:
        The east_y (cm) of the wire.
    """
    return _ufuncs.mdc_gid_to_east_y(gid)


def mdc_gid_to_east_z(gid: IntLike) -> FloatLike:
    """
    Convert gid to east_z (cm).

    Parameters:
        gid: The global ID of the wire.

    Returns:
        The east_z (cm) of the wire.
    """
    return _ufuncs.mdc_gid_to_east_z(gid)


def mdc_gid_z_to_x(gid: IntLike, z: FloatLike) -> FloatLike:
    """
    Get the x (cm) position of the wire at z (cm).

    Parameters:
        gid: The global ID of the wire.
        z: The z (cm) position.

    Returns:
        The x (cm) position of the wire at z (cm).
    """
    return _ufuncs.mdc_gid_z_to_x(gid, z)


def mdc_gid_z_to_y(gid: IntLike, z: FloatLike) -> FloatLike:
    """
    Get the y (cm) position of the wire at z (cm).

    Parameters:
        gid: The global ID of the wire.
        z: The z (cm) position.

    Returns:
        The y (cm) position of the wire at z (cm).
    """
    return _ufuncs.mdc_gid_z_to_y(gid, z)


def parse_mdc_gid(gid: IntLike, geometry: bool = False) -> ak.Array | dict[str, Any]:
    """
    Parse the gid of MDC wires. "gid" is the global ID of the wire, ranges from 0 to 6795.
    When `gid` is an `ak.Array`, the result is an `ak.Array`, otherwise it is a `dict`.

    Keys of the output:

    - `gid`: Global ID of the wire.
    - `layer`: Layer number.
    - `wire`: Local wire number.
    - `stereo`: Stereo type. 0 for axial, -1 for `phi_west < phi_east`, 1 for `phi_west > phi_east`.
    - `is_stereo`: Whether the wire is a stereo wire.
    - `superlayer`: Superlayer number.

    Optional keys of the output when `geometry` is `True`:

    - `mid_x`: x position of the wire at `z=0`.
    - `mid_y`: y position of the wire at `z=0`.
    - `west_x`: x position of the west end of the wire.
    - `west_y`: y position of the west end of the wire.
    - `west_z`: z position of the west end of the wire.
    - `east_x`: x position of the east end of the wire.
    - `east_y`: y position of the east end of the wire.
    - `east_z`: z position of the east end of the wire.

    Parameters:
        gid: The global ID of the wire.
        geometry: Whether to include the geometry information.

    Returns:
        The parsed result.
    """
    layer = _ufuncs.mdc_gid_to_layer(gid)
    wire = _ufuncs.mdc_gid_to_wire(gid)

    res = {
        "gid": gid,
        "layer": layer,
        "wire": wire,
        "stereo": _ufuncs.mdc_gid_to_stereo(gid),
        "is_stereo": _ufuncs.mdc_gid_to_is_stereo(gid),
        "superlayer": _ufuncs.mdc_gid_to_superlayer(gid),
    }

    if geometry:
        west_x = _ufuncs.mdc_gid_to_west_x(gid)
        west_y = _ufuncs.mdc_gid_to_west_y(gid)
        east_x = _ufuncs.mdc_gid_to_east_x(gid)
        east_y = _ufuncs.mdc_gid_to_east_y(gid)
        res["mid_x"] = (west_x + east_x) / 2
        res["mid_y"] = (west_y + east_y) / 2
        res["west_x"] = west_x
        res["west_y"] = west_y
        res["west_z"] = _ufuncs.mdc_gid_to_west_z(gid)
        res["east_x"] = east_x
        res["east_y"] = east_y
        res["east_z"] = _ufuncs.mdc_gid_to_east_z(gid)

    if isinstance(gid, ak.Array):
        return ak.zip(res)
    else:
        return res
