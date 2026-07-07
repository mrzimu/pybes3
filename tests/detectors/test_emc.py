import awkward as ak
import numpy as np
import pytest

import pybes3 as p3
from pybes3.detectors import emc


def test_emc_geom():
    gid: np.ndarray = p3.get_emc_geom_table()["gid"]
    assert np.all(p3.get_emc_gid(emc._part, emc._theta, emc._phi) == gid)
    assert np.all(p3.emc_gid_to_part(gid) == emc._part)
    assert np.all(p3.emc_gid_to_theta(gid) == emc._theta)
    assert np.all(p3.emc_gid_to_phi(gid) == emc._phi)

    for i in range(8):
        assert np.all(p3.emc_gid_to_point_x(gid, i) == emc._points_x[gid, i])
        assert np.all(p3.emc_gid_to_point_y(gid, i) == emc._points_y[gid, i])
        assert np.all(p3.emc_gid_to_point_z(gid, i) == emc._points_z[gid, i])

    assert np.allclose(p3.emc_gid_to_center_x(gid), emc._center_x, atol=1e-6)
    assert np.allclose(p3.emc_gid_to_center_y(gid), emc._center_y, atol=1e-6)
    assert np.allclose(p3.emc_gid_to_center_z(gid), emc._center_z, atol=1e-6)
    assert np.allclose(p3.emc_gid_to_front_center_x(gid), emc._front_center_x, atol=1e-6)
    assert np.allclose(p3.emc_gid_to_front_center_y(gid), emc._front_center_y, atol=1e-6)
    assert np.allclose(p3.emc_gid_to_front_center_z(gid), emc._front_center_z, atol=1e-6)


def test_parse_emc_gid():
    np_gid = p3.get_emc_geom_table()["gid"]
    ak_gid = ak.Array(np_gid)
    emc_fields = [
        "gid",
        "part",
        "theta",
        "phi",
        "front_center_x",
        "front_center_y",
        "front_center_z",
        "center_x",
        "center_y",
        "center_z",
    ]

    ak_res1 = emc.parse_emc_gid(ak_gid, geometry=True)
    assert ak_res1.fields == emc_fields

    ak_res2 = emc.parse_emc_gid(ak_gid, geometry=False)
    assert ak_res2.fields == ["gid", "part", "theta", "phi"]

    np_res1 = emc.parse_emc_gid(np_gid, geometry=True)
    assert list(np_res1.keys()) == emc_fields

    np_res2 = emc.parse_emc_gid(np_gid, geometry=False)
    assert list(np_res2.keys()) == ["gid", "part", "theta", "phi"]


# =============================================================================
# Boundary checks
# =============================================================================


class TestEmcGidBoundary:
    """Test that _check_gid raises ValueError for out-of-range gid."""

    FUNCS = [
        p3.emc_gid_to_part,
        p3.emc_gid_to_theta,
        p3.emc_gid_to_phi,
        p3.emc_gid_to_center_x,
        p3.emc_gid_to_center_y,
        p3.emc_gid_to_center_z,
        p3.emc_gid_to_front_center_x,
        p3.emc_gid_to_front_center_y,
        p3.emc_gid_to_front_center_z,
        emc.parse_emc_gid,
    ]

    # --- scalar ---

    @pytest.mark.parametrize("func", FUNCS)
    def test_scalar_negative(self, func):
        with pytest.raises(ValueError, match="gid"):
            func(-1)

    @pytest.mark.parametrize("func", FUNCS)
    def test_scalar_at_max(self, func):
        with pytest.raises(ValueError, match="gid"):
            func(emc.N_CRYSTALS)

    @pytest.mark.parametrize("func", FUNCS)
    def test_scalar_valid_boundary(self, func):
        """0 and N_CRYSTALS-1 should not raise."""
        func(0)
        func(emc.N_CRYSTALS - 1)

    # --- numpy ---

    @pytest.mark.parametrize("func", FUNCS)
    def test_numpy_contains_negative(self, func):
        arr = np.array([0, 1, -1, 2])
        with pytest.raises(ValueError, match="gid"):
            func(arr)

    @pytest.mark.parametrize("func", FUNCS)
    def test_numpy_contains_at_max(self, func):
        arr = np.array([0, 1, emc.N_CRYSTALS, 2])
        with pytest.raises(ValueError, match="gid"):
            func(arr)

    @pytest.mark.parametrize("func", FUNCS)
    def test_numpy_all_valid(self, func):
        arr = np.array([0, emc.N_CRYSTALS - 1, 100])
        func(arr)  # should not raise

    # --- awkward ---

    @pytest.mark.parametrize("func", FUNCS)
    def test_awkward_contains_negative(self, func):
        arr = ak.Array([0, 1, -1, 2])
        with pytest.raises(ValueError, match="gid"):
            func(arr)

    @pytest.mark.parametrize("func", FUNCS)
    def test_awkward_contains_at_max(self, func):
        arr = ak.Array([0, 1, emc.N_CRYSTALS, 2])
        with pytest.raises(ValueError, match="gid"):
            func(arr)

    @pytest.mark.parametrize("func", FUNCS)
    def test_awkward_all_valid(self, func):
        arr = ak.Array([0, emc.N_CRYSTALS - 1, 100])
        func(arr)  # should not raise


class TestEmcPointBoundary:
    """Test that _check_point raises ValueError for out-of-range point."""

    FUNCS = [
        p3.emc_gid_to_point_x,
        p3.emc_gid_to_point_y,
        p3.emc_gid_to_point_z,
    ]

    # --- scalar gid, scalar point ---

    @pytest.mark.parametrize("func", FUNCS)
    def test_scalar_point_negative(self, func):
        with pytest.raises(ValueError, match="point"):
            func(0, -1)

    @pytest.mark.parametrize("func", FUNCS)
    def test_scalar_point_at_max(self, func):
        with pytest.raises(ValueError, match="point"):
            func(0, 8)

    @pytest.mark.parametrize("func", FUNCS)
    def test_scalar_point_valid_boundary(self, func):
        """0 and 7 should not raise."""
        func(0, 0)
        func(0, 7)

    # --- scalar gid, numpy point ---

    @pytest.mark.parametrize("func", FUNCS)
    def test_numpy_point_contains_negative(self, func):
        pts = np.array([0, 1, -1, 2])
        with pytest.raises(ValueError, match="point"):
            func(0, pts)

    @pytest.mark.parametrize("func", FUNCS)
    def test_numpy_point_contains_at_max(self, func):
        pts = np.array([0, 1, 8, 2])
        with pytest.raises(ValueError, match="point"):
            func(0, pts)

    @pytest.mark.parametrize("func", FUNCS)
    def test_numpy_point_all_valid(self, func):
        pts = np.array([0, 7, 3])
        func(0, pts)  # should not raise

    # --- scalar gid, awkward point ---

    @pytest.mark.parametrize("func", FUNCS)
    def test_awkward_point_contains_negative(self, func):
        pts = ak.Array([0, 1, -1, 2])
        with pytest.raises(ValueError, match="point"):
            func(0, pts)

    @pytest.mark.parametrize("func", FUNCS)
    def test_awkward_point_contains_at_max(self, func):
        pts = ak.Array([0, 1, 8, 2])
        with pytest.raises(ValueError, match="point"):
            func(0, pts)

    @pytest.mark.parametrize("func", FUNCS)
    def test_awkward_point_all_valid(self, func):
        pts = ak.Array([0, 7, 3])
        func(0, pts)  # should not raise

    # --- gid also checked ---

    @pytest.mark.parametrize("func", FUNCS)
    def test_scalar_gid_negative(self, func):
        with pytest.raises(ValueError, match="gid"):
            func(-1, 0)

    @pytest.mark.parametrize("func", FUNCS)
    def test_scalar_gid_at_max(self, func):
        with pytest.raises(ValueError, match="gid"):
            func(emc.N_CRYSTALS, 0)
