from typing import Any, Optional
import numpy as np
from numpy.typing import NDArray

class BaseReader:
    def __init__(self, name: str): ...
    def data(self) -> Any: ...

class Int8Reader(BaseReader):
    def data(self) -> NDArray[np.int8]: ...

class Int16Reader(BaseReader):
    def data(self) -> NDArray[np.int16]: ...

class Int32Reader(BaseReader):
    def data(self) -> NDArray[np.int32]: ...

class Int64Reader(BaseReader):
    def data(self) -> NDArray[np.int64]: ...

class UInt8Reader(BaseReader):
    def data(self) -> NDArray[np.uint8]: ...

class UInt16Reader(BaseReader):
    def data(self) -> NDArray[np.uint16]: ...

class UInt32Reader(BaseReader):
    def data(self) -> NDArray[np.uint32]: ...

class UInt64Reader(BaseReader):
    def data(self) -> NDArray[np.uint64]: ...

class FloatReader(BaseReader):
    def data(self) -> NDArray[np.float32]: ...

class DoubleReader(BaseReader):
    def data(self) -> NDArray[np.float64]: ...

class BoolReader(BaseReader):
    def data(self) -> NDArray[np.bool_]: ...

class STLSeqReader(BaseReader):
    def __init__(
        self,
        name: str,
        is_top: bool,
        element_reader: list[BaseReader],
    ): ...
    def data(self) -> tuple[NDArray[np.uint32], Any]: ...

class STLMapReader(BaseReader):
    def __init__(
        self,
        name: str,
        is_top: bool,
        key_reader: BaseReader,
        value_reader: BaseReader,
    ): ...
    def data(self) -> tuple[NDArray[np.uint32], Any, Any]: ...

class STLStringReader(BaseReader):
    def __init__(
        self,
        name: str,
        is_top: bool,
    ): ...
    def data(self) -> tuple[NDArray[np.uint32], NDArray[np.character]]: ...

class TArrayCReader(BaseReader):
    def data(self) -> tuple[NDArray[np.uint32], NDArray[np.int8]]: ...

class TArraySReader(BaseReader):
    def data(self) -> tuple[NDArray[np.uint32], NDArray[np.int16]]: ...

class TArrayIReader(BaseReader):
    def data(self) -> tuple[NDArray[np.uint32], NDArray[np.int32]]: ...

class TArrayLReader(BaseReader):
    def data(self) -> tuple[NDArray[np.uint32], NDArray[np.int64]]: ...

class TArrayFReader(BaseReader):
    def data(self) -> tuple[NDArray[np.uint32], NDArray[np.float32]]: ...

class TArrayDReader(BaseReader):
    def data(self) -> tuple[NDArray[np.uint32], NDArray[np.float64]]: ...

class TStringReader(BaseReader):
    def data(self) -> tuple[NDArray[np.uint32], NDArray[np.character]]: ...

class TObjectReader(BaseReader):
    def data(self) -> None: ...

class CArrayReader(BaseReader):
    def __init__(
        self,
        name: str,
        is_obj: bool,
        flat_size: int,
        element_reader: BaseReader,
    ): ...

class BaseObjectReader(BaseReader):
    def __init__(
        self,
        name: str,
        sub_readers: list[BaseReader],
    ): ...
    def data(self) -> list: ...

class ObjectHeaderReader(BaseReader):
    def __init__(
        self,
        name: str,
        sub_readers: list[BaseReader],
    ): ...
    def data(self) -> list: ...

class EmptyReader(BaseReader):
    def data(self) -> None: ...

class Bes3TObjArrayReader(BaseReader):
    def __init__(
        self,
        name: str,
        element_reader: BaseReader,
    ): ...
    def data(self) -> tuple[NDArray[np.uint32], Any]: ...

def read_data(
    data: NDArray[np.uint8],
    offsets: NDArray[np.uint32],
    reader: BaseReader,
) -> Any: ...
def read_bes_raw(
    data: NDArray[np.uint32],
    sub_detectors: Optional[list[str]] = None,
) -> dict: ...
