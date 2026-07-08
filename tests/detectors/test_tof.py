from pathlib import Path

import awkward as ak
import numpy as np
import pytest
import uproot

import pybes3 as p3
from pybes3.detectors import tof


def test_tof_idx_conversion(tof_idx_dict):
    ref_idx = tof_idx_dict["gid"]
    ref_part = tof_idx_dict["part"]
    ref_layer_or_module = tof_idx_dict["layer_or_module"]
    ref_phi_or_strip = tof_idx_dict["phi_or_strip"]

    assert np.all(p3.tof_idx_to_part(ref_idx) == ref_part)
    assert np.all(p3.tof_idx_to_layer_or_module(ref_idx) == ref_layer_or_module)
    assert np.all(p3.tof_idx_to_phi_or_strip(ref_idx) == ref_phi_or_strip)
    assert np.all(p3.get_tof_idx(ref_part, ref_layer_or_module, ref_phi_or_strip) == ref_idx)


def test_tof_parse_idx(tof_idx_dict):
    ref_part = tof_idx_dict["part"]
    ref_layer_or_module = tof_idx_dict["layer_or_module"]
    ref_phi_or_strip = tof_idx_dict["phi_or_strip"]

    # scalar
    for tmp_idx in range(tof.N_STRIPS):
        tmp_res = p3.parse_tof_idx(tmp_idx)
        assert tmp_res["part"] == ref_part[tmp_idx]
        assert tmp_res["layer_or_module"] == ref_layer_or_module[tmp_idx]
        assert tmp_res["phi_or_strip"] == ref_phi_or_strip[tmp_idx]

    # numpy
    np_idx = np.arange(tof.N_STRIPS)
    np_res = p3.parse_tof_idx(np_idx)
    assert np.all(np_res["part"] == ref_part)
    assert np.all(np_res["layer_or_module"] == ref_layer_or_module)
    assert np.all(np_res["phi_or_strip"] == ref_phi_or_strip)

    # awkward
    ak_idx = ak.Array(np_idx)
    ak_res = p3.parse_tof_idx(ak_idx)
    assert ak_res.fields == ["part", "layer_or_module", "phi_or_strip"]
    assert ak.all(ak_res["part"] == ref_part)
    assert ak.all(ak_res["layer_or_module"] == ref_layer_or_module)
    assert ak.all(ak_res["phi_or_strip"] == ref_phi_or_strip)


# =============================================================================
# Deprecated gid aliases
# =============================================================================


def test_tof_gid_deprecated_aliases():
    """Deprecated `*_gid_*` names should still work and emit DeprecationWarning."""
    part, layer_or_module, phi_or_strip = 1, 0, 0

    with pytest.deprecated_call():
        gid = p3.get_tof_gid(part, layer_or_module, phi_or_strip)
    assert gid == p3.get_tof_idx(part, layer_or_module, phi_or_strip)

    with pytest.deprecated_call():
        assert p3.tof_gid_to_part(gid) == p3.tof_idx_to_part(gid)
    with pytest.deprecated_call():
        assert p3.tof_gid_to_layer_or_module(gid) == p3.tof_idx_to_layer_or_module(gid)
    with pytest.deprecated_call():
        assert p3.tof_gid_to_phi_or_strip(gid) == p3.tof_idx_to_phi_or_strip(gid)
    with pytest.deprecated_call():
        parsed = p3.parse_tof_gid(gid)
    assert dict(parsed) == dict(p3.parse_tof_idx(gid))


def test_tof_hit_status(test_data_dir: Path):
    raw_arr = uproot.open(test_data_dir / "ref_tof_hit_status.root")["tof_hit_status"].arrays()

    status = raw_arr["status"]

    fields = [
        "is_raw",
        "is_readout",
        "is_counter",
        "is_cluster",
        "is_barrel",
        "is_east",
        "is_overflow",
        "is_multihit",
        "is_mrpc",
        "layer",
        "n_counter",
        "n_east",
        "n_west",
    ]

    # awkward
    zipped = ak.zip({f: raw_arr[f] for f in fields})
    assert ak.array_equal(p3.parse_tof_hit_status(status), zipped, dtype_exact=False)

    # numpy
    flat_status = ak.flatten(status).to_numpy()
    flat_expected = {f: ak.flatten(raw_arr[f]).to_numpy() for f in fields}
    np_parsed = p3.parse_tof_hit_status(flat_status)
    for f in fields:
        assert np.array_equal(np_parsed[f], flat_expected[f])

    # scalar
    s = int(flat_status[0])
    scalar_parsed = p3.parse_tof_hit_status(s)
    for f in fields:
        assert scalar_parsed[f] == flat_expected[f][0]


# =============================================================================
# Boundary checks
# =============================================================================


class TestTofIdxBoundary:
    """Test that _check_idx raises ValueError for out-of-range idx."""

    FUNCS = [
        p3.tof_idx_to_part,
        p3.tof_idx_to_layer_or_module,
        p3.tof_idx_to_phi_or_strip,
        p3.parse_tof_idx,
    ]

    # --- scalar ---

    @pytest.mark.parametrize("func", FUNCS)
    def test_scalar_negative(self, func):
        with pytest.raises(ValueError, match="idx"):
            func(-1)

    @pytest.mark.parametrize("func", FUNCS)
    def test_scalar_at_max(self, func):
        with pytest.raises(ValueError, match="idx"):
            func(tof.N_STRIPS)

    @pytest.mark.parametrize("func", FUNCS)
    def test_scalar_valid_boundary(self, func):
        """0 and N_STRIPS-1 should not raise."""
        func(0)
        func(tof.N_STRIPS - 1)

    # --- numpy ---

    @pytest.mark.parametrize("func", FUNCS)
    def test_numpy_contains_negative(self, func):
        arr = np.array([0, 1, -1, 2])
        with pytest.raises(ValueError, match="idx"):
            func(arr)

    @pytest.mark.parametrize("func", FUNCS)
    def test_numpy_contains_at_max(self, func):
        arr = np.array([0, 1, tof.N_STRIPS, 2])
        with pytest.raises(ValueError, match="idx"):
            func(arr)

    @pytest.mark.parametrize("func", FUNCS)
    def test_numpy_all_valid(self, func):
        arr = np.array([0, tof.N_STRIPS - 1, 100])
        func(arr)  # should not raise

    # --- awkward ---

    @pytest.mark.parametrize("func", FUNCS)
    def test_awkward_contains_negative(self, func):
        arr = ak.Array([0, 1, -1, 2])
        with pytest.raises(ValueError, match="idx"):
            func(arr)

    @pytest.mark.parametrize("func", FUNCS)
    def test_awkward_contains_at_max(self, func):
        arr = ak.Array([0, 1, tof.N_STRIPS, 2])
        with pytest.raises(ValueError, match="idx"):
            func(arr)

    @pytest.mark.parametrize("func", FUNCS)
    def test_awkward_all_valid(self, func):
        arr = ak.Array([0, tof.N_STRIPS - 1, 100])
        func(arr)  # should not raise
