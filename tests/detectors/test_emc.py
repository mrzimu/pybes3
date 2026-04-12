import awkward as ak
import numpy as np

import pybes3 as p3
from pybes3.detectors import emc


def test_emc_geom():
    gid: np.ndarray = p3.get_emc_crystal_position()["gid"]
    assert np.all(p3.get_emc_gid(emc._part, emc._theta, emc._phi) == gid)
    assert np.all(p3.emc_gid_to_part(gid) == emc._part)
    assert np.all(p3.emc_gid_to_theta(gid) == emc._theta)
    assert np.all(p3.emc_gid_to_phi(gid) == emc._phi)

    for i in range(8):
        assert np.all(p3.emc_gid_to_point_x(gid, i) == emc._points_x[gid, i])
        assert np.all(p3.emc_gid_to_point_y(gid, i) == emc._points_y[gid, i])
        assert np.all(p3.emc_gid_to_point_z(gid, i) == emc._points_z[gid, i])

    assert np.allclose(p3.emc_gid_to_center_x(gid), emc._center_x, atol=1e-6)
    assert np.allclose(p3.emc_gid_to_center_y(gid), emc._center_y, atol=1e-6)
    assert np.allclose(p3.emc_gid_to_center_z(gid), emc._center_z, atol=1e-6)
    assert np.allclose(
        p3.emc_gid_to_front_center_x(gid), emc._front_center_x, atol=1e-6
    )
    assert np.allclose(
        p3.emc_gid_to_front_center_y(gid), emc._front_center_y, atol=1e-6
    )
    assert np.allclose(
        p3.emc_gid_to_front_center_z(gid), emc._front_center_z, atol=1e-6
    )


def test_parse_emc_gid():
    np_gid = p3.get_emc_crystal_position()["gid"]
    ak_gid = ak.Array(np_gid)
    emc_fields = [
        "gid",
        "part",
        "theta",
        "phi",
        "front_center_x",
        "front_center_y",
        "front_center_z",
        "center_x",
        "center_y",
        "center_z",
    ]

    ak_res1 = emc.parse_emc_gid(ak_gid, with_pos=True)
    assert ak_res1.fields == emc_fields

    ak_res2 = emc.parse_emc_gid(ak_gid, with_pos=False)
    assert ak_res2.fields == ["gid", "part", "theta", "phi"]

    np_res1 = emc.parse_emc_gid(np_gid, with_pos=True)
    assert list(np_res1.keys()) == emc_fields

    np_res2 = emc.parse_emc_gid(np_gid, with_pos=False)
    assert list(np_res2.keys()) == ["gid", "part", "theta", "phi"]
