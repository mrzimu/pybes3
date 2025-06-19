from pathlib import Path
from typing import Literal

import awkward as ak
import numba as nb
import numpy as np

from ...typing import BoolLike, FloatLike, IntLike

_cur_dir = Path(__file__).resolve().parent

_mdc_wire_position: dict[str, np.ndarray] = dict(np.load(_cur_dir / "mdc_geom.npz"))
_superlayer: np.ndarray = _mdc_wire_position["superlayer"]
_layer: np.ndarray = _mdc_wire_position["layer"]
_wire: np.ndarray = _mdc_wire_position["wire"]
_east_x: np.ndarray = _mdc_wire_position["east_x"]
_east_y: np.ndarray = _mdc_wire_position["east_y"]
_east_z: np.ndarray = _mdc_wire_position["east_z"]
_west_x: np.ndarray = _mdc_wire_position["west_x"]
_west_y: np.ndarray = _mdc_wire_position["west_y"]
_west_z: np.ndarray = _mdc_wire_position["west_z"]
_stereo: np.ndarray = _mdc_wire_position["stereo"]
_is_stereo: np.ndarray = _mdc_wire_position["is_stereo"]

# Generate the wire start index of each layer
layer_start_gid = np.zeros(44, dtype=np.uint16)
for l in range(43):
    layer_start_gid[l + 1] = np.sum(_layer == l)
layer_start_gid = np.cumsum(layer_start_gid)

# Generate the x position along z of each wire
dx_dz = (_east_x - _west_x) / (_east_z - _west_z)
dy_dz = (_east_y - _west_y) / (_east_z - _west_z)

# Generate layer -> is_stereo array
is_layer_stereo = np.zeros(43, dtype=bool)
for l in range(43):
    assert np.unique(_is_stereo[_layer == l]).size == 1
    is_layer_stereo[l] = _is_stereo[_layer == l][0]

# Generate layer -> superlayer array
superlayer_splits = np.array([0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 43])


def get_mdc_wire_position(library: Literal["np", "ak", "pd"] = "np"):
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
    cp: dict[str, np.ndarray] = {k: v.copy() for k, v in _mdc_wire_position.items()}

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


@nb.vectorize(cache=True)
def get_mdc_gid(layer: IntLike, wire: IntLike) -> IntLike:
    """
    Get MDC gid of given layer and wire.

    Parameters:
        layer: The layer number.
        wire: The wire number.

    Returns:
        The gid of the wire.
    """
    return layer_start_gid[layer] + wire


@nb.vectorize(cache=True)
def mdc_gid_to_superlayer(gid: IntLike) -> IntLike:
    """
    Convert gid to superlayer.

    Parameters:
        gid: The gid of the wire.

    Returns:
        The superlayer number of the wire.
    """
    return _superlayer[gid]


@nb.vectorize(cache=True)
def mdc_layer_to_superlayer(layer: IntLike) -> IntLike:
    """
    Convert layer to superlayer.

    Parameters:
        layer: The layer number.

    Returns:
        The superlayer number of the layer.
    """
    return np.digitize(layer, superlayer_splits, right=False) - 1


@nb.vectorize(cache=True)
def mdc_gid_to_layer(gid: IntLike) -> IntLike:
    """
    Convert gid to layer.

    Parameters:
        gid: The gid of the wire.

    Returns:
        The layer number of the wire.
    """
    return _layer[gid]


@nb.vectorize(cache=True)
def mdc_gid_to_wire(gid: IntLike) -> IntLike:
    """
    Convert gid to wire.

    Parameters:
        gid: The gid of the wire.

    Returns:
        The wire number of the wire.
    """
    return _wire[gid]


@nb.vectorize(cache=True)
def mdc_gid_to_stereo(gid: IntLike) -> IntLike:
    """
    Convert gid to stereo.
    `0` for `axial`,
    `-1` for stereo that `phi_west < phi_east`,
    `1` for stereo that `phi_west > phi_east`.

    Parameters:
        gid: The gid of the wire.

    Returns:
        The stereo of the wire.
    """
    return _stereo[gid]


@nb.vectorize(cache=True)
def mdc_layer_to_is_stereo(layer: IntLike) -> BoolLike:
    """
    Convert layer to is_stereo.

    Parameters:
        layer: The layer number.

    Returns:
        The is_stereo of the layer.
    """
    return is_layer_stereo[layer]


@nb.vectorize(cache=True)
def mdc_gid_to_is_stereo(gid: IntLike) -> BoolLike:
    """
    Convert gid to is_stereo.

    Parameters:
        gid: The gid of the wire.

    Returns:
        The is_stereo of the wire.
    """
    return _is_stereo[gid]


@nb.vectorize(cache=True)
def mdc_gid_to_west_x(gid: IntLike) -> FloatLike:
    """
    Convert gid to west_x (cm).

    Parameters:
        gid: The gid of the wire.

    Returns:
        The west_x (cm) of the wire.
    """
    return _west_x[gid]


@nb.vectorize(cache=True)
def mdc_gid_to_west_y(gid: IntLike) -> FloatLike:
    """
    Convert gid to west_y (cm).

    Parameters:
        gid: The gid of the wire.

    Returns:
        The west_y (cm) of the wire.
    """
    return _west_y[gid]


@nb.vectorize(cache=True)
def mdc_gid_to_west_z(gid: IntLike) -> FloatLike:
    """
    Convert gid to west_z (cm).

    Parameters:
        gid: The gid of the wire.

    Returns:
        The west_z (cm) of the wire.
    """
    return _west_z[gid]


@nb.vectorize(cache=True)
def mdc_gid_to_east_x(gid: IntLike) -> FloatLike:
    """
    Convert gid to east_x (cm).

    Parameters:
        gid: The gid of the wire.

    Returns:
        The east_x (cm) of the wire.
    """
    return _east_x[gid]


@nb.vectorize(cache=True)
def mdc_gid_to_east_y(gid: IntLike) -> FloatLike:
    """
    Convert gid to east_y (cm).

    Parameters:
        gid: The gid of the wire.

    Returns:
        The east_y (cm) of the wire.
    """
    return _east_y[gid]


@nb.vectorize(cache=True)
def mdc_gid_to_east_z(gid: IntLike) -> FloatLike:
    """
    Convert gid to east_z (cm).

    Parameters:
        gid: The gid of the wire.

    Returns:
        The east_z (cm) of the wire.
    """
    return _east_z[gid]


@nb.vectorize(cache=True)
def mdc_gid_z_to_x(gid: IntLike, z: FloatLike) -> FloatLike:
    """
    Get the x (cm) position of the wire at z (cm).

    Parameters:
        gid: The gid of the wire.
        z: The z (cm) position.

    Returns:
        The x (cm) position of the wire at z (cm).
    """
    return _west_x[gid] + dx_dz[gid] * (z - _west_z[gid])


@nb.vectorize(cache=True)
def mdc_gid_z_to_y(gid: IntLike, z: FloatLike) -> FloatLike:
    """
    Get the y (cm) position of the wire at z (cm).

    Parameters:
        gid: The gid of the wire.
        z: The z (cm) position.

    Returns:
        The y (cm) position of the wire at z (cm).
    """
    return _west_y[gid] + dy_dz[gid] * (z - _west_z[gid])
