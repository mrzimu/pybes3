from typing import Union, overload

import awkward as ak
import numpy as np

from . import _numba as _det_nb


################################################################################
#                                parse_mdc_teid                                #
################################################################################
@overload
def parse_mdc_teid(mdc_id: ak.Array) -> ak.Array:
    """
    Parse the MDC TEID into the wire, layer, and wiretype.

    Parameters:
        mdc_id (ak.Array): The MDC TEID array.

    Returns:
        ak.Array: The parsed wire, layer, and wiretype.
    """


@overload
def parse_mdc_teid(mdc_id: np.ndarray) -> tuple:
    """
    Parse the MDC TEID into the wire, layer, and wiretype.

    Parameters:
        mdc_id (np.ndarray): The MDC TEID array.

    Returns:
        tuple: The parsed wire, layer, and wiretype.
    """


@overload
def parse_mdc_teid(mdc_id: int) -> tuple:
    """
    Parse the MDC TEID into the wire, layer, and wiretype.

    Parameters:
        mdc_id (int): The MDC TEID array.

    Returns:
        tuple: The parsed wire, layer, and wiretype.
    """


def parse_mdc_teid(mdc_id: Union[ak.Array, np.ndarray, int]) -> Union[ak.Array, tuple]:
    """
    Parse the MDC TEID into the wire, layer, and wiretype.

    Parameters:
        mdc_id (Union[ak.Array, np.ndarray, int]): The MDC TEID array.

    Returns:
        Union[ak.Array, tuple]: The parsed wire, layer, and wiretype.
    """
    is_valid = (
        _det_nb.check_mdc_teid(mdc_id)
        if isinstance(mdc_id, (ak.Array, np.ndarray))
        else _det_nb.check_mdc_teid(np.uint32(mdc_id))
    )

    # np.all can handle int case
    if (isinstance(mdc_id, ak.Array) and not ak.all(is_valid)) or (not np.all(is_valid)):
        raise ValueError("MDC ID is invalid.")

    if isinstance(mdc_id, (ak.Array, np.ndarray)):
        wire = _det_nb.mdc_teid_to_wire(mdc_id)
        layer = _det_nb.mdc_teid_to_layer(mdc_id)
        wire_type = _det_nb.mdc_teid_to_wire_type(mdc_id)

        if isinstance(mdc_id, ak.Array):
            return ak.zip({"wire": wire, "layer": layer, "wire_type": wire_type})
        else:
            return (wire, layer, wire_type)
    else:
        tmp_wire, tmp_layer, tmp_wire_type = (
            _det_nb.mdc_teid_to_wire(np.uint32(mdc_id)),
            _det_nb.mdc_teid_to_layer(np.uint32(mdc_id)),
            _det_nb.mdc_teid_to_wire_type(np.uint32(mdc_id)),
        )
        input_type = type(mdc_id)
        return (input_type(tmp_wire), input_type(tmp_layer), input_type(tmp_wire_type))


################################################################################
#                                 get_mdc_teid                                 #
################################################################################
@overload
def get_mdc_teid(data: ak.Array) -> ak.Array:
    """
    Get the MDC TEID from the wire, layer, and wiretype.

    Parameters:
        data (ak.Array): The wire, layer, and wiretype.

    Returns:
        ak.Array: The MDC TEID.
    """


@overload
def get_mdc_teid(wire: ak.Array, layer: ak.Array, wire_type: ak.Array) -> ak.Array:
    """
    Get the MDC TEID from the wire, layer, and wiretype.

    Parameters:
        wire (ak.Array): The wire ID.
        layer (ak.Array): The layer ID.
        wire_type (ak.Array): The wire type.

    Returns:
        ak.Array: The MDC TEID.
    """


@overload
def get_mdc_teid(wire: np.ndarray, layer: np.ndarray, wire_type: np.ndarray) -> np.ndarray:
    """
    Get the MDC TEID from the wire, layer, and wiretype.

    Parameters:
        wire (np.ndarray): The wire ID.
        layer (np.ndarray): The layer ID.
        wire_type (np.ndarray): The wire type.

    Returns:
        np.ndarray: The MDC TEID.
    """


@overload
def get_mdc_teid(wire: int, layer: int, wire_type: int) -> int:
    """
    Get the MDC TEID from the wire, layer, and wiretype.

    Parameters:
        wire (int): The wire ID.
        layer (int): The layer ID.
        wire_type (int): The wire type.

    Returns:
        int: The MDC TEID.
    """


def get_mdc_teid(
    wire_or_akzipped: Union[np.ndarray, int, ak.Array],
    layer: Union[np.ndarray, int, ak.Array, None] = None,
    wire_type: Union[np.ndarray, int, ak.Array, None] = None,
) -> Union[np.ndarray, int, ak.Array]:
    """
    Get the MDC TEID from the wire, layer, and wiretype.

    Parameters:
        wire (Union[np.ndarray, int, ak.Array]): The wire ID.
        layer (Union[np.ndarray, int, ak.Array]): The layer ID.
        wire_type (Union[np.ndarray, int, ak.Array]): The wire type.

    Returns:
        Union[np.ndarray, int, ak.Array]: The MDC TEID.
    """
    # if layer and wire_type are None, then wire is an ak.Array
    if getattr(wire_or_akzipped, "fields", None) == ["wire", "layer", "wire_type"]:
        return _det_nb.gen_mdc_teid(
            wire_or_akzipped.wire, wire_or_akzipped.layer, wire_or_akzipped.wire_type
        )

    assert (
        type(wire_or_akzipped) == type(layer) == type(wire_type)
    ), "All inputs must be of the same type."

    if not isinstance(wire_or_akzipped, (ak.Array, np.ndarray)):
        res = _det_nb.gen_mdc_teid(
            np.uint32(wire_or_akzipped), np.uint32(layer), np.uint32(wire_type)
        )
        return type(wire_or_akzipped)(res)

    return _det_nb.gen_mdc_teid(wire_or_akzipped, layer, wire_type)


################################################################################
#                                parse_emc_teid                                #
################################################################################
@overload
def parse_emc_teid(emc_id: ak.Array) -> ak.Array:
    """
    Parse the EMC TEID into the module, theta, and phi.

    Parameters:
        emc_id (ak.Array): The EMC TEID array.

    Returns:
        ak.Array: The parsed module, theta, and phi.
    """


@overload
def parse_emc_teid(emc_id: np.ndarray) -> tuple:
    """
    Parse the EMC TEID into the module, theta, and phi.

    Parameters:
        emc_id (np.ndarray): The EMC TEID array.

    Returns:
        tuple: The parsed module, theta, and phi.
    """


@overload
def parse_emc_teid(emc_id: int) -> tuple:
    """
    Parse the EMC TEID into the module, theta, and phi.

    Parameters:
        emc_id (int): The EMC TEID array.

    Returns:
        tuple: The parsed module, theta, and phi.
    """


def parse_emc_teid(emc_id: Union[ak.Array, np.ndarray, int]) -> Union[ak.Array, tuple]:
    """
    Parse the EMC TEID into the module, theta, and phi.

    Parameters:
        emc_id (Union[ak.Array, np.ndarray, int]): The EMC TEID array.

    Returns:
        Union[ak.Array, tuple]: The parsed module, theta, and phi.
    """
    is_valid = (
        _det_nb.check_emc_teid(emc_id)
        if isinstance(emc_id, (ak.Array, np.ndarray))
        else _det_nb.check_emc_teid(np.uint32(emc_id))
    )

    if (isinstance(emc_id, ak.Array) and not ak.all(is_valid)) or (not np.all(is_valid)):
        raise ValueError("EMC ID is invalid.")

    if isinstance(emc_id, (ak.Array, np.ndarray)):
        module = _det_nb.emc_teid_to_module(emc_id)
        theta = _det_nb.emc_teid_to_theta(emc_id)
        phi = _det_nb.emc_teid_to_phi(emc_id)

        if isinstance(emc_id, ak.Array):
            return ak.zip({"module": module, "theta": theta, "phi": phi})
        else:
            return (module, theta, phi)

    else:
        tmp_module, tmp_theta, tmp_phi = (
            _det_nb.emc_teid_to_module(np.uint32(emc_id)),
            _det_nb.emc_teid_to_theta(np.uint32(emc_id)),
            _det_nb.emc_teid_to_phi(np.uint32(emc_id)),
        )
        input_type = type(emc_id)
        return (input_type(tmp_module), input_type(tmp_theta), input_type(tmp_phi))


################################################################################
#                                parse_emc_teid                                #
################################################################################
@overload
def get_emc_teid(data: ak.Array) -> ak.Array:
    """
    Get the EMC TEID from the module, theta, and phi.

    Parameters:
        data (ak.Array): The module, theta, and phi.

    Returns:
        ak.Array: The EMC TEID.
    """


@overload
def get_emc_teid(module: ak.Array, theta: ak.Array, phi: ak.Array) -> ak.Array:
    """
    Get the EMC TEID from the module, theta, and phi.

    Parameters:
        module (ak.Array): The module ID.
        theta (ak.Array): The theta ID.
        phi (ak.Array): The phi ID.

    Returns:
        ak.Array: The EMC TEID.
    """


@overload
def get_emc_teid(module: np.ndarray, theta: np.ndarray, phi: np.ndarray) -> np.ndarray:
    """
    Get the EMC TEID from the module, theta, and phi.

    Parameters:
        module (np.ndarray): The module ID.
        theta (np.ndarray): The theta ID.
        phi (np.ndarray): The phi ID.

    Returns:
        np.ndarray: The EMC TEID.
    """


@overload
def get_emc_teid(module: int, theta: int, phi: int) -> int:
    """
    Get the EMC TEID from the module, theta, and phi.

    Parameters:
        module (int): The module ID.
        theta (int): The theta ID.
        phi (int): The phi ID.

    Returns:
        int: The EMC TEID.
    """


def get_emc_teid(
    module_or_akzipped: Union[ak.Array, np.ndarray, int],
    theta: Union[ak.Array, np.ndarray, int, None] = None,
    phi: Union[ak.Array, np.ndarray, int, None] = None,
) -> Union[ak.Array, np.ndarray, int]:
    """
    Get the EMC TEID from the module, theta, and phi.

    Parameters:
        module (Union[ak.Array, np.ndarray, int]): The module ID.
        theta (Union[ak.Array, np.ndarray, int]): The theta ID.
        phi (Union[ak.Array, np.ndarray, int]): The phi ID.

    Returns:
        Union[ak.Array, np.ndarray, int]: The EMC TEID.
    """
    if getattr(module_or_akzipped, "fields", None) == ["module", "theta", "phi"]:
        return _det_nb.gen_emc_teid(
            module_or_akzipped.module, module_or_akzipped.theta, module_or_akzipped.phi
        )

    assert (
        type(module_or_akzipped) == type(theta) == type(phi)
    ), "All inputs must be of the same type."

    if not isinstance(module_or_akzipped, (ak.Array, np.ndarray)):
        res = _det_nb.gen_emc_teid(
            np.uint32(module_or_akzipped), np.uint32(theta), np.uint32(phi)
        )
        return type(module_or_akzipped)(res)

    return _det_nb.gen_emc_teid(module_or_akzipped, theta, phi)
