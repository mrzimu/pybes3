from __future__ import annotations

from pathlib import Path
from typing import Literal

import awkward as ak
import numba as nb
import numpy as np

from ...typing import BoolLike, FloatLike, IntLike

_cur_dir = Path(__file__).resolve().parent

# Constant (not dependent on geometry data)
superlayer_splits = np.array([0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 43])

# ---------------------------------------------------------------------------
# Lazy loading: geometry arrays are loaded from disk on first use.
# ---------------------------------------------------------------------------
_mdc_wire_position = None
_superlayer = None
_layer = None
_wire = None
_east_x = None
_east_y = None
_east_z = None
_west_x = None
_west_y = None
_west_z = None
_stereo = None
_is_stereo = None
layer_start_gid = None
dx_dz = None
dy_dz = None
is_layer_stereo = None
_loaded = False


def _ensure_loaded():
    """Load MDC geometry data from disk on first access."""
    global _loaded
    if _loaded:
        return

    global _mdc_wire_position, _superlayer, _layer, _wire
    global _east_x, _east_y, _east_z, _west_x, _west_y, _west_z
    global _stereo, _is_stereo, layer_start_gid, dx_dz, dy_dz, is_layer_stereo

    _mdc_wire_position = dict(np.load(_cur_dir / "mdc_geom.npz"))
    _superlayer = _mdc_wire_position["superlayer"]
    _layer = _mdc_wire_position["layer"]
    _wire = _mdc_wire_position["wire"]
    _east_x = _mdc_wire_position["east_x"]
    _east_y = _mdc_wire_position["east_y"]
    _east_z = _mdc_wire_position["east_z"]
    _west_x = _mdc_wire_position["west_x"]
    _west_y = _mdc_wire_position["west_y"]
    _west_z = _mdc_wire_position["west_z"]
    _stereo = _mdc_wire_position["stereo"]
    _is_stereo = _mdc_wire_position["is_stereo"]

    layer_start_gid = np.zeros(44, dtype=np.uint16)
    layer_start_gid[1:] = np.cumsum(np.bincount(_layer, minlength=43))

    dx_dz = (_east_x - _west_x) / (_east_z - _west_z)
    dy_dz = (_east_y - _west_y) / (_east_z - _west_z)

    _first_wire_idx = np.searchsorted(_layer, np.arange(43))
    is_layer_stereo = _is_stereo[_first_wire_idx].astype(bool)

    _loaded = True


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
    _ensure_loaded()
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


# ---------------------------------------------------------------------------
# Apply lazy-loading wrappers to all functions that access geometry data.
# After wrapping, calling any of these functions will first trigger
# _ensure_loaded() to load the .npz data if not already loaded.
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
    "get_mdc_gid",
    "mdc_gid_to_superlayer",
    "mdc_gid_to_layer",
    "mdc_gid_to_wire",
    "mdc_gid_to_stereo",
    "mdc_layer_to_is_stereo",
    "mdc_gid_to_is_stereo",
    "mdc_gid_to_west_x",
    "mdc_gid_to_west_y",
    "mdc_gid_to_west_z",
    "mdc_gid_to_east_x",
    "mdc_gid_to_east_y",
    "mdc_gid_to_east_z",
    "mdc_gid_z_to_x",
    "mdc_gid_z_to_y",
]:
    globals()[_fn_name] = _make_lazy(globals()[_fn_name])
del _fn_name
