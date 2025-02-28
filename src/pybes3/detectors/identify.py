from typing import Literal, Union

import awkward as ak
import numba as nb
import numpy as np

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
@nb.vectorize([nb.boolean(nb.int_)])
def check_mdc_id(
    mdc_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.bool]:
    """
    Check if the MDC ID is valid.

    Parameters:
        mdc_id: The MDC ID array or value.

    Returns:
        Whether the ID is valid.
    """
    return (mdc_id & DIGI_FLAG_MASK) >> DIGI_FLAG_OFFSET == DIGI_MDC_FLAG


@nb.vectorize([nb.uint16(nb.int_)])
def mdc_id_to_wire(
    mdc_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint16]:
    """
    Convert MDC ID to wire ID

    Parameters:
        mdc_id: MDC ID array or value.

    Returns:
        The wire ID.
    """
    return (mdc_id & DIGI_MDC_WIRE_MASK) >> DIGI_MDC_WIRE_OFFSET


@nb.vectorize([nb.uint8(nb.int_)])
def mdc_id_to_layer(
    mdc_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert the MDC ID to the layer ID.

    Parameters:
        mdc_id: The MDC ID array or value.

    Returns:
        The layer ID.
    """
    return (mdc_id & DIGI_MDC_LAYER_MASK) >> DIGI_MDC_LAYER_OFFSET


@nb.vectorize([nb.boolean(nb.int_)])
def mdc_id_to_is_stereo(
    mdc_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.bool]:
    """
    Convert the MDC ID to whether it is a stereo wire.

    Parameters:
        mdc_id: The MDC ID array or value.

    Returns:
        Whether the wire is a stereo wire.
    """
    return (
        mdc_id & DIGI_MDC_WIRETYPE_MASK
    ) >> DIGI_MDC_WIRETYPE_OFFSET == DIGI_MDC_STEREO_WIRE


@nb.vectorize([nb.uint32(nb.int_, nb.int_, nb.int_), nb.uint32(nb.int_, nb.int_, nb.boolean)])
def get_mdc_id(
    wire: Union[ak.Array, np.ndarray, int],
    layer: Union[ak.Array, np.ndarray, int],
    wire_type: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Generate MDC ID based on the wire ID, layer ID, and wire type.

    Parameters:
        wire: The wire ID.
        layer: The layer ID.
        wire_type: The wire type.

    Returns:
        The MDC ID.
    """
    return (
        ((wire << DIGI_MDC_WIRE_OFFSET) & DIGI_MDC_WIRE_MASK)
        | ((layer << DIGI_MDC_LAYER_OFFSET) & DIGI_MDC_LAYER_MASK)
        | ((wire_type << DIGI_MDC_WIRETYPE_OFFSET) & DIGI_MDC_WIRETYPE_MASK)
        | (DIGI_MDC_FLAG << DIGI_FLAG_OFFSET)
    )


###############################################################################
#                                     TOF                                     #
###############################################################################
@nb.vectorize([nb.boolean(nb.int_)])
def check_tof_id(
    tof_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.bool]:
    """
    Check if the TOF ID is valid.

    Parameters:
        tof_id: The TOF ID array or value.

    Returns:
        Whether the ID is valid.
    """
    return (tof_id & DIGI_FLAG_MASK) >> DIGI_FLAG_OFFSET == DIGI_TOF_FLAG


@nb.vectorize([nb.uint8(nb.int_)])
def tof_id_to_part(
    tof_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint8]:
    """
    Convert TOF ID to part ID. 0, 1, 2 for scintillator endcap0/barrel/endcap1,
    3, 4 for MRPC endcap0/endcap1.

    Parameters:
        tof_id: TOF ID array or value.

    Returns:
        The part ID.
    """
    part = (tof_id & DIGI_TOF_PART_MASK) >> DIGI_TOF_PART_OFFSET
    if part == 3:  # += MRPC endcap number
        part += (tof_id & DIGI_TOF_MRPC_ENDCAP_MASK) >> DIGI_TOF_MRPC_ENDCAP_OFFSET
    return part


@nb.vectorize([nb.uint8(nb.int_)])
def tof_id_to_end(
    tof_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint8]:
    """
    Convert the TOF ID to the readout end ID.

    Parameters:
        tof_id: The TOF ID array or value.

    Returns:
        The readout end ID.
    """
    return tof_id % 2


@nb.vectorize([nb.uint8(nb.int_)])
def _tof_id_to_layerOrModule1(
    tof_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint8]:
    """
    Convert the TOF ID to the scintillator layer or MRPC module ID.

    This function is used by `tof_id_to_layerOrModule` when part ID is not provided.

    Parameters:
        tof_id: The TOF ID array or value.

    Returns:
        The scintillator layer or MRPC module ID.
    """
    part = tof_id_to_part(tof_id)
    if part < 3:
        return (tof_id & DIGI_TOF_SCINT_LAYER_MASK) >> DIGI_TOF_SCINT_LAYER_OFFSET
    else:
        return (tof_id & DIGI_TOF_MRPC_MODULE_MASK) >> DIGI_TOF_MRPC_MODULE_OFFSET


@nb.vectorize([nb.uint8(nb.int_, nb.int_)])
def _tof_id_to_layerOrModule2(
    tof_id: Union[ak.Array, np.ndarray, int], part: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint8]:
    """
    Convert the TOF ID to the scintillator layer or MRPC module ID.
    No part ID is provided, so it will be calculated based on the TOF ID.

    This function is used by `tof_id_to_layerOrModule` when part ID is provided.

    Parameters:
        tof_id: The TOF ID array or value.
        part: The part ID.

    Returns:
        The scintillator layer or MRPC module ID based on the part ID.
    """
    if part < 3:
        return (tof_id & DIGI_TOF_SCINT_LAYER_MASK) >> DIGI_TOF_SCINT_LAYER_OFFSET
    else:
        return (tof_id & DIGI_TOF_MRPC_MODULE_MASK) >> DIGI_TOF_MRPC_MODULE_OFFSET


def tof_id_to_layerOrModule(
    tof_id: Union[ak.Array, np.ndarray, int],
    part: Union[ak.Array, np.ndarray, int, None] = None,
) -> Union[ak.Array, np.ndarray, np.uint8]:
    """
    Convert the TOF ID to the scintillator layer or MRPC module ID.
    If `part < 3`, it is scintillator and the return value is layer ID. Otherwise, it is
    MRPC and the return value is module ID.

    Parameters:
        tof_id: The TOF ID array or value.
        part: The part ID. If not provided, it will be calculated based on the TOF ID.

    Returns:
        The scintillator layer or MRPC module ID.
    """
    if part is None:
        return _tof_id_to_layerOrModule1(tof_id)
    else:
        return _tof_id_to_layerOrModule2(tof_id, part)


@nb.vectorize([nb.uint8(nb.int_)])
def _tof_id_to_phiOrStrip1(
    tof_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint8]:
    """
    Convert the TOF ID to the scintillator phi or MRPC strip ID.
    No part ID is provided, so it will be calculated based on the TOF ID.

    This function is used by `tof_id_to_phiOrStrip` when part ID is not provided.

    Parameters:
        tof_id: The TOF ID array or value.

    Returns:
        The scintillator phi or MRPC strip ID.
    """
    part = tof_id_to_part(tof_id)
    if part < 3:
        return (tof_id & DIGI_TOF_SCINT_PHI_MASK) >> DIGI_TOF_SCINT_PHI_OFFSET
    else:
        return (tof_id & DIGI_TOF_MRPC_STRIP_MASK) >> DIGI_TOF_MRPC_STRIP_OFFSET


@nb.vectorize([nb.uint8(nb.int_, nb.int_)])
def _tof_id_to_phiOrStrip2(
    tof_id: Union[ak.Array, np.ndarray, int], part: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint8]:
    """
    Convert the TOF ID to the scintillator phi or MRPC strip ID.

    This function is used by `tof_id_to_phiOrStrip` when part ID is provided.

    Parameters:
        tof_id: The TOF ID array or value.
        part: The part ID.

    Returns:
        The scintillator phi or MRPC strip ID based on the part ID.
    """
    if part < 3:
        return (tof_id & DIGI_TOF_SCINT_PHI_MASK) >> DIGI_TOF_SCINT_PHI_OFFSET
    else:
        return (tof_id & DIGI_TOF_MRPC_STRIP_MASK) >> DIGI_TOF_MRPC_STRIP_OFFSET


def tof_id_to_phiOrStrip(
    tof_id: Union[ak.Array, np.ndarray, int],
    part: Union[ak.Array, np.ndarray, int, None] = None,
) -> Union[ak.Array, np.ndarray, np.uint8]:
    """
    Convert the TOF ID to the scintillator phi or MRPC strip ID, based on the part ID.
    If `part < 3`, it is scintillator and the return value is phi ID. Otherwise, it is
    MRPC and the return value is strip ID.

    Parameters:
        tof_id: The TOF ID array or value.
        part: The part ID. If not provided, it will be calculated based on the TOF ID.

    Returns:
        The scintillator phi or MRPC strip ID.
    """
    if part is None:
        return _tof_id_to_phiOrStrip1(tof_id)
    else:
        return _tof_id_to_phiOrStrip2(tof_id, part)


@nb.vectorize([nb.uint32(nb.int_, nb.int_, nb.int_, nb.int_)])
def get_tof_id(
    part: Union[ak.Array, np.ndarray, int],
    layer_or_module: Union[ak.Array, np.ndarray, int],
    phi_or_strip: Union[ak.Array, np.ndarray, int],
    end: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Generate TOF scintillator ID based on the part ID, layer ID, phi ID, and readout end ID.

    Parameters:
        part: The part ID.
        layer_or_module: The scintillator layer or MRPC module ID.
        phi_or_strip: The scintillator phi or MRPC strip ID.
        end: The readout end ID.

    Returns:
        The TOF ID.
    """
    if part < 3:
        return (
            ((part << DIGI_TOF_PART_OFFSET) & DIGI_TOF_PART_MASK)
            | ((layer_or_module << DIGI_TOF_SCINT_LAYER_OFFSET) & DIGI_TOF_SCINT_LAYER_MASK)
            | ((phi_or_strip << DIGI_TOF_SCINT_PHI_OFFSET) & DIGI_TOF_SCINT_PHI_MASK)
            | ((end << DIGI_TOF_END_OFFSET) & DIGI_TOF_END_MASK)
            | (DIGI_TOF_FLAG << DIGI_FLAG_OFFSET)
        )
    else:
        return (
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
@nb.vectorize([nb.boolean(nb.int_)])
def check_emc_id(
    emc_id: Union[ak.Array, np.ndarray, np.uint32],
) -> Union[ak.Array, np.ndarray, np.bool]:
    """
    Check if the EMC ID is valid.

    Parameters:
        emc_id: The EMC ID array or value.

    Returns:
        Whether the ID is valid.
    """
    return (emc_id & DIGI_FLAG_MASK) >> DIGI_FLAG_OFFSET == DIGI_EMC_FLAG


@nb.vectorize([nb.uint8(nb.int_)])
def emc_id_to_module(
    emc_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint8]:
    """
    Convert EMC ID to module ID

    Parameters:
        emc_id: EMC ID array or value.

    Returns:
        The module ID.
    """
    return (emc_id & DIGI_EMC_MODULE_MASK) >> DIGI_EMC_MODULE_OFFSET


@nb.vectorize([nb.uint8(nb.int_)])
def emc_id_to_theta(
    emc_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint8]:
    """
    Convert the EMC ID to the theta ID.

    Parameters:
        emc_id: The EMC ID array or value.

    Returns:
        The theta ID.
    """
    return (emc_id & DIGI_EMC_THETA_MASK) >> DIGI_EMC_THETA_OFFSET


@nb.vectorize([nb.uint8(nb.int_)])
def emc_id_to_phi(
    emc_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint8]:
    """
    Convert the EMC ID to the phi ID.

    Parameters:
        emc_id: The EMC ID array or value.

    Returns:
        The phi ID.
    """
    return (emc_id & DIGI_EMC_PHI_MASK) >> DIGI_EMC_PHI_OFFSET


@nb.vectorize([nb.uint32(nb.int_, nb.int_, nb.int_)])
def get_emc_id(
    module: Union[ak.Array, np.ndarray, int],
    theta: Union[ak.Array, np.ndarray, int],
    phi: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Generate EMC ID based on the module ID, theta ID, and phi ID.

    Parameters:
        module: The module ID.
        theta: The theta ID.
        phi: The phi ID.

    Returns:
        The EMC ID.
    """
    return (
        ((module << DIGI_EMC_MODULE_OFFSET) & DIGI_EMC_MODULE_MASK)
        | ((theta << DIGI_EMC_THETA_OFFSET) & DIGI_EMC_THETA_MASK)
        | ((phi << DIGI_EMC_PHI_OFFSET) & DIGI_EMC_PHI_MASK)
        | (DIGI_EMC_FLAG << DIGI_FLAG_OFFSET)
    )


###############################################################################
#                                     MUC                                     #
###############################################################################
@nb.vectorize([nb.boolean(nb.int_)])
def check_muc_id(
    muc_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.bool]:
    """
    Check if the MUC ID is valid.

    Parameters:
        muc_id: The MUC ID array or value.

    Returns:
        Whether the ID is valid.
    """
    return (muc_id & DIGI_FLAG_MASK) >> DIGI_FLAG_OFFSET == DIGI_MUC_FLAG


@nb.vectorize([nb.uint8(nb.int_)])
def muc_id_to_part(
    muc_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint8]:
    """
    Convert MUC ID to part ID

    Parameters:
        muc_id: MUC ID array or value.

    Returns:
        The part ID.
    """
    return (muc_id & DIGI_MUC_PART_MASK) >> DIGI_MUC_PART_OFFSET


@nb.vectorize([nb.uint8(nb.int_)])
def muc_id_to_segment(
    muc_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint8]:
    """
    Convert the MUC ID to the segment ID.

    Parameters:
        muc_id: The MUC ID array or value.

    Returns:
        The segment ID.
    """
    return (muc_id & DIGI_MUC_SEGMENT_MASK) >> DIGI_MUC_SEGMENT_OFFSET


@nb.vectorize([nb.uint8(nb.int_)])
def muc_id_to_layer(
    muc_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint8]:
    """
    Convert the MUC ID to the layer ID.

    Parameters:
        muc_id: The MUC ID array or value.

    Returns:
        The layer ID.
    """
    return (muc_id & DIGI_MUC_LAYER_MASK) >> DIGI_MUC_LAYER_OFFSET


@nb.vectorize([nb.uint8(nb.int_)])
def muc_id_to_channel(
    muc_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint8]:
    """
    Convert the MUC ID to the channel ID.

    Parameters:
        muc_id: The MUC ID array or value.

    Returns:
        The channel ID.
    """
    return (muc_id & DIGI_MUC_CHANNEL_MASK) >> DIGI_MUC_CHANNEL_OFFSET


@nb.vectorize([nb.uint32(nb.int_, nb.int_, nb.int_, nb.int_)])
def get_muc_id(
    part: Union[ak.Array, np.ndarray, int],
    segment: Union[ak.Array, np.ndarray, int],
    layer: Union[ak.Array, np.ndarray, int],
    channel: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Generate MUC ID based on the part ID, segment ID, layer ID, and channel ID.

    Parameters:
        part: The part ID.
        segment: The segment ID.
        layer: The layer ID.
        channel: The channel ID.

    Returns:
        The MUC ID.
    """
    return (
        ((part << DIGI_MUC_PART_OFFSET) & DIGI_MUC_PART_MASK)
        | ((segment << DIGI_MUC_SEGMENT_OFFSET) & DIGI_MUC_SEGMENT_MASK)
        | ((layer << DIGI_MUC_LAYER_OFFSET) & DIGI_MUC_LAYER_MASK)
        | ((channel << DIGI_MUC_CHANNEL_OFFSET) & DIGI_MUC_CHANNEL_MASK)
        | (DIGI_MUC_FLAG << DIGI_FLAG_OFFSET)
    )


def muc_id_to_gap(
    muc_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint8]:
    """
    Convert the MUC ID to the gap ID, which is equivalent to layer ID.

    Parameters:
        muc_id: The MUC ID array or value.

    Returns:
        The gap ID.
    """
    return muc_id_to_layer(muc_id)


def muc_id_to_strip(
    muc_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint8]:
    """
    Convert the MUC ID to the strip ID, which is equivalent to channel ID.

    Parameters:
        muc_id: The MUC ID array or value.

    Returns:
        The strip ID.
    """
    return muc_id_to_channel(muc_id)


###############################################################################
#                                    CGEM                                     #
###############################################################################
@nb.vectorize([nb.boolean(nb.int_)])
def check_cgem_id(
    cgem_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.bool]:
    """
    Check if the CGEM ID is valid.

    Parameters:
        cgem_id: The CGEM ID array or value.

    Returns:
        Whether the ID is valid.
    """
    return (cgem_id & DIGI_FLAG_MASK) >> DIGI_FLAG_OFFSET == DIGI_CGEM_FLAG


@nb.vectorize([nb.uint8(nb.int_)])
def cgem_id_to_layer(
    cgem_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint8]:
    """
    Convert the CGEM ID to the layer ID.

    Parameters:
        cgem_id: The CGEM ID array or value.

    Returns:
        The layer ID.
    """
    return (cgem_id & DIGI_CGEM_LAYER_MASK) >> DIGI_CGEM_LAYER_OFFSET


@nb.vectorize([nb.uint8(nb.int_)])
def cgem_id_to_sheet(
    cgem_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint8]:
    """
    Convert the CGEM ID to the sheet ID.

    Parameters:
        cgem_id: The CGEM ID array or value.

    Returns:
        The sheet ID.
    """
    return (cgem_id & DIGI_CGEM_SHEET_MASK) >> DIGI_CGEM_SHEET_OFFSET


@nb.vectorize([nb.uint16(nb.int_)])
def cgem_id_to_strip(
    cgem_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert CGEM ID to strip ID

    Parameters:
        cgem_id: CGEM ID array or value.

    Returns:
        The strip ID.
    """
    return (cgem_id & DIGI_CGEM_STRIP_MASK) >> DIGI_CGEM_STRIP_OFFSET


@nb.vectorize([nb.boolean(nb.int_)])
def cgem_id_to_is_x_strip(
    cgem_id: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.bool]:
    """
    Convert the CGEM ID to whether it is an X-strip.

    Parameters:
        cgem_id: The CGEM ID array or value.

    Returns:
        Whether the strip is an X-strip
    """
    return (
        (cgem_id & DIGI_CGEM_STRIPTYPE_MASK) >> DIGI_CGEM_STRIPTYPE_OFFSET
    ) == DIGI_CGEM_XSTRIP


@nb.vectorize([nb.uint32(nb.int_, nb.int_, nb.int_, nb.boolean)])
def get_cgem_id(
    layer: Union[ak.Array, np.ndarray, int],
    sheet: Union[ak.Array, np.ndarray, int],
    strip: Union[ak.Array, np.ndarray, int],
    is_x_strip: Union[ak.Array, np.ndarray, bool],
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Generate CGEM ID based on the strip ID, strip type, sheet ID, and layer ID.

    Parameters:
        layer: The layer ID.
        sheet: The sheet ID.
        strip: The strip ID.
        is_x_strip: Whether the strip is an X-strip.

    Returns:
        The CGEM ID.
    """
    return (
        ((strip << DIGI_CGEM_STRIP_OFFSET) & DIGI_CGEM_STRIP_MASK)
        | ((~is_x_strip << DIGI_CGEM_STRIPTYPE_OFFSET) & DIGI_CGEM_STRIPTYPE_MASK)
        | ((sheet << DIGI_CGEM_SHEET_OFFSET) & DIGI_CGEM_SHEET_MASK)
        | ((layer << DIGI_CGEM_LAYER_OFFSET) & DIGI_CGEM_LAYER_MASK)
        | (DIGI_CGEM_FLAG << DIGI_FLAG_OFFSET)
    )


###############################################################################
#                                Make awkwards                                #
###############################################################################
def parse_mdc_id(
    mdc_id: Union[ak.Array, np.ndarray, int],
    flat: bool = False,
    library: Literal["ak", "np"] = "ak",
) -> Union[ak.Record, dict[str, np.ndarray], dict[str, np.int_]]:
    """
    Parse MDC ID.

    If `library` is `np`, return `dict[str, np.ndarray]`.

    Available keys of the output:
        - wire: The wire ID.
        - layer: The layer ID.
        - is_stereo: Whether the wire is a stereo wire.

    Parameters:
        mdc_id: The MDC ID.
        flat: Whether to flatten the output.
        library: The library to use as output.

    Returns:
        The parsed MDC ID. If `library` is `ak`, return `ak.Record`.
    """
    if library not in ["ak", "np"]:
        raise ValueError(f"Unsupported library: {library}")

    if flat and isinstance(mdc_id, ak.Array):
        mdc_id = ak.flatten(mdc_id)

    res = {
        "wire": mdc_id_to_wire(mdc_id),
        "layer": mdc_id_to_layer(mdc_id),
        "is_stereo": mdc_id_to_is_stereo(mdc_id),
    }

    if library == "ak":
        return ak.zip(res)
    else:
        return res


def parse_tof_id(
    tof_id: Union[ak.Array, np.ndarray, int],
    flat: bool = False,
    library: Literal["ak", "np"] = "ak",
) -> Union[ak.Record, dict[str, np.ndarray], dict[str, np.int_]]:
    """
    Parse TOF ID.

    If `library` is `ak`, return `ak.Record`. If `library` is `np`, return `dict[str, np.ndarray]`.

    Available keys of the output:
        - part: The part ID. 0 for scintillator endcap0, 1 for scintillator barrel, 2 for scintillator endcap1, 3 for MRPC endcap0, 4 for MRPC endcap1.
        - layer_or_module: The scintillator layer or MRPC module ID, based on the part ID.
        - phi_or_strip: The scintillator phi or MRPC strip ID, based on the part ID.
        - end: The readout end ID.

    The return value is based on the part ID.
    Rows where `part < 3` are scintillator and `layer_or_module` represents layer ID, `phi_or_strip` represents phi ID.
    Rows where `part >= 3` are MRPC and `layer_or_module` represents module ID, `phi_or_strip` represents strip ID.

    Parameters:
        tof_id: The TOF ID.
        flat: Whether to flatten the output.
        library: The library to use as output.

    Returns:
        The parsed TOF ID.

    """
    if library not in ["ak", "np"]:
        raise ValueError(f"Unsupported library: {library}")

    if flat and isinstance(tof_id, ak.Array):
        tof_id = ak.flatten(tof_id)

    part = tof_id_to_part(tof_id)
    res = {
        "part": part,
        "layer_or_module": tof_id_to_layerOrModule(tof_id, part),
        "phi_or_strip": tof_id_to_phiOrStrip(tof_id, part),
        "end": tof_id_to_end(tof_id),
    }

    if library == "ak":
        return ak.zip(res)
    else:
        return res


def parse_emc_id(
    emc_id: Union[ak.Array, np.ndarray, int],
    flat: bool = False,
    library: Literal["ak", "np"] = "ak",
) -> Union[ak.Record, dict[str, np.ndarray], dict[str, np.int_]]:
    """
    Parse EMC ID.

    If `library` is `ak`, return `ak.Record`. If `library` is `np`, return `dict[str, np.ndarray]`.

    Available keys of the output:
        - module: The module ID.
        - theta: The theta ID.
        - phi: The phi ID.

    Parameters:
        emc_id: The EMC ID.
        flat: Whether to flatten the output.
        library: The library to use as output.

    Returns:
        The parsed EMC ID.

    """
    if library not in ["ak", "np"]:
        raise ValueError(f"Unsupported library: {library}")

    if flat and isinstance(emc_id, ak.Array):
        emc_id = ak.flatten(emc_id)

    res = {
        "module": emc_id_to_module(emc_id),
        "theta": emc_id_to_theta(emc_id),
        "phi": emc_id_to_phi(emc_id),
    }

    if library == "ak":
        return ak.zip(res)
    else:
        return res


def parse_muc_id(
    muc_id: Union[ak.Array, np.ndarray, int],
    flat: bool = False,
    library: Literal["ak", "np"] = "ak",
) -> Union[ak.Record, dict[str, np.ndarray], dict[str, np.int_]]:
    """
    Parse MUC ID.

    If `library` is `ak`, return `ak.Record`. If `library` is `np`, return `dict[str, np.ndarray]`.

    Available keys of the output:
        - part: The part ID.
        - segment: The segment ID.
        - layer: The layer ID.
        - channel: The channel ID.
        - gap: The gap ID, which is equivalent to layer ID.
        - strip: The strip ID, which is equivalent to channel ID.

    Parameters:
        muc_id: The MUC ID.
        flat: Whether to flatten the output.
        library: The library to use as output.

    Returns:
        The parsed MUC ID.
    """
    if library not in ["ak", "np"]:
        raise ValueError(f"Unsupported library: {library}")

    if flat and isinstance(muc_id, ak.Array):
        muc_id = ak.flatten(muc_id)

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

    if library == "ak":
        return ak.zip(res)
    else:
        return res


def parse_cgem_id(
    cgem_id: Union[ak.Array, np.ndarray, int],
    flat: bool = False,
    library: Literal["ak", "np"] = "ak",
) -> Union[ak.Record, dict[str, np.ndarray], dict[str, np.int_]]:
    """
    Parse CGEM ID.

    If `library` is `ak`, return `ak.Record`. If `library` is `np`, return `dict[str, np.ndarray]`.

    Available keys of the output:
        - layer: The layer ID.
        - sheet: The sheet ID.
        - strip: The strip ID.
        - is_x_strip: Whether the strip is an X-strip.

    Parameters:
        cgem_id: The CGEM ID.
        flat: Whether to flatten the output.
        library: The library to use as output.

    Returns:
        The parsed CGEM ID.
    """
    if library not in ["ak", "np"]:
        raise ValueError(f"Unsupported library: {library}")

    if flat and isinstance(cgem_id, ak.Array):
        cgem_id = ak.flatten(cgem_id)

    res = {
        "layer": cgem_id_to_layer(cgem_id),
        "sheet": cgem_id_to_sheet(cgem_id),
        "strip": cgem_id_to_strip(cgem_id),
        "is_x_strip": cgem_id_to_is_x_strip(cgem_id),
    }

    if library == "ak":
        return ak.zip(res)
    else:
        return res
