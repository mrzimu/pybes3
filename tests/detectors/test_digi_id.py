from pathlib import Path

import awkward as ak
import numpy as np

import pybes3 as p3
from pybes3 import detectors as det
from pybes3.detectors import digi_id

data_dir = Path(__file__).parent.parent / "data"
rtraw_event = p3.open(data_dir / "test_full_mc_evt_1.rtraw")["Event/TDigiEvent"].arrays()


def test_mdc_digi_id():
    mdc_id_ak: ak.Array = rtraw_event["m_mdcDigiCol"]["m_intId"]

    # Test awkward
    ak_wire, ak_layer, ak_is_stereo = (
        digi_id.mdc_id_to_wire(mdc_id_ak),
        digi_id.mdc_id_to_layer(mdc_id_ak),
        digi_id.mdc_id_to_is_stereo(mdc_id_ak),
    )
    assert ak.all(det.get_mdc_digi_id(ak_wire, ak_layer, ak_is_stereo) == mdc_id_ak)
    assert ak.all(digi_id.check_mdc_id(mdc_id_ak))

    # Test numpy
    mdc_id_np = ak.flatten(mdc_id_ak).to_numpy()
    np_wire, np_layer, np_is_stereo = (
        digi_id.mdc_id_to_wire(mdc_id_np),
        digi_id.mdc_id_to_layer(mdc_id_np),
        digi_id.mdc_id_to_is_stereo(mdc_id_np),
    )
    assert np.all(det.get_mdc_digi_id(np_wire, np_layer, np_is_stereo) == mdc_id_np)
    assert np.all(digi_id.check_mdc_id(mdc_id_np))

    # Test uint32
    tmp_id = mdc_id_np[0]
    tmp_wire, tmp_layer, tmp_is_stereo = (
        digi_id.mdc_id_to_wire(tmp_id),
        digi_id.mdc_id_to_layer(tmp_id),
        digi_id.mdc_id_to_is_stereo(tmp_id),
    )
    assert tmp_wire == np_wire[0]
    assert tmp_layer == np_layer[0]
    assert tmp_is_stereo == np_is_stereo[0]
    assert det.get_mdc_digi_id(tmp_wire, tmp_layer, tmp_is_stereo) == tmp_id
    assert digi_id.check_mdc_id(tmp_id)

    # Test python int
    tmp_id = int(mdc_id_np[0])
    tmp_wire, tmp_layer, tmp_is_stereo = (
        digi_id.mdc_id_to_wire(tmp_id),
        digi_id.mdc_id_to_layer(tmp_id),
        digi_id.mdc_id_to_is_stereo(tmp_id),
    )
    assert tmp_wire == np_wire[0]
    assert tmp_layer == np_layer[0]
    assert tmp_is_stereo == np_is_stereo[0]
    assert det.get_mdc_digi_id(tmp_wire, tmp_layer, tmp_is_stereo) == tmp_id
    assert digi_id.check_mdc_id(tmp_id)


def test_emc_digi_id():
    emc_id_ak: ak.Array = rtraw_event["m_emcDigiCol"]["m_intId"]

    # Test awkward
    ak_module, ak_theta, ak_phi = (
        digi_id.emc_id_to_module(emc_id_ak),
        digi_id.emc_id_to_theta(emc_id_ak),
        digi_id.emc_id_to_phi(emc_id_ak),
    )
    assert ak.all(det.get_emc_digi_id(ak_module, ak_theta, ak_phi) == emc_id_ak)
    assert ak.all(digi_id.check_emc_id(emc_id_ak))

    # Test numpy
    emc_id_np = ak.flatten(emc_id_ak).to_numpy()
    np_module, np_theta, np_phi = (
        digi_id.emc_id_to_module(emc_id_np),
        digi_id.emc_id_to_theta(emc_id_np),
        digi_id.emc_id_to_phi(emc_id_np),
    )
    assert np.all(det.get_emc_digi_id(np_module, np_theta, np_phi) == emc_id_np)
    assert np.all(digi_id.check_emc_id(emc_id_np))

    # Test uint32
    tmp_id = emc_id_np[0]
    tmp_module, tmp_theta, tmp_phi = (
        digi_id.emc_id_to_module(tmp_id),
        digi_id.emc_id_to_theta(tmp_id),
        digi_id.emc_id_to_phi(tmp_id),
    )
    assert tmp_module == np_module[0]
    assert tmp_theta == np_theta[0]
    assert tmp_phi == np_phi[0]
    assert det.get_emc_digi_id(tmp_module, tmp_theta, tmp_phi) == tmp_id
    assert digi_id.check_emc_id(tmp_id)

    # Test python int
    tmp_id = int(emc_id_np[0])
    tmp_module, tmp_theta, tmp_phi = (
        digi_id.emc_id_to_module(tmp_id),
        digi_id.emc_id_to_theta(tmp_id),
        digi_id.emc_id_to_phi(tmp_id),
    )
    assert tmp_module == np_module[0]
    assert tmp_theta == np_theta[0]
    assert tmp_phi == np_phi[0]
    assert det.get_emc_digi_id(tmp_module, tmp_theta, tmp_phi) == tmp_id
    assert digi_id.check_emc_id(tmp_id)


def test_tof_digi_id():
    tof_id_ak: ak.Array = rtraw_event["m_tofDigiCol"]["m_intId"]

    # Test awkward
    ak_part, ak_layer_or_module, ak_phi_or_strip, ak_end = (
        digi_id.tof_id_to_part(tof_id_ak),
        digi_id.tof_id_to_layer_or_module(tof_id_ak),
        digi_id.tof_id_to_phi_or_strip(tof_id_ak),
        digi_id.tof_id_to_end(tof_id_ak),
    )
    assert ak.all(
        det.get_tof_digi_id(ak_part, ak_layer_or_module, ak_phi_or_strip, ak_end) == tof_id_ak
    )
    assert ak.all(digi_id.check_tof_id(tof_id_ak))

    # Test numpy
    tof_id_np = ak.flatten(tof_id_ak).to_numpy()
    np_part, np_layer_or_module, np_phi_or_strip, np_end = (
        digi_id.tof_id_to_part(tof_id_np),
        digi_id.tof_id_to_layer_or_module(tof_id_np),
        digi_id.tof_id_to_phi_or_strip(tof_id_np),
        digi_id.tof_id_to_end(tof_id_np),
    )
    assert np.all(
        det.get_tof_digi_id(np_part, np_layer_or_module, np_phi_or_strip, np_end) == tof_id_np
    )
    assert np.all(digi_id.check_tof_id(tof_id_np))

    # Test uint32
    tmp_id = tof_id_np[0]
    tmp_part, tmp_layer_or_module, tmp_phi_or_strip, tmp_end = (
        digi_id.tof_id_to_part(tmp_id),
        digi_id.tof_id_to_layer_or_module(tmp_id),
        digi_id.tof_id_to_phi_or_strip(tmp_id),
        digi_id.tof_id_to_end(tmp_id),
    )
    assert tmp_part == np_part[0]
    assert tmp_layer_or_module == np_layer_or_module[0]
    assert tmp_phi_or_strip == np_phi_or_strip[0]
    assert tmp_end == np_end[0]
    assert (
        det.get_tof_digi_id(tmp_part, tmp_layer_or_module, tmp_phi_or_strip, tmp_end) == tmp_id
    )
    assert digi_id.check_tof_id(tmp_id)

    # Test python int
    tmp_id = int(tof_id_np[0])
    tmp_part, tmp_layer_or_module, tmp_phi_or_strip, tmp_end = (
        digi_id.tof_id_to_part(tmp_id),
        digi_id.tof_id_to_layer_or_module(tmp_id),
        digi_id.tof_id_to_phi_or_strip(tmp_id),
        digi_id.tof_id_to_end(tmp_id),
    )
    assert tmp_part == np_part[0]
    assert tmp_layer_or_module == np_layer_or_module[0]
    assert tmp_phi_or_strip == np_phi_or_strip[0]
    assert tmp_end == np_end[0]
    assert (
        det.get_tof_digi_id(tmp_part, tmp_layer_or_module, tmp_phi_or_strip, tmp_end) == tmp_id
    )
    assert digi_id.check_tof_id(tmp_id)


def test_muc_digi_id():
    muc_id_ak: ak.Array = rtraw_event["m_mucDigiCol"]["m_intId"]

    # Test awkward
    ak_part, ak_segment, ak_layer, ak_channel, ak_gap, ak_strip = (
        digi_id.muc_id_to_part(muc_id_ak),
        digi_id.muc_id_to_segment(muc_id_ak),
        digi_id.muc_id_to_layer(muc_id_ak),
        digi_id.muc_id_to_channel(muc_id_ak),
        digi_id.muc_id_to_gap(muc_id_ak),
        digi_id.muc_id_to_strip(muc_id_ak),
    )
    assert ak.all(det.get_muc_digi_id(ak_part, ak_segment, ak_layer, ak_channel) == muc_id_ak)
    assert ak.all(digi_id.check_muc_id(muc_id_ak))
    assert ak.all(ak_layer == ak_gap)
    assert ak.all(ak_channel == ak_strip)

    # Test numpy
    muc_id_np = ak.flatten(muc_id_ak).to_numpy()
    np_part, np_segment, np_layer, np_channel, np_gap, np_strip = (
        digi_id.muc_id_to_part(muc_id_np),
        digi_id.muc_id_to_segment(muc_id_np),
        digi_id.muc_id_to_layer(muc_id_np),
        digi_id.muc_id_to_channel(muc_id_np),
        digi_id.muc_id_to_gap(muc_id_np),
        digi_id.muc_id_to_strip(muc_id_np),
    )
    assert np.all(det.get_muc_digi_id(np_part, np_segment, np_layer, np_channel) == muc_id_np)
    assert np.all(digi_id.check_muc_id(muc_id_np))
    assert np.all(np_layer == np_gap)
    assert np.all(np_channel == np_strip)

    # Test uint32
    tmp_id = muc_id_np[0]
    tmp_part, tmp_segment, tmp_layer, tmp_channel, tmp_gap, tmp_strip = (
        digi_id.muc_id_to_part(tmp_id),
        digi_id.muc_id_to_segment(tmp_id),
        digi_id.muc_id_to_layer(tmp_id),
        digi_id.muc_id_to_channel(tmp_id),
        digi_id.muc_id_to_gap(tmp_id),
        digi_id.muc_id_to_strip(tmp_id),
    )
    assert tmp_part == np_part[0]
    assert tmp_segment == np_segment[0]
    assert tmp_layer == np_layer[0]
    assert tmp_channel == np_channel[0]
    assert tmp_gap == np_gap[0]
    assert tmp_strip == np_strip[0]
    assert det.get_muc_digi_id(tmp_part, tmp_segment, tmp_layer, tmp_channel) == tmp_id
    assert digi_id.check_muc_id(tmp_id)

    # Test python int
    tmp_id = int(muc_id_np[0])
    tmp_part, tmp_segment, tmp_layer, tmp_channel, tmp_gap, tmp_strip = (
        digi_id.muc_id_to_part(tmp_id),
        digi_id.muc_id_to_segment(tmp_id),
        digi_id.muc_id_to_layer(tmp_id),
        digi_id.muc_id_to_channel(tmp_id),
        digi_id.muc_id_to_gap(tmp_id),
        digi_id.muc_id_to_strip(tmp_id),
    )
    assert tmp_part == np_part[0]
    assert tmp_segment == np_segment[0]
    assert tmp_layer == np_layer[0]
    assert tmp_channel == np_channel[0]
    assert tmp_gap == np_gap[0]
    assert tmp_strip == np_strip[0]
    assert det.get_muc_digi_id(tmp_part, tmp_segment, tmp_layer, tmp_channel) == tmp_id
    assert digi_id.check_muc_id(tmp_id)


def test_cgem_digi_id():
    cgem_id_ak: ak.Array = p3.open(data_dir / "test_cgem.rtraw")[
        "Event/TDigiEvent/m_cgemDigiCol"
    ].array()["m_intId"]

    # Test awkward
    ak_layer, ak_sheet, ak_strip, ak_is_x_strip = (
        digi_id.cgem_id_to_layer(cgem_id_ak),
        digi_id.cgem_id_to_sheet(cgem_id_ak),
        digi_id.cgem_id_to_strip(cgem_id_ak),
        digi_id.cgem_id_to_is_x_strip(cgem_id_ak),
    )
    assert ak.all(
        det.get_cgem_digi_id(ak_layer, ak_sheet, ak_strip, ak_is_x_strip) == cgem_id_ak
    )
    assert ak.all(digi_id.check_cgem_id(cgem_id_ak))

    # Test numpy
    cgem_id_np = ak.flatten(cgem_id_ak).to_numpy()
    np_layer, np_sheet, np_strip, np_is_x_strip = (
        digi_id.cgem_id_to_layer(cgem_id_np),
        digi_id.cgem_id_to_sheet(cgem_id_np),
        digi_id.cgem_id_to_strip(cgem_id_np),
        digi_id.cgem_id_to_is_x_strip(cgem_id_np),
    )
    assert np.all(
        det.get_cgem_digi_id(np_layer, np_sheet, np_strip, np_is_x_strip) == cgem_id_np
    )
    assert np.all(digi_id.check_cgem_id(cgem_id_np))

    # Test uint32
    tmp_id = cgem_id_np[0]
    tmp_layer, tmp_sheet, tmp_strip, tmp_is_x_strip = (
        digi_id.cgem_id_to_layer(tmp_id),
        digi_id.cgem_id_to_sheet(tmp_id),
        digi_id.cgem_id_to_strip(tmp_id),
        digi_id.cgem_id_to_is_x_strip(tmp_id),
    )
    assert tmp_layer == np_layer[0]
    assert tmp_sheet == np_sheet[0]
    assert tmp_strip == np_strip[0]
    assert tmp_is_x_strip == np_is_x_strip[0]
    assert det.get_cgem_digi_id(tmp_layer, tmp_sheet, tmp_strip, tmp_is_x_strip) == tmp_id
    assert digi_id.check_cgem_id(tmp_id)

    # Test python int
    tmp_id = int(cgem_id_np[0])
    tmp_layer, tmp_sheet, tmp_strip, tmp_is_x_strip = (
        digi_id.cgem_id_to_layer(tmp_id),
        digi_id.cgem_id_to_sheet(tmp_id),
        digi_id.cgem_id_to_strip(tmp_id),
        digi_id.cgem_id_to_is_x_strip(tmp_id),
    )
    assert tmp_layer == np_layer[0]
    assert tmp_sheet == np_sheet[0]
    assert tmp_strip == np_strip[0]
    assert tmp_is_x_strip == np_is_x_strip[0]
    assert det.get_cgem_digi_id(tmp_layer, tmp_sheet, tmp_strip, tmp_is_x_strip) == tmp_id
    assert digi_id.check_cgem_id(tmp_id)


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v", "-s"])
