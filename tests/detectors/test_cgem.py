import awkward as ak
import numpy as np
import pytest

import pybes3 as p3
from pybes3.detectors import cgem


def test_cgem_idx_conversion(cgem_idx_dict):
    ref_idx = cgem_idx_dict["idx"]
    ref_layer = cgem_idx_dict["layer"]
    ref_sheet = cgem_idx_dict["sheet"]
    ref_strip_type = cgem_idx_dict["strip_type"]
    ref_strip = cgem_idx_dict["strip"]

    assert np.all(p3.cgem_idx_to_layer(ref_idx) == ref_layer)
    assert np.all(p3.cgem_idx_to_sheet(ref_idx) == ref_sheet)
    assert np.all(p3.cgem_idx_to_strip_type(ref_idx) == ref_strip_type)
    assert np.all(p3.cgem_idx_to_strip(ref_idx) == ref_strip)
    assert np.all(p3.cgem_idx_to_is_xstrip(ref_idx) == (ref_strip_type == cgem.X_STRIP_TYPE))
    assert np.all(p3.cgem_idx_to_is_vstrip(ref_idx) == (ref_strip_type == cgem.V_STRIP_TYPE))
    assert np.all(p3.get_cgem_idx(ref_layer, ref_sheet, ref_strip_type, ref_strip) == ref_idx)


def test_cgem_parse_idx(cgem_idx_dict):
    ref_layer = cgem_idx_dict["layer"]
    ref_sheet = cgem_idx_dict["sheet"]
    ref_strip_type = cgem_idx_dict["strip_type"]
    ref_strip = cgem_idx_dict["strip"]

    # scalar
    for tmp_idx in range(cgem.N_STRIPS):
        tmp_res = p3.parse_cgem_idx(tmp_idx)
        assert tmp_res["layer"] == ref_layer[tmp_idx]
        assert tmp_res["sheet"] == ref_sheet[tmp_idx]
        assert tmp_res["strip_type"] == ref_strip_type[tmp_idx]
        assert tmp_res["strip"] == ref_strip[tmp_idx]
        assert tmp_res["is_xstrip"] == (ref_strip_type[tmp_idx] == cgem.X_STRIP_TYPE)
        assert tmp_res["is_vstrip"] == (ref_strip_type[tmp_idx] == cgem.V_STRIP_TYPE)

    # numpy
    np_idx = np.arange(cgem.N_STRIPS)
    np_res = p3.parse_cgem_idx(np_idx)
    assert np.all(np_res["layer"] == ref_layer)
    assert np.all(np_res["sheet"] == ref_sheet)
    assert np.all(np_res["strip_type"] == ref_strip_type)
    assert np.all(np_res["strip"] == ref_strip)
    assert np.all(np_res["is_xstrip"] == (ref_strip_type == cgem.X_STRIP_TYPE))
    assert np.all(np_res["is_vstrip"] == (ref_strip_type == cgem.V_STRIP_TYPE))

    # awkward
    ak_idx = ak.Array(np_idx)
    ak_res = p3.parse_cgem_idx(ak_idx)
    assert ak_res.fields == ["layer", "sheet", "strip_type", "strip", "is_xstrip", "is_vstrip"]
    assert ak.all(ak_res["layer"] == ref_layer)
    assert ak.all(ak_res["sheet"] == ref_sheet)
    assert ak.all(ak_res["strip_type"] == ref_strip_type)
    assert ak.all(ak_res["strip"] == ref_strip)
    assert ak.all(ak_res["is_xstrip"] == (ref_strip_type == cgem.X_STRIP_TYPE))
    assert ak.all(ak_res["is_vstrip"] == (ref_strip_type == cgem.V_STRIP_TYPE))


# =============================================================================
# Deprecated gid aliases
# =============================================================================


def test_cgem_gid_deprecated_aliases():
    """Deprecated `*_gid_*` names should still work and emit DeprecationWarning."""
    layer, sheet, strip_type, strip = 0, 0, cgem.X_STRIP_TYPE, 1

    with pytest.deprecated_call():
        gid = p3.get_cgem_gid(layer, sheet, strip_type, strip)
    assert gid == p3.get_cgem_idx(layer, sheet, strip_type, strip)

    with pytest.deprecated_call():
        assert p3.cgem_gid_to_layer(gid) == p3.cgem_idx_to_layer(gid)
    with pytest.deprecated_call():
        assert p3.cgem_gid_to_sheet(gid) == p3.cgem_idx_to_sheet(gid)
    with pytest.deprecated_call():
        assert p3.cgem_gid_to_strip_type(gid) == p3.cgem_idx_to_strip_type(gid)
    with pytest.deprecated_call():
        assert p3.cgem_gid_to_strip(gid) == p3.cgem_idx_to_strip(gid)
    with pytest.deprecated_call():
        assert p3.cgem_gid_to_is_xstrip(gid) == p3.cgem_idx_to_is_xstrip(gid)
    with pytest.deprecated_call():
        assert p3.cgem_gid_to_is_vstrip(gid) == p3.cgem_idx_to_is_vstrip(gid)
    with pytest.deprecated_call():
        parsed = p3.parse_cgem_gid(gid)
    assert dict(parsed) == dict(p3.parse_cgem_idx(gid))
