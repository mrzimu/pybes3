from __future__ import annotations

from typing import Literal

import awkward as ak
import numpy as np

from pybes3 import digi_id
from pybes3.typing import IntLike


def parse_tof_digi_id(
    tof_digi_id: IntLike,
    flat: bool = False,
    library: Literal["ak", "np"] = "ak",
) -> ak.Array | dict[str, np.ndarray] | dict[str, np.int_]:
    """
    Parse TOF digi ID.
    If `library` is `ak`, return `ak.Record`. If `library` is `np`, return `dict[str, np.ndarray]`.

    Available keys of the output:

    - `part`: The part number. `0,1,2` for scintillator endcap0, barrel, endcap1; `3,4` for MRPC endcap0, endcap1.
    - `layer_or_module`: The scintillator layer or MRPC module number, based on the part number.
    - `phi_or_strip`: The scintillator phi or MRPC strip ID, based on the part number.
    - `end`: The readout end ID.

    The return value is based on the part number.

    Rows where `part < 3` are scintillator and `layer_or_module` represents layer number, `phi_or_strip` represents phi number.

    Rows where `part >= 3` are MRPC and `layer_or_module` represents module number, `phi_or_strip` represents strip ID.

    Parameters:
        tof_digi_id: The TOF ID.
        flat: Whether to flatten the output.
        library: The library to use as output.

    Returns:
        The parsed TOF ID.

    """
    if library not in ["ak", "np"]:
        raise ValueError(f"Unsupported library: {library}")

    if flat and isinstance(tof_digi_id, ak.Array):
        tof_digi_id = ak.flatten(tof_digi_id)

    part = digi_id.tof_id_to_part(tof_digi_id)
    res = {
        "part": part,
        "layer_or_module": digi_id.tof_id_to_layer_or_module(tof_digi_id, part),
        "phi_or_strip": digi_id.tof_id_to_phi_or_strip(tof_digi_id, part),
        "end": digi_id.tof_id_to_end(tof_digi_id),
    }

    if library == "ak":
        return ak.zip(res)
    else:
        return res
