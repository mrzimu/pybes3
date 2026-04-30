from __future__ import annotations

from typing import TypeVar

import awkward as ak
import numpy as np

IntLike = ak.Array | np.ndarray | np.integer

# Array generic type
ArrayLike = TypeVar("ArrayLike", bound=ak.Array | np.ndarray)
