from __future__ import annotations

from typing import Any, Optional
import numpy as np
from numpy.typing import NDArray
from uproot_custom.cpp import IElementReader

class Bes3TObjArrayReader(IElementReader):
    def __init__(
        self,
        name: str,
        element_reader: IElementReader,
    ): ...
    def data(self) -> tuple[NDArray[np.uint32], Any]: ...

class Bes3SymMatrixArrayReader(IElementReader):
    def __init__(
        self,
        name: str,
        flat_size: int,
        full_dim: int,
    ): ...
    def data(self) -> NDArray[np.float64]: ...

class Bes3CgemClusterColReader(IElementReader):
    def __init__(self, name: str): ...
    def data(self) -> dict[str, NDArray]: ...

def read_data(
    data: NDArray[np.uint8],
    offsets: NDArray[np.uint32],
    reader: IElementReader,
) -> Any: ...
def read_bes_raw(
    data: NDArray[np.uint32],
    sub_detectors: Optional[list[str]] = None,
) -> dict: ...
