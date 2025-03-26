from typing import Literal, Union

import awkward as ak
import numpy as np

from ..typing import IntLike
from . import digi_id
from .digi_id import (
    get_cgem_digi_id,
    get_emc_digi_id,
    get_mdc_digi_id,
    get_muc_digi_id,
    get_tof_digi_id,
)
from .geometry import (
    emc_barrel_h1,
    emc_barrel_h2,
    emc_barrel_h3,
    emc_barrel_l,
    emc_barrel_offset_1,
    emc_barrel_offset_2,
    emc_barrel_r,
    emc_gid_to_center_x,
    emc_gid_to_center_y,
    emc_gid_to_center_z,
    emc_gid_to_front_center_x,
    emc_gid_to_front_center_y,
    emc_gid_to_front_center_z,
    emc_gid_to_part,
    emc_gid_to_phi,
    emc_gid_to_point_x,
    emc_gid_to_point_y,
    emc_gid_to_point_z,
    emc_gid_to_theta,
    get_emc_crystal_position,
    get_emc_gid,
    get_mdc_gid,
    get_mdc_wire_position,
    mdc_gid_to_east_x,
    mdc_gid_to_east_y,
    mdc_gid_to_east_z,
    mdc_gid_to_is_stereo,
    mdc_gid_to_layer,
    mdc_gid_to_stereo,
    mdc_gid_to_superlayer,
    mdc_gid_to_west_x,
    mdc_gid_to_west_y,
    mdc_gid_to_west_z,
    mdc_gid_to_wire,
    mdc_gid_z_to_x,
    mdc_gid_z_to_y,
    mdc_layer_to_is_stereo,
    mdc_layer_to_superlayer,
)


###############################################################################
#                                     MDC                                     #
###############################################################################
def parse_mdc_gid(gid: IntLike, with_pos: bool = True) -> Union[IntLike, dict[str, IntLike]]:
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
) -> Union[IntLike, dict[str, IntLike]]:
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


###############################################################################
#                                     TOF                                     #
###############################################################################
def parse_tof_digi_id(
    tof_digi_id: IntLike,
    flat: bool = False,
    library: Literal["ak", "np"] = "ak",
) -> Union[ak.Record, dict[str, np.ndarray], dict[str, np.int_]]:
    """
    Parse TOF digi ID.
    If `library` is `ak`, return `ak.Record`. If `library` is `np`, return `dict[str, np.ndarray]`.

    Available keys of the output:

    - `part`: The part number. `0,1,2` for scintillator endcap0, barrel, endcap1; `3,4` for MRPC endcap0, endcap1.
    - `layer_or_module`: The scintillator layer or MRPC module number, based on the part number.
    - `phi_or_strip`: The scintillator phi or MRPC strip ID, based on the part number.
    - `end`: The readout end ID.

    The return value is based on the part number.

    Rows where `part < 3` are scintillator and `layer_or_module` represents layer number, `phi_or_strip` represents phi number.

    Rows where `part >= 3` are MRPC and `layer_or_module` represents module number, `phi_or_strip` represents strip ID.

    Parameters:
        tof_digi_id: The TOF ID.
        flat: Whether to flatten the output.
        library: The library to use as output.

    Returns:
        The parsed TOF ID.

    """
    if library not in ["ak", "np"]:
        raise ValueError(f"Unsupported library: {library}")

    if flat and isinstance(tof_digi_id, ak.Array):
        tof_digi_id = ak.flatten(tof_digi_id)

    part = digi_id.tof_id_to_part(tof_digi_id)
    res = {
        "part": part,
        "layer_or_module": digi_id.tof_id_to_layer_or_module(tof_digi_id, part),
        "phi_or_strip": digi_id.tof_id_to_phi_or_strip(tof_digi_id, part),
        "end": digi_id.tof_id_to_end(tof_digi_id),
    }

    if library == "ak":
        return ak.zip(res)
    else:
        return res


###############################################################################
#                                     EMC                                     #
###############################################################################
def parse_emc_gid(gid: IntLike, with_pos: bool = True) -> Union[IntLike, dict[str, IntLike]]:
    """
    Parse the gid of EMC crystals. "gid" is the global ID of the crystal, ranges from 0 to 6239.
    When `gid` is an `ak.Array`, the result is an `ak.Array`, otherwise it is a `dict`.

    Keys of the output:

    - `gid`: Global ID of the crystal.
    - `part`: Part number, 0 for endcap0, 1 for barrel, 2 for endcap1.
    - `theta`: Theta number.
    - `phi`: Phi number.

    Optional keys of the output when `with_pos` is `True`:

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
        with_pos: Whether to include the position information.

    Returns:
        The parsed result.
    """
    part = emc_gid_to_part(gid)
    theta = emc_gid_to_theta(gid)
    phi = emc_gid_to_phi(gid)

    res = {"gid": gid, "part": part, "theta": theta, "phi": phi}

    if with_pos:
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


def parse_emc_digi_id(
    emc_digi_id: IntLike,
    with_pos: bool = False,
) -> Union[IntLike, dict[str, IntLike]]:
    """
    Parse EMC digi ID.

    When `emc_digi_id` is an `ak.Array`, the result is an `ak.Array`, otherwise it is a `dict`.

    Keys of the output:

    - `gid`: Global ID of the crystal.
    - `part`: Part number, 0 for endcap0, 1 for barrel, 2 for endcap1.
    - `theta`: Theta number.
    - `phi`: Phi number.

    Optional keys of the output when `with_pos` is `True`:

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
        emc_digi_id: The EMC digi ID.
        with_pos: Whether to include the position information.

    Returns:
        The parsed EMC digi ID.

    """
    part = digi_id.emc_id_to_module(emc_digi_id)
    theta = digi_id.emc_id_to_theta(emc_digi_id)
    phi = digi_id.emc_id_to_phi(emc_digi_id)
    gid = get_emc_gid(part, theta, phi)
    return parse_emc_gid(gid, with_pos)


def parse_emc_digi(emc_digi: ak.Record, with_pos: bool = False) -> ak.Record:
    """
    Parse EMC raw digi array. The raw digi array should contain [`m_intId`,
    `m_timeChannel`, `m_chargeChannel`, `m_trackIndex`, `m_measure`] fields.

    Fields of the output:

    - `gid`: Global ID of the crystal.
    - `part`: Part number, 0 for endcap0, 1 for barrel, 2 for endcap1.
    - `theta`: Theta number.
    - `phi`: Phi number.
    - `charge_channel`: Charge channel.
    - `time_channel`: Time channel.
    - `track_index`: Track index.
    - `measure`: Measure value.
    - `digi_id`: Raw digi ID.

    Optional fields of the output when `with_pos` is `True`:

    - `front_center_x`: x position of the front center of the crystal.
    - `front_center_y`: y position of the front center of the crystal.
    - `front_center_z`: z position of the front center of the crystal.
    - `center_x`: x position of the center of the crystal.
    - `center_y`: y position of the center of the crystal.
    - `center_z`: z position of the center of the crystal.

    Parameters:
        emc_digi: The EMC raw digi array.
        with_pos: Whether to include the position information.

    Returns:
        The parsed EMC digi array.
    """
    gid = parse_emc_digi_id(emc_digi["m_intId"], with_pos=with_pos)

    res = {
        "gid": gid["gid"],
        "part": gid["part"],
        "theta": gid["theta"],
        "phi": gid["phi"],
        "charge_channel": emc_digi["m_chargeChannel"],
        "time_channel": emc_digi["m_timeChannel"],
        "track_index": emc_digi["m_trackIndex"],
        "measure": emc_digi["m_measure"],
        "digi_id": emc_digi["m_intId"],
    }

    if with_pos:
        res["front_center_x"] = gid["front_center_x"]
        res["front_center_y"] = gid["front_center_y"]
        res["front_center_z"] = gid["front_center_z"]
        res["center_x"] = gid["center_x"]
        res["center_y"] = gid["center_y"]
        res["center_z"] = gid["center_z"]

    return ak.zip(res)


###############################################################################
#                                     MUC                                     #
###############################################################################
def parse_muc_digi_id(
    muc_digi_id: IntLike,
    flat: bool = False,
    library: Literal["ak", "np"] = "ak",
) -> Union[ak.Record, dict[str, np.ndarray], dict[str, np.int_]]:
    """
    Parse MUC digi ID.

    If `library` is `ak`, return `ak.Record`. If `library` is `np`, return `dict[str, np.ndarray]`.

    Available keys of the output:

    - `part`: The part number.
    - `segment`: The segment number.
    - `layer`: The layer number.
    - `channel`: The channel number.
    - `gap`: The gap number, which is equivalent to layer number.
    - `strip`: The strip number, which is equivalent to channel number.

    Parameters:
        muc_digi_id: The MUC digi ID.
        flat: Whether to flatten the output.
        library: The library to use as output.

    Returns:
        The parsed MUC digi ID.
    """
    if library not in ["ak", "np"]:
        raise ValueError(f"Unsupported library: {library}")

    if flat and isinstance(muc_digi_id, ak.Array):
        muc_digi_id = ak.flatten(muc_digi_id)

    part = digi_id.muc_id_to_part(muc_digi_id)
    segment = digi_id.muc_id_to_segment(muc_digi_id)
    layer = digi_id.muc_id_to_layer(muc_digi_id)
    channel = digi_id.muc_id_to_channel(muc_digi_id)

    res = {
        "part": part,
        "segment": segment,
        "layer": layer,
        "channel": channel,
        "gap": layer,
        "strip": channel,
    }

    if library == "ak":
        return ak.zip(res)
    else:
        return res


###############################################################################
#                                    CGEM                                     #
###############################################################################
def parse_cgem_digi_id(
    cgem_digi_id: IntLike,
    flat: bool = False,
    library: Literal["ak", "np"] = "ak",
) -> Union[ak.Record, dict[str, np.ndarray], dict[str, np.int_]]:
    """
    Parse CGEM digi ID.

    If `library` is `ak`, return `ak.Record`. If `library` is `np`, return `dict[str, np.ndarray]`.

    Available keys of the output:

    - `layer`: The layer number.
    - `sheet`: The sheet ID.
    - `strip`: The strip ID.
    - `is_x_strip`: Whether the strip is an X-strip.

    Parameters:
        cgem_digi_id: The CGEM digi ID.
        flat: Whether to flatten the output.
        library: The library to use as output.

    Returns:
        The parsed CGEM digi ID.
    """
    if library not in ["ak", "np"]:
        raise ValueError(f"Unsupported library: {library}")

    if flat and isinstance(cgem_digi_id, ak.Array):
        cgem_digi_id = ak.flatten(cgem_digi_id)

    res = {
        "layer": digi_id.cgem_id_to_layer(cgem_digi_id),
        "sheet": digi_id.cgem_id_to_sheet(cgem_digi_id),
        "strip": digi_id.cgem_id_to_strip(cgem_digi_id),
        "is_x_strip": digi_id.cgem_id_to_is_x_strip(cgem_digi_id),
    }

    if library == "ak":
        return ak.zip(res)
    else:
        return res


__all__ = [
    # geometry
    "get_mdc_wire_position",
    "mdc_gid_z_to_x",
    "mdc_gid_z_to_y",
    # identifier
    "get_mdc_digi_id",
    "get_tof_digi_id",
    "get_emc_digi_id",
    "get_muc_digi_id",
    "get_cgem_digi_id",
    # parser
    "parse_mdc_gid",
    "parse_mdc_digi_id",
    "parse_tof_digi_id",
    "parse_emc_digi_id",
    "parse_muc_digi_id",
    "parse_cgem_digi_id",
]
