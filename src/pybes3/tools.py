from typing import Union

import awkward as ak
import awkward.contents
import awkward.index
import numba as nb
import numpy as np


def make_jagged_array(data: Union[ak.Array, np.ndarray], n_counts: np.ndarray) -> ak.Array:
    """
    Create a jagged array using the given data and counts.

    Args:
        data (Union[ak.Array, np.ndarray]): The data to be jagged.
        n_counts (np.ndarray): The number of elements in each subarray.

    Returns:
        ak.Array: The jagged array.

    """
    n_counts = ak.to_numpy(n_counts)
    offsets = np.zeros(len(n_counts) + 1, dtype=np.int64)
    offsets[1:] = np.cumsum(n_counts)

    if isinstance(data, np.ndarray):
        layout = awkward.contents.ListOffsetArray(
            awkward.index.Index(offsets), awkward.contents.NumpyArray(data)
        )
    else:
        layout = awkward.contents.ListOffsetArray(awkward.index.Index(offsets), data.layout)

    return ak.Array(layout)
