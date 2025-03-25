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


def test_emc_geom():
    gid: np.ndarray = geom.get_emc_crystal_position()["gid"]
    assert np.all(geom.get_emc_gid(geom.emc._part, geom.emc._theta, geom.emc._phi) == gid)
    assert np.all(geom.emc_gid_to_part(gid) == geom.emc._part)
    assert np.all(geom.emc_gid_to_theta(gid) == geom.emc._theta)
    assert np.all(geom.emc_gid_to_phi(gid) == geom.emc._phi)

    for i in range(8):
        assert np.all(geom.emc_gid_to_point_x(gid, i) == geom.emc._points_x[gid, i])
        assert np.all(geom.emc_gid_to_point_y(gid, i) == geom.emc._points_y[gid, i])
        assert np.all(geom.emc_gid_to_point_z(gid, i) == geom.emc._points_z[gid, i])

    assert np.allclose(geom.emc_gid_to_center_x(gid), geom.emc._center_x, atol=1e-6)
    assert np.allclose(geom.emc_gid_to_center_y(gid), geom.emc._center_y, atol=1e-6)
    assert np.allclose(geom.emc_gid_to_center_z(gid), geom.emc._center_z, atol=1e-6)
    assert np.allclose(
        geom.emc_gid_to_front_center_x(gid), geom.emc._front_center_x, atol=1e-6
    )
    assert np.allclose(
        geom.emc_gid_to_front_center_y(gid), geom.emc._front_center_y, atol=1e-6
    )
    assert np.allclose(
        geom.emc_gid_to_front_center_z(gid), geom.emc._front_center_z, atol=1e-6
    )
