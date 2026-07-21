from __future__ import annotations

from typing import Any, Literal
import warnings

import awkward as ak
import numpy as np

import pybes3._kernels._ufuncs as _ufuncs
import pybes3.detectors as det
from pybes3.typing import BoolLike, IntLike

warnings.warn(
    "'pybes3.digi_id' is deprecated and will be removed in the future. "
    "Use 'pybes3.identifier' instead.",
    DeprecationWarning,
    stacklevel=2,
)

DIGI_MDC_FLAG = 0x10
DIGI_TOF_FLAG = 0x20
DIGI_EMC_FLAG = 0x30
DIGI_MUC_FLAG = 0x40
DIGI_HLT_FLAG = 0x50
DIGI_CGEM_FLAG = 0x60
DIGI_MRPC_FLAG = 0x70
DIGI_FLAG_OFFSET = 24
DIGI_FLAG_MASK = 0xFF000000

# MDC
DIGI_MDC_WIRETYPE_OFFSET = 15
DIGI_MDC_WIRETYPE_MASK = 0x00008000
DIGI_MDC_LAYER_OFFSET = 9
DIGI_MDC_LAYER_MASK = 0x00007E00
DIGI_MDC_WIRE_OFFSET = 0
DIGI_MDC_WIRE_MASK = 0x000001FF
DIGI_MDC_STEREO_WIRE = 1

# TOF
DIGI_TOF_PART_OFFSET = 14
DIGI_TOF_PART_MASK = 0x0000C000
DIGI_TOF_END_OFFSET = 0
DIGI_TOF_END_MASK = 0x00000001

DIGI_TOF_SCINT_LAYER_OFFSET = 8
DIGI_TOF_SCINT_LAYER_MASK = 0x00000100
DIGI_TOF_SCINT_PHI_OFFSET = 1
DIGI_TOF_SCINT_PHI_MASK = 0x000000FE

DIGI_TOF_MRPC_ENDCAP_OFFSET = 11
DIGI_TOF_MRPC_ENDCAP_MASK = 0x00000800
DIGI_TOF_MRPC_MODULE_OFFSET = 5
DIGI_TOF_MRPC_MODULE_MASK = 0x000007E0
DIGI_TOF_MRPC_STRIP_OFFSET = 1
DIGI_TOF_MRPC_STRIP_MASK = 0x0000001E

# EMC
DIGI_EMC_MODULE_OFFSET = 16
DIGI_EMC_MODULE_MASK = 0x000F0000
DIGI_EMC_THETA_OFFSET = 8
DIGI_EMC_THETA_MASK = 0x00003F00
DIGI_EMC_PHI_OFFSET = 0
DIGI_EMC_PHI_MASK = 0x000000FF

# MUC
DIGI_MUC_PART_OFFSET = 16
DIGI_MUC_PART_MASK = 0x000F0000
DIGI_MUC_SEGMENT_OFFSET = 12
DIGI_MUC_SEGMENT_MASK = 0x0000F000
DIGI_MUC_LAYER_OFFSET = 8
DIGI_MUC_LAYER_MASK = 0x00000F00
DIGI_MUC_CHANNEL_OFFSET = 0
DIGI_MUC_CHANNEL_MASK = 0x000000FF

# CGEM
DIGI_CGEM_STRIP_OFFSET = 7
DIGI_CGEM_STRIP_MASK = 0x0007FF80
DIGI_CGEM_STRIPTYPE_OFFSET = 6
DIGI_CGEM_STRIPTYPE_MASK = 0x00000040
DIGI_CGEM_SHEET_OFFSET = 3
DIGI_CGEM_SHEET_MASK = 0x00000038
DIGI_CGEM_LAYER_OFFSET = 0
DIGI_CGEM_LAYER_MASK = 0x00000007
DIGI_CGEM_XSTRIP = 0


###############################################################################
#                                     MDC                                     #
###############################################################################
def check_mdc_id(mdc_digi_id: IntLike) -> BoolLike:
    """
    Check if the MDC digi ID is valid.

    Parameters:
        mdc_digi_id: The MDC digi ID array or value.

    Returns:
        Whether the digi ID is valid.
    """
    return _ufuncs.check_mdc_id(mdc_digi_id)


def mdc_id_to_wire(mdc_digi_id: IntLike) -> IntLike:
    """
    Convert MDC digi ID to wire number.

    Parameters:
        mdc_digi_id: MDC digi ID array or value.

    Returns:
        The wire number.
    """
    return _ufuncs.mdc_id_to_wire(mdc_digi_id)


def mdc_id_to_layer(mdc_digi_id: IntLike) -> IntLike:
    """
    Convert the MDC digi ID to the layer number.

    Parameters:
        mdc_digi_id: The MDC digi ID array or value.

    Returns:
        The layer number.
    """
    return _ufuncs.mdc_id_to_layer(mdc_digi_id)


def mdc_id_to_is_stereo(mdc_digi_id: IntLike) -> BoolLike:
    """
    Convert the MDC digi ID to whether it is a stereo wire.

    Parameters:
        mdc_digi_id: The MDC digi ID array or value.

    Returns:
        Whether the wire is a stereo wire.
    """
    return _ufuncs.mdc_id_to_is_stereo(mdc_digi_id)


def get_mdc_digi_id(
    wire: IntLike,
    layer: IntLike,
    wire_type: IntLike,
) -> IntLike:
    """
    Generate MDC digi ID based on the wire number, layer number, and wire type.

    Parameters:
        wire: The wire number.
        layer: The layer number.
        wire_type: The wire type.

    Returns:
        The MDC digi ID.
    """
    return _ufuncs.get_mdc_id(wire, layer, wire_type)


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
    wire = mdc_id_to_wire(mdc_digi_id)
    layer = mdc_id_to_layer(mdc_digi_id)
    gid = det.get_mdc_gid(layer, wire)
    return det.parse_mdc_gid(gid, with_pos)


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
def check_tof_id(tof_digi_id: IntLike) -> BoolLike:
    """
    Check if the TOF digi ID is valid.

    Parameters:
        tof_digi_id: The TOF digi ID array or value.

    Returns:
        Whether the digi ID is valid.
    """
    return _ufuncs.check_tof_id(tof_digi_id)


def tof_id_to_part(tof_digi_id: IntLike) -> IntLike:
    """
    Convert TOF digi ID to part number. 0, 1, 2 for scintillator endcap0/barrel/endcap1,
    3, 4 for MRPC endcap0/endcap1.

    Parameters:
        tof_digi_id: TOF digi ID array or value.

    Returns:
        The part number.
    """
    return _ufuncs.tof_id_to_part(tof_digi_id)


def tof_id_to_end(tof_digi_id: IntLike) -> IntLike:
    """
    Convert the TOF digi ID to the readout end number.

    Parameters:
        tof_digi_id: The TOF digi ID array or value.

    Returns:
        The readout end number.
    """
    return _ufuncs.tof_id_to_end(tof_digi_id)


def _tof_id_to_layer_or_module_1(tof_digi_id: IntLike) -> IntLike:
    """
    Convert the TOF digi ID to the scintillator layer or MRPC module number.
    No part number is provided, so it will be calculated based on the TOF digi ID.

    This function is used by `tof_id_to_layerOrModule` when part number is not provided.

    Parameters:
        tof_digi_id: The TOF digi ID array or value.

    Returns:
        The scintillator layer or MRPC module number.
    """
    return _ufuncs._tof_id_to_layer_or_module_1(tof_digi_id)


def _tof_id_to_layer_or_module_2(tof_digi_id: IntLike, part: IntLike) -> IntLike:
    """
    Convert the TOF digi ID to the scintillator layer or MRPC module number.

    This function is used by `tof_id_to_layerOrModule` when part number is provided.

    Parameters:
        tof_digi_id: The TOF digi ID array or value.
        part: The part number.

    Returns:
        The scintillator layer or MRPC module number based on the part number.
    """
    return _ufuncs._tof_id_to_layer_or_module_2(tof_digi_id, part)


def tof_id_to_layer_or_module(
    tof_digi_id: IntLike,
    part: IntLike | None = None,
) -> IntLike:
    """
    Convert the TOF digi ID to the scintillator layer or MRPC module number.
    If `part < 3`, it is scintillator and the return value is layer number. Otherwise, it is
    MRPC and the return value is module number.

    Parameters:
        tof_digi_id: The TOF digi ID array or value.
        part: The part number. If not provided, it will be calculated based on the TOF digi ID.

    Returns:
        The scintillator layer or MRPC module number.
    """
    if part is None:
        return _tof_id_to_layer_or_module_1(tof_digi_id)
    else:
        return _tof_id_to_layer_or_module_2(tof_digi_id, part)


def _tof_id_to_phi_or_strip_1(tof_digi_id: IntLike) -> IntLike:
    """
    Convert the TOF digi ID to the scintillator phi or MRPC strip number.
    No part number is provided, so it will be calculated based on the TOF digi ID.

    This function is used by `tof_id_to_phi_or_strip` when part number is not provided.

    Parameters:
        tof_digi_id: The TOF digi ID array or value.

    Returns:
        The scintillator phi or MRPC strip number.
    """
    return _ufuncs._tof_id_to_phi_or_strip_1(tof_digi_id)


def _tof_id_to_phi_or_strip_2(tof_digi_id: IntLike, part: IntLike) -> IntLike:
    """
    Convert the TOF digi ID to the scintillator phi or MRPC strip number.

    This function is used by `tof_id_to_phi_or_strip` when part number is provided.

    Parameters:
        tof_digi_id: The TOF digi ID array or value.
        part: The part number.

    Returns:
        The scintillator phi or MRPC strip number based on the part number.
    """
    return _ufuncs._tof_id_to_phi_or_strip_2(tof_digi_id, part)


def tof_id_to_phi_or_strip(
    tof_digi_id: IntLike,
    part: IntLike | None = None,
) -> IntLike:
    """
    Convert the TOF digi ID to the scintillator phi or MRPC strip number, based on the part number.
    If `part < 3`, it is scintillator and the return value is phi number. Otherwise, it is
    MRPC and the return value is strip number.

    Parameters:
        tof_digi_id: The TOF digi ID array or value.
        part: The part number. If not provided, it will be calculated based on the TOF digi ID.

    Returns:
        The scintillator phi or MRPC strip number.
    """
    if part is None:
        return _tof_id_to_phi_or_strip_1(tof_digi_id)
    else:
        return _tof_id_to_phi_or_strip_2(tof_digi_id, part)


def get_tof_digi_id(
    part: IntLike,
    layer_or_module: IntLike,
    phi_or_strip: IntLike,
    end: IntLike,
) -> IntLike:
    """
    Generate TOF scintillator ID based on the part number, layer number, phi number, and readout end number.

    Parameters:
        part: The part number.
        layer_or_module: The scintillator layer or MRPC module number.
        phi_or_strip: The scintillator phi or MRPC strip number.
        end: The readout end number.

    Returns:
        The TOF digi ID.
    """
    return _ufuncs.get_tof_id(part, layer_or_module, phi_or_strip, end)


def parse_tof_digi_id(
    tof_digi_id: IntLike,
    flat: bool = False,
    library: Literal["ak", "np"] = "ak",
) -> ak.Array | dict[str, np.ndarray] | dict[str, np.int_]:
    """
    Parse TOF digi ID.
    If `library` is `ak`, return `ak.Array`. If `library` is `np`, return `dict[str, np.ndarray]`.

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

    part = tof_id_to_part(tof_digi_id)
    res = {
        "part": part,
        "layer_or_module": tof_id_to_layer_or_module(tof_digi_id, part),
        "phi_or_strip": tof_id_to_phi_or_strip(tof_digi_id, part),
        "end": tof_id_to_end(tof_digi_id),
    }

    if library == "ak":
        return ak.zip(res)
    else:
        return res


###############################################################################
#                                     EMC                                     #
###############################################################################
def check_emc_id(emc_digi_id: IntLike) -> BoolLike:
    """
    Check if the EMC digi ID is valid.

    Parameters:
        emc_digi_id: The EMC digi ID array or value.

    Returns:
        Whether the digi ID is valid.
    """
    return _ufuncs.check_emc_id(emc_digi_id)


def emc_id_to_module(emc_digi_id: IntLike) -> IntLike:
    """
    Convert EMC digi ID to module number

    Parameters:
        emc_digi_id: EMC digi ID array or value.

    Returns:
        The module number.
    """
    return _ufuncs.emc_id_to_module(emc_digi_id)


def emc_id_to_theta(emc_digi_id: IntLike) -> IntLike:
    """
    Convert the EMC digi ID to the theta number.

    Parameters:
        emc_digi_id: The EMC digi ID array or value.

    Returns:
        The theta number.
    """
    return _ufuncs.emc_id_to_theta(emc_digi_id)


def emc_id_to_phi(emc_digi_id: IntLike) -> IntLike:
    """
    Convert the EMC digi ID to the phi number.

    Parameters:
        emc_digi_id: The EMC digi ID array or value.

    Returns:
        The phi number.
    """
    return _ufuncs.emc_id_to_phi(emc_digi_id)


def get_emc_digi_id(
    module: IntLike,
    theta: IntLike,
    phi: IntLike,
) -> IntLike:
    """
    Generate EMC digi ID based on the module number, theta number, and phi number.

    Parameters:
        module: The module number.
        theta: The theta number.
        phi: The phi number.

    Returns:
        The EMC digi ID.
    """
    return _ufuncs.get_emc_id(module, theta, phi)


def parse_emc_digi_id(
    emc_digi_id: IntLike,
    with_pos: bool = False,
) -> ak.Array | dict[str, Any]:
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
    part = emc_id_to_module(emc_digi_id)
    theta = emc_id_to_theta(emc_digi_id)
    phi = emc_id_to_phi(emc_digi_id)
    gid = det.get_emc_gid(part, theta, phi)
    return det.parse_emc_gid(gid, with_pos)


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
def check_muc_id(muc_digi_id: IntLike) -> BoolLike:
    """
    Check if the MUC digi ID is valid.

    Parameters:
        muc_digi_id: The MUC digi ID array or value.

    Returns:
        Whether the digi ID is valid.
    """
    return _ufuncs.check_muc_id(muc_digi_id)


def muc_id_to_part(muc_digi_id: IntLike) -> IntLike:
    """
    Convert MUC digi ID to part number

    Parameters:
        muc_digi_id: MUC digi ID array or value.

    Returns:
        The part number.
    """
    return _ufuncs.muc_id_to_part(muc_digi_id)


def muc_id_to_segment(muc_digi_id: IntLike) -> IntLike:
    """
    Convert the MUC digi ID to the segment number.

    Parameters:
        muc_digi_id: The MUC digi ID array or value.

    Returns:
        The segment number.
    """
    return _ufuncs.muc_id_to_segment(muc_digi_id)


def muc_id_to_layer(muc_digi_id: IntLike) -> IntLike:
    """
    Convert the MUC digi ID to the layer number.

    Parameters:
        muc_digi_id: The MUC digi ID array or value.

    Returns:
        The layer number.
    """
    return _ufuncs.muc_id_to_layer(muc_digi_id)


def muc_id_to_channel(muc_digi_id: IntLike) -> IntLike:
    """
    Convert the MUC digi ID to the channel number.

    Parameters:
        muc_digi_id: The MUC digi ID array or value.

    Returns:
        The channel number.
    """
    return _ufuncs.muc_id_to_channel(muc_digi_id)


def get_muc_digi_id(
    part: IntLike,
    segment: IntLike,
    layer: IntLike,
    channel: IntLike,
) -> IntLike:
    """
    Generate MUC digi ID based on the part number, segment number, layer number, and channel number.

    Parameters:
        part: The part number.
        segment: The segment number.
        layer: The layer number.
        channel: The channel number.

    Returns:
        The MUC digi ID.
    """
    return _ufuncs.get_muc_id(part, segment, layer, channel)


def muc_id_to_gap(muc_digi_id: IntLike) -> IntLike:
    """
    Convert the MUC digi ID to the gap ID, which is equivalent to layer number.

    Parameters:
        muc_digi_id: The MUC digi ID array or value.

    Returns:
        The gap ID.
    """
    return muc_id_to_layer(muc_digi_id)


def muc_id_to_strip(muc_digi_id: IntLike) -> IntLike:
    """
    Convert the MUC digi ID to the strip number, which is equivalent to channel number.

    Parameters:
        muc_digi_id: The MUC digi ID array or value.

    Returns:
        The strip number.
    """
    return muc_id_to_channel(muc_digi_id)


def parse_muc_digi_id(
    muc_digi_id: IntLike,
    flat: bool = False,
    library: Literal["ak", "np"] = "ak",
) -> ak.Array | dict[str, np.ndarray] | dict[str, np.int_]:
    """
    Parse MUC digi ID.

    If `library` is `ak`, return `ak.Array`. If `library` is `np`, return `dict[str, np.ndarray]`.

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

    part = muc_id_to_part(muc_digi_id)
    segment = muc_id_to_segment(muc_digi_id)
    layer = muc_id_to_layer(muc_digi_id)
    channel = muc_id_to_channel(muc_digi_id)

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
def check_cgem_id(cgem_digi_id: IntLike) -> BoolLike:
    """
    Check if the CGEM digi ID is valid.

    Parameters:
        cgem_digi_id: The CGEM digi ID array or value.

    Returns:
        Whether the digi ID is valid.
    """
    return _ufuncs.check_cgem_id(cgem_digi_id)


def cgem_id_to_layer(cgem_digi_id: IntLike) -> IntLike:
    """
    Convert the CGEM digi ID to the layer number.

    Parameters:
        cgem_digi_id: The CGEM digi ID array or value.

    Returns:
        The layer number.
    """
    return _ufuncs.cgem_id_to_layer(cgem_digi_id)


def cgem_id_to_sheet(cgem_digi_id: IntLike) -> IntLike:
    """
    Convert the CGEM digi ID to the sheet number.

    Parameters:
        cgem_digi_id: The CGEM digi ID array or value.

    Returns:
        The sheet number.
    """
    return _ufuncs.cgem_id_to_sheet(cgem_digi_id)


def cgem_id_to_strip_type(cgem_digi_id: IntLike) -> IntLike:
    """
    Convert the CGEM digi ID to the strip type. 0 for X-strip, 1 for V-strip.

    Parameters:
        cgem_digi_id: The CGEM digi ID array or value.

    Returns:
        The strip type. 0 for X-strip, 1 for V-strip.
    """
    return _ufuncs.cgem_id_to_strip_type(cgem_digi_id)


def cgem_id_to_strip(cgem_digi_id: IntLike) -> IntLike:
    """
    Convert CGEM digi ID to strip number

    Parameters:
        cgem_digi_id: CGEM digi ID array or value.

    Returns:
        The strip number.
    """
    return _ufuncs.cgem_id_to_strip(cgem_digi_id)


def get_cgem_digi_id(
    layer: IntLike,
    sheet: IntLike,
    strip_type: IntLike,
    strip: IntLike,
) -> IntLike:
    """
    Generate CGEM digi ID based on the strip number, strip type, sheet number, and layer number.

    Parameters:
        layer: The layer number.
        sheet: The sheet number.
        strip_type: The strip type. 0 for X-strip, 1 for V-strip.
        strip: The strip number.

    Returns:
        The CGEM digi ID.
    """
    return _ufuncs.get_cgem_id(layer, sheet, strip_type, strip)


def parse_cgem_digi_id(
    cgem_digi_id: IntLike,
    flat: bool = False,
    library: Literal["ak", "np"] = "ak",
) -> ak.Array | dict[str, np.ndarray] | dict[str, np.int_]:
    """
    Parse CGEM digi ID.

    If `library` is `ak`, return `ak.Array`. If `library` is `np`, return `dict[str, np.ndarray]`.

    Available keys of the output:

    - `layer`: The layer number.
    - `sheet`: The sheet ID.
    - `strip_type`: The strip type. 0 for X-strip, 1 for V-strip.
    - `strip`: The strip ID.

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
        "layer": cgem_id_to_layer(cgem_digi_id),
        "sheet": cgem_id_to_sheet(cgem_digi_id),
        "strip_type": cgem_id_to_strip_type(cgem_digi_id),
        "strip": cgem_id_to_strip(cgem_digi_id),
    }

    if library == "ak":
        return ak.zip(res)
    else:
        return res
