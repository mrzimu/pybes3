import numpy as np

import pybes3.detectors.geometry as geom


def test_mdc_geom():
    gid: np.ndarray = geom.get_mdc_wire_position()["gid"]
    assert np.all(geom.get_mdc_gid(geom.mdc._layer, geom.mdc._wire) == gid)
    assert np.all(geom.mdc_gid_to_layer(gid) == geom.mdc._layer)
    assert np.all(geom.mdc_gid_to_wire(gid) == geom.mdc._wire)
    assert np.all(geom.mdc_layer_to_is_stereo(geom.mdc._layer) == geom.mdc._is_stereo)
    assert np.all(geom.mdc_gid_to_is_stereo(gid) == geom.mdc._is_stereo)
    assert np.all(geom.mdc_gid_to_east_x(gid) == geom.mdc._east_x)
    assert np.all(geom.mdc_gid_to_east_y(gid) == geom.mdc._east_y)
    assert np.all(geom.mdc_gid_to_east_z(gid) == geom.mdc._east_z)
    assert np.all(geom.mdc_gid_to_west_x(gid) == geom.mdc._west_x)
    assert np.all(geom.mdc_gid_to_west_y(gid) == geom.mdc._west_y)
    assert np.all(geom.mdc_gid_to_west_z(gid) == geom.mdc._west_z)

    assert np.allclose(geom.mdc_gid_z_to_x(gid, geom.mdc._west_z), geom.mdc._west_x, atol=1e-6)
    assert np.allclose(geom.mdc_gid_z_to_y(gid, geom.mdc._west_z), geom.mdc._west_y, atol=1e-6)
    assert np.allclose(geom.mdc_gid_z_to_x(gid, geom.mdc._east_z), geom.mdc._east_x, atol=1e-6)
    assert np.allclose(geom.mdc_gid_z_to_y(gid, geom.mdc._east_z), geom.mdc._east_y, atol=1e-6)
