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
    ak_wire, ak_layer, ak_wire_type = (
        det_id.mdc_id_to_wire(mdc_id_ak),
        det_id.mdc_id_to_layer(mdc_id_ak),
        det_id.mdc_id_to_wire_type(mdc_id_ak),
    )
    assert ak.all(det_id.get_mdc_id(ak_wire, ak_layer, ak_wire_type) == mdc_id_ak)
    assert ak.all(det_id.check_mdc_id(mdc_id_ak))

    # Test numpy
    mdc_id_np = ak.flatten(mdc_id_ak).to_numpy()
    np_wire, np_layer, np_wire_type = (
        det_id.mdc_id_to_wire(mdc_id_np),
        det_id.mdc_id_to_layer(mdc_id_np),
        det_id.mdc_id_to_wire_type(mdc_id_np),
    )
    assert np.all(det_id.get_mdc_id(np_wire, np_layer, np_wire_type) == mdc_id_np)
    assert np.all(det_id.check_mdc_id(mdc_id_np))

    # Test uint32
    tmp_id = mdc_id_np[0]
    tmp_wire, tmp_layer, tmp_wire_type = (
        det_id.mdc_id_to_wire(tmp_id),
        det_id.mdc_id_to_layer(tmp_id),
        det_id.mdc_id_to_wire_type(tmp_id),
    )
    assert tmp_wire == np_wire[0]
    assert tmp_layer == np_layer[0]
    assert tmp_wire_type == np_wire_type[0]
    assert det_id.get_mdc_id(tmp_wire, tmp_layer, tmp_wire_type) == tmp_id
    assert det_id.check_mdc_id(tmp_id)

    # Test python int
    tmp_id = int(mdc_id_np[0])
    tmp_wire, tmp_layer, tmp_wire_type = (
        det_id.mdc_id_to_wire(tmp_id),
        det_id.mdc_id_to_layer(tmp_id),
        det_id.mdc_id_to_wire_type(tmp_id),
    )
    assert tmp_wire == np_wire[0]
    assert tmp_layer == np_layer[0]
    assert tmp_wire_type == np_wire_type[0]
    assert det_id.get_mdc_id(tmp_wire, tmp_layer, tmp_wire_type) == tmp_id
    assert det_id.check_mdc_id(tmp_id)
    assert (
        isinstance(tmp_wire, np.uint32)
        and isinstance(tmp_layer, np.uint32)
        and isinstance(tmp_wire_type, np.uint32)
    )


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
    assert ak.all(det_id.get_emc_id(ak_module, ak_theta, ak_phi) == emc_id_ak)
    assert ak.all(det_id.check_emc_id(emc_id_ak))

    # Test numpy
    emc_id_np = ak.flatten(emc_id_ak).to_numpy()
    np_module, np_theta, np_phi = (
        det_id.emc_id_to_module(emc_id_np),
        det_id.emc_id_to_theta(emc_id_np),
        det_id.emc_id_to_phi(emc_id_np),
    )
    assert np.all(det_id.get_emc_id(np_module, np_theta, np_phi) == emc_id_np)
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
    assert det_id.get_emc_id(tmp_module, tmp_theta, tmp_phi) == tmp_id
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
    assert det_id.get_emc_id(tmp_module, tmp_theta, tmp_phi) == tmp_id
    assert det_id.check_emc_id(tmp_id)
    assert (
        isinstance(tmp_module, np.uint32)
        and isinstance(tmp_theta, np.uint32)
        and isinstance(tmp_phi, np.uint32)
    )


def test_tof_scint_id():
    tof_scint_id_ak: ak.Array = p3.open(data_dir / "test_full_mc_evt_1.rtraw")[
        "Event/TDigiEvent/m_tofDigiCol"
    ].array()["m_intId"]

    # Test awkward
    ak_part, ak_layer, ak_phi, ak_end = (
        det_id.tof_id_to_part(tof_scint_id_ak),
        det_id.tof_id_to_scint_layer(tof_scint_id_ak),
        det_id.tof_id_to_scint_phi(tof_scint_id_ak),
        det_id.tof_id_to_end(tof_scint_id_ak),
    )
    assert ak.all(
        det_id.get_tof_scint_id(ak_part, ak_layer, ak_phi, ak_end) == tof_scint_id_ak
    )
    assert ak.all(det_id.check_tof_id(tof_scint_id_ak))

    # Test numpy
    tof_scint_id_np = ak.flatten(tof_scint_id_ak).to_numpy()
    np_part, np_layer, np_phi, np_end = (
        det_id.tof_id_to_part(tof_scint_id_np),
        det_id.tof_id_to_scint_layer(tof_scint_id_np),
        det_id.tof_id_to_scint_phi(tof_scint_id_np),
        det_id.tof_id_to_end(tof_scint_id_np),
    )
    assert np.all(
        det_id.get_tof_scint_id(np_part, np_layer, np_phi, np_end) == tof_scint_id_np
    )
    assert np.all(det_id.check_tof_id(tof_scint_id_np))

    # Test uint32
    tmp_id = tof_scint_id_np[0]
    tmp_part, tmp_layer, tmp_phi, tmp_end = (
        det_id.tof_id_to_part(tmp_id),
        det_id.tof_id_to_scint_layer(tmp_id),
        det_id.tof_id_to_scint_phi(tmp_id),
        det_id.tof_id_to_end(tmp_id),
    )
    assert tmp_part == np_part[0]
    assert tmp_layer == np_layer[0]
    assert tmp_phi == np_phi[0]
    assert tmp_end == np_end[0]
    assert det_id.get_tof_scint_id(tmp_part, tmp_layer, tmp_phi, tmp_end) == tmp_id
    assert det_id.check_tof_id(tmp_id)

    # Test python int
    tmp_id = int(tof_scint_id_np[0])
    tmp_part, tmp_layer, tmp_phi, tmp_end = (
        det_id.tof_id_to_part(tmp_id),
        det_id.tof_id_to_scint_layer(tmp_id),
        det_id.tof_id_to_scint_phi(tmp_id),
        det_id.tof_id_to_end(tmp_id),
    )
    assert tmp_part == np_part[0]
    assert tmp_layer == np_layer[0]
    assert tmp_phi == np_phi[0]
    assert tmp_end == np_end[0]
    assert det_id.get_tof_scint_id(tmp_part, tmp_layer, tmp_phi, tmp_end) == tmp_id
    assert det_id.check_tof_id(tmp_id)
    assert (
        isinstance(tmp_part, np.uint32)
        and isinstance(tmp_layer, np.uint32)
        and isinstance(tmp_phi, np.uint32)
        and isinstance(tmp_end, np.uint32)
    )


def test_tof_mrpc_id():
    tof_mrpc_id_ak: ak.Array = p3.open(data_dir / "test_mrpc.rtraw")[
        "Event/TDigiEvent/m_tofDigiCol"
    ].array()["m_intId"]

    # Test awkward
    ak_endcap, ak_module, ak_strip, ak_end = (
        det_id.tof_id_to_mrpc_endcap(tof_mrpc_id_ak),
        det_id.tof_id_to_mrpc_module(tof_mrpc_id_ak),
        det_id.tof_id_to_mrpc_strip(tof_mrpc_id_ak),
        det_id.tof_id_to_end(tof_mrpc_id_ak),
    )

    is_mrpc = det_id.tof_id_to_part(tof_mrpc_id_ak) == 3
    assert ak.all(
        det_id.get_tof_mrpc_id(ak_endcap, ak_module, ak_strip, ak_end)[is_mrpc]
        == tof_mrpc_id_ak[is_mrpc]
    )
    assert ak.all(det_id.check_tof_id(tof_mrpc_id_ak))

    # Test numpy
    tof_mrpc_id_np = ak.flatten(tof_mrpc_id_ak).to_numpy()
    np_endcap, np_module, np_strip, np_end = (
        det_id.tof_id_to_mrpc_endcap(tof_mrpc_id_np),
        det_id.tof_id_to_mrpc_module(tof_mrpc_id_np),
        det_id.tof_id_to_mrpc_strip(tof_mrpc_id_np),
        det_id.tof_id_to_end(tof_mrpc_id_np),
    )

    is_mrpc = det_id.tof_id_to_part(tof_mrpc_id_np) == 3
    assert np.all(
        det_id.get_tof_mrpc_id(np_endcap, np_module, np_strip, np_end)[is_mrpc]
        == tof_mrpc_id_np[is_mrpc]
    )
    assert np.all(det_id.check_tof_id(tof_mrpc_id_np))

    # Test uint32
    is_mrpc = det_id.tof_id_to_part(tof_mrpc_id_np) == 3
    tmp_id = tof_mrpc_id_np[is_mrpc][0]
    tmp_endcap, tmp_module, tmp_strip, tmp_end = (
        det_id.tof_id_to_mrpc_endcap(tmp_id),
        det_id.tof_id_to_mrpc_module(tmp_id),
        det_id.tof_id_to_mrpc_strip(tmp_id),
        det_id.tof_id_to_end(tmp_id),
    )
    assert tmp_endcap == np_endcap[is_mrpc][0]
    assert tmp_module == np_module[is_mrpc][0]
    assert tmp_strip == np_strip[is_mrpc][0]
    assert tmp_end == np_end[is_mrpc][0]
    assert det_id.get_tof_mrpc_id(tmp_endcap, tmp_module, tmp_strip, tmp_end) == tmp_id
    assert det_id.check_tof_id(tmp_id)

    # Test python int
    tmp_id = int(tof_mrpc_id_np[is_mrpc][0])
    tmp_endcap, tmp_module, tmp_strip, tmp_end = (
        det_id.tof_id_to_mrpc_endcap(tmp_id),
        det_id.tof_id_to_mrpc_module(tmp_id),
        det_id.tof_id_to_mrpc_strip(tmp_id),
        det_id.tof_id_to_end(tmp_id),
    )
    assert tmp_endcap == np_endcap[is_mrpc][0]
    assert tmp_module == np_module[is_mrpc][0]
    assert tmp_strip == np_strip[is_mrpc][0]
    assert tmp_end == np_end[is_mrpc][0]
    assert det_id.get_tof_mrpc_id(tmp_endcap, tmp_module, tmp_strip, tmp_end) == tmp_id
    assert det_id.check_tof_id(tmp_id)
    assert (
        isinstance(tmp_endcap, np.uint32)
        and isinstance(tmp_module, np.uint32)
        and isinstance(tmp_strip, np.uint32)
        and isinstance(tmp_end, np.uint32)
    )


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
    assert ak.all(det_id.get_muc_id(ak_part, ak_segment, ak_layer, ak_channel) == muc_id_ak)
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
    assert np.all(det_id.get_muc_id(np_part, np_segment, np_layer, np_channel) == muc_id_np)
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
    assert det_id.get_muc_id(tmp_part, tmp_segment, tmp_layer, tmp_channel) == tmp_id
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
    assert det_id.get_muc_id(tmp_part, tmp_segment, tmp_layer, tmp_channel) == tmp_id
    assert det_id.check_muc_id(tmp_id)
    assert (
        isinstance(tmp_part, np.uint32)
        and isinstance(tmp_segment, np.uint32)
        and isinstance(tmp_layer, np.uint32)
        and isinstance(tmp_channel, np.uint32)
        and isinstance(tmp_gap, np.uint32)
        and isinstance(tmp_strip, np.uint32)
    )


def test_cgem_id():
    cgem_id_ak: ak.Array = p3.open(data_dir / "test_cgem.rtraw")[
        "Event/TDigiEvent/m_cgemDigiCol"
    ].array()["m_intId"]

    # Test awkward
    ak_layer, ak_strip, ak_sheet, ak_strip_type, ak_isxstrip = (
        det_id.cgem_id_to_layer(cgem_id_ak),
        det_id.cgem_id_to_strip(cgem_id_ak),
        det_id.cgem_id_to_sheet(cgem_id_ak),
        det_id.cgem_id_to_strip_type(cgem_id_ak),
        det_id.cgem_id_to_isxstrip(cgem_id_ak),
    )
    assert ak.all(
        det_id.get_cgem_id(ak_layer, ak_strip, ak_sheet, ak_strip_type) == cgem_id_ak
    )
    assert ak.all(det_id.check_cgem_id(cgem_id_ak))
    assert ak.all(ak_isxstrip == (ak_strip_type == 0))

    # Test numpy
    cgem_id_np = ak.flatten(cgem_id_ak).to_numpy()
    np_layer, np_strip, np_sheet, np_strip_type, np_isxstrip = (
        det_id.cgem_id_to_layer(cgem_id_np),
        det_id.cgem_id_to_strip(cgem_id_np),
        det_id.cgem_id_to_sheet(cgem_id_np),
        det_id.cgem_id_to_strip_type(cgem_id_np),
        det_id.cgem_id_to_isxstrip(cgem_id_np),
    )
    assert np.all(
        det_id.get_cgem_id(np_layer, np_strip, np_sheet, np_strip_type) == cgem_id_np
    )
    assert np.all(det_id.check_cgem_id(cgem_id_np))
    assert np.all(np_isxstrip == (np_strip_type == 0))

    # Test uint32
    tmp_id = cgem_id_np[0]
    tmp_layer, tmp_strip, tmp_sheet, tmp_strip_type, tmp_isxstrip = (
        det_id.cgem_id_to_layer(tmp_id),
        det_id.cgem_id_to_strip(tmp_id),
        det_id.cgem_id_to_sheet(tmp_id),
        det_id.cgem_id_to_strip_type(tmp_id),
        det_id.cgem_id_to_isxstrip(tmp_id),
    )
    assert tmp_layer == np_layer[0]
    assert tmp_strip == np_strip[0]
    assert tmp_sheet == np_sheet[0]
    assert tmp_strip_type == np_strip_type[0]
    assert tmp_isxstrip == np_isxstrip[0]
    assert det_id.get_cgem_id(tmp_layer, tmp_strip, tmp_sheet, tmp_strip_type) == tmp_id
    assert det_id.check_cgem_id(tmp_id)

    # Test python int
    tmp_id = int(cgem_id_np[0])
    tmp_layer, tmp_strip, tmp_sheet, tmp_strip_type, tmp_isxstrip = (
        det_id.cgem_id_to_layer(tmp_id),
        det_id.cgem_id_to_strip(tmp_id),
        det_id.cgem_id_to_sheet(tmp_id),
        det_id.cgem_id_to_strip_type(tmp_id),
        det_id.cgem_id_to_isxstrip(tmp_id),
    )
    assert tmp_layer == np_layer[0]
    assert tmp_strip == np_strip[0]
    assert tmp_sheet == np_sheet[0]
    assert tmp_strip_type == np_strip_type[0]
    assert tmp_isxstrip == np_isxstrip[0]
    assert det_id.get_cgem_id(tmp_layer, tmp_strip, tmp_sheet, tmp_strip_type) == tmp_id
    assert det_id.check_cgem_id(tmp_id)
    assert (
        isinstance(tmp_layer, np.uint32)
        and isinstance(tmp_strip, np.uint32)
        and isinstance(tmp_sheet, np.uint32)
        and isinstance(tmp_strip_type, np.uint32)
        and isinstance(tmp_isxstrip, np.bool_)
    )


def test_parse_mdc_id():
    mdc_id_ak: ak.Array = p3.open(data_dir / "test_full_mc_evt_1.rtraw")[
        "Event/TDigiEvent/m_mdcDigiCol"
    ].array()["m_intId"]

    wire_ak = det_id.mdc_id_to_wire(mdc_id_ak)
    layer_ak = det_id.mdc_id_to_layer(mdc_id_ak)
    wire_type_ak = det_id.mdc_id_to_wire_type(mdc_id_ak)

    # Test awkward, flat=False, library='ak'
    ak_res1 = det_id.parse_mdc_id(mdc_id_ak, flat=False, library="ak")
    assert ak_res1.fields == ["wire", "layer", "wire_type"]
    assert len(ak_res1.positional_axis) == 2
    assert ak.all(ak_res1["wire"] == wire_ak)
    assert ak.all(ak_res1["layer"] == layer_ak)
    assert ak.all(ak_res1["wire_type"] == wire_type_ak)

    # Test awkward, flat=True, library='ak'
    ak_res2 = det_id.parse_mdc_id(mdc_id_ak, flat=True, library="ak")
    assert ak_res2.fields == ["wire", "layer", "wire_type"]
    assert len(ak_res2.positional_axis) == 1
    assert ak.all(ak_res2["wire"] == ak.flatten(wire_ak))
    assert ak.all(ak_res2["layer"] == ak.flatten(layer_ak))
    assert ak.all(ak_res2["wire_type"] == ak.flatten(wire_type_ak))

    mdc_id_np = ak.flatten(mdc_id_ak).to_numpy()
    wire_np = ak.flatten(wire_ak).to_numpy()
    layer_np = ak.flatten(layer_ak).to_numpy()
    wire_type_np = ak.flatten(wire_type_ak).to_numpy()

    # Test numpy, library='np'
    np_res1 = det_id.parse_mdc_id(mdc_id_np, flat=False, library="np")
    assert list(np_res1.keys()) == ["wire", "layer", "wire_type"]
    assert np.all(np_res1["wire"] == wire_np)
    assert np.all(np_res1["layer"] == layer_np)
    assert np.all(np_res1["wire_type"] == wire_type_np)

    # Test int, library='ak'
    mdc_id_int = int(mdc_id_np[0])
    int_res1 = det_id.parse_mdc_id(mdc_id_int, flat=False, library="ak")
    assert int_res1.fields == ["wire", "layer", "wire_type"]
    assert int_res1["wire"] == wire_np[0]
    assert int_res1["layer"] == layer_np[0]
    assert int_res1["wire_type"] == wire_type_np[0]

    # Test int, library='np'
    int_res2 = det_id.parse_mdc_id(mdc_id_int, flat=False, library="np")
    assert list(int_res2.keys()) == ["wire", "layer", "wire_type"]
    assert int_res2["wire"] == wire_np[0]
    assert int_res2["layer"] == layer_np[0]
    assert int_res2["wire_type"] == wire_type_np[0]


def test_parse_emc_id():
    emc_id_ak: ak.Array = p3.open(data_dir / "test_full_mc_evt_1.rtraw")[
        "Event/TDigiEvent/m_emcDigiCol"
    ].array()["m_intId"]

    module_ak = det_id.emc_id_to_module(emc_id_ak)
    theta_ak = det_id.emc_id_to_theta(emc_id_ak)
    phi_ak = det_id.emc_id_to_phi(emc_id_ak)

    # Test awkward, flat=False, library='ak'
    ak_res1 = det_id.parse_emc_id(emc_id_ak, flat=False, library="ak")
    assert ak_res1.fields == ["module", "theta", "phi"]
    assert len(ak_res1.positional_axis) == 2
    assert ak.all(ak_res1["module"] == module_ak)
    assert ak.all(ak_res1["theta"] == theta_ak)
    assert ak.all(ak_res1["phi"] == phi_ak)

    # Test awkward, flat=True, library='ak'
    ak_res2 = det_id.parse_emc_id(emc_id_ak, flat=True, library="ak")
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
    np_res1 = det_id.parse_emc_id(emc_id_np, flat=False, library="np")
    assert list(np_res1.keys()) == ["module", "theta", "phi"]
    assert np.all(np_res1["module"] == module_np)
    assert np.all(np_res1["theta"] == theta_np)
    assert np.all(np_res1["phi"] == phi_np)

    # Test int, library='ak'
    emc_id_int = int(emc_id_np[0])
    int_res1 = det_id.parse_emc_id(emc_id_int, flat=False, library="ak")
    assert int_res1.fields == ["module", "theta", "phi"]
    assert int_res1["module"] == module_np[0]
    assert int_res1["theta"] == theta_np[0]
    assert int_res1["phi"] == phi_np[0]

    # Test int, library='np'
    int_res2 = det_id.parse_emc_id(emc_id_int, flat=False, library="np")
    assert list(int_res2.keys()) == ["module", "theta", "phi"]
    assert int_res2["module"] == module_np[0]
    assert int_res2["theta"] == theta_np[0]
    assert int_res2["phi"] == phi_np[0]


def test_parse_tof_id():
    tof_id_ak: ak.Array = p3.open(data_dir / "test_mrpc.rtraw")[
        "Event/TDigiEvent/m_tofDigiCol"
    ].array()["m_intId"]

    part_ak = det_id.tof_id_to_part(tof_id_ak)
    end_ak = det_id.tof_id_to_end(tof_id_ak)
    scint_layer_ak = det_id.tof_id_to_scint_layer(tof_id_ak)
    scint_phi_ak = det_id.tof_id_to_scint_phi(tof_id_ak)
    mrpc_endcap_ak = det_id.tof_id_to_mrpc_endcap(tof_id_ak)
    mrpc_module_ak = det_id.tof_id_to_mrpc_module(tof_id_ak)
    mrpc_strip_ak = det_id.tof_id_to_mrpc_strip(tof_id_ak)

    # Test awkward, flat=False, library='ak'
    ak_res1 = det_id.parse_tof_id(tof_id_ak, flat=False, library="ak")
    assert ak_res1.fields == [
        "part",
        "end",
        "scint_layer",
        "scint_phi",
        "mrpc_endcap",
        "mrpc_module",
        "mrpc_strip",
        "is_mrpc",
    ]
    assert len(ak_res1.positional_axis) == 2
    assert ak.all(ak_res1["part"] == part_ak)
    assert ak.all(ak_res1["end"] == end_ak)
    assert ak.all(ak_res1["scint_layer"] == scint_layer_ak)
    assert ak.all(ak_res1["scint_phi"] == scint_phi_ak)
    assert ak.all(ak_res1["mrpc_endcap"] == mrpc_endcap_ak)
    assert ak.all(ak_res1["mrpc_module"] == mrpc_module_ak)
    assert ak.all(ak_res1["mrpc_strip"] == mrpc_strip_ak)

    # Test awkward, flat=True, library='ak'
    ak_res2 = det_id.parse_tof_id(tof_id_ak, flat=True, library="ak")
    assert ak_res2.fields == [
        "part",
        "end",
        "scint_layer",
        "scint_phi",
        "mrpc_endcap",
        "mrpc_module",
        "mrpc_strip",
        "is_mrpc",
    ]
    assert len(ak_res2.positional_axis) == 1
    assert ak.all(ak_res2["part"] == ak.flatten(part_ak))
    assert ak.all(ak_res2["end"] == ak.flatten(end_ak))
    assert ak.all(ak_res2["scint_layer"] == ak.flatten(scint_layer_ak))
    assert ak.all(ak_res2["scint_phi"] == ak.flatten(scint_phi_ak))
    assert ak.all(ak_res2["mrpc_endcap"] == ak.flatten(mrpc_endcap_ak))
    assert ak.all(ak_res2["mrpc_module"] == ak.flatten(mrpc_module_ak))
    assert ak.all(ak_res2["mrpc_strip"] == ak.flatten(mrpc_strip_ak))

    tof_id_np = ak.flatten(tof_id_ak).to_numpy()
    part_np = ak.flatten(part_ak).to_numpy()
    end_np = ak.flatten(end_ak).to_numpy()
    scint_layer_np = ak.flatten(scint_layer_ak).to_numpy()
    scint_phi_np = ak.flatten(scint_phi_ak).to_numpy()
    mrpc_endcap_np = ak.flatten(mrpc_endcap_ak).to_numpy()
    mrpc_module_np = ak.flatten(mrpc_module_ak).to_numpy()
    mrpc_strip_np = ak.flatten(mrpc_strip_ak).to_numpy()

    # Test numpy, library='np'
    np_res1 = det_id.parse_tof_id(tof_id_np, flat=False, library="np")
    assert list(np_res1.keys()) == [
        "part",
        "end",
        "scint_layer",
        "scint_phi",
        "mrpc_endcap",
        "mrpc_module",
        "mrpc_strip",
        "is_mrpc",
    ]
    assert np.all(np_res1["part"] == part_np)
    assert np.all(np_res1["end"] == end_np)
    assert np.all(np_res1["scint_layer"] == scint_layer_np)
    assert np.all(np_res1["scint_phi"] == scint_phi_np)
    assert np.all(np_res1["mrpc_endcap"] == mrpc_endcap_np)
    assert np.all(np_res1["mrpc_module"] == mrpc_module_np)
    assert np.all(np_res1["mrpc_strip"] == mrpc_strip_np)

    # Test int, library='ak'
    tof_id_int = int(tof_id_np[0])
    int_res1 = det_id.parse_tof_id(tof_id_int, flat=False, library="ak")
    assert int_res1.fields == [
        "part",
        "end",
        "scint_layer",
        "scint_phi",
        "mrpc_endcap",
        "mrpc_module",
        "mrpc_strip",
        "is_mrpc",
    ]
    assert int_res1["part"] == part_np[0]
    assert int_res1["end"] == end_np[0]
    assert int_res1["scint_layer"] == scint_layer_np[0]
    assert int_res1["scint_phi"] == scint_phi_np[0]
    assert int_res1["mrpc_endcap"] == mrpc_endcap_np[0]
    assert int_res1["mrpc_module"] == mrpc_module_np[0]
    assert int_res1["mrpc_strip"] == mrpc_strip_np[0]

    # Test int, library='np'
    int_res2 = det_id.parse_tof_id(tof_id_int, flat=False, library="np")
    assert list(int_res2.keys()) == [
        "part",
        "end",
        "scint_layer",
        "scint_phi",
        "mrpc_endcap",
        "mrpc_module",
        "mrpc_strip",
        "is_mrpc",
    ]
    assert int_res2["part"] == part_np[0]
    assert int_res2["end"] == end_np[0]
    assert int_res2["scint_layer"] == scint_layer_np[0]
    assert int_res2["scint_phi"] == scint_phi_np[0]
    assert int_res2["mrpc_endcap"] == mrpc_endcap_np[0]
    assert int_res2["mrpc_module"] == mrpc_module_np[0]
    assert int_res2["mrpc_strip"] == mrpc_strip_np[0]


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
    ak_res1 = det_id.parse_muc_id(muc_id_ak, flat=False, library="ak")
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
    ak_res2 = det_id.parse_muc_id(muc_id_ak, flat=True, library="ak")
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
    np_res1 = det_id.parse_muc_id(muc_id_np, flat=False, library="np")
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
    strip_ak = det_id.cgem_id_to_strip(cgem_id_ak)
    sheet_ak = det_id.cgem_id_to_sheet(cgem_id_ak)
    strip_type_ak = det_id.cgem_id_to_strip_type(cgem_id_ak)
    isxstrip_ak = det_id.cgem_id_to_isxstrip(cgem_id_ak)

    # Test awkward, flat=False, library='ak'
    ak_res1 = det_id.parse_cgem_id(cgem_id_ak, flat=False, library="ak")
    assert ak_res1.fields == ["layer", "strip", "sheet", "strip_type", "is_xstrip"]
    assert len(ak_res1.positional_axis) == 2
    assert ak.all(ak_res1["layer"] == layer_ak)
    assert ak.all(ak_res1["strip"] == strip_ak)
    assert ak.all(ak_res1["sheet"] == sheet_ak)
    assert ak.all(ak_res1["strip_type"] == strip_type_ak)
    assert ak.all(ak_res1["is_xstrip"] == isxstrip_ak)

    # Test awkward, flat=True, library='ak'
    ak_res2 = det_id.parse_cgem_id(cgem_id_ak, flat=True, library="ak")
    assert ak_res2.fields == ["layer", "strip", "sheet", "strip_type", "is_xstrip"]
    assert len(ak_res2.positional_axis) == 1
    assert ak.all(ak_res2["layer"] == ak.flatten(layer_ak))
    assert ak.all(ak_res2["strip"] == ak.flatten(strip_ak))
    assert ak.all(ak_res2["sheet"] == ak.flatten(sheet_ak))
    assert ak.all(ak_res2["strip_type"] == ak.flatten(strip_type_ak))
    assert ak.all(ak_res2["is_xstrip"] == ak.flatten(isxstrip_ak))

    cgem_id_np = ak.flatten(cgem_id_ak).to_numpy()
    layer_np = ak.flatten(layer_ak).to_numpy()
    strip_np = ak.flatten(strip_ak).to_numpy()
    sheet_np = ak.flatten(sheet_ak).to_numpy()
    strip_type_np = ak.flatten(strip_type_ak).to_numpy()
    isxstrip_np = ak.flatten(isxstrip_ak).to_numpy()

    # Test numpy, library='np'
    np_res1 = det_id.parse_cgem_id(cgem_id_np, flat=False, library="np")
    assert list(np_res1.keys()) == ["layer", "strip", "sheet", "strip_type", "is_xstrip"]
    assert np.all(np_res1["layer"] == layer_np)
    assert np.all(np_res1["strip"] == strip_np)
    assert np.all(np_res1["sheet"] == sheet_np)
    assert np.all(np_res1["strip_type"] == strip_type_np)
    assert np.all(np_res1["is_xstrip"] == isxstrip_np)

    # Test int, library='ak'
    cgem_id_int = int(cgem_id_np[0])
    int_res1 = det_id.parse_cgem_id(cgem_id_int, flat=False, library="ak")
    assert int_res1.fields == ["layer", "strip", "sheet", "strip_type", "isxstrip"]
    assert int_res1["layer"] == layer_np[0]
    assert int_res1["strip"] == strip_np[0]
    assert int_res1["sheet"] == sheet_np[0]
    assert int_res1["strip_type"] == strip_type_np[0]
    assert int_res1["is_xstrip"] == isxstrip_np[0]

    # Test int, library='np'
    int_res2 = det_id.parse_cgem_id(cgem_id_int, flat=False, library="np")
    assert list(int_res2.keys()) == ["layer", "strip", "sheet", "strip_type", "isxstrip"]
    assert int_res2["layer"] == layer_np[0]
    assert int_res2["strip"] == strip_np[0]
    assert int_res2["sheet"] == sheet_np[0]
    assert int_res2["strip_type"] == strip_type_np[0]
    assert int_res2["is_xstrip"] == isxstrip_np[0]
