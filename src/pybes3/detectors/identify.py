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


def _regularize_uint32(
    val: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Make sure the value type is compatible to uint32.

    If `val` is `ak.Array` or `np.ndarray`, check whether its type is uint32.
    If `val` is an integer, transform it to np.uint32.

    Parameters:
        val: The value to be checked.

    Returns:
        The regularized value. If `val` is array, return itself. If `val` is integer, return itself as np.uint32.

    Raises:
        TypeError: If `val` is not an instance of `ak.Array`, `np.ndarray`, `int`, `np.signedinteger` and `np.unsignedinteger`.
    """
    if isinstance(val, ak.Array):
        type_str = val.typestr
        assert type_str.endswith("uint32"), "Array must be uint32 type."
        return val
    elif isinstance(val, np.ndarray):
        assert val.dtype == np.uint32, "Array must be uint32 type."
        return val
    else:
        if not isinstance(val, (int, np.signedinteger, np.unsignedinteger)):
            raise TypeError(f"Unsupport type: {type(val)}")

        assert (
            0 <= val <= 2**32 - 1
        ), f"uint32 value requires 0 <= value <= 2^32-1, but value = {val}"
        return np.uint32(val)


def regularize_args_uint32(func):
    """
    Decorator that applies `_regularize_uint32` on all arguments of a function.
    """

    def wrapper(*args, **kwargs):
        new_args = (_regularize_uint32(i) for i in args)
        new_kwargs = {k: _regularize_uint32(v) for k, v in kwargs.items()}
        return func(*new_args, **new_kwargs)

    return wrapper


###############################################################################
#                                     MDC                                     #
###############################################################################
@regularize_args_uint32
@nb.vectorize([nb.boolean(nb.uint32)])
def check_mdc_id(
    mdc_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.bool_]:
    """
    Check if the MDC ID is valid.

    Parameters:
        mdc_id: The MDC ID array or value.

    Returns:
        Whether the ID is valid.
    """
    return (mdc_id & DIGI_FLAG_MASK) >> DIGI_FLAG_OFFSET == DIGI_MDC_FLAG


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32)])
def mdc_id_to_wire(
    mdc_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert MDC ID to wire ID

    Parameters:
        mdc_id: MDC ID array or value.

    Returns:
        The wire ID.
    """
    return (mdc_id & DIGI_MDC_WIRE_MASK) >> DIGI_MDC_WIRE_OFFSET


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32)])
def mdc_id_to_layer(
    mdc_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert the MDC ID to the layer ID.

    Parameters:
        mdc_id: The MDC ID array or value.

    Returns:
        The layer ID.
    """
    return (mdc_id & DIGI_MDC_LAYER_MASK) >> DIGI_MDC_LAYER_OFFSET


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32)])
def mdc_id_to_wire_type(
    mdc_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert the MDC ID to the wire type.

    Parameters:
        mdc_id: The MDC ID array.

    Returns:
       The wire type.
    """
    return (mdc_id & DIGI_MDC_WIRETYPE_MASK) >> DIGI_MDC_WIRETYPE_OFFSET


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32, nb.uint32, nb.uint32)])
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
@regularize_args_uint32
@nb.vectorize([nb.boolean(nb.uint32)])
def check_tof_id(
    tof_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.bool_]:
    """
    Check if the TOF ID is valid.

    Parameters:
        tof_id: The TOF ID array or value.

    Returns:
        Whether the ID is valid.
    """
    return (tof_id & DIGI_FLAG_MASK) >> DIGI_FLAG_OFFSET == DIGI_TOF_FLAG


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32)])
def tof_id_to_part(
    tof_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert TOF ID to part ID

    Parameters:
        tof_id: TOF ID array or value.

    Returns:
        The part ID.
    """
    return (tof_id & DIGI_TOF_PART_MASK) >> DIGI_TOF_PART_OFFSET


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32)])
def tof_id_to_end(
    tof_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert the TOF ID to the readout end ID.

    Parameters:
        tof_id: The TOF ID array or value.

    Returns:
        The readout end ID.
    """
    return (tof_id & DIGI_TOF_END_MASK) >> DIGI_TOF_END_OFFSET


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32)])
def tof_id_to_scint_layer(
    tof_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert the TOF ID to the scintillator layer ID.

    Parameters:
        tof_id: The TOF ID array or value.

    Returns:
        The scintillator layer ID.
    """
    return (tof_id & DIGI_TOF_SCINT_LAYER_MASK) >> DIGI_TOF_SCINT_LAYER_OFFSET


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32)])
def tof_id_to_scint_phi(
    tof_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert the TOF ID to the scintillator phi ID.

    Parameters:
        tof_id: The TOF ID array or value.

    Returns:
        The scintillator phi ID.
    """
    return (tof_id & DIGI_TOF_SCINT_PHI_MASK) >> DIGI_TOF_SCINT_PHI_OFFSET


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32)])
def tof_id_to_mrpc_endcap(
    tof_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert the TOF ID to the MRPC endcap ID.

    Parameters:
        tof_id: The TOF ID array or value.

    Returns:
        The MRPC endcap ID.
    """
    return (tof_id & DIGI_TOF_MRPC_ENDCAP_MASK) >> DIGI_TOF_MRPC_ENDCAP_OFFSET


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32)])
def tof_id_to_mrpc_module(
    tof_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert the TOF ID to the MRPC module ID.

    Parameters:
        tof_id: The TOF ID array or value.

    Returns:
        The MRPC module ID.
    """
    return (tof_id & DIGI_TOF_MRPC_MODULE_MASK) >> DIGI_TOF_MRPC_MODULE_OFFSET


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32)])
def tof_id_to_mrpc_strip(
    tof_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert the TOF ID to the MRPC strip ID.

    Parameters:
        tof_id: The TOF ID array or value.

    Returns:
        The MRPC strip ID.
    """
    return (tof_id & DIGI_TOF_MRPC_STRIP_MASK) >> DIGI_TOF_MRPC_STRIP_OFFSET


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32, nb.uint32, nb.uint32, nb.uint32)])
def get_tof_scint_id(
    part: Union[ak.Array, np.ndarray, int],
    layer: Union[ak.Array, np.ndarray, int],
    phi: Union[ak.Array, np.ndarray, int],
    end: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Generate TOF scintillator ID based on the part ID, layer ID, phi ID, and readout end ID.

    Parameters:
        part: The part ID.
        layer: The layer ID.
        phi: The phi ID.
        end: The readout end ID.

    Returns:
        The TOF scintillator ID.
    """
    return (
        ((part << DIGI_TOF_PART_OFFSET) & DIGI_TOF_PART_MASK)
        | ((layer << DIGI_TOF_SCINT_LAYER_OFFSET) & DIGI_TOF_SCINT_LAYER_MASK)
        | ((phi << DIGI_TOF_SCINT_PHI_OFFSET) & DIGI_TOF_SCINT_PHI_MASK)
        | ((end << DIGI_TOF_END_OFFSET) & DIGI_TOF_END_MASK)
        | (DIGI_TOF_FLAG << DIGI_FLAG_OFFSET)
    )


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32, nb.uint32, nb.uint32, nb.uint32)])
def get_tof_mrpc_id(
    endcap: Union[ak.Array, np.ndarray, int],
    module: Union[ak.Array, np.ndarray, int],
    strip: Union[ak.Array, np.ndarray, int],
    end: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Generate TOF MRPC ID based on the endcap ID, module ID, strip ID, and readout end ID.

    Parameters:
        endcap: The endcap ID.
        module: The module ID.
        strip: The strip ID.
        end: The readout end ID.

    Returns:
        The TOF MRPC ID.
    """
    return (
        ((np.uint32(3) << DIGI_TOF_PART_OFFSET) & DIGI_TOF_PART_MASK)
        | ((endcap << DIGI_TOF_MRPC_ENDCAP_OFFSET) & DIGI_TOF_MRPC_ENDCAP_MASK)
        | ((module << DIGI_TOF_MRPC_MODULE_OFFSET) & DIGI_TOF_MRPC_MODULE_MASK)
        | ((strip << DIGI_TOF_MRPC_STRIP_OFFSET) & DIGI_TOF_MRPC_STRIP_MASK)
        | ((end << DIGI_TOF_END_OFFSET) & DIGI_TOF_END_MASK)
        | (DIGI_TOF_FLAG << DIGI_FLAG_OFFSET)
    )


###############################################################################
#                                     EMC                                     #
###############################################################################
@regularize_args_uint32
@nb.vectorize([nb.boolean(nb.uint32)])
def check_emc_id(
    emc_id: Union[ak.Array, np.ndarray, np.uint32]
) -> Union[ak.Array, np.ndarray, np.bool_]:
    """
    Check if the EMC ID is valid.

    Parameters:
        emc_id: The EMC ID array or value.

    Returns:
        Whether the ID is valid.
    """
    return (emc_id & DIGI_FLAG_MASK) >> DIGI_FLAG_OFFSET == DIGI_EMC_FLAG


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32)])
def emc_id_to_module(
    emc_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert EMC ID to module ID

    Parameters:
        emc_id: EMC ID array or value.

    Returns:
        The module ID.
    """
    return (emc_id & DIGI_EMC_MODULE_MASK) >> DIGI_EMC_MODULE_OFFSET


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32)])
def emc_id_to_theta(
    emc_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert the EMC ID to the theta ID.

    Parameters:
        emc_id: The EMC ID array or value.

    Returns:
        The theta ID.
    """
    return (emc_id & DIGI_EMC_THETA_MASK) >> DIGI_EMC_THETA_OFFSET


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32)])
def emc_id_to_phi(
    emc_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert the EMC ID to the phi ID.

    Parameters:
        emc_id: The EMC ID array or value.

    Returns:
        The phi ID.
    """
    return (emc_id & DIGI_EMC_PHI_MASK) >> DIGI_EMC_PHI_OFFSET


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32, nb.uint32, nb.uint32)])
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
@regularize_args_uint32
@nb.vectorize([nb.boolean(nb.uint32)])
def check_muc_id(
    muc_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.bool_]:
    """
    Check if the MUC ID is valid.

    Parameters:
        muc_id: The MUC ID array or value.

    Returns:
        Whether the ID is valid.
    """
    return (muc_id & DIGI_FLAG_MASK) >> DIGI_FLAG_OFFSET == DIGI_MUC_FLAG


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32)])
def muc_id_to_part(
    muc_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert MUC ID to part ID

    Parameters:
        muc_id: MUC ID array or value.

    Returns:
        The part ID.
    """
    return (muc_id & DIGI_MUC_PART_MASK) >> DIGI_MUC_PART_OFFSET


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32)])
def muc_id_to_segment(
    muc_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert the MUC ID to the segment ID.

    Parameters:
        muc_id: The MUC ID array or value.

    Returns:
        The segment ID.
    """
    return (muc_id & DIGI_MUC_SEGMENT_MASK) >> DIGI_MUC_SEGMENT_OFFSET


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32)])
def muc_id_to_layer(
    muc_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert the MUC ID to the layer ID.

    Parameters:
        muc_id: The MUC ID array or value.

    Returns:
        The layer ID.
    """
    return (muc_id & DIGI_MUC_LAYER_MASK) >> DIGI_MUC_LAYER_OFFSET


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32)])
def muc_id_to_channel(
    muc_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert the MUC ID to the channel ID.

    Parameters:
        muc_id: The MUC ID array or value.

    Returns:
        The channel ID.
    """
    return (muc_id & DIGI_MUC_CHANNEL_MASK) >> DIGI_MUC_CHANNEL_OFFSET


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32, nb.uint32, nb.uint32, nb.uint32)])
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
    muc_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert the MUC ID to the gap ID, which is equivalent to layer ID.

    Parameters:
        muc_id: The MUC ID array or value.

    Returns:
        The gap ID.
    """
    return muc_id_to_layer(muc_id)


def muc_id_to_strip(
    muc_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
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
@regularize_args_uint32
@nb.vectorize([nb.boolean(nb.uint32)])
def check_cgem_id(
    cgem_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.bool_]:
    """
    Check if the CGEM ID is valid.

    Parameters:
        cgem_id: The CGEM ID array or value.

    Returns:
        Whether the ID is valid.
    """
    return (cgem_id & DIGI_FLAG_MASK) >> DIGI_FLAG_OFFSET == DIGI_CGEM_FLAG


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32)])
def cgem_id_to_strip(
    cgem_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert CGEM ID to strip ID

    Parameters:
        cgem_id: CGEM ID array or value.

    Returns:
        The strip ID.
    """
    return (cgem_id & DIGI_CGEM_STRIP_MASK) >> DIGI_CGEM_STRIP_OFFSET


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32)])
def cgem_id_to_strip_type(
    cgem_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert the CGEM ID to the strip type.

    Parameters:
        cgem_id: The CGEM ID array or value.

    Returns:
        The strip type.
    """
    return (cgem_id & DIGI_CGEM_STRIPTYPE_MASK) >> DIGI_CGEM_STRIPTYPE_OFFSET


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32)])
def cgem_id_to_sheet(
    cgem_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert the CGEM ID to the sheet ID.

    Parameters:
        cgem_id: The CGEM ID array or value.

    Returns:
        The sheet ID.
    """
    return (cgem_id & DIGI_CGEM_SHEET_MASK) >> DIGI_CGEM_SHEET_OFFSET


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32)])
def cgem_id_to_layer(
    cgem_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Convert the CGEM ID to the layer ID.

    Parameters:
        cgem_id: The CGEM ID array or value.

    Returns:
        The layer ID.
    """
    return (cgem_id & DIGI_CGEM_LAYER_MASK) >> DIGI_CGEM_LAYER_OFFSET


@regularize_args_uint32
@nb.vectorize([nb.bool(nb.uint32)])
def cgem_id_to_isxstrip(
    cgem_id: Union[ak.Array, np.ndarray, int]
) -> Union[ak.Array, np.ndarray, np.bool_]:
    """
    Convert the CGEM ID to whether it is an X-strip.

    Parameters:
        cgem_id: The CGEM ID array or value.

    Returns:
        Whether the strip is an X-strip.
    """
    return (
        (cgem_id & DIGI_CGEM_STRIPTYPE_MASK) >> DIGI_CGEM_STRIPTYPE_OFFSET
    ) == DIGI_CGEM_XSTRIP


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32, nb.uint32, nb.uint32, nb.uint32)])
def get_cgem_id(
    strip: Union[ak.Array, np.ndarray, int],
    striptype: Union[ak.Array, np.ndarray, int],
    sheet: Union[ak.Array, np.ndarray, int],
    layer: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, np.uint32]:
    """
    Generate CGEM ID based on the strip ID, strip type, sheet ID, and layer ID.

    Parameters:
        strip: The strip ID.
        striptype: The strip type. 0 for X-strip, 1 for V-strip.
        sheet: The sheet ID.
        layer: The layer ID.

    Returns:
        The CGEM ID.
    """
    return (
        ((strip << DIGI_CGEM_STRIP_OFFSET) & DIGI_CGEM_STRIP_MASK)
        | ((striptype << DIGI_CGEM_STRIPTYPE_OFFSET) & DIGI_CGEM_STRIPTYPE_MASK)
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
) -> Union[ak.Record, dict[str, np.ndarray], dict[str, np.uint32]]:
    """
    Parse MDC ID.

    Parameters:
        mdc_id: The MDC ID.
        flat: Whether to flatten the output.
        library: The library to use as output.

    Returns:
        The parsed MDC ID. If `library` is `ak`, return `ak.Record`.
        If `library` is `np`, return `dict[str, np.ndarray]`.

        Available keys of the output are:
            - wire: The wire ID.
            - layer: The layer ID.
            - wire_type: The wire type
    """
    if library not in ["ak", "np"]:
        raise ValueError(f"Unsupported library: {library}")

    if flat and isinstance(mdc_id, ak.Array):
        mdc_id = ak.flatten(mdc_id)

    res = {
        "wire": mdc_id_to_wire(mdc_id),
        "layer": mdc_id_to_layer(mdc_id),
        "wire_type": mdc_id_to_wire_type(mdc_id),
    }

    if library == "ak":
        return ak.zip(res)
    else:
        return res


def parse_tof_id(
    tof_id: Union[ak.Array, np.ndarray, int],
    flat: bool = False,
    library: Literal["ak", "np"] = "ak",
) -> Union[ak.Record, dict[str, np.ndarray], dict[str, np.uint32]]:
    """
    Parse TOF ID.

    Parameters:
        tof_id: The TOF ID.
        flat: Whether to flatten the output.
        library: The library to use as output.

    Returns:
        The parsed TOF ID.
        If `library` is `ak`, return `ak.Record`. If `library` is `np`, return `dict[str, np.ndarray]`.
        Available keys of the output are:
            - part: The part ID.
            - end: The readout end ID.
            - scint_layer: The scintillator layer ID.
            - scint_phi: The scintillator phi ID.
            - mrpc_endcap: The MRPC endcap ID.
            - mrpc_module: The MRPC module ID.
            - mrpc_strip: The MRPC strip ID.
            - is_mrpc: Whether the TOF ID is MRPC ID.

        Note that no matter an ID is MRPC or not, it will always have both scintillator and MRPC keys.
    """
    if library not in ["ak", "np"]:
        raise ValueError(f"Unsupported library: {library}")

    if flat and isinstance(tof_id, ak.Array):
        tof_id = ak.flatten(tof_id)

    res = {
        "part": tof_id_to_part(tof_id),
        "end": tof_id_to_end(tof_id),
        "scint_layer": tof_id_to_scint_layer(tof_id),
        "scint_phi": tof_id_to_scint_phi(tof_id),
        "mrpc_endcap": tof_id_to_mrpc_endcap(tof_id),
        "mrpc_module": tof_id_to_mrpc_module(tof_id),
        "mrpc_strip": tof_id_to_mrpc_strip(tof_id),
    }

    res["is_mrpc"] = res["part"] == 3

    if library == "ak":
        return ak.zip(res)
    else:
        return res


def parse_emc_id(
    emc_id: Union[ak.Array, np.ndarray, int],
    flat: bool = False,
    library: Literal["ak", "np"] = "ak",
) -> Union[ak.Record, dict[str, np.ndarray], dict[str, np.uint32]]:
    """
    Parse EMC ID.

    Parameters:
        emc_id: The EMC ID.
        flat: Whether to flatten the output.
        library: The library to use as output.

    Returns:
        The parsed EMC ID.
        If `library` is `ak`, return `ak.Record`. If `library` is `np`, return `dict[str, np.ndarray]`.
        Available keys of the output are:
            - module: The module ID.
            - theta: The theta ID.
            - phi: The phi ID.
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
) -> Union[ak.Record, dict[str, np.ndarray], dict[str, np.uint32]]:
    """
    Parse MUC ID.

    Parameters:
        muc_id: The MUC ID.
        flat: Whether to flatten the output.
        library: The library to use as output.

    Returns:
        The parsed MUC ID.
        If `library` is `ak`, return `ak.Record`. If `library` is `np`, return `dict[str, np.ndarray]`.
        Available keys of the output are:
            - part: The part ID.
            - segment: The segment ID.
            - layer: The layer ID.
            - channel: The channel ID.
            - gap: The gap ID, which is equivalent to layer ID.
            - strip: The strip ID, which is equivalent to channel ID.
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
) -> Union[ak.Record, dict[str, np.ndarray], dict[str, np.uint32]]:
    """
    Parse CGEM ID.

    Parameters:
        cgem_id: The CGEM ID.
        flat: Whether to flatten the output.
        library: The library to use as output.

    Returns:
        The parsed CGEM ID.
        If `library` is `ak`, return `ak.Record`. If `library` is `np`, return `dict[str, np.ndarray]`.
        Available keys of the output are:
            - strip: The strip ID.
            - strip_type: The strip type.
            - sheet: The sheet ID.
            - layer: The layer ID.
            - is_xstrip: Whether the strip is an X-strip.
    """
    if library not in ["ak", "np"]:
        raise ValueError(f"Unsupported library: {library}")

    if flat and isinstance(cgem_id, ak.Array):
        cgem_id = ak.flatten(cgem_id)

    res = {
        "strip": cgem_id_to_strip(cgem_id),
        "strip_type": cgem_id_to_strip_type(cgem_id),
        "sheet": cgem_id_to_sheet(cgem_id),
        "layer": cgem_id_to_layer(cgem_id),
        "is_xstrip": cgem_id_to_isxstrip(cgem_id),
    }

    if library == "ak":
        return ak.zip(res)
    else:
        return res
