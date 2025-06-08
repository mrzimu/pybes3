from pathlib import Path

import awkward as ak
import numpy as np

import pybes3 as p3
import pybes3.detectors as det

data_dir = Path(__file__).parent.parent / "data"
rtraw_event = p3.open(data_dir / "test_full_mc_evt_1.rtraw")["Event/TDigiEvent"].arrays()


def test_mdc_parse_gid():
    np_gid = det.get_mdc_wire_position()["gid"]
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

    ak_res1 = p3.parse_mdc_gid(ak_gid, with_pos=True)
    assert ak_res1.fields == mdc_fields

    ak_res2 = p3.parse_mdc_gid(ak_gid, with_pos=False)
    assert ak_res2.fields == ["gid", "layer", "wire", "stereo", "is_stereo", "superlayer"]

    np_res1 = p3.parse_mdc_gid(np_gid, with_pos=True)
    assert list(np_res1.keys()) == mdc_fields

    np_res2 = p3.parse_mdc_gid(np_gid, with_pos=False)
    assert list(np_res2.keys()) == [
        "gid",
        "layer",
        "wire",
        "stereo",
        "is_stereo",
        "superlayer",
    ]


def test_parse_mdc_digi_id():
    mdc_id_ak: ak.Array = rtraw_event["m_mdcDigiCol"]["m_intId"]
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

    wire_ak = det.digi_id.mdc_id_to_wire(mdc_id_ak)
    layer_ak = det.digi_id.mdc_id_to_layer(mdc_id_ak)
    is_stereo_ak = det.digi_id.mdc_id_to_is_stereo(mdc_id_ak)

    # Test awkward, default option: with_pos=True
    ak_res1 = p3.parse_mdc_digi_id(mdc_id_ak, with_pos=True)
    assert ak_res1.fields == mdc_fields
    assert len(ak_res1.positional_axis) == 2
    assert ak.all(ak_res1["wire"] == wire_ak)
    assert ak.all(ak_res1["layer"] == layer_ak)
    assert ak.all(ak_res1["is_stereo"] == is_stereo_ak)

    mdc_id_np = ak.flatten(mdc_id_ak).to_numpy()
    wire_np = ak.flatten(wire_ak).to_numpy()
    layer_np = ak.flatten(layer_ak).to_numpy()
    is_stereo_np = ak.flatten(is_stereo_ak).to_numpy()

    # Test numpy, default option: with_pos=True
    np_res1 = p3.parse_mdc_digi_id(mdc_id_np, with_pos=True)
    assert list(np_res1.keys()) == mdc_fields
    assert np.all(np_res1["wire"] == wire_np)
    assert np.all(np_res1["layer"] == layer_np)
    assert np.all(np_res1["is_stereo"] == is_stereo_np)

    # Test int, default option: with_pos=True
    mdc_id_int = int(mdc_id_np[0])
    int_res1 = p3.parse_mdc_digi_id(mdc_id_int, with_pos=True)
    assert int_res1["wire"] == wire_np[0]
    assert int_res1["layer"] == layer_np[0]
    assert int_res1["is_stereo"] == is_stereo_np[0]

    # Test awkward, with_pos=False
    ak_res2 = p3.parse_mdc_digi_id(mdc_id_ak, with_pos=False)
    assert ak_res2.fields == ["gid", "layer", "wire", "stereo", "is_stereo", "superlayer"]
    assert len(ak_res2.positional_axis) == 2
    assert ak.all(ak_res2["wire"] == wire_ak)
    assert ak.all(ak_res2["layer"] == layer_ak)
    assert ak.all(ak_res2["is_stereo"] == is_stereo_ak)


def test_parse_mdc_digi():
    mdc_digi_ak: ak.Record = rtraw_event["m_mdcDigiCol"]
    base_fields = [
        "gid",
        "wire",
        "layer",
        "stereo",
        "is_stereo",
        "superlayer",
        "charge_channel",
        "time_channel",
        "track_index",
        "overflow",
        "digi_id",
    ]

    opt_fields = [
        "mid_x",
        "mid_y",
        "west_x",
        "west_y",
        "west_z",
        "east_x",
        "east_y",
        "east_z",
    ]

    ak_res1 = p3.parse_mdc_digi(mdc_digi_ak, with_pos=True)
    assert ak_res1.fields == base_fields + opt_fields
    assert len(ak_res1.positional_axis) == 2

    ak_res2 = p3.parse_mdc_digi(mdc_digi_ak, with_pos=False)
    assert ak_res2.fields == base_fields
    assert len(ak_res2.positional_axis) == 2


def test_parse_emc_gid():
    np_gid = det.get_emc_crystal_position()["gid"]
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

    ak_res1 = p3.parse_emc_gid(ak_gid, with_pos=True)
    assert ak_res1.fields == emc_fields

    ak_res2 = p3.parse_emc_gid(ak_gid, with_pos=False)
    assert ak_res2.fields == ["gid", "part", "theta", "phi"]

    np_res1 = p3.parse_emc_gid(np_gid, with_pos=True)
    assert list(np_res1.keys()) == emc_fields

    np_res2 = p3.parse_emc_gid(np_gid, with_pos=False)
    assert list(np_res2.keys()) == ["gid", "part", "theta", "phi"]


def test_parse_emc_digi_id():
    emc_id_ak: ak.Array = rtraw_event["m_emcDigiCol"]["m_intId"]
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

    module_ak = det.digi_id.emc_id_to_module(emc_id_ak)
    theta_ak = det.digi_id.emc_id_to_theta(emc_id_ak)
    phi_ak = det.digi_id.emc_id_to_phi(emc_id_ak)

    # Test awkward, with_pos=True
    ak_res1 = p3.parse_emc_digi_id(emc_id_ak, with_pos=True)
    assert ak_res1.fields == emc_fields
    assert len(ak_res1.positional_axis) == 2
    assert ak.all(ak_res1["part"] == module_ak)
    assert ak.all(ak_res1["theta"] == theta_ak)
    assert ak.all(ak_res1["phi"] == phi_ak)

    emc_id_np = ak.flatten(emc_id_ak).to_numpy()
    module_np = ak.flatten(module_ak).to_numpy()
    theta_np = ak.flatten(theta_ak).to_numpy()
    phi_np = ak.flatten(phi_ak).to_numpy()

    # Test numpy, with_pos=True
    np_res1 = p3.parse_emc_digi_id(emc_id_np, with_pos=True)
    assert list(np_res1.keys()) == emc_fields
    assert np.all(np_res1["part"] == module_np)
    assert np.all(np_res1["theta"] == theta_np)
    assert np.all(np_res1["phi"] == phi_np)

    # Test int, with_pos=True
    emc_id_int = int(emc_id_np[0])
    int_res1 = p3.parse_emc_digi_id(emc_id_int, with_pos=True)
    assert int_res1["part"] == module_np[0]
    assert int_res1["theta"] == theta_np[0]
    assert int_res1["phi"] == phi_np[0]

    # Test awkward, with_pos=False
    ak_res2 = p3.parse_emc_digi_id(emc_id_ak, with_pos=False)
    assert ak_res2.fields == ["gid", "part", "theta", "phi"]
    assert len(ak_res2.positional_axis) == 2
    assert ak.all(ak_res2["part"] == module_ak)
    assert ak.all(ak_res2["theta"] == theta_ak)
    assert ak.all(ak_res2["phi"] == phi_ak)


def test_parse_emc_digi():
    emc_digi_ak: ak.Record = rtraw_event["m_emcDigiCol"]
    base_fields = [
        "gid",
        "part",
        "theta",
        "phi",
        "charge_channel",
        "time_channel",
        "track_index",
        "measure",
        "digi_id",
    ]

    opt_fields = [
        "front_center_x",
        "front_center_y",
        "front_center_z",
        "center_x",
        "center_y",
        "center_z",
    ]

    ak_res1 = p3.parse_emc_digi(emc_digi_ak, with_pos=True)
    assert ak_res1.fields == base_fields + opt_fields
    assert len(ak_res1.positional_axis) == 2

    ak_res2 = p3.parse_emc_digi(emc_digi_ak, with_pos=False)
    assert ak_res2.fields == base_fields
    assert len(ak_res2.positional_axis) == 2


def test_parse_tof_digi_id():
    tof_id_ak: ak.Array = p3.open(data_dir / "test_mrpc.rtraw")[
        "Event/TDigiEvent/m_tofDigiCol"
    ].array()["m_intId"]

    part_ak = det.digi_id.tof_id_to_part(tof_id_ak)
    layer_or_module_ak = det.digi_id.tof_id_to_layer_or_module(tof_id_ak)
    phi_or_strip_ak = det.digi_id.tof_id_to_phi_or_strip(tof_id_ak)
    end_ak = det.digi_id.tof_id_to_end(tof_id_ak)

    # Test awkward, flat=False, library='ak'
    ak_res1 = p3.parse_tof_digi_id(tof_id_ak, flat=False, library="ak")
    assert ak_res1.fields == ["part", "layer_or_module", "phi_or_strip", "end"]
    assert len(ak_res1.positional_axis) == 2
    assert ak.all(ak_res1["part"] == part_ak)
    assert ak.all(ak_res1["layer_or_module"] == layer_or_module_ak)
    assert ak.all(ak_res1["phi_or_strip"] == phi_or_strip_ak)
    assert ak.all(ak_res1["end"] == end_ak)

    # Test awkward, flat=True, library='ak'
    ak_res2 = p3.parse_tof_digi_id(tof_id_ak, flat=True, library="ak")
    assert ak_res2.fields == ["part", "layer_or_module", "phi_or_strip", "end"]
    assert len(ak_res2.positional_axis) == 1
    assert ak.all(ak_res2["part"] == ak.flatten(part_ak))
    assert ak.all(ak_res2["layer_or_module"] == ak.flatten(layer_or_module_ak))
    assert ak.all(ak_res2["phi_or_strip"] == ak.flatten(phi_or_strip_ak))
    assert ak.all(ak_res2["end"] == ak.flatten(end_ak))

    tof_id_np = ak.flatten(tof_id_ak).to_numpy()
    part_np = ak.flatten(part_ak).to_numpy()
    layer_or_module_np = ak.flatten(layer_or_module_ak).to_numpy()
    phi_or_strip_np = ak.flatten(phi_or_strip_ak).to_numpy()
    end_np = ak.flatten(end_ak).to_numpy()

    # Test numpy, library='np'
    np_res1 = p3.parse_tof_digi_id(tof_id_np, flat=False, library="np")
    assert list(np_res1.keys()) == ["part", "layer_or_module", "phi_or_strip", "end"]
    assert np.all(np_res1["part"] == part_np)
    assert np.all(np_res1["layer_or_module"] == layer_or_module_np)
    assert np.all(np_res1["phi_or_strip"] == phi_or_strip_np)
    assert np.all(np_res1["end"] == end_np)

    # Test int, library='ak'
    tof_id_int = int(tof_id_np[0])
    int_res1 = p3.parse_tof_digi_id(tof_id_int, flat=False, library="ak")
    assert int_res1.fields == ["part", "layer_or_module", "phi_or_strip", "end"]
    assert int_res1["part"] == part_np[0]
    assert int_res1["layer_or_module"] == layer_or_module_np[0]
    assert int_res1["phi_or_strip"] == phi_or_strip_np[0]
    assert int_res1["end"] == end_np[0]

    # Test int, library='np'
    int_res2 = p3.parse_tof_digi_id(tof_id_int, flat=False, library="np")
    assert list(int_res2.keys()) == ["part", "layer_or_module", "phi_or_strip", "end"]
    assert int_res2["part"] == part_np[0]
    assert int_res2["layer_or_module"] == layer_or_module_np[0]
    assert int_res2["phi_or_strip"] == phi_or_strip_np[0]
    assert int_res2["end"] == end_np[0]


def test_parse_muc_digi_id():
    muc_id_ak: ak.Array = p3.open(data_dir / "test_full_mc_evt_1.rtraw")[
        "Event/TDigiEvent/m_mucDigiCol"
    ].array()["m_intId"]

    part_ak = det.digi_id.muc_id_to_part(muc_id_ak)
    segment_ak = det.digi_id.muc_id_to_segment(muc_id_ak)
    layer_ak = det.digi_id.muc_id_to_layer(muc_id_ak)
    channel_ak = det.digi_id.muc_id_to_channel(muc_id_ak)
    gap_ak = det.digi_id.muc_id_to_gap(muc_id_ak)
    strip_ak = det.digi_id.muc_id_to_strip(muc_id_ak)

    # Test awkward, flat=False, library='ak'
    ak_res1 = p3.parse_muc_digi_id(muc_id_ak, flat=False, library="ak")
    assert ak_res1.fields == [
        "part",
        "segment",
        "layer",
        "channel",
        "gap",
        "strip",
    ]
    assert len(ak_res1.positional_axis) == 2
    assert ak.all(ak_res1["part"] == part_ak)
    assert ak.all(ak_res1["segment"] == segment_ak)
    assert ak.all(ak_res1["layer"] == layer_ak)
    assert ak.all(ak_res1["channel"] == channel_ak)
    assert ak.all(ak_res1["gap"] == gap_ak)
    assert ak.all(ak_res1["strip"] == strip_ak)

    # Test awkward, flat=True, library='ak'
    ak_res2 = p3.parse_muc_digi_id(muc_id_ak, flat=True, library="ak")
    assert ak_res2.fields == [
        "part",
        "segment",
        "layer",
        "channel",
        "gap",
        "strip",
    ]
    assert len(ak_res2.positional_axis) == 1
    assert ak.all(ak_res2["part"] == ak.flatten(part_ak))
    assert ak.all(ak_res2["segment"] == ak.flatten(segment_ak))
    assert ak.all(ak_res2["layer"] == ak.flatten(layer_ak))
    assert ak.all(ak_res2["channel"] == ak.flatten(channel_ak))
    assert ak.all(ak_res2["gap"] == ak.flatten(gap_ak))
    assert ak.all(ak_res2["strip"] == ak.flatten(strip_ak))

    muc_id_np = ak.flatten(muc_id_ak).to_numpy()
    part_np = ak.flatten(part_ak).to_numpy()
    segment_np = ak.flatten(segment_ak).to_numpy()
    layer_np = ak.flatten(layer_ak).to_numpy()
    channel_np = ak.flatten(channel_ak).to_numpy()
    gap_np = ak.flatten(gap_ak).to_numpy()
    strip_np = ak.flatten(strip_ak).to_numpy()

    # Test numpy, library='np'
    np_res1 = p3.parse_muc_digi_id(muc_id_np, flat=False, library="np")
    assert list(np_res1.keys()) == [
        "part",
        "segment",
        "layer",
        "channel",
        "gap",
        "strip",
    ]
    assert np.all(np_res1["part"] == part_np)
    assert np.all(np_res1["segment"] == segment_np)
    assert np.all(np_res1["layer"] == layer_np)
    assert np.all(np_res1["channel"] == channel_np)
    assert np.all(np_res1["gap"] == gap_np)
    assert np.all(np_res1["strip"] == strip_np)


def test_parse_cgem_digi_id():
    cgem_id_ak: ak.Array = p3.open(data_dir / "test_cgem.rtraw")[
        "Event/TDigiEvent/m_cgemDigiCol"
    ].array()["m_intId"]

    layer_ak = det.digi_id.cgem_id_to_layer(cgem_id_ak)
    sheet_ak = det.digi_id.cgem_id_to_sheet(cgem_id_ak)
    strip_ak = det.digi_id.cgem_id_to_strip(cgem_id_ak)
    is_x_strip_ak = det.digi_id.cgem_id_to_is_x_strip(cgem_id_ak)

    # Test awkward, flat=False, library='ak'
    ak_res1 = p3.parse_cgem_digi_id(cgem_id_ak, flat=False, library="ak")
    assert ak_res1.fields == ["layer", "sheet", "strip", "is_x_strip"]
    assert len(ak_res1.positional_axis) == 2
    assert ak.all(ak_res1["layer"] == layer_ak)
    assert ak.all(ak_res1["sheet"] == sheet_ak)
    assert ak.all(ak_res1["strip"] == strip_ak)
    assert ak.all(ak_res1["is_x_strip"] == is_x_strip_ak)

    # Test awkward, flat=True, library='ak'
    ak_res2 = p3.parse_cgem_digi_id(cgem_id_ak, flat=True, library="ak")
    assert ak_res2.fields == ["layer", "sheet", "strip", "is_x_strip"]
    assert len(ak_res2.positional_axis) == 1
    assert ak.all(ak_res2["layer"] == ak.flatten(layer_ak))
    assert ak.all(ak_res2["sheet"] == ak.flatten(sheet_ak))
    assert ak.all(ak_res2["strip"] == ak.flatten(strip_ak))
    assert ak.all(ak_res2["is_x_strip"] == ak.flatten(is_x_strip_ak))

    cgem_id_np = ak.flatten(cgem_id_ak).to_numpy()
    layer_np = ak.flatten(layer_ak).to_numpy()
    strip_np = ak.flatten(strip_ak).to_numpy()
    sheet_np = ak.flatten(sheet_ak).to_numpy()
    is_x_strip_np = ak.flatten(is_x_strip_ak).to_numpy()

    # Test numpy, library='np'
    np_res1 = p3.parse_cgem_digi_id(cgem_id_np, flat=False, library="np")
    assert list(np_res1.keys()) == ["layer", "sheet", "strip", "is_x_strip"]
    assert np.all(np_res1["layer"] == layer_np)
    assert np.all(np_res1["sheet"] == sheet_np)
    assert np.all(np_res1["strip"] == strip_np)
    assert np.all(np_res1["is_x_strip"] == is_x_strip_np)

    # Test int, library='ak'
    cgem_id_int = int(cgem_id_np[0])
    int_res1 = p3.parse_cgem_digi_id(cgem_id_int, flat=False, library="ak")
    assert int_res1.fields == ["layer", "sheet", "strip", "is_x_strip"]
    assert int_res1["layer"] == layer_np[0]
    assert int_res1["sheet"] == sheet_np[0]
    assert int_res1["strip"] == strip_np[0]
    assert int_res1["is_x_strip"] == is_x_strip_np[0]

    # Test int, library='np'
    int_res2 = p3.parse_cgem_digi_id(cgem_id_int, flat=False, library="np")
    assert list(int_res2.keys()) == ["layer", "sheet", "strip", "is_x_strip"]
    assert int_res2["layer"] == layer_np[0]
    assert int_res2["sheet"] == sheet_np[0]
    assert int_res2["strip"] == strip_np[0]
    assert int_res2["is_x_strip"] == is_x_strip_np[0]


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v", "-s"])
