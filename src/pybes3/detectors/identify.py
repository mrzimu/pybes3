from typing import Union, overload

import awkward as ak
import numba as nb
import numpy as np

from . import _numba as _det_nb
from . import constants as det_consts


################################################################################
#                                parse_mdc_teid                                #
################################################################################
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
        check_mdc_teid(mdc_id)
        if isinstance(mdc_id, (ak.Array, np.ndarray))
        else check_mdc_teid(np.uint32(mdc_id))
    )

    # np.all can handle int case
    if (isinstance(mdc_id, ak.Array) and not ak.all(is_valid)) or (not np.all(is_valid)):
        raise ValueError("MDC ID is invalid.")

    if isinstance(mdc_id, (ak.Array, np.ndarray)):
        wire = mdc_teid_to_wire(mdc_id)
        layer = mdc_teid_to_layer(mdc_id)
        wire_type = mdc_teid_to_wire_type(mdc_id)

        if isinstance(mdc_id, ak.Array):
            return ak.zip({"wire": wire, "layer": layer, "wire_type": wire_type})
        else:
            return (wire, layer, wire_type)
    else:
        tmp_wire, tmp_layer, tmp_wire_type = (
            mdc_teid_to_wire(np.uint32(mdc_id)),
            mdc_teid_to_layer(np.uint32(mdc_id)),
            mdc_teid_to_wire_type(np.uint32(mdc_id)),
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
        wire_or_akzipped (Union[np.ndarray, int, ak.Array]): The wire ID or the akzipped array.
        layer (Union[np.ndarray, int, ak.Array]): The layer ID.
        wire_type (Union[np.ndarray, int, ak.Array]): The wire type.

    Returns:
        Union[np.ndarray, int, ak.Array]: The MDC TEID.
    """
    # if layer and wire_type are None, then wire is an ak.Array
    if hasattr(wire_or_akzipped, "fields") and set(wire_or_akzipped.fields) >= {
        "wire",
        "layer",
        "wire_type",
    }:
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
        check_emc_teid(emc_id)
        if isinstance(emc_id, (ak.Array, np.ndarray))
        else check_emc_teid(np.uint32(emc_id))
    )

    if (isinstance(emc_id, ak.Array) and not ak.all(is_valid)) or (not np.all(is_valid)):
        raise ValueError("EMC ID is invalid.")

    if isinstance(emc_id, (ak.Array, np.ndarray)):
        module = emc_teid_to_module(emc_id)
        theta = emc_teid_to_theta(emc_id)
        phi = emc_teid_to_phi(emc_id)

        if isinstance(emc_id, ak.Array):
            return ak.zip({"module": module, "theta": theta, "phi": phi})
        else:
            return (module, theta, phi)

    else:
        tmp_module, tmp_theta, tmp_phi = (
            emc_teid_to_module(np.uint32(emc_id)),
            emc_teid_to_theta(np.uint32(emc_id)),
            emc_teid_to_phi(np.uint32(emc_id)),
        )
        input_type = type(emc_id)
        return (input_type(tmp_module), input_type(tmp_theta), input_type(tmp_phi))


################################################################################
#                                 get_emc_teid                                 #
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
        module_or_akzipped (Union[ak.Array, np.ndarray, int]): The module ID or the akzipped array.
        theta (Union[ak.Array, np.ndarray, int]): The theta ID.
        phi (Union[ak.Array, np.ndarray, int]): The phi ID.

    Returns:
        Union[ak.Array, np.ndarray, int]: The EMC TEID.
    """
    if hasattr(module_or_akzipped, "fields") and set(module_or_akzipped.fields) >= {
        "module",
        "theta",
        "phi",
    }:
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


################################################################################
#                                parse_tof_teid                                #
################################################################################
@nb.vectorize([nb.uint32(nb.uint32)])
def check_tof_teid(tof_id: int) -> bool:
    """
    Check if the TOF TEID is valid.

    Parameters:
        tof_id (int): The TOF TEID array.

    Returns:
        bool: Whether the ID is valid.
    """
    return (
        tof_id & det_consts.DIGI_FLAG_MASK
    ) >> det_consts.DIGI_FLAG_OFFSET == det_consts.DIGI_TOF_FLAG


@nb.vectorize([nb.uint32(nb.uint32)])
def tof_teid_to_part(tof_id: int) -> int:
    """
    Convert the TOF TEID to the part ID.
    `0` for endcap0, `1` for barrel, and `2` for endcap1, `3` for MRPC.

    Parameters:
        tof_id (int): The TOF TEID array.

    Returns:
        int: The part ID.
    """
    return (tof_id & det_consts.DIGI_TOF_PART_MASK) >> det_consts.DIGI_TOF_PART_OFFSET


@nb.vectorize([nb.uint32(nb.uint32)])
def tof_teid_to_end(tof_id: int) -> int:
    """
    Convert the TOF TEID to the readout end ID.

    Parameters:
        tof_id (int): The TOF TEID array.

    Returns:
        int: The end ID.
    """
    return (tof_id & det_consts.DIGI_TOF_END_MASK) >> det_consts.DIGI_TOF_END_OFFSET


@nb.vectorize([nb.uint32(nb.uint32)])
def tof_teid_to_scint_layer(tof_id: int) -> int:
    """
    Convert the TOF TEID to the scintillator layer ID.

    Parameters:
        tof_id (int): The TOF TEID array.

    Returns:
        int: The scintillator layer ID.
    """
    return (
        tof_id & det_consts.DIGI_TOF_SCINT_LAYER_MASK
    ) >> det_consts.DIGI_TOF_SCINT_LAYER_OFFSET


@nb.vectorize([nb.uint32(nb.uint32)])
def tof_teid_to_scint_phi(tof_id: int) -> int:
    """
    Convert the TOF TEID to the scintillator phi ID.

    Parameters:
        tof_id (int): The TOF TEID array.

    Returns:
        int: The scintillator phi ID.
    """
    return (
        tof_id & det_consts.DIGI_TOF_SCINT_PHI_MASK
    ) >> det_consts.DIGI_TOF_SCINT_PHI_OFFSET


@nb.vectorize([nb.uint32(nb.uint32)])
def tof_teid_to_mrpc_endcap(tof_id: int) -> int:
    """
    Convert the TOF TEID to the MRPC endcap ID.

    Parameters:
        tof_id (int): The TOF TEID array.

    Returns:
        int: The MRPC endcap ID.
    """
    return (
        tof_id & det_consts.DIGI_TOF_MRPC_ENDCAP_MASK
    ) >> det_consts.DIGI_TOF_MRPC_ENDCAP_OFFSET


@nb.vectorize([nb.uint32(nb.uint32)])
def tof_teid_to_mrpc_module(tof_id: int) -> int:
    """
    Convert the TOF TEID to the MRPC module ID.

    Parameters:
        tof_id (int): The TOF TEID array.

    Returns:
        int: The MRPC module ID.
    """
    return (
        tof_id & det_consts.DIGI_TOF_MRPC_MODULE_MASK
    ) >> det_consts.DIGI_TOF_MRPC_MODULE_OFFSET


@nb.vectorize([nb.uint32(nb.uint32)])
def tof_teid_to_mrpc_strip(tof_id: int) -> int:
    """
    Convert the TOF TEID to the MRPC strip ID.

    Parameters:
        tof_id (int): The TOF TEID array.

    Returns:
        int: The MRPC strip ID.
    """
    return (
        tof_id & det_consts.DIGI_TOF_MRPC_STRIP_MASK
    ) >> det_consts.DIGI_TOF_MRPC_STRIP_OFFSET


@overload
def parse_tof_teid(tof_id: ak.Array) -> ak.Array:
    """
    Parse the TOF TEID into the part, layer, strip and end.

    Parameters:
        tof_id (ak.Array): The TOF TEID array.

    Returns:
        ak.Array: The parsed part, layer, strip and end.
    """


@overload
def parse_tof_teid(tof_id: np.ndarray) -> dict:
    """
    Parse the TOF TEID into the part, layer, strip and end.

    Parameters:
        tof_id (np.ndarray): The TOF TEID array.

    Returns:
        dict: The parsed part, layer, strip and end.
    """


@overload
def parse_tof_teid(tof_id: int) -> dict:
    """
    Parse the TOF TEID into the part, layer, strip and end.

    Parameters:
        tof_id (int): The TOF TEID array.

    Returns:
        dict: The parsed part, layer, strip and end.
    """


def parse_tof_teid(tof_id: Union[ak.Array, np.ndarray, int]) -> Union[ak.Array, dict]:
    """
    Parse the TOF TEID into the part, layer, strip and end.

    Parameters:
        tof_id (Union[ak.Array, np.ndarray, int]): The TOF TEID array.

    Returns:
        Union[ak.Array, tuple]: The parsed part, layer, strip and end.
    """
    is_valid = (
        check_tof_teid(tof_id)
        if isinstance(tof_id, (ak.Array, np.ndarray))
        else check_tof_teid(np.uint32(tof_id))
    )

    if (isinstance(tof_id, ak.Array) and not ak.all(is_valid)) or (not np.all(is_valid)):
        raise ValueError("TOF ID is invalid.")

    if isinstance(tof_id, (ak.Array, np.ndarray)):
        part = tof_teid_to_part(tof_id)

        is_scint = part < 3
        has_scint = ak.any(is_scint)
        if has_scint:
            scint_id = tof_id[is_scint]
            scint_part = part[is_scint]
            scint_layer = tof_teid_to_scint_layer(scint_id)
            scint_phi = tof_teid_to_scint_phi(scint_id)
            scint_end = tof_teid_to_end(scint_id)
            scint_res = {
                "part": scint_part,
                "layer": scint_layer,
                "phi": scint_phi,
                "end": scint_end,
            }

        has_mrpc = not ak.all(is_scint)
        if has_mrpc:
            is_mrpc = ~is_scint
            mrpc_id = tof_id[is_mrpc]
            mrpc_part = part[is_mrpc]
            mrpc_endcap = tof_teid_to_mrpc_endcap(mrpc_id)
            mrpc_module = tof_teid_to_mrpc_module(mrpc_id)
            mrpc_strip = tof_teid_to_mrpc_strip(mrpc_id)
            mrpc_end = tof_teid_to_end(mrpc_id)
            mrpc_res = {
                "part": mrpc_part,
                "endcap": mrpc_endcap,
                "module": mrpc_module,
                "strip": mrpc_strip,
                "end": mrpc_end,
            }

        res = {}
        if has_scint:
            res["scint"] = ak.zip(scint_res) if isinstance(tof_id, ak.Array) else scint_res
        if has_mrpc:
            res["mrpc"] = ak.zip(mrpc_res) if isinstance(tof_id, ak.Array) else mrpc_res
        return res

    else:
        tmp_part = tof_teid_to_part(np.uint32(tof_id))
        input_type = type(tof_id)
        if tmp_part < 3:
            tmp_scint_layer = tof_teid_to_scint_layer(np.uint32(tof_id))
            tmp_scint_phi = tof_teid_to_scint_phi(np.uint32(tof_id))
            tmp_scint_end = tof_teid_to_end(np.uint32(tof_id))
            return {
                "part": input_type(tmp_part),
                "layer": input_type(tmp_scint_layer),
                "phi": input_type(tmp_scint_phi),
                "end": input_type(tmp_scint_end),
            }
        else:
            tmp_mrpc_endcap = tof_teid_to_mrpc_endcap(np.uint32(tof_id))
            tmp_mrpc_module = tof_teid_to_mrpc_module(np.uint32(tof_id))
            tmp_mrpc_strip = tof_teid_to_mrpc_strip(np.uint32(tof_id))
            tmp_mrpc_end = tof_teid_to_end(np.uint32(tof_id))
            return {
                "part": input_type(tmp_part),
                "endcap": input_type(tmp_mrpc_endcap),
                "module": input_type(tmp_mrpc_module),
                "strip": input_type(tmp_mrpc_strip),
                "end": input_type(tmp_mrpc_end),
            }


################################################################################
#                                 get_tof_teid                                 #
################################################################################
@overload
def get_tof_scint_teid(data: ak.Array) -> ak.Array:
    """
    Get the TOF TEID from the part, layer, strip and end for scintillator.

    Parameters:
        data (ak.Array): The part, layer, strip and end.

    Returns:
        ak.Array: The TOF TEID.
    """


@overload
def get_tof_scint_teid(
    part: ak.Array, layer: ak.Array, phi: ak.Array, end: ak.Array
) -> ak.Array:
    """
    Get the TOF TEID from the part, layer, strip and end for scintillator.

    Parameters:
        part (ak.Array): The part ID.
        layer (ak.Array): The layer ID.
        phi (ak.Array): The phi ID.
        end (ak.Array): The end ID.

    Returns:
        ak.Array: The TOF TEID.
    """


@overload
def get_tof_scint_teid(
    part: np.ndarray, layer: np.ndarray, phi: np.ndarray, end: np.ndarray
) -> np.ndarray:
    """
    Get the TOF TEID from the part, layer, strip and end for scintillator.

    Parameters:
        part (np.ndarray): The part ID.
        layer (np.ndarray): The layer ID.
        phi (np.ndarray): The phi ID.
        end (np.ndarray): The end ID.

    Returns:
        np.ndarray: The TOF TEID.
    """


@overload
def get_tof_scint_teid(part: int, layer: int, phi: int, end: int) -> int:
    """
    Get the TOF TEID from the part, layer, strip and end for scintillator.

    Parameters:
        part (int): The part ID.
        layer (int): The layer ID.
        phi (int): The phi ID.
        end (int): The end ID.

    Returns:
        int: The TOF TEID.
    """


def get_tof_scint_teid(
    part_or_akzipped: Union[ak.Array, np.ndarray, int],
    layer: Union[ak.Array, np.ndarray, int, None] = None,
    phi: Union[ak.Array, np.ndarray, int, None] = None,
    end: Union[ak.Array, np.ndarray, int, None] = None,
) -> Union[ak.Array, np.ndarray, int]:
    """
    Get the TOF TEID from the part, layer, strip and end for scintillator.

    Parameters:
        part_or_akzipped (Union[ak.Array, np.ndarray, int]): The part ID or the akzipped array.
        layer (Union[ak.Array, np.ndarray, int]): The layer ID.
        phi (Union[ak.Array, np.ndarray, int]): The phi ID.
        end (Union[ak.Array, np.ndarray, int]): The end ID.

    Returns:
        Union[ak.Array, np.ndarray, int]: The TOF TEID.
    """
    if hasattr(part_or_akzipped, "fields") and set(part_or_akzipped.fields) >= {
        "part",
        "layer",
        "phi",
        "end",
    }:
        return _det_nb.gen_tof_scint_teid(
            part_or_akzipped["part"],
            part_or_akzipped["layer"],
            part_or_akzipped["phi"],
            part_or_akzipped["end"],
        )

    assert (
        type(part_or_akzipped) == type(layer) == type(phi) == type(end)
    ), "All inputs must be of the same type."

    if not isinstance(part_or_akzipped, (ak.Array, np.ndarray)):
        res = _det_nb.gen_tof_scint_teid(
            np.uint32(part_or_akzipped), np.uint32(layer), np.uint32(phi), np.uint32(end)
        )
        return type(part_or_akzipped)(res)

    return _det_nb.gen_tof_scint_teid(part_or_akzipped, layer, phi, end)


@overload
def get_tof_mrpc_teid(data: ak.Array) -> ak.Array:
    """
    Get the TOF TEID from the endcap, module, strip and end for MRPC.

    Parameters:
        data (ak.Array): The endcap, module, strip and end.

    Returns:
        ak.Array: The TOF TEID.
    """


@overload
def get_tof_mrpc_teid(
    endcap: ak.Array, module: ak.Array, strip: ak.Array, end: ak.Array
) -> ak.Array:
    """
    Get the TOF TEID from the endcap, module, strip and end for MRPC.

    Parameters:
        endcap (ak.Array): The endcap ID.
        module (ak.Array): The module ID.
        strip (ak.Array): The strip ID.
        end (ak.Array): The end ID.

    Returns:
        ak.Array: The TOF TEID.
    """


@overload
def get_tof_mrpc_teid(
    endcap: np.ndarray, module: np.ndarray, strip: np.ndarray, end: np.ndarray
) -> np.ndarray:
    """
    Get the TOF TEID from the endcap, module, strip and end for MRPC.

    Parameters:
        endcap (np.ndarray): The endcap ID.
        module (np.ndarray): The module ID.
        strip (np.ndarray): The strip ID.
        end (np.ndarray): The end ID.

    Returns:
        np.ndarray: The TOF TEID.
    """


@overload
def get_tof_mrpc_teid(endcap: int, module: int, strip: int, end: int) -> int:
    """
    Get the TOF TEID from the endcap, module, strip and end for MRPC.

    Parameters:
        endcap (int): The endcap ID.
        module (int): The module ID.
        strip (int): The strip ID.
        end (int): The end ID.

    Returns:
        int: The TOF TEID.
    """


def get_tof_mrpc_teid(
    endcap_or_akzipped: Union[ak.Array, np.ndarray, int],
    module: Union[ak.Array, np.ndarray, int, None] = None,
    strip: Union[ak.Array, np.ndarray, int, None] = None,
    end: Union[ak.Array, np.ndarray, int, None] = None,
) -> Union[ak.Array, np.ndarray, int]:
    """
    Get the TOF TEID from the endcap, module, strip and end for MRPC.

    Parameters:
        endcap_or_akzipped (Union[ak.Array, np.ndarray, int]): The endcap ID or the akzipped array.
        module (Union[ak.Array, np.ndarray, int]): The module ID.
        strip (Union[ak.Array, np.ndarray, int]): The strip ID.
        end (Union[ak.Array, np.ndarray, int]): The end ID.

    Returns:
        Union[ak.Array, np.ndarray, int]: The TOF TEID.
    """
    if hasattr(endcap_or_akzipped, "fields") and set(endcap_or_akzipped.fields) >= {
        "endcap",
        "module",
        "strip",
        "end",
    }:
        return _det_nb.gen_tof_mrpc_teid(
            endcap_or_akzipped["endcap"],
            endcap_or_akzipped["module"],
            endcap_or_akzipped["strip"],
            endcap_or_akzipped["end"],
        )

    assert (
        type(endcap_or_akzipped) == type(module) == type(strip) == type(end)
    ), "All inputs must be of the same type."

    if not isinstance(endcap_or_akzipped, (ak.Array, np.ndarray)):
        res = _det_nb.gen_tof_mrpc_teid(
            np.uint32(endcap_or_akzipped),
            np.uint32(module),
            np.uint32(strip),
            np.uint32(end),
        )
        return type(endcap_or_akzipped)(res)

    return _det_nb.gen_tof_mrpc_teid(endcap_or_akzipped, module, strip, end)
