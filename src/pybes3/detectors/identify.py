from typing import Union

import awkward as ak
import numpy as np

from ..tools import make_jagged_array
from ._numba import _gen_mdc_id, _parse_mdc_id
from .constants import MdcDigiConst


def parse_mdc_id(mdc_id: Union[ak.Array, np.ndarray, int], check_valid: bool = True) -> tuple:
    """
    Parse the MDC ID into wire ID, layer ID, and wire type.

    Args:
        mdc_id (Union[ak.Array, np.ndarray, int]): The MDC ID.
        check_valid (bool, optional): Whether to check if the ID is valid. Defaults to True.

    Returns:
        tuple: The wire ID, layer ID, and wire type.

    """
    # ak.Array
    if isinstance(mdc_id, ak.Array):
        if len(mdc_id.positional_axis) == 1:
            flat_id = ak.to_numpy(mdc_id)
            wire_id, layer_id, wire_type = _parse_mdc_id(flat_id, check_valid)

        elif len(mdc_id.positional_axis) == 2:
            n_digis = ak.count(mdc_id, axis=1)
            flat_id = ak.to_numpy(ak.flatten(mdc_id))

            flat_wire_id, flat_layer_id, flat_wire_type = _parse_mdc_id(flat_id, check_valid)

            wire_id = make_jagged_array(flat_wire_id, n_digis)
            layer_id = make_jagged_array(flat_layer_id, n_digis)
            wire_type = make_jagged_array(flat_wire_type, n_digis)

        return wire_id, layer_id, wire_type

    # np.ndarray
    elif isinstance(mdc_id, np.ndarray):
        wire_id, layer_id, wire_type = _parse_mdc_id(mdc_id, check_valid)
        return wire_id, layer_id, wire_type

    # int
    else:
        mdc_id = int(mdc_id)

        if check_valid:
            assert (
                mdc_id & MdcDigiConst.DIGI_MASK
            ) >> MdcDigiConst.DIGI_FLAG == MdcDigiConst.DIGI_FLAG

        wire_id = (mdc_id & MdcDigiConst.WIRE_MASK) >> MdcDigiConst.WIRE_OFFSET
        layer_id = (mdc_id & MdcDigiConst.LAYER_MASK) >> MdcDigiConst.LAYER_OFFSET
        wire_type = (mdc_id & MdcDigiConst.WIRETYPE_MASK) >> MdcDigiConst.WIRETYPE_OFFSET

        return wire_id, layer_id, wire_type


def get_mdc_id(
    wire_id: Union[ak.Array, np.ndarray, int],
    layer_id: Union[ak.Array, np.ndarray, int],
    wire_type: Union[ak.Array, np.ndarray, int],
) -> Union[ak.Array, np.ndarray, int]:
    """
    Get the MDC ID from wire ID, layer ID, and wire type.

    Args:
        wire_id (Union[ak.Array, np.ndarray, int]): The wire ID.
        layer_id (Union[ak.Array, np.ndarray, int]): The layer ID.
        wire_type (Union[ak.Array, np.ndarray, int]): The wire type.

    Returns:
        Union[ak.Array, np.ndarray, int]: The MDC ID.

    """
    assert isinstance(wire_id, type(layer_id)) and isinstance(
        layer_id, type(wire_type)
    ), "The input types must be the same."

    # ak.Array
    if isinstance(wire_id, ak.Array):
        if len(wire_id.positional_axis) == 1:
            flat_wire_id = ak.to_numpy(wire_id)
            flat_layer_id = ak.to_numpy(layer_id)
            flat_wire_type = ak.to_numpy(wire_type)

            mdc_id = _gen_mdc_id(flat_wire_id, flat_layer_id, flat_wire_type)

        elif len(wire_id.positional_axis) == 2:
            n_digis = ak.count(wire_id, axis=1)
            flat_wire_id = ak.to_numpy(ak.flatten(wire_id))
            flat_layer_id = ak.to_numpy(ak.flatten(layer_id))
            flat_wire_type = ak.to_numpy(ak.flatten(wire_type))

            mdc_id = _gen_mdc_id(flat_wire_id, flat_layer_id, flat_wire_type)
            mdc_id = make_jagged_array(mdc_id, n_digis)

        return mdc_id

    # np.ndarray
    elif isinstance(wire_id, np.ndarray):
        mdc_id = _gen_mdc_id(wire_id, layer_id, wire_type)
        return mdc_id

    # int
    else:
        mdc_id = (
            (int(wire_id) << MdcDigiConst.WIRE_OFFSET)
            | (int(layer_id) << MdcDigiConst.LAYER_OFFSET)
            | (int(wire_type) << MdcDigiConst.WIRETYPE_OFFSET)
        )

        return mdc_id


def parse_emc_id(emc_id: Union[ak.Array, np.ndarray, int], check_valid: bool = True) -> tuple:
    """
    Parse the EMC ID into module ID, theta ID, and phi ID.

    Args:
        emc_id (Union[ak.Array, np.ndarray, int]): The EMC ID.

    Returns:
        tuple: The module ID, theta ID, and phi ID.

    """
    raise NotImplementedError
