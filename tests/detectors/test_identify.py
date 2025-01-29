from pathlib import Path

import awkward as ak
import numpy as np

import pybes3 as p3
from pybes3.detectors import identify as det_id

data_dir = Path(__file__).parent.parent / "data"


def test_mdc_teid():
    mdc_teid_ak: ak.Array = p3.open(data_dir / "test_full_mc_evt_1.rtraw")[
        "Event/TDigiEvent/m_mdcDigiCol"
    ].array()["m_intId"]

    # Test awkward
    ak_res = det_id.parse_mdc_teid(mdc_teid_ak)
    assert ak_res.fields == ["wire", "layer", "wire_type"]
    assert ak.all(det_id.get_mdc_teid(ak_res) == mdc_teid_ak)
    assert ak.all(
        det_id.get_mdc_teid(ak_res["wire"], ak_res["layer"], ak_res["wire_type"])
        == mdc_teid_ak
    )

    # Test numpy
    mdc_teid_np = ak.flatten(mdc_teid_ak).to_numpy()
    np_wire, np_layer, np_wire_type = det_id.parse_mdc_teid(mdc_teid_np)
    assert np.all(det_id.get_mdc_teid(np_wire, np_layer, np_wire_type) == mdc_teid_np)

    # Test uint32
    tmp_id = mdc_teid_np[0]
    tmp_wire, tmp_layer, tmp_wire_type = det_id.parse_mdc_teid(tmp_id)
    assert tmp_wire == np_wire[0]
    assert tmp_layer == np_layer[0]
    assert tmp_wire_type == np_wire_type[0]
    assert det_id.get_mdc_teid(tmp_wire, tmp_layer, tmp_wire_type) == tmp_id

    # Test python int
    tmp_id = int(mdc_teid_np[0])
    tmp_wire, tmp_layer, tmp_wire_type = det_id.parse_mdc_teid(tmp_id)
    assert tmp_wire == np_wire[0]
    assert tmp_layer == np_layer[0]
    assert tmp_wire_type == np_wire_type[0]
    assert det_id.get_mdc_teid(tmp_wire, tmp_layer, tmp_wire_type) == tmp_id
    assert (
        isinstance(tmp_wire, int)
        and isinstance(tmp_layer, int)
        and isinstance(tmp_wire_type, int)
    )


def test_emc_teid():
    emc_teid_ak: ak.Array = p3.open(data_dir / "test_full_mc_evt_1.rtraw")[
        "Event/TDigiEvent/m_emcDigiCol"
    ].array()["m_intId"]

    # Test awkward
    ak_res = det_id.parse_emc_teid(emc_teid_ak)
    assert ak_res.fields == ["module", "theta", "phi"]
    assert ak.all(det_id.get_emc_teid(ak_res) == emc_teid_ak)
    assert ak.all(
        det_id.get_emc_teid(ak_res["module"], ak_res["theta"], ak_res["phi"]) == emc_teid_ak
    )

    # Test numpy
    emc_teid_np = ak.flatten(emc_teid_ak).to_numpy()
    np_module, np_theta, np_phi = det_id.parse_emc_teid(emc_teid_np)
    assert np.all(det_id.get_emc_teid(np_module, np_theta, np_phi) == emc_teid_np)

    # Test uint32
    tmp_id = emc_teid_np[0]
    tmp_module, tmp_theta, tmp_phi = det_id.parse_emc_teid(tmp_id)
    assert tmp_module == np_module[0]
    assert tmp_theta == np_theta[0]
    assert tmp_phi == np_phi[0]
    assert det_id.get_emc_teid(tmp_module, tmp_theta, tmp_phi) == tmp_id

    # Test python int
    tmp_id = int(emc_teid_np[0])
    tmp_module, tmp_theta, tmp_phi = det_id.parse_emc_teid(tmp_id)
    assert tmp_module == np_module[0]
    assert tmp_theta == np_theta[0]
    assert tmp_phi == np_phi[0]
    assert det_id.get_emc_teid(tmp_module, tmp_theta, tmp_phi) == tmp_id
    assert (
        isinstance(tmp_module, int) and isinstance(tmp_theta, int) and isinstance(tmp_phi, int)
    )


def test_tof_scint_teid():
    tof_scint_teid_ak: ak.Array = p3.open(data_dir / "test_full_mc_evt_1.rtraw")[
        "Event/TDigiEvent/m_tofDigiCol"
    ].array()["m_intId"]

    # Test awkward
    ak_res = det_id.parse_tof_teid(tof_scint_teid_ak)
    assert isinstance(ak_res, dict)
    assert set(ak_res.keys()) == {"scint"}
    ak_res = ak_res["scint"]
    assert ak_res.fields == ["part", "layer", "phi", "end"]
    assert ak.all(det_id.get_tof_scint_teid(ak_res) == tof_scint_teid_ak)
    assert ak.all(
        det_id.get_tof_scint_teid(
            ak_res["part"], ak_res["layer"], ak_res["phi"], ak_res["end"]
        )
        == tof_scint_teid_ak
    )

    # Test numpy
    tof_scint_teid_np = ak.flatten(tof_scint_teid_ak).to_numpy()
    np_res = det_id.parse_tof_teid(tof_scint_teid_np)
    assert isinstance(np_res, dict)
    np_res = np_res["scint"]
    np_part = np_res["part"]
    np_layer = np_res["layer"]
    np_phi = np_res["phi"]
    np_end = np_res["end"]
    assert np.all(
        det_id.get_tof_scint_teid(np_part, np_layer, np_phi, np_end) == tof_scint_teid_np
    )

    # Test uint32
    tmp_id = tof_scint_teid_np[0]
    tmp_res = det_id.parse_tof_teid(tmp_id)
    assert isinstance(tmp_res, dict)
    tmp_part = tmp_res["part"]
    tmp_layer = tmp_res["layer"]
    tmp_phi = tmp_res["phi"]
    tmp_end = tmp_res["end"]
    assert tmp_part == np_part[0]
    assert tmp_layer == np_layer[0]
    assert tmp_phi == np_phi[0]
    assert tmp_end == np_end[0]
    assert det_id.get_tof_scint_teid(tmp_part, tmp_layer, tmp_phi, tmp_end) == tmp_id

    # Test python int
    tmp_id = int(tof_scint_teid_np[0])
    tmp_res = det_id.parse_tof_teid(tmp_id)
    assert isinstance(tmp_res, dict)
    tmp_part = tmp_res["part"]
    tmp_layer = tmp_res["layer"]
    tmp_phi = tmp_res["phi"]
    tmp_end = tmp_res["end"]
    assert tmp_part == np_part[0]
    assert tmp_layer == np_layer[0]
    assert tmp_phi == np_phi[0]
    assert tmp_end == np_end[0]
    assert det_id.get_tof_scint_teid(tmp_part, tmp_layer, tmp_phi, tmp_end) == tmp_id
    assert (
        isinstance(tmp_part, int)
        and isinstance(tmp_layer, int)
        and isinstance(tmp_phi, int)
        and isinstance(tmp_end, int)
    )


def test_tof_mrpc_teid():
    tof_mrpc_teid_ak: ak.Array = p3.open(data_dir / "test_mrpc.rtraw")[
        "Event/TDigiEvent/m_tofDigiCol"
    ].array()["m_intId"]

    # Test awkward
    ak_res = det_id.parse_tof_teid(tof_mrpc_teid_ak)
    assert isinstance(ak_res, dict)
    assert set(ak_res.keys()) == {"mrpc", "scint"}
    ak_res = ak_res["mrpc"]
    assert ak_res.fields == ["part", "endcap", "module", "strip", "end"]

    is_mrpc = det_id.tof_teid_to_part(tof_mrpc_teid_ak) == 3
    assert ak.all(det_id.get_tof_mrpc_teid(ak_res) == tof_mrpc_teid_ak[is_mrpc])
    assert ak.all(
        det_id.get_tof_mrpc_teid(
            ak_res["endcap"], ak_res["module"], ak_res["strip"], ak_res["end"]
        )
        == tof_mrpc_teid_ak[is_mrpc]
    )

    # Test numpy
    tof_mrpc_teid_np = ak.flatten(tof_mrpc_teid_ak).to_numpy()
    np_res = det_id.parse_tof_teid(tof_mrpc_teid_np)
    assert isinstance(np_res, dict)
    np_res = np_res["mrpc"]
    np_endcap = np_res["endcap"]
    np_module = np_res["module"]
    np_strip = np_res["strip"]
    np_end = np_res["end"]

    is_mrpc = det_id.tof_teid_to_part(tof_mrpc_teid_np) == 3
    assert np.all(
        det_id.get_tof_mrpc_teid(np_endcap, np_module, np_strip, np_end)
        == tof_mrpc_teid_np[is_mrpc]
    )

    # Test uint32
    is_mrpc = det_id.tof_teid_to_part(tof_mrpc_teid_np) == 3
    tmp_id = tof_mrpc_teid_np[is_mrpc][0]
    tmp_res = det_id.parse_tof_teid(tmp_id)
    assert isinstance(tmp_res, dict)
    tmp_endcap = tmp_res["endcap"]
    tmp_module = tmp_res["module"]
    tmp_strip = tmp_res["strip"]
    tmp_end = tmp_res["end"]
    assert tmp_endcap == np_endcap[0]
    assert tmp_module == np_module[0]
    assert tmp_strip == np_strip[0]
    assert tmp_end == np_end[0]
    assert det_id.get_tof_mrpc_teid(tmp_endcap, tmp_module, tmp_strip, tmp_end) == tmp_id

    # Test python int
    tmp_id = int(tof_mrpc_teid_np[is_mrpc][0])
    tmp_res = det_id.parse_tof_teid(tmp_id)
    assert isinstance(tmp_res, dict)
    tmp_endcap = tmp_res["endcap"]
    tmp_module = tmp_res["module"]
    tmp_strip = tmp_res["strip"]
    tmp_end = tmp_res["end"]
    assert tmp_endcap == np_endcap[0]
    assert tmp_module == np_module[0]
    assert tmp_strip == np_strip[0]
    assert tmp_end == np_end[0]
