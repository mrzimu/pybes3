from pathlib import Path

import awkward as ak

import pybes3 as p3

data_dir = Path(__file__).parent.parent / "data"

helix_ak = p3.open(data_dir / "test_full_mc_evt_1.dst")[
    "Event/TDstEvent/m_mdcTrackCol"
].array()["m_helix"]

helix_np = ak.flatten(helix_ak, axis=1).to_numpy()


def test_parse_helix():
    fields = [
        "x",
        "y",
        "z",
        "r",
        "px",
        "py",
        "pz",
        "pt",
        "p",
        "theta",
        "phi",
        "charge",
    ]

    p_helix_ak1 = p3.parse_helix(helix_ak)
    assert p_helix_ak1.fields == fields

    p_helix_ak2 = p3.parse_helix(helix_np, library="ak")
    assert p_helix_ak2.fields == fields

    p_helix_np = p3.parse_helix(helix_np)
    assert list(p_helix_np.keys()) == fields
