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

    # Test numpy
    mdc_id_np = ak.flatten(mdc_id_ak).to_numpy()
    np_wire, np_layer, np_wire_type = (
        det_id.mdc_id_to_wire(mdc_id_np),
        det_id.mdc_id_to_layer(mdc_id_np),
        det_id.mdc_id_to_wire_type(mdc_id_np),
    )
    assert np.all(det_id.get_mdc_id(np_wire, np_layer, np_wire_type) == mdc_id_np)

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

    # Test numpy
    emc_id_np = ak.flatten(emc_id_ak).to_numpy()
    np_module, np_theta, np_phi = (
        det_id.emc_id_to_module(emc_id_np),
        det_id.emc_id_to_theta(emc_id_np),
        det_id.emc_id_to_phi(emc_id_np),
    )
    assert np.all(det_id.get_emc_id(np_module, np_theta, np_phi) == emc_id_np)

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
    assert (
        isinstance(tmp_endcap, np.uint32)
        and isinstance(tmp_module, np.uint32)
        and isinstance(tmp_strip, np.uint32)
        and isinstance(tmp_end, np.uint32)
    )
