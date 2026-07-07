import awkward as ak
import numpy as np
import pytest

import pybes3 as p3
from pybes3.detectors import mdc


def test_mdc_index():
    geom_table = p3.get_mdc_geom_table()
    ref_gid = geom_table["gid"]
    ref_layer = geom_table["layer"]
    ref_wire = geom_table["wire"]

    assert np.all(p3.get_mdc_gid(ref_layer, ref_wire) == ref_gid)
    assert np.all(p3.mdc_gid_to_layer(ref_gid) == ref_layer)
    assert np.all(p3.mdc_gid_to_wire(ref_gid) == ref_wire)
    assert np.all(p3.mdc_layer_to_superlayer(ref_layer) == geom_table["superlayer"])
    assert np.all(p3.mdc_gid_to_superlayer(ref_gid) == geom_table["superlayer"])
    assert np.all(p3.mdc_gid_to_stereo(ref_gid) == geom_table["stereo"])
    assert np.all(p3.mdc_layer_to_is_stereo(ref_layer) == geom_table["is_stereo"])
    assert np.all(p3.mdc_gid_to_is_stereo(ref_gid) == geom_table["is_stereo"])
    assert np.all(p3.mdc_gid_to_east_x(ref_gid) == geom_table["east_x"])
    assert np.all(p3.mdc_gid_to_east_y(ref_gid) == geom_table["east_y"])
    assert np.all(p3.mdc_gid_to_east_z(ref_gid) == geom_table["east_z"])
    assert np.all(p3.mdc_gid_to_west_x(ref_gid) == geom_table["west_x"])
    assert np.all(p3.mdc_gid_to_west_y(ref_gid) == geom_table["west_y"])
    assert np.all(p3.mdc_gid_to_west_z(ref_gid) == geom_table["west_z"])

    assert np.allclose(
        p3.mdc_gid_z_to_x(ref_gid, geom_table["west_z"]),
        geom_table["west_x"],
        atol=1e-6,
    )
    assert np.allclose(
        p3.mdc_gid_z_to_y(ref_gid, geom_table["west_z"]),
        geom_table["west_y"],
        atol=1e-6,
    )
    assert np.allclose(
        p3.mdc_gid_z_to_x(ref_gid, geom_table["east_z"]),
        geom_table["east_x"],
        atol=1e-6,
    )
    assert np.allclose(
        p3.mdc_gid_z_to_y(ref_gid, geom_table["east_z"]),
        geom_table["east_y"],
        atol=1e-6,
    )


def test_mdc_parse_gid():
    np_gid = p3.get_mdc_geom_table()["gid"]
    ak_gid = ak.Array(np_gid)
    mdc_fields = [
        "gid",
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

    ak_res1 = p3.parse_mdc_gid(ak_gid, geometry=True)
    assert ak_res1.fields == mdc_fields

    ak_res2 = p3.parse_mdc_gid(ak_gid, geometry=False)
    assert ak_res2.fields == [
        "gid",
        "layer",
        "wire",
        "stereo",
        "is_stereo",
        "superlayer",
    ]

    np_res1 = p3.parse_mdc_gid(np_gid, geometry=True)
    assert list(np_res1.keys()) == mdc_fields

    np_res2 = p3.parse_mdc_gid(np_gid, geometry=False)
    assert list(np_res2.keys()) == [
        "gid",
        "layer",
        "wire",
        "stereo",
        "is_stereo",
        "superlayer",
    ]


# =============================================================================
# Boundary checks
# =============================================================================


class TestMdcGidBoundary:
    """Test that _check_gid raises ValueError for out-of-range gid."""

    # Functions that take only gid
    FUNCS = [
        p3.mdc_gid_to_superlayer,
        p3.mdc_gid_to_layer,
        p3.mdc_gid_to_wire,
        p3.mdc_gid_to_stereo,
        p3.mdc_gid_to_is_stereo,
        p3.mdc_gid_to_west_x,
        p3.mdc_gid_to_west_y,
        p3.mdc_gid_to_west_z,
        p3.mdc_gid_to_east_x,
        p3.mdc_gid_to_east_y,
        p3.mdc_gid_to_east_z,
        p3.parse_mdc_gid,
    ]

    # --- scalar ---

    @pytest.mark.parametrize("func", FUNCS)
    def test_scalar_negative(self, func):
        with pytest.raises(ValueError, match="gid"):
            func(-1)

    @pytest.mark.parametrize("func", FUNCS)
    def test_scalar_at_max(self, func):
        with pytest.raises(ValueError, match="gid"):
            func(mdc.N_WIRES)

    @pytest.mark.parametrize("func", FUNCS)
    def test_scalar_valid_boundary(self, func):
        """0 and N_WIRES-1 should not raise."""
        func(0)
        func(mdc.N_WIRES - 1)

    # --- numpy ---

    @pytest.mark.parametrize("func", FUNCS)
    def test_numpy_contains_negative(self, func):
        arr = np.array([0, 1, -1, 2])
        with pytest.raises(ValueError, match="gid"):
            func(arr)

    @pytest.mark.parametrize("func", FUNCS)
    def test_numpy_contains_at_max(self, func):
        arr = np.array([0, 1, mdc.N_WIRES, 2])
        with pytest.raises(ValueError, match="gid"):
            func(arr)

    @pytest.mark.parametrize("func", FUNCS)
    def test_numpy_all_valid(self, func):
        arr = np.array([0, mdc.N_WIRES - 1, 100])
        func(arr)  # should not raise

    # --- awkward ---

    @pytest.mark.parametrize("func", FUNCS)
    def test_awkward_contains_negative(self, func):
        arr = ak.Array([0, 1, -1, 2])
        with pytest.raises(ValueError, match="gid"):
            func(arr)

    @pytest.mark.parametrize("func", FUNCS)
    def test_awkward_contains_at_max(self, func):
        arr = ak.Array([0, 1, mdc.N_WIRES, 2])
        with pytest.raises(ValueError, match="gid"):
            func(arr)

    @pytest.mark.parametrize("func", FUNCS)
    def test_awkward_all_valid(self, func):
        arr = ak.Array([0, mdc.N_WIRES - 1, 100])
        func(arr)  # should not raise

    # --- mdc_gid_z_to_x/y have gid as first arg (z is unchecked) ---

    def test_z_to_x_scalar_gid_negative(self):
        with pytest.raises(ValueError, match="gid"):
            p3.mdc_gid_z_to_x(-1, 0.0)

    def test_z_to_y_scalar_gid_at_max(self):
        with pytest.raises(ValueError, match="gid"):
            p3.mdc_gid_z_to_y(mdc.N_WIRES, 0.0)


class TestMdcLayerBoundary:
    """Test that _check_layer raises ValueError for out-of-range layer.

    Layer is 0-indexed, valid range is [0, N_LAYERS) = [0, 43).
    """

    FUNCS = [
        p3.mdc_layer_to_superlayer,
        p3.mdc_layer_to_is_stereo,
    ]

    # --- scalar ---

    @pytest.mark.parametrize("func", FUNCS)
    def test_scalar_below_min(self, func):
        with pytest.raises(ValueError, match="layer"):
            func(-1)

    @pytest.mark.parametrize("func", FUNCS)
    def test_scalar_at_max(self, func):
        with pytest.raises(ValueError, match="layer"):
            func(mdc.N_LAYERS)

    @pytest.mark.parametrize("func", FUNCS)
    def test_scalar_valid_boundary(self, func):
        """0 and N_LAYERS-1 should not raise."""
        func(0)
        func(mdc.N_LAYERS - 1)

    # --- numpy ---

    @pytest.mark.parametrize("func", FUNCS)
    def test_numpy_contains_below_min(self, func):
        arr = np.array([1, 2, -1, 3])
        with pytest.raises(ValueError, match="layer"):
            func(arr)

    @pytest.mark.parametrize("func", FUNCS)
    def test_numpy_contains_at_max(self, func):
        arr = np.array([1, 2, mdc.N_LAYERS, 3])
        with pytest.raises(ValueError, match="layer"):
            func(arr)

    @pytest.mark.parametrize("func", FUNCS)
    def test_numpy_all_valid(self, func):
        arr = np.array([0, mdc.N_LAYERS - 1, 20])
        func(arr)  # should not raise

    # --- awkward ---

    @pytest.mark.parametrize("func", FUNCS)
    def test_awkward_contains_below_min(self, func):
        arr = ak.Array([1, 2, -1, 3])
        with pytest.raises(ValueError, match="layer"):
            func(arr)

    @pytest.mark.parametrize("func", FUNCS)
    def test_awkward_contains_at_max(self, func):
        arr = ak.Array([1, 2, mdc.N_LAYERS, 3])
        with pytest.raises(ValueError, match="layer"):
            func(arr)

    @pytest.mark.parametrize("func", FUNCS)
    def test_awkward_all_valid(self, func):
        arr = ak.Array([0, mdc.N_LAYERS - 1, 20])
        func(arr)  # should not raise
