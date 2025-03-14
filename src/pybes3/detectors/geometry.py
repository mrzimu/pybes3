from pathlib import Path
from typing import TypeVar, Union

import awkward as ak
import numba as nb
import numpy as np

TINT = TypeVar("ak.Array | np.ndarray | int")
TFLOAT = TypeVar("ak.Array | np.ndarray | float")
TBOOL = TypeVar("ak.Array | np.ndarray | bool")

cur_dir = Path(__file__).resolve().parent

###############################################################################
#                                     MDC                                     #
###############################################################################
mdc_wire_position: dict[str, np.ndarray] = dict(np.load(cur_dir / "MdcWirePosition.npz"))
layer: np.ndarray = mdc_wire_position["layer"]
wire: np.ndarray = mdc_wire_position["wire"]
east_x: np.ndarray = mdc_wire_position["east_x"]
east_y: np.ndarray = mdc_wire_position["east_y"]
east_z: np.ndarray = mdc_wire_position["east_z"]
west_x: np.ndarray = mdc_wire_position["west_x"]
west_y: np.ndarray = mdc_wire_position["west_y"]
west_z: np.ndarray = mdc_wire_position["west_z"]
is_stereo: np.ndarray = mdc_wire_position["is_stereo"]

# Generate the wire start index of each layer
layer_start_gid = np.zeros(44, dtype=np.uint16)
for l in range(43):
    layer_start_gid[l + 1] = np.sum(layer == l)
layer_start_gid = np.cumsum(layer_start_gid)

# Generate the x position along z of each wire
dx_dz = (east_x - west_x) / (east_z - west_z)
dy_dz = (east_y - west_y) / (east_z - west_z)

# Generate layer -> is_stereo array
is_layer_stereo = np.zeros(43, dtype=bool)
for l in range(43):
    assert np.unique(is_stereo[layer == l]).size == 1
    is_layer_stereo[l] = is_stereo[layer == l][0]


@nb.vectorize([nb.int_(nb.int_, nb.int_)])
def mdc_layer_wire_to_gid(layer: TINT, wire: TINT) -> TINT:
    """
    Convert layer and wire to gid (global index, ranges from 0 to 6795) of the wire.

    Parameters:
        layer: The layer number.
        wire: The wire number.

    Returns:
        The gid of the wire.
    """
    return layer_start_gid[layer] + wire


@nb.vectorize([nb.int_(nb.int_)])
def mdc_gid_to_layer(gid: TINT) -> TINT:
    """
    Convert gid to layer.

    Parameters:
        gid: The gid of the wire.

    Returns:
        The layer number of the wire.
    """
    return layer[gid]


@nb.vectorize([nb.int_(nb.int_)])
def mdc_gid_to_wire(gid: TINT) -> TINT:
    """
    Convert gid to wire.

    Parameters:
        gid: The gid of the wire.

    Returns:
        The wire number of the wire.
    """
    return wire[gid]


@nb.vectorize([nb.boolean(nb.int_)])
def mdc_layer_to_is_stereo(layer: TINT) -> TBOOL:
    """
    Convert layer to is_stereo.

    Parameters:
        layer: The layer number.

    Returns:
        The is_stereo of the layer.
    """
    return is_layer_stereo[layer]


@nb.vectorize([nb.boolean(nb.int_)])
def mdc_gid_to_is_stereo(gid: TINT) -> TBOOL:
    """
    Convert gid to is_stereo.

    Parameters:
        gid: The gid of the wire.

    Returns:
        The is_stereo of the wire.
    """
    return is_stereo[gid]


@nb.vectorize([nb.float32(nb.int_)])
def mdc_gid_to_west_x(gid: TINT) -> TFLOAT:
    """
    Convert gid to west_x (cm).

    Parameters:
        gid: The gid of the wire.

    Returns:
        The west_x (cm) of the wire.
    """
    return west_x[gid]


@nb.vectorize([nb.float32(nb.int_)])
def mdc_gid_to_west_y(gid: TINT) -> TFLOAT:
    """
    Convert gid to west_y (cm).

    Parameters:
        gid: The gid of the wire.

    Returns:
        The west_y (cm) of the wire.
    """
    return west_y[gid]


@nb.vectorize([nb.float32(nb.int_)])
def mdc_gid_to_west_z(gid: TINT) -> TFLOAT:
    """
    Convert gid to west_z (cm).

    Parameters:
        gid: The gid of the wire.

    Returns:
        The west_z (cm) of the wire.
    """
    return west_z[gid]


@nb.vectorize([nb.float32(nb.int_)])
def mdc_gid_to_east_x(gid: TINT) -> TFLOAT:
    """
    Convert gid to east_x (cm).

    Parameters:
        gid: The gid of the wire.

    Returns:
        The east_x (cm) of the wire.
    """
    return east_x[gid]


@nb.vectorize([nb.float32(nb.int_)])
def mdc_gid_to_east_y(gid: TINT) -> TFLOAT:
    """
    Convert gid to east_y (cm).

    Parameters:
        gid: The gid of the wire.

    Returns:
        The east_y (cm) of the wire.
    """
    return east_y[gid]


@nb.vectorize([nb.float32(nb.int_)])
def mdc_gid_to_east_z(gid: TINT) -> TFLOAT:
    """
    Convert gid to east_z (cm).

    Parameters:
        gid: The gid of the wire.

    Returns:
        The east_z (cm) of the wire.
    """
    return east_z[gid]


@nb.vectorize([nb.float32(nb.int_, nb.float32)])
def mdc_gid_z_to_x(gid: TINT, z: TFLOAT) -> TFLOAT:
    """
    Get the x (cm) position of the wire at z (cm).

    Parameters:
        gid: The gid of the wire.
        z: The z (cm) position.

    Returns:
        The x (cm) position of the wire at z (cm).
    """
    return west_x[gid] + dx_dz[gid] * (z - west_z[gid])


@nb.vectorize([nb.float32(nb.int_, nb.float32)])
def mdc_gid_z_to_y(gid: TINT, z: TFLOAT) -> TFLOAT:
    """
    Get the y (cm) position of the wire at z (cm).

    Parameters:
        gid: The gid of the wire.
        z: The z (cm) position.

    Returns:
        The y (cm) position of the wire at z (cm).
    """
    return west_y[gid] + dy_dz[gid] * (z - west_z[gid])


def parse_mdc_gid(gid: TINT, with_pos: bool = True) -> Union[TINT, dict[str, TINT]]:
    """
    Parse the gid of the wire. The gid is the global index of the wire, ranges from 0 to 6795.

    When gid is an ak.Array, the result is an ak.Array, otherwise it is a dict.

    Parameters:
        gid: The gid of the wire.
        with_pos: Whether to include the position information.

    Returns:
        The parsed result, including `gid`, `layer`, `wire`, `is_stereo`, and optionally \
            `west_x`, `west_y`, `west_z`, `east_x`, `east_y`, `east_z` if `with_pos` is True. \
    """
    layer = mdc_gid_to_layer(gid)
    wire = mdc_gid_to_wire(gid)

    res = {"gid": gid, "layer": layer, "wire": wire, "is_stereo": mdc_gid_to_is_stereo(gid)}

    if with_pos:
        res["west_x"] = mdc_gid_to_west_x(gid)
        res["west_y"] = mdc_gid_to_west_y(gid)
        res["west_z"] = mdc_gid_to_west_z(gid)
        res["east_x"] = mdc_gid_to_east_x(gid)
        res["east_y"] = mdc_gid_to_east_y(gid)
        res["east_z"] = mdc_gid_to_east_z(gid)

    if isinstance(gid, ak.Array):
        return ak.zip(res)
    else:
        return res
