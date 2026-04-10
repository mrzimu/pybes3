from __future__ import annotations

from typing import Literal

import awkward as ak
import numpy as np

from pybes3 import digi_id
from pybes3.typing import IntLike


def parse_cgem_digi_id(
    cgem_digi_id: IntLike,
    flat: bool = False,
    library: Literal["ak", "np"] = "ak",
) -> ak.Array | dict[str, np.ndarray] | dict[str, np.int_]:
    """
    Parse CGEM digi ID.

    If `library` is `ak`, return `ak.Record`. If `library` is `np`, return `dict[str, np.ndarray]`.

    Available keys of the output:

    - `layer`: The layer number.
    - `sheet`: The sheet ID.
    - `strip`: The strip ID.
    - `is_x_strip`: Whether the strip is an X-strip.

    Parameters:
        cgem_digi_id: The CGEM digi ID.
        flat: Whether to flatten the output.
        library: The library to use as output.

    Returns:
        The parsed CGEM digi ID.
    """
    if library not in ["ak", "np"]:
        raise ValueError(f"Unsupported library: {library}")

    if flat and isinstance(cgem_digi_id, ak.Array):
        cgem_digi_id = ak.flatten(cgem_digi_id)

    res = {
        "layer": digi_id.cgem_id_to_layer(cgem_digi_id),
        "sheet": digi_id.cgem_id_to_sheet(cgem_digi_id),
        "strip": digi_id.cgem_id_to_strip(cgem_digi_id),
        "is_x_strip": digi_id.cgem_id_to_is_x_strip(cgem_digi_id),
    }

    if library == "ak":
        return ak.zip(res)
    else:
        return res
