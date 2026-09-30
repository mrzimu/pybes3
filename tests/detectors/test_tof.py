from pathlib import Path

import awkward as ak
import numpy as np
import pytest
import uproot

import pybes3 as p3
from pybes3 import identifier as ident
from pybes3 import tof


def test_tof_gid_conversion(tof_gid_dict):
    ref_gid = tof_gid_dict["gid"]
    ref_part = tof_gid_dict["part"]
    ref_layer_or_module = tof_gid_dict["layer_or_module"]
    ref_phi_or_strip = tof_gid_dict["phi_or_strip"]

    assert np.all(p3.tof_gid_to_part(ref_gid) == ref_part)
    assert np.all(p3.tof_gid_to_layer_or_module(ref_gid) == ref_layer_or_module)
    assert np.all(p3.tof_gid_to_phi_or_strip(ref_gid) == ref_phi_or_strip)
    assert np.all(p3.get_tof_gid(ref_part, ref_layer_or_module, ref_phi_or_strip) == ref_gid)


def test_tof_geom():
    gid = np.arange(tof.N_STRIPS)
    assert np.all(p3.tof_gid_to_part(gid) == tof._part)
    assert np.all(p3.tof_gid_to_layer_or_module(gid) == tof._layer_or_module)
    assert np.all(p3.tof_gid_to_phi_or_strip(gid) == tof._phi_or_strip)

    for i in range(8):
        assert np.all(p3.tof_gid_to_point_x(gid, i) == tof._points_x[gid, i])
        assert np.all(p3.tof_gid_to_point_y(gid, i) == tof._points_y[gid, i])
        assert np.all(p3.tof_gid_to_point_z(gid, i) == tof._points_z[gid, i])

    p3.get_tof_geom_table(library="np")
    p3.get_tof_geom_table(library="ak")
    p3.get_tof_geom_table(library="pd")


def test_tof_parse_gid(tof_gid_dict):
    ref_part = tof_gid_dict["part"]
    ref_layer_or_module = tof_gid_dict["layer_or_module"]
    ref_phi_or_strip = tof_gid_dict["phi_or_strip"]

    # scalar
    for tmp_gid in range(tof.N_STRIPS):
        tmp_res = p3.parse_tof_gid(tmp_gid)
        assert tmp_res["part"] == ref_part[tmp_gid]
        assert tmp_res["layer_or_module"] == ref_layer_or_module[tmp_gid]
        assert tmp_res["phi_or_strip"] == ref_phi_or_strip[tmp_gid]

    # numpy
    np_gid = np.arange(tof.N_STRIPS)
    np_res = p3.parse_tof_gid(np_gid)
    assert np.all(np_res["part"] == ref_part)
    assert np.all(np_res["layer_or_module"] == ref_layer_or_module)
    assert np.all(np_res["phi_or_strip"] == ref_phi_or_strip)

    # awkward
    ak_gid = ak.Array(np_gid)
    ak_res = p3.parse_tof_gid(ak_gid)
    assert ak_res.fields == ["part", "layer_or_module", "phi_or_strip"]
    assert ak.all(ak_res["part"] == ref_part)
    assert ak.all(ak_res["layer_or_module"] == ref_layer_or_module)
    assert ak.all(ak_res["phi_or_strip"] == ref_phi_or_strip)


def test_tof_hit_status(test_data_dir: Path):
    raw_arr = uproot.open(test_data_dir / "ref_tof_hit_status.root")["tof_hit_status"].arrays()

    status = raw_arr["status"]

    fields = [
        "is_raw",
        "is_readout",
        "is_counter",
        "is_cluster",
        "is_barrel",
        "is_east",
        "is_overflow",
        "is_multihit",
        "is_mrpc",
        "layer",
        "n_counter",
        "n_east",
        "n_west",
    ]

    # awkward
    zipped = ak.zip({f: raw_arr[f] for f in fields})
    assert ak.array_equal(p3.parse_tof_hit_status(status), zipped, dtype_exact=False)

    # numpy
    flat_status = ak.flatten(status).to_numpy()
    flat_expected = {f: ak.flatten(raw_arr[f]).to_numpy() for f in fields}
    np_parsed = p3.parse_tof_hit_status(flat_status)
    for f in fields:
        assert np.array_equal(np_parsed[f], flat_expected[f])

    # scalar
    s = int(flat_status[0])
    scalar_parsed = p3.parse_tof_hit_status(s)
    for f in fields:
        assert scalar_parsed[f] == flat_expected[f][0]


def test_tof_hit_status_id_to_gid(test_data_dir: Path):
    tof_digis = ak.from_parquet(test_data_dir / "test_mrpc.rtraw.parquet")["m_tofDigiCol"]
    ref_gid = ident.parse_tof_digi(tof_digis)["gid"]

    tof_trks = ak.from_parquet(test_data_dir / "test_mrpc.dst.parquet")["m_tofTrackCol"]
    status = tof_trks["m_status"]

    with pytest.raises(ValueError):
        p3.tof_hit_status_id_to_gid(status, -1)  # ak
        p3.tof_hit_status_id_to_gid(status[0].to_numpy(), -1)  # np
        p3.tof_hit_status_id_to_gid(int(status[0][0]), -1)  # scalar

    tof_id = tof_trks["m_tofID"]
    mask = (tof_id >= 0) & (status != 0)

    m_status = status[mask]
    m_tofid = tof_id[mask]

    test_gid = p3.tof_hit_status_id_to_gid(m_status, m_tofid)  # ak
    p3.tof_hit_status_id_to_gid(m_status[0].to_numpy(), m_tofid[0].to_numpy())  # np
    p3.tof_hit_status_id_to_gid(int(m_status[0][0]), int(m_tofid[0][0]))  # scalar

    for i in range(len(ref_gid)):
        test_gid_np = test_gid[i].to_numpy()
        ref_gid_np = ref_gid[i].to_numpy()
        assert np.isin(test_gid_np, ref_gid_np).all()
