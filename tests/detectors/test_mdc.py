import awkward as ak
import numpy as np

import pybes3 as p3


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
