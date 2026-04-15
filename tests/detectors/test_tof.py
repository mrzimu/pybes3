import awkward as ak
import numpy as np

import pybes3 as p3
from pybes3.detectors import tof


def test_tof_gid_conversion(tof_gid_dict):
    ref_gid = tof_gid_dict["gid"]
    ref_part = tof_gid_dict["part"]
    ref_layer_or_module = tof_gid_dict["layer_or_module"]
    ref_phi_or_strip = tof_gid_dict["phi_or_strip"]

    assert np.all(p3.tof_gid_to_part(ref_gid) == ref_part)
    assert np.all(p3.tof_gid_to_layer_or_module(ref_gid) == ref_layer_or_module)
    assert np.all(p3.tof_gid_to_phi_or_strip(ref_gid) == ref_phi_or_strip)
    assert np.all(p3.get_tof_gid(ref_part, ref_layer_or_module, ref_phi_or_strip) == ref_gid)


def test_tof_parse_gid(tof_gid_dict):
    ref_part = tof_gid_dict["part"]
    ref_layer_or_module = tof_gid_dict["layer_or_module"]
    ref_phi_or_strip = tof_gid_dict["phi_or_strip"]

    # scalar
    for tmp_gid in range(tof.N_STRIPS):
        tmp_res = p3.parse_tof_gid(tmp_gid)
        assert tmp_res["part"] == ref_part[tmp_gid]
        assert tmp_res["layer_or_module"] == ref_layer_or_module[tmp_gid]
        assert tmp_res["phi_or_strip"] == ref_phi_or_strip[tmp_gid]

    # numpy
    np_gid = np.arange(tof.N_STRIPS)
    np_res = p3.parse_tof_gid(np_gid)
    assert np.all(np_res["part"] == ref_part)
    assert np.all(np_res["layer_or_module"] == ref_layer_or_module)
    assert np.all(np_res["phi_or_strip"] == ref_phi_or_strip)

    # awkward
    ak_gid = ak.Array(np_gid)
    ak_res = p3.parse_tof_gid(ak_gid)
    assert ak_res.fields == ["part", "layer_or_module", "phi_or_strip"]
    assert ak.all(ak_res["part"] == ref_part)
    assert ak.all(ak_res["layer_or_module"] == ref_layer_or_module)
    assert ak.all(ak_res["phi_or_strip"] == ref_phi_or_strip)
