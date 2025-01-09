import numpy as np
import awkward as ak
import numba as nb


class Helix:
    def __init__(self, helix_arr: ak.Array) -> None:
        self._data = helix_arr
