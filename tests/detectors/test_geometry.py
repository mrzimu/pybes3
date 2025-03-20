import numpy as np

import pybes3.detectors.geometry as geom


def test_mdc_geom():
    gid: np.ndarray = geom.get_mdc_wire_position()["gid"]
    assert np.all(geom.get_mdc_gid(geom._layer, geom._wire) == gid)
    assert np.all(geom.mdc_gid_to_layer(gid) == geom._layer)
    assert np.all(geom.mdc_gid_to_wire(gid) == geom._wire)
    assert np.all(geom.mdc_layer_to_is_stereo(geom._layer) == geom._is_stereo)
    assert np.all(geom.mdc_gid_to_is_stereo(gid) == geom._is_stereo)
    assert np.all(geom.mdc_gid_to_east_x(gid) == geom._east_x)
    assert np.all(geom.mdc_gid_to_east_y(gid) == geom._east_y)
    assert np.all(geom.mdc_gid_to_east_z(gid) == geom._east_z)
    assert np.all(geom.mdc_gid_to_west_x(gid) == geom._west_x)
    assert np.all(geom.mdc_gid_to_west_y(gid) == geom._west_y)
    assert np.all(geom.mdc_gid_to_west_z(gid) == geom._west_z)

    assert np.allclose(geom.mdc_gid_z_to_x(gid, geom._west_z), geom._west_x, atol=1e-6)
    assert np.allclose(geom.mdc_gid_z_to_y(gid, geom._west_z), geom._west_y, atol=1e-6)
    assert np.allclose(geom.mdc_gid_z_to_x(gid, geom._east_z), geom._east_x, atol=1e-6)
    assert np.allclose(geom.mdc_gid_z_to_y(gid, geom._east_z), geom._east_y, atol=1e-6)
