import numpy as np

def read_bes_tobject(
    data: np.ndarray,
    byte_offsets: np.ndarray,
    type_name: str,
    member_streamers_info: list[dict],
) -> list: ...
def read_bes_tobjarray(
    data: np.ndarray,
    byte_offsets: np.ndarray,
    type_name: str,
    member_streamers_info: list[dict],
) -> dict: ...
def read_bes_stl(
    data: np.ndarray,
    byte_offsets: np.ndarray,
    type_name: str,
    member_streamers_info: list[dict],
) -> dict: ...
def read_bes_raw(data: np.ndarray, sub_detectors: list[str]) -> dict: ...
