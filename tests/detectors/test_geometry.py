import numpy as np

import pybes3 as p3
import pybes3.detectors as det


def test_mdc_geom():
    gid: np.ndarray = p3.get_mdc_wire_position()["gid"]
    assert np.all(p3.get_mdc_gid(det.mdc._layer, det.mdc._wire) == gid)
    assert np.all(p3.mdc_gid_to_superlayer(gid) == det.mdc._superlayer)
    assert np.all(p3.mdc_layer_to_superlayer(det.mdc._layer) == det.mdc._superlayer)
    assert np.all(p3.mdc_gid_to_layer(gid) == det.mdc._layer)
    assert np.all(p3.mdc_gid_to_wire(gid) == det.mdc._wire)
    assert np.all(p3.mdc_gid_to_stereo(gid) == det.mdc._stereo)
    assert np.all(p3.mdc_layer_to_is_stereo(det.mdc._layer) == det.mdc._is_stereo)
    assert np.all(p3.mdc_gid_to_is_stereo(gid) == det.mdc._is_stereo)
    assert np.all(p3.mdc_gid_to_east_x(gid) == det.mdc._east_x)
    assert np.all(p3.mdc_gid_to_east_y(gid) == det.mdc._east_y)
    assert np.all(p3.mdc_gid_to_east_z(gid) == det.mdc._east_z)
    assert np.all(p3.mdc_gid_to_west_x(gid) == det.mdc._west_x)
    assert np.all(p3.mdc_gid_to_west_y(gid) == det.mdc._west_y)
    assert np.all(p3.mdc_gid_to_west_z(gid) == det.mdc._west_z)

    assert np.allclose(
        p3.mdc_gid_z_to_x(gid, det.mdc._west_z), det.mdc._west_x, atol=1e-6
    )
    assert np.allclose(
        p3.mdc_gid_z_to_y(gid, det.mdc._west_z), det.mdc._west_y, atol=1e-6
    )
    assert np.allclose(
        p3.mdc_gid_z_to_x(gid, det.mdc._east_z), det.mdc._east_x, atol=1e-6
    )
    assert np.allclose(
        p3.mdc_gid_z_to_y(gid, det.mdc._east_z), det.mdc._east_y, atol=1e-6
    )


def test_emc_geom():
    gid: np.ndarray = p3.get_emc_crystal_position()["gid"]
    assert np.all(p3.get_emc_gid(det.emc._part, det.emc._theta, det.emc._phi) == gid)
    assert np.all(p3.emc_gid_to_part(gid) == det.emc._part)
    assert np.all(p3.emc_gid_to_theta(gid) == det.emc._theta)
    assert np.all(p3.emc_gid_to_phi(gid) == det.emc._phi)

    for i in range(8):
        assert np.all(p3.emc_gid_to_point_x(gid, i) == det.emc._points_x[gid, i])
        assert np.all(p3.emc_gid_to_point_y(gid, i) == det.emc._points_y[gid, i])
        assert np.all(p3.emc_gid_to_point_z(gid, i) == det.emc._points_z[gid, i])

    assert np.allclose(p3.emc_gid_to_center_x(gid), det.emc._center_x, atol=1e-6)
    assert np.allclose(p3.emc_gid_to_center_y(gid), det.emc._center_y, atol=1e-6)
    assert np.allclose(p3.emc_gid_to_center_z(gid), det.emc._center_z, atol=1e-6)
    assert np.allclose(
        p3.emc_gid_to_front_center_x(gid), det.emc._front_center_x, atol=1e-6
    )
    assert np.allclose(
        p3.emc_gid_to_front_center_y(gid), det.emc._front_center_y, atol=1e-6
    )
    assert np.allclose(
        p3.emc_gid_to_front_center_z(gid), det.emc._front_center_z, atol=1e-6
    )


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v", "-s"])
