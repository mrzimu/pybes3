import awkward as ak
import numpy as np
import pytest

import pybes3 as p3


def test_mdc_index():
    geom_table = p3.get_mdc_geom_table()
    ref_idx = geom_table["idx"]
    ref_layer = geom_table["layer"]
    ref_wire = geom_table["wire"]

    assert np.all(p3.get_mdc_idx(ref_layer, ref_wire) == ref_idx)
    assert np.all(p3.mdc_idx_to_layer(ref_idx) == ref_layer)
    assert np.all(p3.mdc_idx_to_wire(ref_idx) == ref_wire)
    assert np.all(p3.mdc_layer_to_superlayer(ref_layer) == geom_table["superlayer"])
    assert np.all(p3.mdc_idx_to_superlayer(ref_idx) == geom_table["superlayer"])
    assert np.all(p3.mdc_idx_to_stereo(ref_idx) == geom_table["stereo"])
    assert np.all(p3.mdc_layer_to_is_stereo(ref_layer) == geom_table["is_stereo"])
    assert np.all(p3.mdc_idx_to_is_stereo(ref_idx) == geom_table["is_stereo"])
    assert np.all(p3.mdc_idx_to_east_x(ref_idx) == geom_table["east_x"])
    assert np.all(p3.mdc_idx_to_east_y(ref_idx) == geom_table["east_y"])
    assert np.all(p3.mdc_idx_to_east_z(ref_idx) == geom_table["east_z"])
    assert np.all(p3.mdc_idx_to_west_x(ref_idx) == geom_table["west_x"])
    assert np.all(p3.mdc_idx_to_west_y(ref_idx) == geom_table["west_y"])
    assert np.all(p3.mdc_idx_to_west_z(ref_idx) == geom_table["west_z"])

    assert np.allclose(
        p3.mdc_idx_z_to_x(ref_idx, geom_table["west_z"]),
        geom_table["west_x"],
        atol=1e-6,
    )
    assert np.allclose(
        p3.mdc_idx_z_to_y(ref_idx, geom_table["west_z"]),
        geom_table["west_y"],
        atol=1e-6,
    )
    assert np.allclose(
        p3.mdc_idx_z_to_x(ref_idx, geom_table["east_z"]),
        geom_table["east_x"],
        atol=1e-6,
    )
    assert np.allclose(
        p3.mdc_idx_z_to_y(ref_idx, geom_table["east_z"]),
        geom_table["east_y"],
        atol=1e-6,
    )


def test_mdc_parse_idx():
    np_idx = p3.get_mdc_geom_table()["idx"]
    ak_idx = ak.Array(np_idx)
    mdc_fields = [
        "idx",
        "layer",
        "wire",
        "stereo",
        "is_stereo",
        "superlayer",
        "mid_x",
        "mid_y",
        "west_x",
        "west_y",
        "west_z",
        "east_x",
        "east_y",
        "east_z",
    ]

    ak_res1 = p3.parse_mdc_idx(ak_idx, geometry=True)
    assert ak_res1.fields == mdc_fields

    ak_res2 = p3.parse_mdc_idx(ak_idx, geometry=False)
    assert ak_res2.fields == [
        "idx",
        "layer",
        "wire",
        "stereo",
        "is_stereo",
        "superlayer",
    ]

    np_res1 = p3.parse_mdc_idx(np_idx, geometry=True)
    assert list(np_res1.keys()) == mdc_fields

    np_res2 = p3.parse_mdc_idx(np_idx, geometry=False)
    assert list(np_res2.keys()) == [
        "idx",
        "layer",
        "wire",
        "stereo",
        "is_stereo",
        "superlayer",
    ]


# =============================================================================
# Deprecated gid aliases
# =============================================================================


def test_mdc_gid_deprecated_aliases():
    """Deprecated `*_gid_*` names should still work and emit DeprecationWarning."""
    layer, wire = 1, 1

    with pytest.deprecated_call():
        gid = p3.get_mdc_gid(layer, wire)
    assert gid == p3.get_mdc_idx(layer, wire)

    with pytest.deprecated_call():
        assert p3.mdc_gid_to_layer(gid) == p3.mdc_idx_to_layer(gid)
    with pytest.deprecated_call():
        assert p3.mdc_gid_to_wire(gid) == p3.mdc_idx_to_wire(gid)
    with pytest.deprecated_call():
        assert p3.mdc_gid_to_superlayer(gid) == p3.mdc_idx_to_superlayer(gid)
    with pytest.deprecated_call():
        assert p3.mdc_gid_to_stereo(gid) == p3.mdc_idx_to_stereo(gid)
    with pytest.deprecated_call():
        assert p3.mdc_gid_to_is_stereo(gid) == p3.mdc_idx_to_is_stereo(gid)
    with pytest.deprecated_call():
        assert p3.mdc_gid_to_west_x(gid) == p3.mdc_idx_to_west_x(gid)
    with pytest.deprecated_call():
        assert p3.mdc_gid_to_west_y(gid) == p3.mdc_idx_to_west_y(gid)
    with pytest.deprecated_call():
        assert p3.mdc_gid_to_west_z(gid) == p3.mdc_idx_to_west_z(gid)
    with pytest.deprecated_call():
        assert p3.mdc_gid_to_east_x(gid) == p3.mdc_idx_to_east_x(gid)
    with pytest.deprecated_call():
        assert p3.mdc_gid_to_east_y(gid) == p3.mdc_idx_to_east_y(gid)
    with pytest.deprecated_call():
        assert p3.mdc_gid_to_east_z(gid) == p3.mdc_idx_to_east_z(gid)
    with pytest.deprecated_call():
        assert p3.mdc_gid_z_to_x(gid, 1.0) == p3.mdc_idx_z_to_x(gid, 1.0)
    with pytest.deprecated_call():
        assert p3.mdc_gid_z_to_y(gid, 1.0) == p3.mdc_idx_z_to_y(gid, 1.0)
    with pytest.deprecated_call():
        parsed = p3.parse_mdc_gid(gid)
    assert dict(parsed) == dict(p3.parse_mdc_idx(gid))
