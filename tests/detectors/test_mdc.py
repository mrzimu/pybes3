import awkward as ak
import numpy as np

import pybes3 as p3
from pybes3.detectors import mdc


def test_mdc_geom():
    gid: np.ndarray = p3.get_mdc_geom_table()["gid"]
    assert np.all(p3.get_mdc_gid(mdc._layer, mdc._wire) == gid)
    assert np.all(p3.mdc_gid_to_superlayer(gid) == mdc._superlayer)
    assert np.all(p3.mdc_layer_to_superlayer(mdc._layer) == mdc._superlayer)
    assert np.all(p3.mdc_gid_to_layer(gid) == mdc._layer)
    assert np.all(p3.mdc_gid_to_wire(gid) == mdc._wire)
    assert np.all(p3.mdc_gid_to_stereo(gid) == mdc._stereo)
    assert np.all(p3.mdc_layer_to_is_stereo(mdc._layer) == mdc._is_stereo)
    assert np.all(p3.mdc_gid_to_is_stereo(gid) == mdc._is_stereo)
    assert np.all(p3.mdc_gid_to_east_x(gid) == mdc._east_x)
    assert np.all(p3.mdc_gid_to_east_y(gid) == mdc._east_y)
    assert np.all(p3.mdc_gid_to_east_z(gid) == mdc._east_z)
    assert np.all(p3.mdc_gid_to_west_x(gid) == mdc._west_x)
    assert np.all(p3.mdc_gid_to_west_y(gid) == mdc._west_y)
    assert np.all(p3.mdc_gid_to_west_z(gid) == mdc._west_z)

    assert np.allclose(p3.mdc_gid_z_to_x(gid, mdc._west_z), mdc._west_x, atol=1e-6)
    assert np.allclose(p3.mdc_gid_z_to_y(gid, mdc._west_z), mdc._west_y, atol=1e-6)
    assert np.allclose(p3.mdc_gid_z_to_x(gid, mdc._east_z), mdc._east_x, atol=1e-6)
    assert np.allclose(p3.mdc_gid_z_to_y(gid, mdc._east_z), mdc._east_y, atol=1e-6)


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
