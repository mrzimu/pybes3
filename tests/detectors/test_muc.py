import awkward as ak
import numpy as np

import pybes3 as p3
from pybes3 import muc


def test_muc_geom():
    geom = p3.get_muc_geom_table()
    gid = np.arange(muc.N_STRIPS)
    assert np.all(geom["gid"] == gid)
    assert np.all(p3.get_muc_gid(muc._part, muc._segment, muc._layer, muc._strip) == gid)
    assert np.all(p3.muc_gid_to_part(gid) == muc._part)
    assert np.all(p3.muc_gid_to_segment(gid) == muc._segment)
    assert np.all(p3.muc_gid_to_layer(gid) == muc._layer)
    assert np.all(p3.muc_gid_to_strip(gid) == muc._strip)

    for i in range(8):
        assert np.all(p3.muc_gid_to_point_x(gid, i) == muc._points_x[gid, i])
        assert np.all(p3.muc_gid_to_point_y(gid, i) == muc._points_y[gid, i])
        assert np.all(p3.muc_gid_to_point_z(gid, i) == muc._points_z[gid, i])

    assert np.allclose(p3.muc_gid_to_center_x(gid), muc._center_x, atol=1e-6)
    assert np.allclose(p3.muc_gid_to_center_y(gid), muc._center_y, atol=1e-6)
    assert np.allclose(p3.muc_gid_to_center_z(gid), muc._center_z, atol=1e-6)
    assert np.allclose(p3.muc_gid_to_dx(gid), muc._dx, atol=1e-6)
    assert np.allclose(p3.muc_gid_to_dy(gid), muc._dy, atol=1e-6)
    assert np.allclose(p3.muc_gid_to_dz(gid), muc._dz, atol=1e-6)

    p3.get_muc_geom_table(library="np")
    p3.get_muc_geom_table(library="ak")
    p3.get_muc_geom_table(library="pd")


def test_parse_muc_gid():
    np_gid = p3.get_muc_geom_table()["gid"]
    ak_gid = ak.Array(np_gid)
    muc_fields = [
        "gid",
        "part",
        "segment",
        "layer",
        "strip",
        "center_x",
        "center_y",
        "center_z",
        "dx",
        "dy",
        "dz",
    ]

    ak_res1 = muc.parse_muc_gid(ak_gid, geometry=True)
    assert ak_res1.fields == muc_fields

    ak_res2 = muc.parse_muc_gid(ak_gid, geometry=False)
    assert ak_res2.fields == ["gid", "part", "segment", "layer", "strip"]

    np_res1 = muc.parse_muc_gid(np_gid, geometry=True)
    assert list(np_res1.keys()) == muc_fields

    np_res2 = muc.parse_muc_gid(np_gid, geometry=False)
    assert list(np_res2.keys()) == ["gid", "part", "segment", "layer", "strip"]
