from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

import awkward as ak
import numba as nb
import numpy as np

from pybes3 import digi_id
from pybes3.typing import BoolLike, FloatLike, IntLike

_geom_data_path = Path(__file__).resolve().parent.parent / "data" / "mdc_geom.npz"

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

    _mdc_wire_position = dict(np.load(_geom_data_path))
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


def parse_mdc_gid(gid: IntLike, with_pos: bool = True) -> ak.Array | dict[str, Any]:
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

    Optional keys of the output when `with_pos` is `True`:

    - `mid_x`: x position of the wire at `z=0`.
    - `mid_y`: y position of the wire at `z=0`.
    - `west_x`: x position of the west end of the wire.
    - `west_y`: y position of the west end of the wire.
    - `west_z`: z position of the west end of the wire.
    - `east_x`: x position of the east end of the wire.
    - `east_y`: y position of the east end of the wire.
    - `east_z`: z position of the east end of the wire.

    Parameters:
        gid: The gid of the wire.
        with_pos: Whether to include the position information.

    Returns:
        The parsed result.
    """
    layer = mdc_gid_to_layer(gid)
    wire = mdc_gid_to_wire(gid)

    res = {
        "gid": gid,
        "layer": layer,
        "wire": wire,
        "stereo": mdc_gid_to_stereo(gid),
        "is_stereo": mdc_gid_to_is_stereo(gid),
        "superlayer": mdc_gid_to_superlayer(gid),
    }

    if with_pos:
        west_x = mdc_gid_to_west_x(gid)
        west_y = mdc_gid_to_west_y(gid)
        east_x = mdc_gid_to_east_x(gid)
        east_y = mdc_gid_to_east_y(gid)
        res["mid_x"] = (west_x + east_x) / 2
        res["mid_y"] = (west_y + east_y) / 2
        res["west_x"] = west_x
        res["west_y"] = west_y
        res["west_z"] = mdc_gid_to_west_z(gid)
        res["east_x"] = east_x
        res["east_y"] = east_y
        res["east_z"] = mdc_gid_to_east_z(gid)

    if isinstance(gid, ak.Array):
        return ak.zip(res)
    else:
        return res


def parse_mdc_digi_id(
    mdc_digi_id: IntLike,
    with_pos: bool = False,
) -> ak.Array | dict[str, Any]:
    """
    Parse MDC digi ID.

    When `mdc_digi_id` is an `ak.Array`, the result is an `ak.Array`, otherwise it is a `dict`.

    Keys of the output:

    - `gid`: Global ID of the wire.
    - `wire`: Local wire number.
    - `layer`: Layer number.
    - `stereo`: Stereo type. 0 for axial, -1 for `phi_west < phi_east`, 1 for `phi_west > phi_east`.
    - `is_stereo`: Whether the wire is a stereo wire.
    - `superlayer`: Superlayer number.

    Optional keys of the output when `with_pos` is `True`:

    - `mid_x`: x position of the wire at `z=0`.
    - `mid_y`: y position of the wire at `z=0`.
    - `west_x`: x position of the west end of the wire.
    - `west_y`: y position of the west end of the wire.
    - `west_z`: z position of the west end of the wire.
    - `east_x`: x position of the east end of the wire.
    - `east_y`: y position of the east end of the wire.
    - `east_z`: z position of the east end of the wire.

    Parameters:
        mdc_digi_id: The MDC digi ID.
        with_pos: Whether to include the position information.

    Returns:
        The parsed result.
    """
    wire = digi_id.mdc_id_to_wire(mdc_digi_id)
    layer = digi_id.mdc_id_to_layer(mdc_digi_id)
    gid = get_mdc_gid(layer, wire)
    return parse_mdc_gid(gid, with_pos)


def parse_mdc_digi(mdc_digi: ak.Record, with_pos: bool = False) -> ak.Record:
    """
    Parse MDC raw digi array. The raw digi array should contain [`m_intId`,
    `m_timeChannel`, `m_chargeChannel`, `m_trackIndex`, `m_overflow`] fields.

    Fields of the output:

    - `gid`: Global ID of the wire.
    - `wire`: Local wire number.
    - `layer`: Layer number.
    - `stereo`: Stereo type. 0 for axial, -1 for `phi_west < phi_east`, 1 for `phi_west > phi_east`.
    - `is_stereo`: Whether the wire is a stereo wire.
    - `superlayer`: Superlayer number.
    - `charge_channel`: Charge channel.
    - `time_channel`: Time channel.
    - `track_index`: Track index.
    - `overflow`: Overflow flag.
    - `digi_id`: Raw digi ID.

    Optional fields of the output when `with_pos` is `True`:

    - `mid_x`: x position of the wire at `z=0`.
    - `mid_y`: y position of the wire at `z=0`.
    - `west_x`: x position of the west end of the wire.
    - `west_y`: y position of the west end of the wire.
    - `west_z`: z position of the west end of the wire.
    - `east_x`: x position of the east end of the wire.
    - `east_y`: y position of the east end of the wire.
    - `east_z`: z position of the east end of the wire.

    Parameters:
        mdc_digi: The MDC raw digi array.
        with_pos: Whether to include the position information.

    Returns:
        The parsed MDC digi array.
    """
    gid = parse_mdc_digi_id(mdc_digi["m_intId"], with_pos=with_pos)

    res = {
        "gid": gid["gid"],
        "wire": gid["wire"],
        "layer": gid["layer"],
        "stereo": gid["stereo"],
        "is_stereo": gid["is_stereo"],
        "superlayer": gid["superlayer"],
        "charge_channel": mdc_digi["m_chargeChannel"],
        "time_channel": mdc_digi["m_timeChannel"],
        "track_index": mdc_digi["m_trackIndex"],
        "overflow": mdc_digi["m_overflow"],
        "digi_id": mdc_digi["m_intId"],
    }

    if with_pos:
        res["mid_x"] = gid["mid_x"]
        res["mid_y"] = gid["mid_y"]
        res["west_x"] = gid["west_x"]
        res["west_y"] = gid["west_y"]
        res["west_z"] = gid["west_z"]
        res["east_x"] = gid["east_x"]
        res["east_y"] = gid["east_y"]
        res["east_z"] = gid["east_z"]

    return ak.zip(res)
