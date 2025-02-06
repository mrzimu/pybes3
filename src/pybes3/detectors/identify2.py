from typing import TypeVar, Union, overload

import awkward as ak
import numba as nb
import numpy as np

T = TypeVar("T")

DIGI_MDC_FLAG = np.uint32(0x10)
DIGI_TOF_FLAG = np.uint32(0x20)
DIGI_EMC_FLAG = np.uint32(0x30)
DIGI_MUC_FLAG = np.uint32(0x40)
DIGI_HLT_FLAG = np.uint32(0x50)
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

# EMC
DIGI_EMC_MODULE_OFFSET = np.uint32(16)
DIGI_EMC_MODULE_MASK = np.uint32(0x000F0000)
DIGI_EMC_THETA_OFFSET = np.uint32(8)
DIGI_EMC_THETA_MASK = np.uint32(0x00003F00)
DIGI_EMC_PHI_OFFSET = np.uint32(0)
DIGI_EMC_PHI_MASK = np.uint32(0x000000FF)

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


@regularize_args_uint32
@nb.vectorize([nb.boolean(nb.uint32)])
def check_mdc_id(
    mdc_id: Union[ak.Array, np.ndarray, np.uint32]
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
) -> Union[ak.Array, np.ndarray, int]:
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
def mdc_id_to_layer(mdc_id: int) -> int:
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
def mdc_id_to_wire_type(mdc_id: int) -> int:
    """
    Convert the MDC ID to the wire type.

    Parameters:
        mdc_id: The MDC ID array.

    Returns:
       The wire type.
    """
    return (mdc_id & DIGI_MDC_WIRETYPE_MASK) >> DIGI_MDC_WIRETYPE_OFFSET


def parse_mdc_id(mdc_id: T) -> dict[str, T]:
    """
    Parse the MDC ID into the wire, layer, and wiretype.

    Parameters:
        mdc_id (Union[ak.Array, np.ndarray, int]): The MDC ID array or value.

    Returns:
        The parsed result, {"wire": wire, "layer": layer, "wire_type": wire_type}
    """
    is_valid = check_mdc_id(mdc_id)

    # np.all can handle int case
    if (isinstance(mdc_id, ak.Array) and not ak.all(is_valid)) or (not np.all(is_valid)):
        raise ValueError("MDC ID is invalid.")

    wire = mdc_id_to_wire(mdc_id)
    layer = mdc_id_to_layer(mdc_id)
    wire_type = mdc_id_to_wire_type(mdc_id)

    if isinstance(mdc_id, ak.Array):
        return ak.zip({"wire": wire, "layer": layer, "wire_type": wire_type})
    elif isinstance(mdc_id, np.ndarray):
        return {"wire": wire, "layer": layer, "wire_type": wire_type}
    else:
        input_type = type(mdc_id)
        return {
            "wire": input_type(wire),
            "layer": input_type(layer),
            "wire_type": input_type(wire_type),
        }


@regularize_args_uint32
@nb.vectorize([nb.uint32(nb.uint32, nb.uint32, nb.uint32)])
def gen_mdc_id(wire: T, layer: T, wire_type: T) -> T:
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
