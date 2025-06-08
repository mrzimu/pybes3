from pathlib import Path

import awkward as ak
import numpy as np
import pytest

import pybes3 as p3

data_dir = Path(__file__).parent.parent / "data"

helix_ak = p3.open(data_dir / "test_full_mc_evt_1.dst")[
    "Event/TDstEvent/m_mdcTrackCol"
].array()["m_helix"]

helix_np = ak.flatten(helix_ak, axis=1).to_numpy()


def test_helix():
    # parse_helix
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
        "r_trk",
    ]

    with pytest.warns(DeprecationWarning):
        p_helix_ak1 = p3.parse_helix(helix_ak)
    assert p_helix_ak1.fields == fields

    with pytest.warns(DeprecationWarning):
        p_helix_ak2 = p3.parse_helix(helix_np, library="ak")
    assert p_helix_ak2.fields == fields

    with pytest.warns(DeprecationWarning):
        p_helix_np = p3.parse_helix(helix_np)
    assert list(p_helix_np.keys()) == fields

    # regularize_helix
    with pytest.warns(DeprecationWarning):
        r_helix_ak = p3.regularize_helix(helix_ak)
    assert ak.all(r_helix_ak[..., 0] > 0)
    assert ak.all(r_helix_ak[..., 1] > 0) and ak.all(r_helix_ak[..., 1] < 2 * np.pi)

    with pytest.warns(DeprecationWarning):
        r_helix_np = p3.regularize_helix(helix_np)
    assert np.all(r_helix_np[..., 0] > 0)
    assert np.all(r_helix_np[..., 1] > 0) and np.all(r_helix_np[..., 1] < 2 * np.pi)

    # compute_helix
    with pytest.warns(DeprecationWarning):
        c_helix_ak1 = p3.compute_helix(p_helix_ak1)
    assert ak.all(np.isclose(c_helix_ak1, r_helix_ak))

    with pytest.warns(DeprecationWarning):
        c_helix_ak2 = p3.compute_helix(p_helix_np, library="ak")
    assert ak.all(np.isclose(c_helix_ak2, r_helix_np))

    with pytest.warns(DeprecationWarning):
        c_helix_np = p3.compute_helix(p_helix_np)
    assert np.all(np.isclose(c_helix_np, r_helix_np))


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
