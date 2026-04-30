from __future__ import annotations

from typing import TypeVar

import awkward as ak
import numpy as np

IntLike = ak.Array | np.ndarray | np.integer
FloatLike = ak.Array | np.ndarray | np.floating
BoolLike = ak.Array | np.ndarray | np.bool_

# Array generic type
ArrayLike = TypeVar("ArrayLike", bound=ak.Array | np.ndarray)
