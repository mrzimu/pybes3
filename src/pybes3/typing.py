from __future__ import annotations

from typing import Union

import awkward as ak
import numpy as np

IntLike = Union[ak.Array, np.ndarray, int]
FloatLike = Union[ak.Array, np.ndarray, float]
BoolLike = Union[ak.Array, np.ndarray, bool]
