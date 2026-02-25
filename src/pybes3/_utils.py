from __future__ import annotations

import awkward as ak
import awkward.contents
import numpy as np


def _extract_index(layout: ak.contents.Content) -> list:
    if isinstance(layout, awkward.contents.ListOffsetArray):
        offsets = layout.offsets.data
        return [offsets[1:] - offsets[:-1]] + _extract_index(layout.content)

    if isinstance(layout, awkward.contents.RegularArray):
        return [layout.size] + _extract_index(layout.content)

    if isinstance(layout, awkward.contents.NumpyArray):
        return []

    if isinstance(layout, awkward.contents.RecordArray):
        return []

    if isinstance(layout, awkward.contents.IndexedArray):
        return _extract_index(layout.content)

    if isinstance(layout, (awkward.contents.ByteMaskedArray, awkward.contents.BitMaskedArray)):
        return _extract_index(layout.content)

    if isinstance(layout, awkward.contents.UnmaskedArray):
        return _extract_index(layout.content)

    if isinstance(layout, awkward.contents.UnionArray):
        return _extract_index(layout.contents[0])

    raise TypeError(
        f"Unsupported awkward layout type in _extract_index: {type(layout).__name__}"
    )


def _flat_to_numpy(array: ak.Array | ak.Record | np.ndarray | float) -> np.ndarray:
    """
    Converts a flat awkward array to a numpy array.

    Args:
        array: The input awkward array, numpy array, or scalar.

    Returns:
        The converted numpy array.
    """
    if isinstance(array, (ak.Array, ak.Record)):
        return ak.flatten(array, axis=None).to_numpy()
    else:
        return array


def _recover_shape(array: np.ndarray | ak.Array, index: list) -> ak.Array:
    """
    Recovers the shape of a numpy array based on the provided index.

    Args:
        array: The input numpy array or awkward array.
        index: The index list that defines the shape.

    Returns:
        The reshaped awkward array.
    """
    res = ak.Array(array)
    for i in index:
        res = ak.unflatten(res, i)
    return res
