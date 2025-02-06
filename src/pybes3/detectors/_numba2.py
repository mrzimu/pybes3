from typing import Union

import awkward as ak
import numba as nb
import numpy as np

from . import constants as det_consts


@nb.vectorize([nb.boolean(nb.uint32)])
def check_mdc_id(
    id: Union[ak.Array, np.ndarray, np.uint32]
) -> Union[ak.Array, np.ndarray, np.bool_]:
    """
    Check if the MDC ID is valid.

    Parameters:
        id: The MDC ID array or value.

    Returns:
        Whether the ID is valid.
    """
    return (
        id & det_consts.DIGI_FLAG_MASK
    ) >> det_consts.DIGI_FLAG_OFFSET == det_consts.DIGI_MDC_FLAG
