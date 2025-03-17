from typing import TypeVar

import awkward as ak
import numpy as np

IntLike = TypeVar("ak.Array | np.ndarray | int", ak.Array, np.ndarray, int)
FloatLike = TypeVar("ak.Array | np.ndarray | float", ak.Array, np.ndarray, float)
BoolLike = TypeVar("ak.Array | np.ndarray | bool", ak.Array, np.ndarray, bool)
