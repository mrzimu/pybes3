from pathlib import Path

import awkward as ak
import numpy as np

import pybes3 as p3
from pybes3.detectors import identify as det_id

data_dir = Path(__file__).parent.parent / "data"


def test_mdc_teid():
    mdc_teid_ak = (
        p3.open(data_dir / "test_full_mc_evt_1.rtraw")["Event/TDigiEvent/m_mdcDigiCol"]
        .array()
        .m_intId
    )

    # Test awkward
    ak_res = det_id.parse_mdc_teid(mdc_teid_ak)
    assert ak_res.fields == ["wire", "layer", "wire_type"]
    assert ak.all(det_id.get_mdc_teid(ak_res) == mdc_teid_ak)
    assert ak.all(
        det_id.get_mdc_teid(ak_res.wire, ak_res.layer, ak_res.wire_type) == mdc_teid_ak
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
    emc_teid_ak = (
        p3.open(data_dir / "test_full_mc_evt_1.rtraw")["Event/TDigiEvent/m_emcDigiCol"]
        .array()
        .m_intId
    )

    # Test awkward
    ak_res = det_id.parse_emc_teid(emc_teid_ak)
    assert ak_res.fields == ["module", "theta", "phi"]
    assert ak.all(det_id.get_emc_teid(ak_res) == emc_teid_ak)
    assert ak.all(det_id.get_emc_teid(ak_res.module, ak_res.theta, ak_res.phi) == emc_teid_ak)

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
