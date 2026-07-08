from __future__ import annotations

from typing import Any, Literal

import awkward as ak
import numpy as np

import pybes3._kernels._ufuncs as _ufuncs
from pybes3._utils import _check_range
from pybes3.data import MDC_GEOM
from pybes3.typing import BoolLike, FloatLike, IntLike

N_WIRES = 6796
N_LAYERS = 43
N_SUPERLAYERS = 12


with np.load(MDC_GEOM) as f:
    _mdc_geom_table = dict(f)

_mdc_geom_table["idx"] = _mdc_geom_table.pop("gid")
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


def _check_idx(idx: IntLike) -> None:
    _check_range(idx, 0, N_WIRES, "idx")


def _check_layer(layer: IntLike) -> None:
    _check_range(layer, 0, N_LAYERS, "layer")


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


def get_mdc_idx(layer: IntLike, wire: IntLike) -> IntLike:
    """
    Get the MDC wire index for the given layer and local wire number.

    Parameters:
        layer: The layer number.
        wire: The local wire number within the layer.

    Returns:
        The index of the wire.
    """
    return _ufuncs.get_mdc_idx(layer, wire)


def get_mdc_gid(layer: IntLike, wire: IntLike) -> IntLike:
    """
    !!! warning "Deprecated"
        This function is deprecated, use `get_mdc_idx` instead.
    """
    import warnings

    warnings.warn(
        "get_mdc_gid is deprecated, use get_mdc_idx instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return get_mdc_idx(layer, wire)


def mdc_idx_to_superlayer(idx: IntLike) -> IntLike:
    """
    Convert index to superlayer.

    Parameters:
        idx: The index of the wire.

    Returns:
        The superlayer number of the wire.
    """
    _check_idx(idx)
    return _ufuncs.mdc_idx_to_superlayer(idx)


def mdc_gid_to_superlayer(gid: IntLike) -> IntLike:
    """
    !!! warning "Deprecated"
        This function is deprecated, use `mdc_idx_to_superlayer` instead.
    """
    import warnings

    warnings.warn(
        "mdc_gid_to_superlayer is deprecated, use mdc_idx_to_superlayer instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return mdc_idx_to_superlayer(gid)


def mdc_layer_to_superlayer(layer: IntLike) -> IntLike:
    """
    Convert layer to superlayer.

    Parameters:
        layer: The layer number.

    Returns:
        The superlayer number of the layer.
    """
    _check_layer(layer)
    return _ufuncs.mdc_layer_to_superlayer(layer)


def mdc_idx_to_layer(idx: IntLike) -> IntLike:
    """
    Convert index to layer.

    Parameters:
        idx: The index of the wire.

    Returns:
        The layer number of the wire.
    """
    _check_idx(idx)
    return _ufuncs.mdc_idx_to_layer(idx)


def mdc_gid_to_layer(gid: IntLike) -> IntLike:
    """
    !!! warning "Deprecated"
        This function is deprecated, use `mdc_idx_to_layer` instead.
    """
    import warnings

    warnings.warn(
        "mdc_gid_to_layer is deprecated, use mdc_idx_to_layer instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return mdc_idx_to_layer(gid)


def mdc_idx_to_wire(idx: IntLike) -> IntLike:
    """
    Convert index to wire.

    Parameters:
        idx: The index of the wire.

    Returns:
        The wire number of the wire.
    """
    _check_idx(idx)
    return _ufuncs.mdc_idx_to_wire(idx)


def mdc_gid_to_wire(gid: IntLike) -> IntLike:
    """
    !!! warning "Deprecated"
        This function is deprecated, use `mdc_idx_to_wire` instead.
    """
    import warnings

    warnings.warn(
        "mdc_gid_to_wire is deprecated, use mdc_idx_to_wire instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return mdc_idx_to_wire(gid)


def mdc_idx_to_stereo(idx: IntLike) -> IntLike:
    """
    Convert index to stereo.
    `0` for `axial`,
    `-1` for stereo that `phi_west < phi_east`,
    `1` for stereo that `phi_west > phi_east`.

    Parameters:
        idx: The index of the wire.

    Returns:
        The stereo of the wire.
    """
    _check_idx(idx)
    return _ufuncs.mdc_idx_to_stereo(idx)


def mdc_gid_to_stereo(gid: IntLike) -> IntLike:
    """
    !!! warning "Deprecated"
        This function is deprecated, use `mdc_idx_to_stereo` instead.
    """
    import warnings

    warnings.warn(
        "mdc_gid_to_stereo is deprecated, use mdc_idx_to_stereo instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return mdc_idx_to_stereo(gid)


def mdc_layer_to_is_stereo(layer: IntLike) -> BoolLike:
    """
    Convert layer to is_stereo.

    Parameters:
        layer: The layer number.

    Returns:
        The is_stereo of the layer.
    """
    _check_layer(layer)
    return _ufuncs.mdc_layer_to_is_stereo(layer)


def mdc_idx_to_is_stereo(idx: IntLike) -> BoolLike:
    """
    Convert index to is_stereo.

    Parameters:
        idx: The index of the wire.

    Returns:
        The is_stereo of the wire.
    """
    _check_idx(idx)
    return _ufuncs.mdc_idx_to_is_stereo(idx)


def mdc_gid_to_is_stereo(gid: IntLike) -> BoolLike:
    """
    !!! warning "Deprecated"
        This function is deprecated, use `mdc_idx_to_is_stereo` instead.
    """
    import warnings

    warnings.warn(
        "mdc_gid_to_is_stereo is deprecated, use mdc_idx_to_is_stereo instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return mdc_idx_to_is_stereo(gid)


def mdc_idx_to_west_x(idx: IntLike) -> FloatLike:
    """
    Convert index to west_x (cm).

    Parameters:
        idx: The index of the wire.

    Returns:
        The west_x (cm) of the wire.
    """
    _check_idx(idx)
    return _ufuncs.mdc_idx_to_west_x(idx)


def mdc_gid_to_west_x(gid: IntLike) -> FloatLike:
    """
    !!! warning "Deprecated"
        This function is deprecated, use `mdc_idx_to_west_x` instead.
    """
    import warnings

    warnings.warn(
        "mdc_gid_to_west_x is deprecated, use mdc_idx_to_west_x instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return mdc_idx_to_west_x(gid)


def mdc_idx_to_west_y(idx: IntLike) -> FloatLike:
    """
    Convert index to west_y (cm).

    Parameters:
        idx: The index of the wire.

    Returns:
        The west_y (cm) of the wire.
    """
    _check_idx(idx)
    return _ufuncs.mdc_idx_to_west_y(idx)


def mdc_gid_to_west_y(gid: IntLike) -> FloatLike:
    """
    !!! warning "Deprecated"
        This function is deprecated, use `mdc_idx_to_west_y` instead.
    """
    import warnings

    warnings.warn(
        "mdc_gid_to_west_y is deprecated, use mdc_idx_to_west_y instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return mdc_idx_to_west_y(gid)


def mdc_idx_to_west_z(idx: IntLike) -> FloatLike:
    """
    Convert index to west_z (cm).

    Parameters:
        idx: The index of the wire.

    Returns:
        The west_z (cm) of the wire.
    """
    _check_idx(idx)
    return _ufuncs.mdc_idx_to_west_z(idx)


def mdc_gid_to_west_z(gid: IntLike) -> FloatLike:
    """
    !!! warning "Deprecated"
        This function is deprecated, use `mdc_idx_to_west_z` instead.
    """
    import warnings

    warnings.warn(
        "mdc_gid_to_west_z is deprecated, use mdc_idx_to_west_z instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return mdc_idx_to_west_z(gid)


def mdc_idx_to_east_x(idx: IntLike) -> FloatLike:
    """
    Convert index to east_x (cm).

    Parameters:
        idx: The index of the wire.

    Returns:
        The east_x (cm) of the wire.
    """
    _check_idx(idx)
    return _ufuncs.mdc_idx_to_east_x(idx)


def mdc_gid_to_east_x(gid: IntLike) -> FloatLike:
    """
    !!! warning "Deprecated"
        This function is deprecated, use `mdc_idx_to_east_x` instead.
    """
    import warnings

    warnings.warn(
        "mdc_gid_to_east_x is deprecated, use mdc_idx_to_east_x instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return mdc_idx_to_east_x(gid)


def mdc_idx_to_east_y(idx: IntLike) -> FloatLike:
    """
    Convert index to east_y (cm).

    Parameters:
        idx: The index of the wire.

    Returns:
        The east_y (cm) of the wire.
    """
    _check_idx(idx)
    return _ufuncs.mdc_idx_to_east_y(idx)


def mdc_gid_to_east_y(gid: IntLike) -> FloatLike:
    """
    !!! warning "Deprecated"
        This function is deprecated, use `mdc_idx_to_east_y` instead.
    """
    import warnings

    warnings.warn(
        "mdc_gid_to_east_y is deprecated, use mdc_idx_to_east_y instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return mdc_idx_to_east_y(gid)


def mdc_idx_to_east_z(idx: IntLike) -> FloatLike:
    """
    Convert index to east_z (cm).

    Parameters:
        idx: The index of the wire.

    Returns:
        The east_z (cm) of the wire.
    """
    _check_idx(idx)
    return _ufuncs.mdc_idx_to_east_z(idx)


def mdc_gid_to_east_z(gid: IntLike) -> FloatLike:
    """
    !!! warning "Deprecated"
        This function is deprecated, use `mdc_idx_to_east_z` instead.
    """
    import warnings

    warnings.warn(
        "mdc_gid_to_east_z is deprecated, use mdc_idx_to_east_z instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return mdc_idx_to_east_z(gid)


def mdc_idx_z_to_x(idx: IntLike, z: FloatLike) -> FloatLike:
    """
    Get the x (cm) position of the wire at z (cm).

    Parameters:
        idx: The index of the wire.
        z: The z (cm) position.

    Returns:
        The x (cm) position of the wire at z (cm).
    """
    _check_idx(idx)
    return _ufuncs.mdc_idx_z_to_x(idx, z)


def mdc_gid_z_to_x(gid: IntLike, z: FloatLike) -> FloatLike:
    """
    !!! warning "Deprecated"
        This function is deprecated, use `mdc_idx_z_to_x` instead.
    """
    import warnings

    warnings.warn(
        "mdc_gid_z_to_x is deprecated, use mdc_idx_z_to_x instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return mdc_idx_z_to_x(gid, z)


def mdc_idx_z_to_y(idx: IntLike, z: FloatLike) -> FloatLike:
    """
    Get the y (cm) position of the wire at z (cm).

    Parameters:
        idx: The index of the wire.
        z: The z (cm) position.

    Returns:
        The y (cm) position of the wire at z (cm).
    """
    _check_idx(idx)
    return _ufuncs.mdc_idx_z_to_y(idx, z)


def mdc_gid_z_to_y(gid: IntLike, z: FloatLike) -> FloatLike:
    """
    !!! warning "Deprecated"
        This function is deprecated, use `mdc_idx_z_to_y` instead.
    """
    import warnings

    warnings.warn(
        "mdc_gid_z_to_y is deprecated, use mdc_idx_z_to_y instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return mdc_idx_z_to_y(gid, z)


def parse_mdc_idx(idx: IntLike, geometry: bool = False) -> ak.Array | dict[str, Any]:
    """
    Parse the index of MDC wires. The index ranges from 0 to 6795.
    When `idx` is an `ak.Array`, the result is an `ak.Array`, otherwise it is a `dict`.

    Keys of the output:

    - `idx`: Index of the wire.
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
        idx: The index of the wire.
        geometry: Whether to include the geometry information.

    Returns:
        The parsed result.
    """
    _check_idx(idx)
    layer = _ufuncs.mdc_idx_to_layer(idx)
    wire = _ufuncs.mdc_idx_to_wire(idx)

    res = {
        "idx": idx,
        "layer": layer,
        "wire": wire,
        "stereo": _ufuncs.mdc_idx_to_stereo(idx),
        "is_stereo": _ufuncs.mdc_idx_to_is_stereo(idx),
        "superlayer": _ufuncs.mdc_idx_to_superlayer(idx),
    }

    if geometry:
        west_x = _ufuncs.mdc_idx_to_west_x(idx)
        west_y = _ufuncs.mdc_idx_to_west_y(idx)
        east_x = _ufuncs.mdc_idx_to_east_x(idx)
        east_y = _ufuncs.mdc_idx_to_east_y(idx)
        res["mid_x"] = (west_x + east_x) / 2
        res["mid_y"] = (west_y + east_y) / 2
        res["west_x"] = west_x
        res["west_y"] = west_y
        res["west_z"] = _ufuncs.mdc_idx_to_west_z(idx)
        res["east_x"] = east_x
        res["east_y"] = east_y
        res["east_z"] = _ufuncs.mdc_idx_to_east_z(idx)

    if isinstance(idx, ak.Array):
        return ak.zip(res)
    else:
        return res


def parse_mdc_gid(gid: IntLike, geometry: bool = False) -> ak.Array | dict[str, Any]:
    """
    !!! warning "Deprecated"
        This function is deprecated, use `parse_mdc_idx` instead.
    """
    import warnings

    warnings.warn(
        "parse_mdc_gid is deprecated, use parse_mdc_idx instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return parse_mdc_idx(gid, geometry)
