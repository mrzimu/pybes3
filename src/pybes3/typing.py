from __future__ import annotations

from typing import TypeVar, Union

import awkward as ak
import numpy as np

IntLike = Union[ak.Array, np.ndarray, int, np.integer]
FloatLike = Union[ak.Array, np.ndarray, float, np.floating]
BoolLike = Union[ak.Array, np.ndarray, bool, np.bool_]

# Array generic type
ArrayLike = TypeVar("ArrayLike", ak.Array, np.ndarray)
