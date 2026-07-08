import awkward as ak
import numpy as np
import pytest

import pybes3 as p3
from pybes3.detectors import emc


def test_emc_geom():
    idx: np.ndarray = p3.get_emc_geom_table()["idx"]
    assert np.all(p3.get_emc_idx(emc._part, emc._theta, emc._phi) == idx)
    assert np.all(p3.emc_idx_to_part(idx) == emc._part)
    assert np.all(p3.emc_idx_to_theta(idx) == emc._theta)
    assert np.all(p3.emc_idx_to_phi(idx) == emc._phi)

    for i in range(8):
        assert np.all(p3.emc_idx_to_point_x(idx, i) == emc._points_x[idx, i])
        assert np.all(p3.emc_idx_to_point_y(idx, i) == emc._points_y[idx, i])
        assert np.all(p3.emc_idx_to_point_z(idx, i) == emc._points_z[idx, i])

    assert np.allclose(p3.emc_idx_to_center_x(idx), emc._center_x, atol=1e-6)
    assert np.allclose(p3.emc_idx_to_center_y(idx), emc._center_y, atol=1e-6)
    assert np.allclose(p3.emc_idx_to_center_z(idx), emc._center_z, atol=1e-6)
    assert np.allclose(p3.emc_idx_to_front_center_x(idx), emc._front_center_x, atol=1e-6)
    assert np.allclose(p3.emc_idx_to_front_center_y(idx), emc._front_center_y, atol=1e-6)
    assert np.allclose(p3.emc_idx_to_front_center_z(idx), emc._front_center_z, atol=1e-6)


def test_parse_emc_idx():
    np_idx = p3.get_emc_geom_table()["idx"]
    ak_idx = ak.Array(np_idx)
    emc_fields = [
        "idx",
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

    ak_res1 = emc.parse_emc_idx(ak_idx, geometry=True)
    assert ak_res1.fields == emc_fields

    ak_res2 = emc.parse_emc_idx(ak_idx, geometry=False)
    assert ak_res2.fields == ["idx", "part", "theta", "phi"]

    np_res1 = emc.parse_emc_idx(np_idx, geometry=True)
    assert list(np_res1.keys()) == emc_fields

    np_res2 = emc.parse_emc_idx(np_idx, geometry=False)
    assert list(np_res2.keys()) == ["idx", "part", "theta", "phi"]


# =============================================================================
# Deprecated gid aliases
# =============================================================================


def test_emc_gid_deprecated_aliases():
    """Deprecated `*_gid_*` names should still work and emit DeprecationWarning."""
    part, theta, phi = 1, 0, 0

    with pytest.deprecated_call():
        gid = p3.get_emc_gid(part, theta, phi)
    assert gid == p3.get_emc_idx(part, theta, phi)

    with pytest.deprecated_call():
        assert p3.emc_gid_to_part(gid) == p3.emc_idx_to_part(gid)
    with pytest.deprecated_call():
        assert p3.emc_gid_to_theta(gid) == p3.emc_idx_to_theta(gid)
    with pytest.deprecated_call():
        assert p3.emc_gid_to_phi(gid) == p3.emc_idx_to_phi(gid)
    with pytest.deprecated_call():
        assert p3.emc_gid_to_point_x(gid, 0) == p3.emc_idx_to_point_x(gid, 0)
    with pytest.deprecated_call():
        assert p3.emc_gid_to_point_y(gid, 0) == p3.emc_idx_to_point_y(gid, 0)
    with pytest.deprecated_call():
        assert p3.emc_gid_to_point_z(gid, 0) == p3.emc_idx_to_point_z(gid, 0)
    with pytest.deprecated_call():
        assert p3.emc_gid_to_center_x(gid) == p3.emc_idx_to_center_x(gid)
    with pytest.deprecated_call():
        assert p3.emc_gid_to_center_y(gid) == p3.emc_idx_to_center_y(gid)
    with pytest.deprecated_call():
        assert p3.emc_gid_to_center_z(gid) == p3.emc_idx_to_center_z(gid)
    with pytest.deprecated_call():
        assert p3.emc_gid_to_front_center_x(gid) == p3.emc_idx_to_front_center_x(gid)
    with pytest.deprecated_call():
        assert p3.emc_gid_to_front_center_y(gid) == p3.emc_idx_to_front_center_y(gid)
    with pytest.deprecated_call():
        assert p3.emc_gid_to_front_center_z(gid) == p3.emc_idx_to_front_center_z(gid)
    with pytest.deprecated_call():
        parsed = emc.parse_emc_gid(gid)
    assert dict(parsed) == dict(emc.parse_emc_idx(gid))


# =============================================================================
# Boundary checks
# =============================================================================


class TestEmcIdxBoundary:
    """Test that _check_idx raises ValueError for out-of-range idx."""

    FUNCS = [
        p3.emc_idx_to_part,
        p3.emc_idx_to_theta,
        p3.emc_idx_to_phi,
        p3.emc_idx_to_center_x,
        p3.emc_idx_to_center_y,
        p3.emc_idx_to_center_z,
        p3.emc_idx_to_front_center_x,
        p3.emc_idx_to_front_center_y,
        p3.emc_idx_to_front_center_z,
        emc.parse_emc_idx,
    ]

    # --- scalar ---

    @pytest.mark.parametrize("func", FUNCS)
    def test_scalar_negative(self, func):
        with pytest.raises(ValueError, match="idx"):
            func(-1)

    @pytest.mark.parametrize("func", FUNCS)
    def test_scalar_at_max(self, func):
        with pytest.raises(ValueError, match="idx"):
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
        with pytest.raises(ValueError, match="idx"):
            func(arr)

    @pytest.mark.parametrize("func", FUNCS)
    def test_numpy_contains_at_max(self, func):
        arr = np.array([0, 1, emc.N_CRYSTALS, 2])
        with pytest.raises(ValueError, match="idx"):
            func(arr)

    @pytest.mark.parametrize("func", FUNCS)
    def test_numpy_all_valid(self, func):
        arr = np.array([0, emc.N_CRYSTALS - 1, 100])
        func(arr)  # should not raise

    # --- awkward ---

    @pytest.mark.parametrize("func", FUNCS)
    def test_awkward_contains_negative(self, func):
        arr = ak.Array([0, 1, -1, 2])
        with pytest.raises(ValueError, match="idx"):
            func(arr)

    @pytest.mark.parametrize("func", FUNCS)
    def test_awkward_contains_at_max(self, func):
        arr = ak.Array([0, 1, emc.N_CRYSTALS, 2])
        with pytest.raises(ValueError, match="idx"):
            func(arr)

    @pytest.mark.parametrize("func", FUNCS)
    def test_awkward_all_valid(self, func):
        arr = ak.Array([0, emc.N_CRYSTALS - 1, 100])
        func(arr)  # should not raise


class TestEmcPointBoundary:
    """Test that _check_point raises ValueError for out-of-range point."""

    FUNCS = [
        p3.emc_idx_to_point_x,
        p3.emc_idx_to_point_y,
        p3.emc_idx_to_point_z,
    ]

    # --- scalar idx, scalar point ---

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

    # --- scalar idx, numpy point ---

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

    # --- scalar idx, awkward point ---

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

    # --- idx also checked ---

    @pytest.mark.parametrize("func", FUNCS)
    def test_scalar_idx_negative(self, func):
        with pytest.raises(ValueError, match="idx"):
            func(-1, 0)

    @pytest.mark.parametrize("func", FUNCS)
    def test_scalar_idx_at_max(self, func):
        with pytest.raises(ValueError, match="idx"):
            func(emc.N_CRYSTALS, 0)
