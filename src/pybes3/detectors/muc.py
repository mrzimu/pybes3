from __future__ import annotations

from typing import Literal

import awkward as ak
import numpy as np

from pybes3 import digi_id
from pybes3.typing import IntLike


def parse_muc_digi_id(
    muc_digi_id: IntLike,
    flat: bool = False,
    library: Literal["ak", "np"] = "ak",
) -> ak.Array | dict[str, np.ndarray] | dict[str, np.int_]:
    """
    Parse MUC digi ID.

    If `library` is `ak`, return `ak.Array`. If `library` is `np`, return `dict[str, np.ndarray]`.

    Available keys of the output:

    - `part`: The part number.
    - `segment`: The segment number.
    - `layer`: The layer number.
    - `channel`: The channel number.
    - `gap`: The gap number, which is equivalent to layer number.
    - `strip`: The strip number, which is equivalent to channel number.

    Parameters:
        muc_digi_id: The MUC digi ID.
        flat: Whether to flatten the output.
        library: The library to use as output.

    Returns:
        The parsed MUC digi ID.
    """
    if library not in ["ak", "np"]:
        raise ValueError(f"Unsupported library: {library}")

    if flat and isinstance(muc_digi_id, ak.Array):
        muc_digi_id = ak.flatten(muc_digi_id)

    part = digi_id.muc_id_to_part(muc_digi_id)
    segment = digi_id.muc_id_to_segment(muc_digi_id)
    layer = digi_id.muc_id_to_layer(muc_digi_id)
    channel = digi_id.muc_id_to_channel(muc_digi_id)

    res = {
        "part": part,
        "segment": segment,
        "layer": layer,
        "channel": channel,
        "gap": layer,
        "strip": channel,
    }

    if library == "ak":
        return ak.zip(res)
    else:
        return res
