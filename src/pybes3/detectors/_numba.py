import numba as nb

from . import constants as det_consts


@nb.vectorize([nb.boolean(nb.uint32)])
def check_mdc_teid(mdc_id: int) -> bool:
    """
    Check if the MDC TEID is valid.

    Parameters:
        mdc_id (int): The MDC TEID array.

    Returns:
        bool: Whether the ID is valid.
    """
    return (
        mdc_id & det_consts.DIGI_FLAG_MASK
    ) >> det_consts.DIGI_FLAG_OFFSET == det_consts.DIGI_MDC_FLAG


@nb.vectorize([nb.uint32(nb.uint32)])
def mdc_teid_to_wire(mdc_id: int) -> int:
    """
    Convert the MDC TEID to the wire ID.

    Parameters:
        mdc_id (int): The MDC TEID array.

    Returns:
        int: The wire ID.
    """
    return (mdc_id & det_consts.DIGI_MDC_WIRE_MASK) >> det_consts.DIGI_MDC_WIRE_OFFSET


@nb.vectorize([nb.uint32(nb.uint32)])
def mdc_teid_to_layer(mdc_id: int) -> int:
    """
    Convert the MDC TEID to the layer ID.

    Parameters:
        mdc_id (int): The MDC TEID array.

    Returns:
        int: The layer ID.
    """
    return (mdc_id & det_consts.DIGI_MDC_LAYER_MASK) >> det_consts.DIGI_MDC_LAYER_OFFSET


@nb.vectorize([nb.uint32(nb.uint32)])
def mdc_teid_to_wire_type(mdc_id: int) -> int:
    """
    Convert the MDC TEID to the wire type.

    Parameters:
        mdc_id (int): The MDC TEID array.

    Returns:
        int: The wire type.
    """
    return (mdc_id & det_consts.DIGI_MDC_WIRETYPE_MASK) >> det_consts.DIGI_MDC_WIRETYPE_OFFSET


@nb.vectorize([nb.uint32(nb.uint32, nb.uint32, nb.uint32)])
def gen_mdc_teid(wire: int, layer: int, wire_type: int) -> int:
    """
    Generate the MDC TEID based on the wire ID, layer ID, and wire type.

    Parameters:
        wire (int): The wire ID.
        layer (int): The layer ID.
        wire_type (int): The wire type.

    Returns:
        int: The MDC TEID.
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


@nb.vectorize([nb.uint32(nb.uint32)])
def check_emc_teid(emc_id: int) -> bool:
    """
    Check if the EMC TEID is valid.

    Parameters:
        emc_id (int): The EMC TEID array.

    Returns:
        bool: Whether the ID is valid.
    """
    return (
        emc_id & det_consts.DIGI_FLAG_MASK
    ) >> det_consts.DIGI_FLAG_OFFSET == det_consts.DIGI_EMC_FLAG


@nb.vectorize([nb.uint32(nb.uint32)])
def emc_teid_to_module(emc_id: int) -> int:
    """
    Convert the EMC TEID to the module ID.

    Parameters:
        emc_id (int): The EMC TEID array.

    Returns:
        int: The module ID.
    """
    return (emc_id & det_consts.DIGI_EMC_MODULE_MASK) >> det_consts.DIGI_EMC_MODULE_OFFSET


@nb.vectorize([nb.uint32(nb.uint32)])
def emc_teid_to_theta(emc_id: int) -> int:
    """
    Convert the EMC TEID to the theta ID.

    Parameters:
        emc_id (int): The EMC TEID array.

    Returns:
        int: The theta ID.
    """
    return (emc_id & det_consts.DIGI_EMC_THETA_MASK) >> det_consts.DIGI_EMC_THETA_OFFSET


@nb.vectorize([nb.uint32(nb.uint32)])
def emc_teid_to_phi(emc_id: int) -> int:
    """
    Convert the EMC TEID to the phi ID.

    Parameters:
        emc_id (int): The EMC TEID array.

    Returns:
        int: The phi ID.
    """
    return (emc_id & det_consts.DIGI_EMC_PHI_MASK) >> det_consts.DIGI_EMC_PHI_OFFSET


@nb.vectorize([nb.uint32(nb.uint32, nb.uint32, nb.uint32)])
def gen_emc_teid(module_id: int, theta_id: int, phi_id: int) -> int:
    """
    Generate the EMC TEID based on the module ID, theta ID, and phi ID.

    Parameters:
        module_id (int): The module ID.
        theta_id (int): The theta ID.
        phi_id (int): The phi ID.

    Returns:
        int: The EMC TEID.
    """
    return (
        ((module_id << det_consts.DIGI_EMC_MODULE_OFFSET) & det_consts.DIGI_EMC_MODULE_MASK)
        | ((theta_id << det_consts.DIGI_EMC_THETA_OFFSET) & det_consts.DIGI_EMC_THETA_MASK)
        | ((phi_id << det_consts.DIGI_EMC_PHI_OFFSET) & det_consts.DIGI_EMC_PHI_MASK)
        | (det_consts.DIGI_EMC_FLAG << det_consts.DIGI_FLAG_OFFSET)
    )
