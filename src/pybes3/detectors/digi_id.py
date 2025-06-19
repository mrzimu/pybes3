from typing import Optional

import numba as nb
import numpy as np

from ..typing import BoolLike, IntLike

DIGI_MDC_FLAG = np.uint32(0x10)
DIGI_TOF_FLAG = np.uint32(0x20)
DIGI_EMC_FLAG = np.uint32(0x30)
DIGI_MUC_FLAG = np.uint32(0x40)
DIGI_HLT_FLAG = np.uint32(0x50)
DIGI_CGEM_FLAG = np.uint32(0x60)
DIGI_MRPC_FLAG = np.uint32(0x70)
DIGI_FLAG_OFFSET = np.uint32(24)
DIGI_FLAG_MASK = np.uint32(0xFF000000)

# MDC
DIGI_MDC_WIRETYPE_OFFSET = np.uint32(15)
DIGI_MDC_WIRETYPE_MASK = np.uint32(0x00008000)
DIGI_MDC_LAYER_OFFSET = np.uint32(9)
DIGI_MDC_LAYER_MASK = np.uint32(0x00007E00)
DIGI_MDC_WIRE_OFFSET = np.uint32(0)
DIGI_MDC_WIRE_MASK = np.uint32(0x000001FF)
DIGI_MDC_STEREO_WIRE = np.uint32(1)

# TOF
DIGI_TOF_PART_OFFSET = np.uint32(14)
DIGI_TOF_PART_MASK = np.uint32(0x0000C000)
DIGI_TOF_END_OFFSET = np.uint32(0)
DIGI_TOF_END_MASK = np.uint32(0x00000001)

DIGI_TOF_SCINT_LAYER_OFFSET = np.uint32(8)
DIGI_TOF_SCINT_LAYER_MASK = np.uint32(0x00000100)
DIGI_TOF_SCINT_PHI_OFFSET = np.uint32(1)
DIGI_TOF_SCINT_PHI_MASK = np.uint32(0x000000FE)

DIGI_TOF_MRPC_ENDCAP_OFFSET = np.uint32(11)
DIGI_TOF_MRPC_ENDCAP_MASK = np.uint32(0x00000800)
DIGI_TOF_MRPC_MODULE_OFFSET = np.uint32(5)
DIGI_TOF_MRPC_MODULE_MASK = np.uint32(0x000007E0)
DIGI_TOF_MRPC_STRIP_OFFSET = np.uint32(1)
DIGI_TOF_MRPC_STRIP_MASK = np.uint32(0x0000001E)

# EMC
DIGI_EMC_MODULE_OFFSET = np.uint32(16)
DIGI_EMC_MODULE_MASK = np.uint32(0x000F0000)
DIGI_EMC_THETA_OFFSET = np.uint32(8)
DIGI_EMC_THETA_MASK = np.uint32(0x00003F00)
DIGI_EMC_PHI_OFFSET = np.uint32(0)
DIGI_EMC_PHI_MASK = np.uint32(0x000000FF)

# MUC
DIGI_MUC_PART_OFFSET = np.uint32(16)
DIGI_MUC_PART_MASK = np.uint32(0x000F0000)
DIGI_MUC_SEGMENT_OFFSET = np.uint32(12)
DIGI_MUC_SEGMENT_MASK = np.uint32(0x0000F000)
DIGI_MUC_LAYER_OFFSET = np.uint32(8)
DIGI_MUC_LAYER_MASK = np.uint32(0x00000F00)
DIGI_MUC_CHANNEL_OFFSET = np.uint32(0)
DIGI_MUC_CHANNEL_MASK = np.uint32(0x000000FF)

# CGEM
DIGI_CGEM_STRIP_OFFSET = np.uint32(7)
DIGI_CGEM_STRIP_MASK = np.uint32(0x0007FF80)
DIGI_CGEM_STRIPTYPE_OFFSET = np.uint32(6)
DIGI_CGEM_STRIPTYPE_MASK = np.uint32(0x00000040)
DIGI_CGEM_SHEET_OFFSET = np.uint32(3)
DIGI_CGEM_SHEET_MASK = np.uint32(0x00000038)
DIGI_CGEM_LAYER_OFFSET = np.uint32(0)
DIGI_CGEM_LAYER_MASK = np.uint32(0x00000007)
DIGI_CGEM_XSTRIP = np.uint32(0)


###############################################################################
#                                     MDC                                     #
###############################################################################
@nb.vectorize(cache=True)
def check_mdc_id(mdc_digi_id: IntLike) -> BoolLike:
    """
    Check if the MDC digi ID is valid.

    Parameters:
        mdc_digi_id: The MDC digi ID array or value.

    Returns:
        Whether the digi ID is valid.
    """
    return (mdc_digi_id & DIGI_FLAG_MASK) >> DIGI_FLAG_OFFSET == DIGI_MDC_FLAG


@nb.vectorize(cache=True)
def mdc_id_to_wire(mdc_digi_id: IntLike) -> IntLike:
    """
    Convert MDC digi ID to wire number.

    Parameters:
        mdc_digi_id: MDC digi ID array or value.

    Returns:
        The wire number.
    """
    return np.uint16((mdc_digi_id & DIGI_MDC_WIRE_MASK) >> DIGI_MDC_WIRE_OFFSET)


@nb.vectorize(cache=True)
def mdc_id_to_layer(mdc_digi_id: IntLike) -> IntLike:
    """
    Convert the MDC digi ID to the layer number.

    Parameters:
        mdc_digi_id: The MDC digi ID array or value.

    Returns:
        The layer number.
    """
    return np.uint8((mdc_digi_id & DIGI_MDC_LAYER_MASK) >> DIGI_MDC_LAYER_OFFSET)


@nb.vectorize(cache=True)
def mdc_id_to_is_stereo(mdc_digi_id: IntLike) -> BoolLike:
    """
    Convert the MDC digi ID to whether it is a stereo wire.

    Parameters:
        mdc_digi_id: The MDC digi ID array or value.

    Returns:
        Whether the wire is a stereo wire.
    """
    return (
        mdc_digi_id & DIGI_MDC_WIRETYPE_MASK
    ) >> DIGI_MDC_WIRETYPE_OFFSET == DIGI_MDC_STEREO_WIRE


@nb.vectorize(cache=True)
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
    return np.uint32(
        ((wire << DIGI_MDC_WIRE_OFFSET) & DIGI_MDC_WIRE_MASK)
        | ((layer << DIGI_MDC_LAYER_OFFSET) & DIGI_MDC_LAYER_MASK)
        | ((wire_type << DIGI_MDC_WIRETYPE_OFFSET) & DIGI_MDC_WIRETYPE_MASK)
        | (DIGI_MDC_FLAG << DIGI_FLAG_OFFSET)
    )


###############################################################################
#                                     TOF                                     #
###############################################################################
@nb.vectorize(cache=True)
def check_tof_id(tof_digi_id: IntLike) -> BoolLike:
    """
    Check if the TOF digi ID is valid.

    Parameters:
        tof_digi_id: The TOF digi ID array or value.

    Returns:
        Whether the digi ID is valid.
    """
    return (tof_digi_id & DIGI_FLAG_MASK) >> DIGI_FLAG_OFFSET == DIGI_TOF_FLAG


@nb.vectorize(cache=True)
def tof_id_to_part(tof_digi_id: IntLike) -> IntLike:
    """
    Convert TOF digi ID to part number. 0, 1, 2 for scintillator endcap0/barrel/endcap1,
    3, 4 for MRPC endcap0/endcap1.

    Parameters:
        tof_digi_id: TOF digi ID array or value.

    Returns:
        The part number.
    """
    part = (tof_digi_id & DIGI_TOF_PART_MASK) >> DIGI_TOF_PART_OFFSET
    if part == 3:  # += MRPC endcap number
        part += (tof_digi_id & DIGI_TOF_MRPC_ENDCAP_MASK) >> DIGI_TOF_MRPC_ENDCAP_OFFSET
    return np.uint8(part)


@nb.vectorize(cache=True)
def tof_id_to_end(tof_digi_id: IntLike) -> IntLike:
    """
    Convert the TOF digi ID to the readout end number.

    Parameters:
        tof_digi_id: The TOF digi ID array or value.

    Returns:
        The readout end number.
    """
    return np.uint8(tof_digi_id % 2)


@nb.vectorize(cache=True)
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
    part = tof_id_to_part(tof_digi_id)
    if part < 3:
        res = (tof_digi_id & DIGI_TOF_SCINT_LAYER_MASK) >> DIGI_TOF_SCINT_LAYER_OFFSET
    else:
        res = (tof_digi_id & DIGI_TOF_MRPC_MODULE_MASK) >> DIGI_TOF_MRPC_MODULE_OFFSET
    return np.uint8(res)


@nb.vectorize(cache=True)
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
    if part < 3:
        res = (tof_digi_id & DIGI_TOF_SCINT_LAYER_MASK) >> DIGI_TOF_SCINT_LAYER_OFFSET
    else:
        res = (tof_digi_id & DIGI_TOF_MRPC_MODULE_MASK) >> DIGI_TOF_MRPC_MODULE_OFFSET
    return np.uint8(res)


def tof_id_to_layer_or_module(
    tof_digi_id: IntLike,
    part: Optional[IntLike] = None,
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


@nb.vectorize(cache=True)
def _tof_id_to_phi_or_strip_1(tof_digi_id: IntLike) -> IntLike:
    """
    Convert the TOF digi ID to the scintillator phi or MRPC strip number.
    No part number is provided, so it will be calculated based on the TOF digi ID.

    This function is used by `tof_id_to_phiOrStrip` when part number is not provided.

    Parameters:
        tof_digi_id: The TOF digi ID array or value.

    Returns:
        The scintillator phi or MRPC strip number.
    """
    part = tof_id_to_part(tof_digi_id)
    if part < 3:
        res = (tof_digi_id & DIGI_TOF_SCINT_PHI_MASK) >> DIGI_TOF_SCINT_PHI_OFFSET
    else:
        res = (tof_digi_id & DIGI_TOF_MRPC_STRIP_MASK) >> DIGI_TOF_MRPC_STRIP_OFFSET
    return np.uint8(res)


@nb.vectorize(cache=True)
def _tof_id_to_phi_or_strip_2(tof_digi_id: IntLike, part: IntLike) -> IntLike:
    """
    Convert the TOF digi ID to the scintillator phi or MRPC strip number.

    This function is used by `tof_id_to_phiOrStrip` when part number is provided.

    Parameters:
        tof_digi_id: The TOF digi ID array or value.
        part: The part number.

    Returns:
        The scintillator phi or MRPC strip number based on the part number.
    """
    if part < 3:
        res = (tof_digi_id & DIGI_TOF_SCINT_PHI_MASK) >> DIGI_TOF_SCINT_PHI_OFFSET
    else:
        res = (tof_digi_id & DIGI_TOF_MRPC_STRIP_MASK) >> DIGI_TOF_MRPC_STRIP_OFFSET
    return np.uint8(res)


def tof_id_to_phi_or_strip(
    tof_digi_id: IntLike,
    part: Optional[IntLike] = None,
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


@nb.vectorize(cache=True)
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
    if part < 3:
        return np.uint32(
            ((part << DIGI_TOF_PART_OFFSET) & DIGI_TOF_PART_MASK)
            | ((layer_or_module << DIGI_TOF_SCINT_LAYER_OFFSET) & DIGI_TOF_SCINT_LAYER_MASK)
            | ((phi_or_strip << DIGI_TOF_SCINT_PHI_OFFSET) & DIGI_TOF_SCINT_PHI_MASK)
            | ((end << DIGI_TOF_END_OFFSET) & DIGI_TOF_END_MASK)
            | (DIGI_TOF_FLAG << DIGI_FLAG_OFFSET)
        )
    else:
        return np.uint32(
            ((3 << DIGI_TOF_PART_OFFSET) & DIGI_TOF_PART_MASK)
            | (((part - 3) << DIGI_TOF_MRPC_ENDCAP_OFFSET) & DIGI_TOF_MRPC_ENDCAP_MASK)
            | ((layer_or_module << DIGI_TOF_MRPC_MODULE_OFFSET) & DIGI_TOF_MRPC_MODULE_MASK)
            | ((phi_or_strip << DIGI_TOF_MRPC_STRIP_OFFSET) & DIGI_TOF_MRPC_STRIP_MASK)
            | ((end << DIGI_TOF_END_OFFSET) & DIGI_TOF_END_MASK)
            | (DIGI_TOF_FLAG << DIGI_FLAG_OFFSET)
        )


###############################################################################
#                                     EMC                                     #
###############################################################################
@nb.vectorize(cache=True)
def check_emc_id(emc_digi_id: IntLike) -> BoolLike:
    """
    Check if the EMC digi ID is valid.

    Parameters:
        emc_digi_id: The EMC digi ID array or value.

    Returns:
        Whether the digi ID is valid.
    """
    return (emc_digi_id & DIGI_FLAG_MASK) >> DIGI_FLAG_OFFSET == DIGI_EMC_FLAG


@nb.vectorize(cache=True)
def emc_id_to_module(emc_digi_id: IntLike) -> IntLike:
    """
    Convert EMC digi ID to module number

    Parameters:
        emc_digi_id: EMC digi ID array or value.

    Returns:
        The module number.
    """
    return np.uint8((emc_digi_id & DIGI_EMC_MODULE_MASK) >> DIGI_EMC_MODULE_OFFSET)


@nb.vectorize(cache=True)
def emc_id_to_theta(emc_digi_id: IntLike) -> IntLike:
    """
    Convert the EMC digi ID to the theta number.

    Parameters:
        emc_digi_id: The EMC digi ID array or value.

    Returns:
        The theta number.
    """
    return np.uint8((emc_digi_id & DIGI_EMC_THETA_MASK) >> DIGI_EMC_THETA_OFFSET)


@nb.vectorize(cache=True)
def emc_id_to_phi(emc_digi_id: IntLike) -> IntLike:
    """
    Convert the EMC digi ID to the phi number.

    Parameters:
        emc_digi_id: The EMC digi ID array or value.

    Returns:
        The phi number.
    """
    return np.uint8((emc_digi_id & DIGI_EMC_PHI_MASK) >> DIGI_EMC_PHI_OFFSET)


@nb.vectorize(cache=True)
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
    return np.uint32(
        ((module << DIGI_EMC_MODULE_OFFSET) & DIGI_EMC_MODULE_MASK)
        | ((theta << DIGI_EMC_THETA_OFFSET) & DIGI_EMC_THETA_MASK)
        | ((phi << DIGI_EMC_PHI_OFFSET) & DIGI_EMC_PHI_MASK)
        | (DIGI_EMC_FLAG << DIGI_FLAG_OFFSET)
    )


###############################################################################
#                                     MUC                                     #
###############################################################################
@nb.vectorize(cache=True)
def check_muc_id(muc_digi_id: IntLike) -> BoolLike:
    """
    Check if the MUC digi ID is valid.

    Parameters:
        muc_digi_id: The MUC digi ID array or value.

    Returns:
        Whether the digi ID is valid.
    """
    return (muc_digi_id & DIGI_FLAG_MASK) >> DIGI_FLAG_OFFSET == DIGI_MUC_FLAG


@nb.vectorize(cache=True)
def muc_id_to_part(muc_digi_id: IntLike) -> IntLike:
    """
    Convert MUC digi ID to part number

    Parameters:
        muc_digi_id: MUC digi ID array or value.

    Returns:
        The part number.
    """
    return np.uint8((muc_digi_id & DIGI_MUC_PART_MASK) >> DIGI_MUC_PART_OFFSET)


@nb.vectorize(cache=True)
def muc_id_to_segment(muc_digi_id: IntLike) -> IntLike:
    """
    Convert the MUC digi ID to the segment number.

    Parameters:
        muc_digi_id: The MUC digi ID array or value.

    Returns:
        The segment number.
    """
    return np.uint8((muc_digi_id & DIGI_MUC_SEGMENT_MASK) >> DIGI_MUC_SEGMENT_OFFSET)


@nb.vectorize(cache=True)
def muc_id_to_layer(muc_digi_id: IntLike) -> IntLike:
    """
    Convert the MUC digi ID to the layer number.

    Parameters:
        muc_digi_id: The MUC digi ID array or value.

    Returns:
        The layer number.
    """
    return np.uint8((muc_digi_id & DIGI_MUC_LAYER_MASK) >> DIGI_MUC_LAYER_OFFSET)


@nb.vectorize(cache=True)
def muc_id_to_channel(muc_digi_id: IntLike) -> IntLike:
    """
    Convert the MUC digi ID to the channel number.

    Parameters:
        muc_digi_id: The MUC digi ID array or value.

    Returns:
        The channel number.
    """
    return np.uint8((muc_digi_id & DIGI_MUC_CHANNEL_MASK) >> DIGI_MUC_CHANNEL_OFFSET)


@nb.vectorize(cache=True)
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
    return np.uint32(
        ((part << DIGI_MUC_PART_OFFSET) & DIGI_MUC_PART_MASK)
        | ((segment << DIGI_MUC_SEGMENT_OFFSET) & DIGI_MUC_SEGMENT_MASK)
        | ((layer << DIGI_MUC_LAYER_OFFSET) & DIGI_MUC_LAYER_MASK)
        | ((channel << DIGI_MUC_CHANNEL_OFFSET) & DIGI_MUC_CHANNEL_MASK)
        | (DIGI_MUC_FLAG << DIGI_FLAG_OFFSET)
    )


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


###############################################################################
#                                    CGEM                                     #
###############################################################################
@nb.vectorize(cache=True)
def check_cgem_id(cgem_digi_id: IntLike) -> BoolLike:
    """
    Check if the CGEM digi ID is valid.

    Parameters:
        cgem_digi_id: The CGEM digi ID array or value.

    Returns:
        Whether the digi ID is valid.
    """
    return (cgem_digi_id & DIGI_FLAG_MASK) >> DIGI_FLAG_OFFSET == DIGI_CGEM_FLAG


@nb.vectorize(cache=True)
def cgem_id_to_layer(cgem_digi_id: IntLike) -> IntLike:
    """
    Convert the CGEM digi ID to the layer number.

    Parameters:
        cgem_digi_id: The CGEM digi ID array or value.

    Returns:
        The layer number.
    """
    return np.uint8((cgem_digi_id & DIGI_CGEM_LAYER_MASK) >> DIGI_CGEM_LAYER_OFFSET)


@nb.vectorize(cache=True)
def cgem_id_to_sheet(cgem_digi_id: IntLike) -> IntLike:
    """
    Convert the CGEM digi ID to the sheet number.

    Parameters:
        cgem_digi_id: The CGEM digi ID array or value.

    Returns:
        The sheet number.
    """
    return np.uint8((cgem_digi_id & DIGI_CGEM_SHEET_MASK) >> DIGI_CGEM_SHEET_OFFSET)


@nb.vectorize(cache=True)
def cgem_id_to_strip(cgem_digi_id: IntLike) -> IntLike:
    """
    Convert CGEM digi ID to strip number

    Parameters:
        cgem_digi_id: CGEM digi ID array or value.

    Returns:
        The strip number.
    """
    return np.uint16((cgem_digi_id & DIGI_CGEM_STRIP_MASK) >> DIGI_CGEM_STRIP_OFFSET)


@nb.vectorize(cache=True)
def cgem_id_to_is_x_strip(cgem_digi_id: IntLike) -> BoolLike:
    """
    Convert the CGEM digi ID to whether it is an X-strip.

    Parameters:
        cgem_digi_id: The CGEM digi ID array or value.

    Returns:
        Whether the strip is an X-strip
    """
    return (
        (cgem_digi_id & DIGI_CGEM_STRIPTYPE_MASK) >> DIGI_CGEM_STRIPTYPE_OFFSET
    ) == DIGI_CGEM_XSTRIP


@nb.vectorize(cache=True)
def get_cgem_digi_id(
    layer: IntLike,
    sheet: IntLike,
    strip: IntLike,
    is_x_strip: BoolLike,
) -> IntLike:
    """
    Generate CGEM digi ID based on the strip number, strip type, sheet number, and layer number.

    Parameters:
        layer: The layer number.
        sheet: The sheet number.
        strip: The strip number.
        is_x_strip: Whether the strip is an X-strip.

    Returns:
        The CGEM digi ID.
    """
    return np.uint32(
        ((strip << DIGI_CGEM_STRIP_OFFSET) & DIGI_CGEM_STRIP_MASK)
        | ((~is_x_strip << DIGI_CGEM_STRIPTYPE_OFFSET) & DIGI_CGEM_STRIPTYPE_MASK)
        | ((sheet << DIGI_CGEM_SHEET_OFFSET) & DIGI_CGEM_SHEET_MASK)
        | ((layer << DIGI_CGEM_LAYER_OFFSET) & DIGI_CGEM_LAYER_MASK)
        | (DIGI_CGEM_FLAG << DIGI_FLAG_OFFSET)
    )
