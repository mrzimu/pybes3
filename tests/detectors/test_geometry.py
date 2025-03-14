import awkward as ak
import numpy as np

import pybes3.detectors.geometry as geom
import pybes3.detectors as det


def test_mdc_geom():
    gid: np.ndarray = det.mdc_wire_position["gid"]
    assert np.all(det.mdc_layer_wire_to_gid(geom.layer, geom.wire) == gid)
    assert np.all(det.mdc_gid_to_layer(gid) == geom.layer)
    assert np.all(det.mdc_gid_to_wire(gid) == geom.wire)
    assert np.all(det.mdc_layer_to_is_stereo(geom.layer) == geom.is_stereo)
    assert np.all(det.mdc_gid_to_is_stereo(gid) == geom.is_stereo)
    assert np.all(det.mdc_gid_to_east_x(gid) == geom.east_x)
    assert np.all(det.mdc_gid_to_east_y(gid) == geom.east_y)
    assert np.all(det.mdc_gid_to_east_z(gid) == geom.east_z)
    assert np.all(det.mdc_gid_to_west_x(gid) == geom.west_x)
    assert np.all(det.mdc_gid_to_west_y(gid) == geom.west_y)
    assert np.all(det.mdc_gid_to_west_z(gid) == geom.west_z)

    assert np.allclose(det.mdc_gid_z_to_x(gid, geom.west_z), geom.west_x, atol=1e-6)
    assert np.allclose(det.mdc_gid_z_to_y(gid, geom.west_z), geom.west_y, atol=1e-6)
    assert np.allclose(det.mdc_gid_z_to_x(gid, geom.east_z), geom.east_x, atol=1e-6)
    assert np.allclose(det.mdc_gid_z_to_y(gid, geom.east_z), geom.east_y, atol=1e-6)


def test_mdc_parse_gid():
    np_gid = det.mdc_wire_position["gid"]
    ak_gid = ak.Array(np_gid)

    ak_res1 = geom.parse_mdc_gid(ak_gid)
    assert ak_res1.fields == [
        "gid",
        "layer",
        "wire",
        "is_stereo",
        "west_x",
        "west_y",
        "west_z",
        "east_x",
        "east_y",
        "east_z",
    ]

    ak_res2 = geom.parse_mdc_gid(ak_gid, with_pos=False)
    assert ak_res2.fields == ["gid", "layer", "wire", "is_stereo"]

    np_res1 = geom.parse_mdc_gid(np_gid)
    assert list(np_res1.keys()) == [
        "gid",
        "layer",
        "wire",
        "is_stereo",
        "west_x",
        "west_y",
        "west_z",
        "east_x",
        "east_y",
        "east_z",
    ]

    np_res2 = geom.parse_mdc_gid(np_gid, with_pos=False)
    assert list(np_res2.keys()) == ["gid", "layer", "wire", "is_stereo"]
