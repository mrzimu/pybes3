import numba as nb
import numpy as np

from . import constants as det_consts


@nb.vectorize([nb.uint32(nb.uint32, nb.uint32, nb.uint32)])
def gen_mdc_teid(wire: int, layer: int, wire_type: int) -> int:
    """
    Generate the MDC TEID based on the wire ID, layer ID, and wire type.

    Parameters:
        wire (int): The wire ID.
        layer (int): The layer ID.
        wire_type (int): The wire type.

    Returns:
        The MDC TEID.
    """
    return (
        ((wire << det_consts.DIGI_MDC_WIRE_OFFSET) & det_consts.DIGI_MDC_WIRE_MASK)
        | ((layer << det_consts.DIGI_MDC_LAYER_OFFSET) & det_consts.DIGI_MDC_LAYER_MASK)
        | (
            (wire_type << det_consts.DIGI_MDC_WIRETYPE_OFFSET)
            & det_consts.DIGI_MDC_WIRETYPE_MASK
        )
        | (det_consts.DIGI_MDC_FLAG << det_consts.DIGI_FLAG_OFFSET)
    )


@nb.vectorize([nb.uint32(nb.uint32, nb.uint32, nb.uint32)])
def gen_emc_teid(module_id: int, theta_id: int, phi_id: int) -> int:
    """
    Generate the EMC TEID based on the module ID, theta ID, and phi ID.

    Parameters:
        module_id (int): The module ID.
        theta_id (int): The theta ID.
        phi_id (int): The phi ID.

    Returns:
        The EMC TEID.
    """
    return (
        ((module_id << det_consts.DIGI_EMC_MODULE_OFFSET) & det_consts.DIGI_EMC_MODULE_MASK)
        | ((theta_id << det_consts.DIGI_EMC_THETA_OFFSET) & det_consts.DIGI_EMC_THETA_MASK)
        | ((phi_id << det_consts.DIGI_EMC_PHI_OFFSET) & det_consts.DIGI_EMC_PHI_MASK)
        | (det_consts.DIGI_EMC_FLAG << det_consts.DIGI_FLAG_OFFSET)
    )


@nb.vectorize([nb.uint32(nb.uint32, nb.uint32, nb.uint32, nb.uint32)])
def gen_tof_scint_teid(part: int, layer: int, phi: int, end: int):

    return (
        ((part << det_consts.DIGI_TOF_PART_OFFSET) & det_consts.DIGI_TOF_PART_MASK)
        | (
            (layer << det_consts.DIGI_TOF_SCINT_LAYER_OFFSET)
            & det_consts.DIGI_TOF_SCINT_LAYER_MASK
        )
        | ((phi << det_consts.DIGI_TOF_SCINT_PHI_OFFSET) & det_consts.DIGI_TOF_SCINT_PHI_MASK)
        | ((end << det_consts.DIGI_TOF_END_OFFSET) & det_consts.DIGI_TOF_END_MASK)
        | (det_consts.DIGI_TOF_FLAG << det_consts.DIGI_FLAG_OFFSET)
    )


@nb.vectorize([nb.uint32(nb.uint32, nb.uint32, nb.uint32, nb.uint32)])
def gen_tof_mrpc_teid(endcap: int, module: int, strip: int, end: int):
    return (
        ((np.uint32(3) << det_consts.DIGI_TOF_PART_OFFSET) & det_consts.DIGI_TOF_PART_MASK)
        | (
            (endcap << det_consts.DIGI_TOF_MRPC_ENDCAP_OFFSET)
            & det_consts.DIGI_TOF_MRPC_ENDCAP_MASK
        )
        | (
            (module << det_consts.DIGI_TOF_MRPC_MODULE_OFFSET)
            & det_consts.DIGI_TOF_MRPC_MODULE_MASK
        )
        | (
            (strip << det_consts.DIGI_TOF_MRPC_STRIP_OFFSET)
            & det_consts.DIGI_TOF_MRPC_STRIP_MASK
        )
        | ((end << det_consts.DIGI_TOF_END_OFFSET) & det_consts.DIGI_TOF_END_MASK)
        | (det_consts.DIGI_TOF_FLAG << det_consts.DIGI_FLAG_OFFSET)
    )
