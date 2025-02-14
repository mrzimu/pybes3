from pathlib import Path

import awkward as ak
import numpy as np

import pybes3 as p3
from pybes3.detectors import identify as det_id

data_dir = Path(__file__).parent.parent / "data"


def test_mdc_id():
    mdc_id_ak: ak.Array = p3.open(data_dir / "test_full_mc_evt_1.rtraw")[
        "Event/TDigiEvent/m_mdcDigiCol"
    ].array()["m_intId"]

    # Test awkward
    ak_wire, ak_layer, ak_is_stereo = (
        det_id.mdc_id_to_wire(mdc_id_ak),
        det_id.mdc_id_to_layer(mdc_id_ak),
        det_id.mdc_id_to_is_stereo(mdc_id_ak),
    )
    assert ak.all(p3.get_mdc_id(ak_wire, ak_layer, ak_is_stereo) == mdc_id_ak)
    assert ak.all(det_id.check_mdc_id(mdc_id_ak))

    # Test numpy
    mdc_id_np = ak.flatten(mdc_id_ak).to_numpy()
    np_wire, np_layer, np_is_stereo = (
        det_id.mdc_id_to_wire(mdc_id_np),
        det_id.mdc_id_to_layer(mdc_id_np),
        det_id.mdc_id_to_is_stereo(mdc_id_np),
    )
    assert np.all(p3.get_mdc_id(np_wire, np_layer, np_is_stereo) == mdc_id_np)
    assert np.all(det_id.check_mdc_id(mdc_id_np))

    # Test uint32
    tmp_id = mdc_id_np[0]
    tmp_wire, tmp_layer, tmp_is_stereo = (
        det_id.mdc_id_to_wire(tmp_id),
        det_id.mdc_id_to_layer(tmp_id),
        det_id.mdc_id_to_is_stereo(tmp_id),
    )
    assert tmp_wire == np_wire[0]
    assert tmp_layer == np_layer[0]
    assert tmp_is_stereo == np_is_stereo[0]
    assert p3.get_mdc_id(tmp_wire, tmp_layer, tmp_is_stereo) == tmp_id
    assert det_id.check_mdc_id(tmp_id)

    # Test python int
    tmp_id = int(mdc_id_np[0])
    tmp_wire, tmp_layer, tmp_is_stereo = (
        det_id.mdc_id_to_wire(tmp_id),
        det_id.mdc_id_to_layer(tmp_id),
        det_id.mdc_id_to_is_stereo(tmp_id),
    )
    assert tmp_wire == np_wire[0]
    assert tmp_layer == np_layer[0]
    assert tmp_is_stereo == np_is_stereo[0]
    assert p3.get_mdc_id(tmp_wire, tmp_layer, tmp_is_stereo) == tmp_id
    assert det_id.check_mdc_id(tmp_id)


def test_emc_id():
    emc_id_ak: ak.Array = p3.open(data_dir / "test_full_mc_evt_1.rtraw")[
        "Event/TDigiEvent/m_emcDigiCol"
    ].array()["m_intId"]

    # Test awkward
    ak_module, ak_theta, ak_phi = (
        det_id.emc_id_to_module(emc_id_ak),
        det_id.emc_id_to_theta(emc_id_ak),
        det_id.emc_id_to_phi(emc_id_ak),
    )
    assert ak.all(p3.get_emc_id(ak_module, ak_theta, ak_phi) == emc_id_ak)
    assert ak.all(det_id.check_emc_id(emc_id_ak))

    # Test numpy
    emc_id_np = ak.flatten(emc_id_ak).to_numpy()
    np_module, np_theta, np_phi = (
        det_id.emc_id_to_module(emc_id_np),
        det_id.emc_id_to_theta(emc_id_np),
        det_id.emc_id_to_phi(emc_id_np),
    )
    assert np.all(p3.get_emc_id(np_module, np_theta, np_phi) == emc_id_np)
    assert np.all(det_id.check_emc_id(emc_id_np))

    # Test uint32
    tmp_id = emc_id_np[0]
    tmp_module, tmp_theta, tmp_phi = (
        det_id.emc_id_to_module(tmp_id),
        det_id.emc_id_to_theta(tmp_id),
        det_id.emc_id_to_phi(tmp_id),
    )
    assert tmp_module == np_module[0]
    assert tmp_theta == np_theta[0]
    assert tmp_phi == np_phi[0]
    assert p3.get_emc_id(tmp_module, tmp_theta, tmp_phi) == tmp_id
    assert det_id.check_emc_id(tmp_id)

    # Test python int
    tmp_id = int(emc_id_np[0])
    tmp_module, tmp_theta, tmp_phi = (
        det_id.emc_id_to_module(tmp_id),
        det_id.emc_id_to_theta(tmp_id),
        det_id.emc_id_to_phi(tmp_id),
    )
    assert tmp_module == np_module[0]
    assert tmp_theta == np_theta[0]
    assert tmp_phi == np_phi[0]
    assert p3.get_emc_id(tmp_module, tmp_theta, tmp_phi) == tmp_id
    assert det_id.check_emc_id(tmp_id)


def test_tof_id():
    tof_id_ak: ak.Array = p3.concatenate(
        [data_dir / "test_full_mc_evt_1.rtraw", data_dir / "test_mrpc.rtraw"],
        "Event/TDigiEvent/m_tofDigiCol",
    )["m_tofDigiCol"]["m_intId"]

    # Test awkward
    ak_part, ak_layer_or_module, ak_phi_or_strip, ak_end = (
        det_id.tof_id_to_part(tof_id_ak),
        det_id.tof_id_to_layerOrModule(tof_id_ak),
        det_id.tof_id_to_phiOrStrip(tof_id_ak),
        det_id.tof_id_to_end(tof_id_ak),
    )
    assert ak.all(
        p3.get_tof_id(ak_part, ak_layer_or_module, ak_phi_or_strip, ak_end) == tof_id_ak
    )
    assert ak.all(det_id.check_tof_id(tof_id_ak))

    # Test numpy
    tof_id_np = ak.flatten(tof_id_ak).to_numpy()
    np_part, np_layer_or_module, np_phi_or_strip, np_end = (
        det_id.tof_id_to_part(tof_id_np),
        det_id.tof_id_to_layerOrModule(tof_id_np),
        det_id.tof_id_to_phiOrStrip(tof_id_np),
        det_id.tof_id_to_end(tof_id_np),
    )
    assert np.all(
        p3.get_tof_id(np_part, np_layer_or_module, np_phi_or_strip, np_end) == tof_id_np
    )
    assert np.all(det_id.check_tof_id(tof_id_np))

    # Test uint32
    tmp_id = tof_id_np[0]
    tmp_part, tmp_layer_or_module, tmp_phi_or_strip, tmp_end = (
        det_id.tof_id_to_part(tmp_id),
        det_id.tof_id_to_layerOrModule(tmp_id),
        det_id.tof_id_to_phiOrStrip(tmp_id),
        det_id.tof_id_to_end(tmp_id),
    )
    assert tmp_part == np_part[0]
    assert tmp_layer_or_module == np_layer_or_module[0]
    assert tmp_phi_or_strip == np_phi_or_strip[0]
    assert tmp_end == np_end[0]
    assert p3.get_tof_id(tmp_part, tmp_layer_or_module, tmp_phi_or_strip, tmp_end) == tmp_id
    assert det_id.check_tof_id(tmp_id)

    # Test python int
    tmp_id = int(tof_id_np[0])
    tmp_part, tmp_layer_or_module, tmp_phi_or_strip, tmp_end = (
        det_id.tof_id_to_part(tmp_id),
        det_id.tof_id_to_layerOrModule(tmp_id),
        det_id.tof_id_to_phiOrStrip(tmp_id),
        det_id.tof_id_to_end(tmp_id),
    )
    assert tmp_part == np_part[0]
    assert tmp_layer_or_module == np_layer_or_module[0]
    assert tmp_phi_or_strip == np_phi_or_strip[0]
    assert tmp_end == np_end[0]
    assert p3.get_tof_id(tmp_part, tmp_layer_or_module, tmp_phi_or_strip, tmp_end) == tmp_id
    assert det_id.check_tof_id(tmp_id)


def test_muc_id():
    muc_id_ak: ak.Array = p3.open(data_dir / "test_full_mc_evt_1.rtraw")[
        "Event/TDigiEvent/m_mucDigiCol"
    ].array()["m_intId"]

    # Test awkward
    ak_part, ak_segment, ak_layer, ak_channel, ak_gap, ak_strip = (
        det_id.muc_id_to_part(muc_id_ak),
        det_id.muc_id_to_segment(muc_id_ak),
        det_id.muc_id_to_layer(muc_id_ak),
        det_id.muc_id_to_channel(muc_id_ak),
        det_id.muc_id_to_gap(muc_id_ak),
        det_id.muc_id_to_strip(muc_id_ak),
    )
    assert ak.all(p3.get_muc_id(ak_part, ak_segment, ak_layer, ak_channel) == muc_id_ak)
    assert ak.all(det_id.check_muc_id(muc_id_ak))
    assert ak.all(ak_layer == ak_gap)
    assert ak.all(ak_channel == ak_strip)

    # Test numpy
    muc_id_np = ak.flatten(muc_id_ak).to_numpy()
    np_part, np_segment, np_layer, np_channel, np_gap, np_strip = (
        det_id.muc_id_to_part(muc_id_np),
        det_id.muc_id_to_segment(muc_id_np),
        det_id.muc_id_to_layer(muc_id_np),
        det_id.muc_id_to_channel(muc_id_np),
        det_id.muc_id_to_gap(muc_id_np),
        det_id.muc_id_to_strip(muc_id_np),
    )
    assert np.all(p3.get_muc_id(np_part, np_segment, np_layer, np_channel) == muc_id_np)
    assert np.all(det_id.check_muc_id(muc_id_np))
    assert np.all(np_layer == np_gap)
    assert np.all(np_channel == np_strip)

    # Test uint32
    tmp_id = muc_id_np[0]
    tmp_part, tmp_segment, tmp_layer, tmp_channel, tmp_gap, tmp_strip = (
        det_id.muc_id_to_part(tmp_id),
        det_id.muc_id_to_segment(tmp_id),
        det_id.muc_id_to_layer(tmp_id),
        det_id.muc_id_to_channel(tmp_id),
        det_id.muc_id_to_gap(tmp_id),
        det_id.muc_id_to_strip(tmp_id),
    )
    assert tmp_part == np_part[0]
    assert tmp_segment == np_segment[0]
    assert tmp_layer == np_layer[0]
    assert tmp_channel == np_channel[0]
    assert tmp_gap == np_gap[0]
    assert tmp_strip == np_strip[0]
    assert p3.get_muc_id(tmp_part, tmp_segment, tmp_layer, tmp_channel) == tmp_id
    assert det_id.check_muc_id(tmp_id)

    # Test python int
    tmp_id = int(muc_id_np[0])
    tmp_part, tmp_segment, tmp_layer, tmp_channel, tmp_gap, tmp_strip = (
        det_id.muc_id_to_part(tmp_id),
        det_id.muc_id_to_segment(tmp_id),
        det_id.muc_id_to_layer(tmp_id),
        det_id.muc_id_to_channel(tmp_id),
        det_id.muc_id_to_gap(tmp_id),
        det_id.muc_id_to_strip(tmp_id),
    )
    assert tmp_part == np_part[0]
    assert tmp_segment == np_segment[0]
    assert tmp_layer == np_layer[0]
    assert tmp_channel == np_channel[0]
    assert tmp_gap == np_gap[0]
    assert tmp_strip == np_strip[0]
    assert p3.get_muc_id(tmp_part, tmp_segment, tmp_layer, tmp_channel) == tmp_id
    assert det_id.check_muc_id(tmp_id)


def test_cgem_id():
    cgem_id_ak: ak.Array = p3.open(data_dir / "test_cgem.rtraw")[
        "Event/TDigiEvent/m_cgemDigiCol"
    ].array()["m_intId"]

    # Test awkward
    ak_layer, ak_sheet, ak_strip, ak_is_x_strip = (
        det_id.cgem_id_to_layer(cgem_id_ak),
        det_id.cgem_id_to_sheet(cgem_id_ak),
        det_id.cgem_id_to_strip(cgem_id_ak),
        det_id.cgem_id_to_is_x_strip(cgem_id_ak),
    )
    assert ak.all(p3.get_cgem_id(ak_layer, ak_sheet, ak_strip, ak_is_x_strip) == cgem_id_ak)
    assert ak.all(det_id.check_cgem_id(cgem_id_ak))

    # Test numpy
    cgem_id_np = ak.flatten(cgem_id_ak).to_numpy()
    np_layer, np_sheet, np_strip, np_is_x_strip = (
        det_id.cgem_id_to_layer(cgem_id_np),
        det_id.cgem_id_to_sheet(cgem_id_np),
        det_id.cgem_id_to_strip(cgem_id_np),
        det_id.cgem_id_to_is_x_strip(cgem_id_np),
    )
    assert np.all(p3.get_cgem_id(np_layer, np_sheet, np_strip, np_is_x_strip) == cgem_id_np)
    assert np.all(det_id.check_cgem_id(cgem_id_np))

    # Test uint32
    tmp_id = cgem_id_np[0]
    tmp_layer, tmp_sheet, tmp_strip, tmp_is_x_strip = (
        det_id.cgem_id_to_layer(tmp_id),
        det_id.cgem_id_to_sheet(tmp_id),
        det_id.cgem_id_to_strip(tmp_id),
        det_id.cgem_id_to_is_x_strip(tmp_id),
    )
    assert tmp_layer == np_layer[0]
    assert tmp_sheet == np_sheet[0]
    assert tmp_strip == np_strip[0]
    assert tmp_is_x_strip == np_is_x_strip[0]
    assert p3.get_cgem_id(tmp_layer, tmp_sheet, tmp_strip, tmp_is_x_strip) == tmp_id
    assert det_id.check_cgem_id(tmp_id)

    # Test python int
    tmp_id = int(cgem_id_np[0])
    tmp_layer, tmp_sheet, tmp_strip, tmp_is_x_strip = (
        det_id.cgem_id_to_layer(tmp_id),
        det_id.cgem_id_to_sheet(tmp_id),
        det_id.cgem_id_to_strip(tmp_id),
        det_id.cgem_id_to_is_x_strip(tmp_id),
    )
    assert tmp_layer == np_layer[0]
    assert tmp_sheet == np_sheet[0]
    assert tmp_strip == np_strip[0]
    assert tmp_is_x_strip == np_is_x_strip[0]
    assert p3.get_cgem_id(tmp_layer, tmp_sheet, tmp_strip, tmp_is_x_strip) == tmp_id
    assert det_id.check_cgem_id(tmp_id)


def test_parse_mdc_id():
    mdc_id_ak: ak.Array = p3.open(data_dir / "test_full_mc_evt_1.rtraw")[
        "Event/TDigiEvent/m_mdcDigiCol"
    ].array()["m_intId"]

    wire_ak = det_id.mdc_id_to_wire(mdc_id_ak)
    layer_ak = det_id.mdc_id_to_layer(mdc_id_ak)
    is_stereo_ak = det_id.mdc_id_to_is_stereo(mdc_id_ak)

    # Test awkward, flat=False, library='ak'
    ak_res1 = p3.parse_mdc_id(mdc_id_ak, flat=False, library="ak")
    assert ak_res1.fields == ["wire", "layer", "is_stereo"]
    assert len(ak_res1.positional_axis) == 2
    assert ak.all(ak_res1["wire"] == wire_ak)
    assert ak.all(ak_res1["layer"] == layer_ak)
    assert ak.all(ak_res1["is_stereo"] == is_stereo_ak)

    # Test awkward, flat=True, library='ak'
    ak_res2 = p3.parse_mdc_id(mdc_id_ak, flat=True, library="ak")
    assert ak_res2.fields == ["wire", "layer", "is_stereo"]
    assert len(ak_res2.positional_axis) == 1
    assert ak.all(ak_res2["wire"] == ak.flatten(wire_ak))
    assert ak.all(ak_res2["layer"] == ak.flatten(layer_ak))
    assert ak.all(ak_res2["is_stereo"] == ak.flatten(is_stereo_ak))

    mdc_id_np = ak.flatten(mdc_id_ak).to_numpy()
    wire_np = ak.flatten(wire_ak).to_numpy()
    layer_np = ak.flatten(layer_ak).to_numpy()
    is_stereo_np = ak.flatten(is_stereo_ak).to_numpy()

    # Test numpy, library='np'
    np_res1 = p3.parse_mdc_id(mdc_id_np, flat=False, library="np")
    assert list(np_res1.keys()) == ["wire", "layer", "is_stereo"]
    assert np.all(np_res1["wire"] == wire_np)
    assert np.all(np_res1["layer"] == layer_np)
    assert np.all(np_res1["is_stereo"] == is_stereo_np)

    # Test int, library='ak'
    mdc_id_int = int(mdc_id_np[0])
    int_res1 = p3.parse_mdc_id(mdc_id_int, flat=False, library="ak")
    assert int_res1.fields == ["wire", "layer", "is_stereo"]
    assert int_res1["wire"] == wire_np[0]
    assert int_res1["layer"] == layer_np[0]
    assert int_res1["is_stereo"] == is_stereo_np[0]

    # Test int, library='np'
    int_res2 = p3.parse_mdc_id(mdc_id_int, flat=False, library="np")
    assert list(int_res2.keys()) == ["wire", "layer", "is_stereo"]
    assert int_res2["wire"] == wire_np[0]
    assert int_res2["layer"] == layer_np[0]
    assert int_res2["is_stereo"] == is_stereo_np[0]


def test_parse_emc_id():
    emc_id_ak: ak.Array = p3.open(data_dir / "test_full_mc_evt_1.rtraw")[
        "Event/TDigiEvent/m_emcDigiCol"
    ].array()["m_intId"]

    module_ak = det_id.emc_id_to_module(emc_id_ak)
    theta_ak = det_id.emc_id_to_theta(emc_id_ak)
    phi_ak = det_id.emc_id_to_phi(emc_id_ak)

    # Test awkward, flat=False, library='ak'
    ak_res1 = p3.parse_emc_id(emc_id_ak, flat=False, library="ak")
    assert ak_res1.fields == ["module", "theta", "phi"]
    assert len(ak_res1.positional_axis) == 2
    assert ak.all(ak_res1["module"] == module_ak)
    assert ak.all(ak_res1["theta"] == theta_ak)
    assert ak.all(ak_res1["phi"] == phi_ak)

    # Test awkward, flat=True, library='ak'
    ak_res2 = p3.parse_emc_id(emc_id_ak, flat=True, library="ak")
    assert ak_res2.fields == ["module", "theta", "phi"]
    assert len(ak_res2.positional_axis) == 1
    assert ak.all(ak_res2["module"] == ak.flatten(module_ak))
    assert ak.all(ak_res2["theta"] == ak.flatten(theta_ak))
    assert ak.all(ak_res2["phi"] == ak.flatten(phi_ak))

    emc_id_np = ak.flatten(emc_id_ak).to_numpy()
    module_np = ak.flatten(module_ak).to_numpy()
    theta_np = ak.flatten(theta_ak).to_numpy()
    phi_np = ak.flatten(phi_ak).to_numpy()

    # Test numpy, library='np'
    np_res1 = p3.parse_emc_id(emc_id_np, flat=False, library="np")
    assert list(np_res1.keys()) == ["module", "theta", "phi"]
    assert np.all(np_res1["module"] == module_np)
    assert np.all(np_res1["theta"] == theta_np)
    assert np.all(np_res1["phi"] == phi_np)

    # Test int, library='ak'
    emc_id_int = int(emc_id_np[0])
    int_res1 = p3.parse_emc_id(emc_id_int, flat=False, library="ak")
    assert int_res1.fields == ["module", "theta", "phi"]
    assert int_res1["module"] == module_np[0]
    assert int_res1["theta"] == theta_np[0]
    assert int_res1["phi"] == phi_np[0]

    # Test int, library='np'
    int_res2 = p3.parse_emc_id(emc_id_int, flat=False, library="np")
    assert list(int_res2.keys()) == ["module", "theta", "phi"]
    assert int_res2["module"] == module_np[0]
    assert int_res2["theta"] == theta_np[0]
    assert int_res2["phi"] == phi_np[0]


def test_parse_tof_id():
    tof_id_ak: ak.Array = p3.open(data_dir / "test_mrpc.rtraw")[
        "Event/TDigiEvent/m_tofDigiCol"
    ].array()["m_intId"]

    part_ak = det_id.tof_id_to_part(tof_id_ak)
    layer_or_module_ak = det_id.tof_id_to_layerOrModule(tof_id_ak)
    phi_or_strip_ak = det_id.tof_id_to_phiOrStrip(tof_id_ak)
    end_ak = det_id.tof_id_to_end(tof_id_ak)

    # Test awkward, flat=False, library='ak'
    ak_res1 = p3.parse_tof_id(tof_id_ak, flat=False, library="ak")
    assert ak_res1.fields == ["part", "layer_or_module", "phi_or_strip", "end"]
    assert len(ak_res1.positional_axis) == 2
    assert ak.all(ak_res1["part"] == part_ak)
    assert ak.all(ak_res1["layer_or_module"] == layer_or_module_ak)
    assert ak.all(ak_res1["phi_or_strip"] == phi_or_strip_ak)
    assert ak.all(ak_res1["end"] == end_ak)

    # Test awkward, flat=True, library='ak'
    ak_res2 = p3.parse_tof_id(tof_id_ak, flat=True, library="ak")
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
    np_res1 = p3.parse_tof_id(tof_id_np, flat=False, library="np")
    assert list(np_res1.keys()) == ["part", "layer_or_module", "phi_or_strip", "end"]
    assert np.all(np_res1["part"] == part_np)
    assert np.all(np_res1["layer_or_module"] == layer_or_module_np)
    assert np.all(np_res1["phi_or_strip"] == phi_or_strip_np)
    assert np.all(np_res1["end"] == end_np)

    # Test int, library='ak'
    tof_id_int = int(tof_id_np[0])
    int_res1 = p3.parse_tof_id(tof_id_int, flat=False, library="ak")
    assert int_res1.fields == ["part", "layer_or_module", "phi_or_strip", "end"]
    assert int_res1["part"] == part_np[0]
    assert int_res1["layer_or_module"] == layer_or_module_np[0]
    assert int_res1["phi_or_strip"] == phi_or_strip_np[0]
    assert int_res1["end"] == end_np[0]

    # Test int, library='np'
    int_res2 = p3.parse_tof_id(tof_id_int, flat=False, library="np")
    assert list(int_res2.keys()) == ["part", "layer_or_module", "phi_or_strip", "end"]
    assert int_res2["part"] == part_np[0]
    assert int_res2["layer_or_module"] == layer_or_module_np[0]
    assert int_res2["phi_or_strip"] == phi_or_strip_np[0]
    assert int_res2["end"] == end_np[0]


def test_parse_muc_id():
    muc_id_ak: ak.Array = p3.open(data_dir / "test_full_mc_evt_1.rtraw")[
        "Event/TDigiEvent/m_mucDigiCol"
    ].array()["m_intId"]

    part_ak = det_id.muc_id_to_part(muc_id_ak)
    segment_ak = det_id.muc_id_to_segment(muc_id_ak)
    layer_ak = det_id.muc_id_to_layer(muc_id_ak)
    channel_ak = det_id.muc_id_to_channel(muc_id_ak)
    gap_ak = det_id.muc_id_to_gap(muc_id_ak)
    strip_ak = det_id.muc_id_to_strip(muc_id_ak)

    # Test awkward, flat=False, library='ak'
    ak_res1 = p3.parse_muc_id(muc_id_ak, flat=False, library="ak")
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
    ak_res2 = p3.parse_muc_id(muc_id_ak, flat=True, library="ak")
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
    np_res1 = p3.parse_muc_id(muc_id_np, flat=False, library="np")
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


def test_parse_cgem_id():
    cgem_id_ak: ak.Array = p3.open(data_dir / "test_cgem.rtraw")[
        "Event/TDigiEvent/m_cgemDigiCol"
    ].array()["m_intId"]

    layer_ak = det_id.cgem_id_to_layer(cgem_id_ak)
    sheet_ak = det_id.cgem_id_to_sheet(cgem_id_ak)
    strip_ak = det_id.cgem_id_to_strip(cgem_id_ak)
    is_x_strip_ak = det_id.cgem_id_to_is_x_strip(cgem_id_ak)

    # Test awkward, flat=False, library='ak'
    ak_res1 = p3.parse_cgem_id(cgem_id_ak, flat=False, library="ak")
    assert ak_res1.fields == ["layer", "sheet", "strip", "is_x_strip"]
    assert len(ak_res1.positional_axis) == 2
    assert ak.all(ak_res1["layer"] == layer_ak)
    assert ak.all(ak_res1["sheet"] == sheet_ak)
    assert ak.all(ak_res1["strip"] == strip_ak)
    assert ak.all(ak_res1["is_x_strip"] == is_x_strip_ak)

    # Test awkward, flat=True, library='ak'
    ak_res2 = p3.parse_cgem_id(cgem_id_ak, flat=True, library="ak")
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
    np_res1 = p3.parse_cgem_id(cgem_id_np, flat=False, library="np")
    assert list(np_res1.keys()) == ["layer", "sheet", "strip", "is_x_strip"]
    assert np.all(np_res1["layer"] == layer_np)
    assert np.all(np_res1["sheet"] == sheet_np)
    assert np.all(np_res1["strip"] == strip_np)
    assert np.all(np_res1["is_x_strip"] == is_x_strip_np)

    # Test int, library='ak'
    cgem_id_int = int(cgem_id_np[0])
    int_res1 = p3.parse_cgem_id(cgem_id_int, flat=False, library="ak")
    assert int_res1.fields == ["layer", "sheet", "strip", "is_x_strip"]
    assert int_res1["layer"] == layer_np[0]
    assert int_res1["sheet"] == sheet_np[0]
    assert int_res1["strip"] == strip_np[0]
    assert int_res1["is_x_strip"] == is_x_strip_np[0]

    # Test int, library='np'
    int_res2 = p3.parse_cgem_id(cgem_id_int, flat=False, library="np")
    assert list(int_res2.keys()) == ["layer", "sheet", "strip", "is_x_strip"]
    assert int_res2["layer"] == layer_np[0]
    assert int_res2["sheet"] == sheet_np[0]
    assert int_res2["strip"] == strip_np[0]
    assert int_res2["is_x_strip"] == is_x_strip_np[0]
