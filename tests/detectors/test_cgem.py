import awkward as ak
import numpy as np

import pybes3 as p3
from pybes3.detectors import cgem


def test_cgem_gid_conversion(cgem_gid_dict):
    ref_gid = cgem_gid_dict["gid"]
    ref_layer = cgem_gid_dict["layer"]
    ref_sheet = cgem_gid_dict["sheet"]
    ref_strip_type = cgem_gid_dict["strip_type"]
    ref_strip = cgem_gid_dict["strip"]

    assert np.all(p3.cgem_gid_to_layer(ref_gid) == ref_layer)
    assert np.all(p3.cgem_gid_to_sheet(ref_gid) == ref_sheet)
    assert np.all(p3.cgem_gid_to_strip_type(ref_gid) == ref_strip_type)
    assert np.all(p3.cgem_gid_to_strip(ref_gid) == ref_strip)

    assert np.all(
        p3.cgem_gid_to_is_xstrip(ref_gid) == (ref_strip_type == cgem.X_STRIP_TYPE)
    )

    assert np.all(
        p3.cgem_gid_to_is_vstrip(ref_gid) == (ref_strip_type == cgem.V_STRIP_TYPE)
    )

    assert np.all(
        p3.get_cgem_gid(
            ref_layer,
            ref_sheet,
            ref_strip_type,
            ref_strip,
        )
        == ref_gid
    )


def test_cgem_parse_gid(cgem_gid_dict):
    ref_layer = cgem_gid_dict["layer"]
    ref_sheet = cgem_gid_dict["sheet"]
    ref_strip_type = cgem_gid_dict["strip_type"]
    ref_strip = cgem_gid_dict["strip"]

    # scalar
    for tmp_gid in range(cgem.N_STRIPS):
        tmp_res = p3.parse_cgem_gid(tmp_gid)
        assert tmp_res["layer"] == ref_layer[tmp_gid]
        assert tmp_res["sheet"] == ref_sheet[tmp_gid]
        assert tmp_res["strip_type"] == ref_strip_type[tmp_gid]
        assert tmp_res["strip"] == ref_strip[tmp_gid]
        assert tmp_res["is_xstrip"] == (ref_strip_type[tmp_gid] == cgem.X_STRIP_TYPE)
        assert tmp_res["is_vstrip"] == (ref_strip_type[tmp_gid] == cgem.V_STRIP_TYPE)

    # numpy
    np_gid = np.arange(cgem.N_STRIPS)
    np_res = p3.parse_cgem_gid(np_gid)
    assert np.all(np_res["layer"] == ref_layer)
    assert np.all(np_res["sheet"] == ref_sheet)
    assert np.all(np_res["strip_type"] == ref_strip_type)
    assert np.all(np_res["strip"] == ref_strip)
    assert np.all(np_res["is_xstrip"] == (ref_strip_type == cgem.X_STRIP_TYPE))
    assert np.all(np_res["is_vstrip"] == (ref_strip_type == cgem.V_STRIP_TYPE))

    # awkward
    ak_gid = ak.Array(np_gid)
    ak_res = p3.parse_cgem_gid(ak_gid)
    assert ak_res.fields == [
        "layer",
        "sheet",
        "strip_type",
        "strip",
        "is_xstrip",
        "is_vstrip",
    ]
    assert ak.all(ak_res["layer"] == ref_layer)
    assert ak.all(ak_res["sheet"] == ref_sheet)
    assert ak.all(ak_res["strip_type"] == ref_strip_type)
    assert ak.all(ak_res["strip"] == ref_strip)
    assert ak.all(ak_res["is_xstrip"] == (ref_strip_type == cgem.X_STRIP_TYPE))
    assert ak.all(ak_res["is_vstrip"] == (ref_strip_type == cgem.V_STRIP_TYPE))
