from __future__ import annotations

import awkward as ak
import numpy as np

import pybes3._kernels._ufuncs as _ufuncs
import pybes3.detectors as det
from pybes3.typing import BoolLike, IntLike


def _add_field_if_exist(digi: ak.Array | dict, res: dict, field: str, output: str):
    if isinstance(digi, ak.Array):
        if field in digi.fields:
            res[output] = digi[field]
    else:
        if field in digi:
            res[output] = digi[field]


###############################################################################
#                                     MDC                                     #
###############################################################################
def check_mdc_id(mdc_id: IntLike) -> BoolLike:
    """
    Check if the MDC digi ID is valid.

    Parameters:
        mdc_id: The MDC digi ID array or value.

    Returns:
        Whether the digi ID is valid.
    """
    return _ufuncs.check_mdc_id(mdc_id)


def mdc_id_to_wire(mdc_id: IntLike) -> IntLike:
    """
    Convert MDC digi ID to wire number.

    Parameters:
        mdc_id: MDC digi ID array or value.

    Returns:
        The wire number.
    """
    return _ufuncs.mdc_id_to_wire(mdc_id)


def mdc_id_to_layer(mdc_id: IntLike) -> IntLike:
    """
    Convert the MDC digi ID to the layer number.

    Parameters:
        mdc_id: The MDC digi ID array or value.

    Returns:
        The layer number.
    """
    return _ufuncs.mdc_id_to_layer(mdc_id)


def mdc_id_to_is_stereo(mdc_id: IntLike) -> BoolLike:
    """
    Convert the MDC digi ID to whether it is a stereo wire.

    Parameters:
        mdc_id: The MDC digi ID array or value.

    Returns:
        Whether the wire is a stereo wire.
    """
    return _ufuncs.mdc_id_to_is_stereo(mdc_id)


def get_mdc_id(wire: IntLike, layer: IntLike, wire_type: IntLike) -> IntLike:
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


def mdc_id_to_gid(mdc_id: IntLike) -> IntLike:
    """
    Convert MDC digi ID to global wire ID (gid).

    Parameters:
        mdc_id: The MDC digi ID array or value.

    Returns:
        The global wire ID.
    """
    return det.get_mdc_gid(mdc_id_to_layer(mdc_id), mdc_id_to_wire(mdc_id))


def parse_mdc_id(mdc_id: IntLike) -> ak.Array | dict[str, np.ndarray | int]:
    """
    Parse MDC digi ID.

    Available keys of the output:

    - `gid`: Global ID of the wire.
    - `layer`: Layer number.
    - `wire`: Local wire number.
    - `is_stereo`: Whether the wire is a stereo wire.

    Parameters:
        mdc_id: The MDC digi ID.

    Returns:
        The parsed MDC digi ID.
    """

    res = {
        "gid": mdc_id_to_gid(mdc_id),
        "layer": mdc_id_to_layer(mdc_id),
        "wire": mdc_id_to_wire(mdc_id),
        "is_stereo": mdc_id_to_is_stereo(mdc_id),
    }

    if isinstance(mdc_id, ak.Array):
        return ak.zip(res)
    else:
        return res


def parse_mdc_digi(
    mdc_digi: ak.Array | dict[str, np.ndarray | int],
) -> ak.Array | dict[str, np.ndarray | int]:
    """
    Parse MDC raw digi array. The raw digi array should contain [`m_intId`,
    `m_timeChannel`, `m_chargeChannel`, `m_overflow`] fields.

    Fields of the output:

    - `gid`: Global ID of the wire.
    - `wire`: Local wire number.
    - `layer`: Layer number.
    - `is_stereo`: Whether the wire is a stereo wire.
    - `charge_channel`: Charge channel.
    - `time_channel`: Time channel.
    - `overflow`: Overflow flag.
    - `track_index`: Track index.

    Parameters:
        mdc_digi: The MDC raw digi array.

    Returns:
        The parsed MDC digi array.
    """
    parsed_id = parse_mdc_id(mdc_digi["m_intId"])

    charge_channel = mdc_digi["m_chargeChannel"]
    time_channel = mdc_digi["m_timeChannel"]
    overflow = mdc_digi["m_overflow"]

    res = {
        "gid": parsed_id["gid"],
        "wire": parsed_id["wire"],
        "layer": parsed_id["layer"],
        "is_stereo": parsed_id["is_stereo"],
        "charge_channel": charge_channel,
        "time_channel": time_channel,
        "overflow": overflow,
    }

    _add_field_if_exist(mdc_digi, res, "m_trackIndex", "track_index")

    if isinstance(mdc_digi, ak.Array):
        return ak.zip(res)
    else:
        return res


###############################################################################
#                                     TOF                                     #
###############################################################################


def check_tof_id(tof_id: IntLike) -> BoolLike:
    """
    Check if the TOF digi ID is valid.

    Parameters:
        tof_id: The TOF digi ID array or value.

    Returns:
        Whether the digi ID is valid.
    """
    return _ufuncs.check_tof_id(tof_id)


def tof_id_to_part(tof_id: IntLike) -> IntLike:
    """
    Convert TOF digi ID to part number. 0, 1, 2 for scintillator endcap0/barrel/endcap1,
    3, 4 for MRPC endcap0/endcap1.

    Parameters:
        tof_id: TOF digi ID array or value.

    Returns:
        The part number.
    """
    return _ufuncs.tof_id_to_part(tof_id)


def tof_id_to_end(tof_id: IntLike) -> IntLike:
    """
    Convert the TOF digi ID to the readout end number.

    Parameters:
        tof_id: The TOF digi ID array or value.

    Returns:
        The readout end number.
    """
    return _ufuncs.tof_id_to_end(tof_id)


def _tof_id_to_layer_or_module_1(tof_id: IntLike) -> IntLike:
    """
    Convert the TOF digi ID to the scintillator layer or MRPC module number.
    No part number is provided, so it will be calculated based on the TOF digi ID.

    This function is used by `tof_id_to_layer_or_module` when part number is not provided.

    Parameters:
        tof_id: The TOF digi ID array or value.

    Returns:
        The scintillator layer or MRPC module number.
    """
    return _ufuncs._tof_id_to_layer_or_module_1(tof_id)


def _tof_id_to_layer_or_module_2(tof_id: IntLike, part: IntLike) -> IntLike:
    """
    Convert the TOF digi ID to the scintillator layer or MRPC module number.

    This function is used by `tof_id_to_layer_or_module` when part number is provided.

    Parameters:
        tof_id: The TOF digi ID array or value.
        part: The part number.

    Returns:
        The scintillator layer or MRPC module number based on the part number.
    """
    return _ufuncs._tof_id_to_layer_or_module_2(tof_id, part)


def tof_id_to_layer_or_module(
    tof_id: IntLike,
    part: IntLike | None = None,
) -> IntLike:
    """
    Convert the TOF digi ID to the scintillator layer or MRPC module number.
    If `part < 3`, it is scintillator and the return value is layer number. Otherwise, it is
    MRPC and the return value is module number.

    Parameters:
        tof_id: The TOF digi ID array or value.
        part: The part number. If not provided, it will be calculated based on the TOF digi ID.

    Returns:
        The scintillator layer or MRPC module number.
    """
    if part is None:
        return _tof_id_to_layer_or_module_1(tof_id)
    else:
        return _tof_id_to_layer_or_module_2(tof_id, part)


def _tof_id_to_phi_or_strip_1(tof_id: IntLike) -> IntLike:
    """
    Convert the TOF digi ID to the scintillator phi or MRPC strip number.
    No part number is provided, so it will be calculated based on the TOF digi ID.

    This function is used by `tof_id_to_phi_or_strip` when part number is not provided.

    Parameters:
        tof_id: The TOF digi ID array or value.

    Returns:
        The scintillator phi or MRPC strip number.
    """
    return _ufuncs._tof_id_to_phi_or_strip_1(tof_id)


def _tof_id_to_phi_or_strip_2(tof_id: IntLike, part: IntLike) -> IntLike:
    """
    Convert the TOF digi ID to the scintillator phi or MRPC strip number.

    This function is used by `tof_id_to_phi_or_strip` when part number is provided.

    Parameters:
        tof_id: The TOF digi ID array or value.
        part: The part number.

    Returns:
        The scintillator phi or MRPC strip number based on the part number.
    """
    return _ufuncs._tof_id_to_phi_or_strip_2(tof_id, part)


def tof_id_to_phi_or_strip(
    tof_id: IntLike,
    part: IntLike | None = None,
) -> IntLike:
    """
    Convert the TOF digi ID to the scintillator phi or MRPC strip number, based on the part number.
    If `part < 3`, it is scintillator and the return value is phi number. Otherwise, it is
    MRPC and the return value is strip number.

    Parameters:
        tof_id: The TOF digi ID array or value.
        part: The part number. If not provided, it will be calculated based on the TOF digi ID.

    Returns:
        The scintillator phi or MRPC strip number.
    """
    if part is None:
        return _tof_id_to_phi_or_strip_1(tof_id)
    else:
        return _tof_id_to_phi_or_strip_2(tof_id, part)


def get_tof_id(
    part: IntLike, layer_or_module: IntLike, phi_or_strip: IntLike, end: IntLike
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


def tof_id_to_gid(tof_id: IntLike) -> IntLike:
    """
    Convert TOF digi ID to global strip ID (gid).

    Parameters:
        tof_id: The TOF digi ID array or value.

    Returns:
        The global strip ID.
    """
    part = tof_id_to_part(tof_id)
    return det.get_tof_gid(
        part,
        tof_id_to_layer_or_module(tof_id, part),
        tof_id_to_phi_or_strip(tof_id, part),
    )


def parse_tof_id(tof_id: IntLike) -> ak.Array | dict[str, np.ndarray | int]:
    """
    Parse TOF digi ID.

    Available keys of the output:

    - `gid`: Global ID of the strip. Note that it corresponds to the strip instead of readout end, so it is the same for both ends of the strip.
    - `part`: The part number. `0,1,2` for scintillator endcap0, barrel, endcap1; `3,4` for MRPC endcap0, endcap1.
    - `layer_or_module`: The scintillator layer or MRPC module number, based on the part number.
    - `phi_or_strip`: The scintillator phi or MRPC strip ID, based on the part number.
    - `end`: The readout end ID.

    The return value is based on the part number.

    Rows where `part < 3` are scintillator and `layer_or_module` represents layer number, `phi_or_strip` represents phi number.

    Rows where `part >= 3` are MRPC and `layer_or_module` represents module number, `phi_or_strip` represents strip ID.

    Parameters:
        tof_id: The TOF ID.

    Returns:
        The parsed TOF ID.

    """

    part = tof_id_to_part(tof_id)
    layer_or_module = tof_id_to_layer_or_module(tof_id, part)
    phi_or_strip = tof_id_to_phi_or_strip(tof_id, part)
    end = tof_id_to_end(tof_id)
    gid = det.get_tof_gid(part, layer_or_module, phi_or_strip)

    res = {
        "gid": gid,
        "part": part,
        "layer_or_module": layer_or_module,
        "phi_or_strip": phi_or_strip,
        "end": end,
    }

    if isinstance(tof_id, ak.Array):
        return ak.zip(res)
    else:
        return res


def parse_tof_digi(
    tof_digi: ak.Array | dict[str, np.ndarray | int],
) -> ak.Array | dict[str, np.ndarray | int]:
    """
    Parse TOF raw digi array. The raw digi array should contain [`m_intId`,
    `m_timeChannel`, `m_chargeChannel`, `m_overflow`] fields.

    Fields of the output:

    - `gid`: Global ID of the strip. Note that it corresponds to the strip instead of readout end, so it is the same for both ends of the strip.
    - `part`: The part number. `0,1,2` for scintillator endcap0, barrel, endcap1; `3,4` for MRPC endcap0, endcap1.
    - `layer_or_module`: The scintillator layer or MRPC module number, based on the part number.
    - `phi_or_strip`: The scintillator phi or MRPC strip ID, based on the part number.
    - `end`: The readout end ID.
    - `charge_channel`: Charge channel.
    - `time_channel`: Time channel.
    - `overflow`: Overflow flag.

    Parameters:
        tof_digi: The TOF raw digi array.

    Returns:
        The parsed TOF digi array.
    """
    parsed_id = parse_tof_id(tof_digi["m_intId"])

    charge_channel = tof_digi["m_chargeChannel"]
    time_channel = tof_digi["m_timeChannel"]

    res = {
        "gid": parsed_id["gid"],
        "part": parsed_id["part"],
        "layer_or_module": parsed_id["layer_or_module"],
        "phi_or_strip": parsed_id["phi_or_strip"],
        "end": parsed_id["end"],
        "charge_channel": charge_channel,
        "time_channel": time_channel,
        "overflow": tof_digi["m_overflow"],
    }

    _add_field_if_exist(tof_digi, res, "m_trackIndex", "track_index")

    if isinstance(tof_digi, ak.Array):
        return ak.zip(res)
    else:
        return res


###############################################################################
#                                     EMC                                     #
###############################################################################


def check_emc_id(emc_id: IntLike) -> BoolLike:
    """
    Check if the EMC digi ID is valid.

    Parameters:
        emc_id: The EMC digi ID array or value.

    Returns:
        Whether the digi ID is valid.
    """
    return _ufuncs.check_emc_id(emc_id)


def emc_id_to_module(emc_id: IntLike) -> IntLike:
    """
    Convert EMC digi ID to module number

    Parameters:
        emc_id: EMC digi ID array or value.

    Returns:
        The module number.
    """
    return _ufuncs.emc_id_to_module(emc_id)


def emc_id_to_theta(emc_id: IntLike) -> IntLike:
    """
    Convert the EMC digi ID to the theta number.

    Parameters:
        emc_id: The EMC digi ID array or value.

    Returns:
        The theta number.
    """
    return _ufuncs.emc_id_to_theta(emc_id)


def emc_id_to_phi(emc_id: IntLike) -> IntLike:
    """
    Convert the EMC digi ID to the phi number.

    Parameters:
        emc_id: The EMC digi ID array or value.

    Returns:
        The phi number.
    """
    return _ufuncs.emc_id_to_phi(emc_id)


def get_emc_id(module: IntLike, theta: IntLike, phi: IntLike) -> IntLike:
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


def emc_id_to_gid(emc_id: IntLike) -> IntLike:
    """
    Convert EMC digi ID to global crystal ID (gid).

    Parameters:
        emc_id: The EMC digi ID array or value.

    Returns:
        The global crystal ID.
    """
    return det.get_emc_gid(
        emc_id_to_module(emc_id),
        emc_id_to_theta(emc_id),
        emc_id_to_phi(emc_id),
    )


def parse_emc_id(emc_id: IntLike) -> ak.Array | dict[str, np.ndarray | int]:
    """
    Parse EMC digi ID.

    Available keys of the output:

    - `gid`: Global ID of the crystal.
    - `part`: Part number, 0 for endcap0, 1 for barrel, 2 for endcap1.
    - `theta`: Theta number.
    - `phi`: Phi number.

    Parameters:
        emc_id: The EMC digi ID.

    Returns:
        The parsed EMC digi ID.
    """
    module = emc_id_to_module(emc_id)
    theta = emc_id_to_theta(emc_id)
    phi = emc_id_to_phi(emc_id)
    res = {
        "gid": det.get_emc_gid(module, theta, phi),
        "part": module,
        "theta": theta,
        "phi": phi,
    }

    if isinstance(emc_id, ak.Array):
        return ak.zip(res)
    else:
        return res


def parse_emc_digi(
    emc_digi: ak.Array | dict[str, np.ndarray | int],
) -> ak.Array | dict[str, np.ndarray | int]:
    """
    Parse EMC raw digi array. The raw digi array should contain [`m_intId`,
    `m_timeChannel`, `m_chargeChannel`, `m_measure`] fields.

    Fields of the output:

    - `gid`: Global ID of the crystal.
    - `part`: Part number, 0 for endcap0, 1 for barrel, 2 for endcap1.
    - `theta`: Theta number.
    - `phi`: Phi number.
    - `charge_channel`: Charge channel.
    - `time_channel`: Time channel.
    - `measure`: Measure value.
    - `track_index`: Track index.

    Parameters:
        emc_digi: The EMC raw digi array.

    Returns:
        The parsed EMC digi array.
    """
    parsed_id = parse_emc_id(emc_digi["m_intId"])

    charge_channel = emc_digi["m_chargeChannel"]
    time_channel = emc_digi["m_timeChannel"]
    measure = emc_digi["m_measure"]

    res = {
        "gid": parsed_id["gid"],
        "part": parsed_id["part"],
        "theta": parsed_id["theta"],
        "phi": parsed_id["phi"],
        "charge_channel": charge_channel,
        "time_channel": time_channel,
        "measure": measure,
    }

    _add_field_if_exist(emc_digi, res, "m_trackIndex", "track_index")

    if isinstance(emc_digi, ak.Array):
        return ak.zip(res)
    else:
        return res


###############################################################################
#                                     MUC                                     #
###############################################################################


def check_muc_id(muc_id: IntLike) -> BoolLike:
    """
    Check if the MUC digi ID is valid.

    Parameters:
        muc_id: The MUC digi ID array or value.

    Returns:
        Whether the digi ID is valid.
    """
    return _ufuncs.check_muc_id(muc_id)


def muc_id_to_part(muc_id: IntLike) -> IntLike:
    """
    Convert MUC digi ID to part number

    Parameters:
        muc_id: MUC digi ID array or value.

    Returns:
        The part number.
    """
    return _ufuncs.muc_id_to_part(muc_id)


def muc_id_to_segment(muc_id: IntLike) -> IntLike:
    """
    Convert the MUC digi ID to the segment number.

    Parameters:
        muc_id: The MUC digi ID array or value.

    Returns:
        The segment number.
    """
    return _ufuncs.muc_id_to_segment(muc_id)


def muc_id_to_layer(muc_id: IntLike) -> IntLike:
    """
    Convert the MUC digi ID to the layer number.

    Parameters:
        muc_id: The MUC digi ID array or value.

    Returns:
        The layer number.
    """
    return _ufuncs.muc_id_to_layer(muc_id)


def muc_id_to_channel(muc_id: IntLike) -> IntLike:
    """
    Convert the MUC digi ID to the channel number.

    Parameters:
        muc_id: The MUC digi ID array or value.

    Returns:
        The channel number.
    """
    return _ufuncs.muc_id_to_channel(muc_id)


def get_muc_id(part: IntLike, segment: IntLike, layer: IntLike, channel: IntLike) -> IntLike:
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


def muc_id_to_gap(muc_id: IntLike) -> IntLike:
    """
    Convert the MUC digi ID to the gap ID, which is equivalent to layer number.

    Parameters:
        muc_id: The MUC digi ID array or value.

    Returns:
        The gap ID.
    """
    return muc_id_to_layer(muc_id)


def muc_id_to_strip(muc_id: IntLike) -> IntLike:
    """
    Convert the MUC digi ID to the strip number, which is equivalent to channel number.

    Parameters:
        muc_id: The MUC digi ID array or value.

    Returns:
        The strip number.
    """
    return muc_id_to_channel(muc_id)


def parse_muc_id(muc_id: IntLike) -> ak.Array | dict[str, np.ndarray | int]:
    """
    Parse MUC digi ID.

    Available keys of the output:

    - `part`: The part number.
    - `segment`: The segment number.
    - `layer`: The layer number.
    - `channel`: The channel number.
    - `gap`: The gap number, which is equivalent to layer number.
    - `strip`: The strip number, which is equivalent to channel number.

    Parameters:
        muc_id: The MUC digi ID.

    Returns:
        The parsed MUC digi ID.
    """
    part = muc_id_to_part(muc_id)
    segment = muc_id_to_segment(muc_id)
    layer = muc_id_to_layer(muc_id)
    channel = muc_id_to_channel(muc_id)

    res = {
        "part": part,
        "segment": segment,
        "layer": layer,
        "channel": channel,
        "gap": layer,
        "strip": channel,
    }

    if isinstance(muc_id, ak.Array):
        return ak.zip(res)
    else:
        return res


###############################################################################
#                                    CGEM                                     #
###############################################################################


def check_cgem_id(cgem_id: IntLike) -> BoolLike:
    """
    Check if the CGEM digi ID is valid.

    Parameters:
        cgem_id: The CGEM digi ID array or value.

    Returns:
        Whether the digi ID is valid.
    """
    return _ufuncs.check_cgem_id(cgem_id)


def cgem_id_to_layer(cgem_id: IntLike) -> IntLike:
    """
    Convert the CGEM digi ID to the layer number.

    Parameters:
        cgem_id: The CGEM digi ID array or value.

    Returns:
        The layer number.
    """
    return _ufuncs.cgem_id_to_layer(cgem_id)


def cgem_id_to_sheet(cgem_id: IntLike) -> IntLike:
    """
    Convert the CGEM digi ID to the sheet number.

    Parameters:
        cgem_id: The CGEM digi ID array or value.

    Returns:
        The sheet number.
    """
    return _ufuncs.cgem_id_to_sheet(cgem_id)


def cgem_id_to_strip_type(cgem_id: IntLike) -> IntLike:
    """
    Convert the CGEM digi ID to the strip type. 0 for X-strip, 1 for V-strip.

    Parameters:
        cgem_id: The CGEM digi ID array or value.

    Returns:
        The strip type. 0 for X-strip, 1 for V-strip.
    """
    return _ufuncs.cgem_id_to_strip_type(cgem_id)


def cgem_id_to_strip(cgem_id: IntLike) -> IntLike:
    """
    Convert CGEM digi ID to strip number

    Parameters:
        cgem_id: CGEM digi ID array or value.

    Returns:
        The strip number.
    """
    return _ufuncs.cgem_id_to_strip(cgem_id)


def get_cgem_id(
    layer: IntLike, sheet: IntLike, strip_type: IntLike, strip: IntLike
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


def cgem_id_to_gid(cgem_id: IntLike) -> IntLike:
    """
    Convert CGEM digi ID to global strip ID (gid).

    Parameters:
        cgem_id: The CGEM digi ID array or value.

    Returns:
        The global strip ID.
    """
    return det.get_cgem_gid(
        cgem_id_to_layer(cgem_id),
        cgem_id_to_sheet(cgem_id),
        cgem_id_to_strip_type(cgem_id),
        cgem_id_to_strip(cgem_id),
    )


def parse_cgem_id(cgem_id: IntLike) -> ak.Array | dict[str, np.ndarray | int]:
    """
    Parse CGEM digi ID.

    Available keys of the output:

    - `gid`: The global strip ID.
    - `layer`: The layer number.
    - `sheet`: The sheet ID.
    - `strip_type`: The strip type. 0 for X-strip, 1 for V-strip.
    - `strip`: The strip ID.

    Parameters:
        cgem_id: The CGEM digi ID.

    Returns:
        The parsed CGEM digi ID.
    """
    layer = cgem_id_to_layer(cgem_id)
    sheet = cgem_id_to_sheet(cgem_id)
    strip_type = cgem_id_to_strip_type(cgem_id)
    strip = cgem_id_to_strip(cgem_id)
    gid = det.get_cgem_gid(layer, sheet, strip_type, strip)

    res = {
        "gid": gid,
        "layer": layer,
        "sheet": sheet,
        "strip_type": strip_type,
        "strip": strip,
    }

    if isinstance(cgem_id, ak.Array):
        return ak.zip(res)
    else:
        return res


def parse_cgem_digi(
    cgem_digi: ak.Array | dict[str, np.ndarray | int],
) -> ak.Array | dict[str, np.ndarray | int]:
    """
    Parse CGEM raw digi array. The raw digi array should contain [`m_intId`,
    `m_timeChannel`, `m_chargeChannel`, `m_overflow`] fields.

    Fields of the output:

    - `gid`: The global strip ID.
    - `layer`: The layer number.
    - `sheet`: The sheet ID.
    - `strip_type`: The strip type. 0 for X-strip, 1 for V-strip.
    - `strip`: The strip ID.
    - `charge_channel`: Charge channel.
    - `time_channel`: Time channel.
    - `overflow`: Overflow flag.
    - `track_index`: Track index.

    Parameters:
        cgem_digi: The CGEM raw digi array.

    Returns:
        The parsed CGEM digi array.
    """
    parsed_id = parse_cgem_id(cgem_digi["m_intId"])

    charge_channel = cgem_digi["m_chargeChannel"]
    time_channel = cgem_digi["m_timeChannel"]

    res = {
        "gid": parsed_id["gid"],
        "layer": parsed_id["layer"],
        "sheet": parsed_id["sheet"],
        "strip_type": parsed_id["strip_type"],
        "strip": parsed_id["strip"],
        "charge_channel": charge_channel,
        "time_channel": time_channel,
    }

    _add_field_if_exist(cgem_digi, res, "m_overflow", "overflow")
    _add_field_if_exist(cgem_digi, res, "m_trackIndex", "track_index")

    if isinstance(cgem_digi, ak.Array):
        return ak.zip(res)
    else:
        return res
