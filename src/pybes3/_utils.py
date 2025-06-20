import awkward as ak
import awkward.contents
import numpy as np


def _extract_index(layout) -> list:
    if isinstance(layout, awkward.contents.ListOffsetArray):
        offsets = layout.offsets.data
        return [offsets[1:] - offsets[:-1]] + _extract_index(layout.content)

    if isinstance(layout, awkward.contents.RegularArray):
        return [layout.size] + _extract_index(layout.content)

    if isinstance(layout, awkward.contents.NumpyArray):
        return []

    if isinstance(layout, awkward.contents.RecordArray):
        return []


def _flat_to_numpy(array) -> np.ndarray:
    """
    Converts a flat awkward array to a numpy array.

    Args:
        array (ak.Array): The input awkward array.

    Returns:
        np.ndarray: The converted numpy array.
    """
    if isinstance(array, (ak.Array, ak.Record)):
        return ak.flatten(array, axis=None).to_numpy()
    else:
        return array


def _recover_shape(array, index) -> ak.Array:
    """
    Recovers the shape of a numpy array based on the provided index.

    Args:
        array (np.ndarray | ak.Array): The input numpy array.
        index (list): The index list that defines the shape.

    Returns:
        ak.Array: The reshaped awkward array.
    """
    res = ak.Array(array)
    for i in index:
        res = ak.unflatten(res, i)
    return res
