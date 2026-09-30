import awkward as ak
import numpy as np

import pybes3 as p3
from pybes3 import cgem


def test_cgem_gid_conversion(cgem_gid_dict):
    ref_gid = cgem_gid_dict["gid"]
    ref_layer = cgem_gid_dict["layer"]
    ref_sheet = cgem_gid_dict["sheet"]
    ref_strip_type = cgem_gid_dict["strip_type"]
    ref_strip = cgem_gid_dict["strip"]

    assert np.all(p3.cgem_gid_to_layer(ref_gid) == ref_layer)
    assert np.all(p3.cgem_gid_to_sheet(ref_gid) == ref_sheet)
    assert np.all(p3.cgem_gid_to_strip_type(ref_gid) == ref_strip_type)
    assert np.all(p3.cgem_gid_to_strip(ref_gid) == ref_strip)
    assert np.all(p3.cgem_gid_to_is_xstrip(ref_gid) == (ref_strip_type == cgem.X_STRIP_TYPE))
    assert np.all(p3.cgem_gid_to_is_vstrip(ref_gid) == (ref_strip_type == cgem.V_STRIP_TYPE))
    assert np.all(p3.get_cgem_gid(ref_layer, ref_sheet, ref_strip_type, ref_strip) == ref_gid)


def test_cgem_geom(cgem_geom_dict):
    ref = cgem_geom_dict
    gid = np.arange(cgem.N_STRIPS)

    assert np.array_equal(ref["gid"], gid)
    assert np.all(
        p3.get_cgem_gid(ref["layer"], ref["sheet"], ref["strip_type"], ref["strip"]) == gid
    )

    # strip geometry of `cgem_geom.npz`, cross-checked against the BOSS reference
    geom = p3.get_cgem_geom_table()
    assert np.array_equal(geom["gid"], gid)
    assert np.array_equal(geom["layer"], ref["layer"])
    assert np.array_equal(geom["sheet"], ref["sheet"])
    assert np.array_equal(geom["strip_type"], ref["strip_type"])
    assert np.array_equal(geom["strip"], ref["strip"])

    assert np.allclose(geom["r"], ref["r"], atol=1e-9)
    assert np.allclose(geom["width"], ref["width"], atol=1e-9)
    assert np.allclose(geom["phi0"], ref["phi0"], atol=1e-9)
    assert np.allclose(geom["dphi"], ref["dphi"], atol=1e-9)
    assert np.allclose(geom["z0"], ref["z0"], atol=1e-9)
    assert np.allclose(geom["dz"], ref["dz"], atol=1e-9)

    # the ufuncs must return the same values as the ones stored in `cgem_geom.npz`
    assert np.allclose(p3.cgem_gid_to_radius(gid), geom["r"], atol=1e-12)
    assert np.allclose(p3.cgem_gid_to_width(gid), geom["width"], atol=1e-12)
    assert np.allclose(p3.cgem_gid_to_phi0(gid), geom["phi0"], atol=1e-12)
    assert np.allclose(p3.cgem_gid_to_dphi(gid), geom["dphi"], atol=1e-12)
    assert np.allclose(p3.cgem_gid_to_z0(gid), geom["z0"], atol=1e-12)
    assert np.allclose(p3.cgem_gid_to_dz(gid), geom["dz"], atol=1e-12)

    # phi <-> z of a point on a strip: the two ends are mapped onto each other
    phi0 = geom["phi0"]
    dphi = geom["dphi"]
    z0 = geom["z0"]
    dz = geom["dz"]
    v_strip = geom["strip_type"] == cgem.V_STRIP_TYPE

    assert np.allclose(
        p3.cgem_gid_phi_to_z(gid[v_strip], phi0[v_strip]), z0[v_strip], atol=1e-9
    )
    assert np.allclose(
        p3.cgem_gid_phi_to_z(gid[v_strip], (phi0 + dphi)[v_strip]),
        (z0 + dz)[v_strip],
        atol=1e-9,
    )
    assert np.allclose(
        p3.cgem_gid_z_to_phi(gid[v_strip], z0[v_strip]), phi0[v_strip], atol=1e-9
    )
    assert np.allclose(
        p3.cgem_gid_z_to_phi(gid[v_strip], (z0 + dz)[v_strip]),
        (phi0 + dphi)[v_strip],
        atol=1e-9,
    )

    # an x-strip runs along the z axis: z gives its phi0, while phi gives no z
    assert np.allclose(
        p3.cgem_gid_z_to_phi(gid[~v_strip], z0[~v_strip]), phi0[~v_strip], atol=1e-9
    )
    assert np.isnan(p3.cgem_gid_phi_to_z(gid[~v_strip], phi0[~v_strip])).all()

    p3.get_cgem_geom_table(library="np")
    p3.get_cgem_geom_table(library="ak")
    p3.get_cgem_geom_table(library="pd")


def test_cgem_parse_gid(cgem_gid_dict):
    ref_layer = cgem_gid_dict["layer"]
    ref_sheet = cgem_gid_dict["sheet"]
    ref_strip_type = cgem_gid_dict["strip_type"]
    ref_strip = cgem_gid_dict["strip"]

    # scalar
    for tmp_gid in range(cgem.N_STRIPS):
        tmp_res = p3.parse_cgem_gid(tmp_gid)
        assert tmp_res["layer"] == ref_layer[tmp_gid]
        assert tmp_res["sheet"] == ref_sheet[tmp_gid]
        assert tmp_res["strip_type"] == ref_strip_type[tmp_gid]
        assert tmp_res["strip"] == ref_strip[tmp_gid]
        assert tmp_res["is_xstrip"] == (ref_strip_type[tmp_gid] == cgem.X_STRIP_TYPE)
        assert tmp_res["is_vstrip"] == (ref_strip_type[tmp_gid] == cgem.V_STRIP_TYPE)

    # numpy
    np_gid = np.arange(cgem.N_STRIPS)
    np_res = p3.parse_cgem_gid(np_gid)
    assert np.all(np_res["layer"] == ref_layer)
    assert np.all(np_res["sheet"] == ref_sheet)
    assert np.all(np_res["strip_type"] == ref_strip_type)
    assert np.all(np_res["strip"] == ref_strip)
    assert np.all(np_res["is_xstrip"] == (ref_strip_type == cgem.X_STRIP_TYPE))
    assert np.all(np_res["is_vstrip"] == (ref_strip_type == cgem.V_STRIP_TYPE))

    # awkward
    ak_gid = ak.Array(np_gid)
    ak_res = p3.parse_cgem_gid(ak_gid)
    assert ak_res.fields == [
        "layer",
        "sheet",
        "strip_type",
        "strip",
        "is_xstrip",
        "is_vstrip",
    ]
    assert ak.all(ak_res["layer"] == ref_layer)
    assert ak.all(ak_res["sheet"] == ref_sheet)
    assert ak.all(ak_res["strip_type"] == ref_strip_type)
    assert ak.all(ak_res["strip"] == ref_strip)
    assert ak.all(ak_res["is_xstrip"] == (ref_strip_type == cgem.X_STRIP_TYPE))
    assert ak.all(ak_res["is_vstrip"] == (ref_strip_type == cgem.V_STRIP_TYPE))
