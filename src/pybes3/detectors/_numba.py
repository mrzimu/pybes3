import numba as nb
import numpy as np

from .constants import MdcDigiConst, EmcDigiConst


# MDC digi
@nb.njit
def _parse_mdc_id(
    mdc_id: np.ndarray, check_valid: bool = True
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Parse the MDC ID into wire ID, layer ID, and wire type.

    Parameters:
        mdc_id (np.ndarray): The MDC ID array.
        check_valid (bool, optional): Whether to check the validity of the MDC ID. Defaults to True.

    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray]: A tuple containing the wire ID, layer ID, and wire type arrays.
    """

    if check_valid:
        assert np.all(
            (mdc_id & MdcDigiConst.DIGI_MASK) >> MdcDigiConst.DIGI_OFFSET
            == MdcDigiConst.DIGI_FLAG
        )

    wire_id = (mdc_id & MdcDigiConst.WIRE_MASK) >> MdcDigiConst.WIRE_OFFSET
    layer_id = (mdc_id & MdcDigiConst.LAYER_MASK) >> MdcDigiConst.LAYER_OFFSET
    wire_type = (mdc_id & MdcDigiConst.WIRETYPE_MASK) >> MdcDigiConst.WIRETYPE_OFFSET

    return wire_id, layer_id, wire_type


@nb.njit
def _gen_mdc_id(
    wire_id: np.ndarray, layer_id: np.ndarray, wire_type: np.ndarray
) -> np.ndarray:
    """
    Generate the MDC ID based on the wire ID, layer ID, and wire type.

    Parameters:
    wire_id (np.ndarray): Array of wire IDs.
    layer_id (np.ndarray): Array of layer IDs.
    wire_type (np.ndarray): Array of wire types.

    Returns:
    np.ndarray: Array of MDC IDs.

    """

    mdc_id = (
        (wire_id << MdcDigiConst.WIRE_OFFSET)
        | (layer_id << MdcDigiConst.LAYER_OFFSET)
        | (wire_type << MdcDigiConst.WIRETYPE_OFFSET)
        | MdcDigiConst.DIGI_FLAG
    )

    return mdc_id


@nb.njit
def _parse_emc_id(emc_id: np.ndarray, check_valid: bool = True) -> tuple[np.ndarray]:
    """
    Parse the EMC ID into module ID, theta ID, and phi ID.

    Parameters:
        emc_id (np.ndarray): The EMC ID array.
        check_valid (bool, optional): Whether to check the validity of the EMC ID. Defaults to True.

    Returns:
        tuple[np.ndarray]: A tuple containing the module ID, theta ID, and phi ID arrays.
    """

    if check_valid:
        assert np.all(
            (emc_id & EmcDigiConst.DIGI_MASK) >> EmcDigiConst.DIGI_OFFSET
            == EmcDigiConst.DIGI_FLAG
        )

    module_id = (emc_id & EmcDigiConst.MODULE_MASK) >> EmcDigiConst.MODULE_OFFSET
    theta_id = (emc_id & EmcDigiConst.THETA_MASK) >> EmcDigiConst.THETA_OFFSET
    phi_id = (emc_id & EmcDigiConst.PHI_MASK) >> EmcDigiConst.PHI_OFFSET

    return module_id, theta_id, phi_id
