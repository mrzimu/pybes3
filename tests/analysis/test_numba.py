from pathlib import Path

import awkward as ak
import numpy as np
import pytest

import pybes3 as p3
import pybes3.analysis.numba as p3nb

data_dir = Path(__file__).parent.parent / "test_data"

dst_data = p3.open(data_dir / "test_full_mc_evt_1.dst")["Event/TDstEvent"].arrays()
mdc_trks = dst_data.m_mdcTrackCol
emc_trks = dst_data.m_emcTrackCol
tof_trks = dst_data.m_tofTrackCol
kal_trks = dst_data.m_mdcKalTrackCol


def test__regularize_phi():
    phi1 = np.array([-np.pi, np.pi, 3 * np.pi])
    p3nb._regularize_phi(phi1, 0, 2 * np.pi)
    assert np.allclose(phi1, [np.pi, np.pi, np.pi])

    phi2 = np.array([-np.pi / 2 - 2 * np.pi, np.pi / 2 + 2 * np.pi])
    p3nb._regularize_phi(phi2, -np.pi, np.pi)
    assert np.allclose(phi2, [-np.pi / 2, np.pi / 2])


def test__pivot():
    flat_helix = ak.to_numpy(ak.flatten(mdc_trks.m_helix))

    dr = flat_helix[:, 0]
    phi0 = flat_helix[:, 1]
    kappa = flat_helix[:, 2]
    dz = flat_helix[:, 3]
    tanl = flat_helix[:, 4]

    rel_dx = np.zeros_like(dr)
    rel_dy = np.zeros_like(dr)
    rel_dz = np.zeros_like(dr)

    Bz = 1.0

    new_dr, new_phi0, new_dz = p3nb._pivot(
        dr, phi0, kappa, dz, tanl, Bz, rel_dx, rel_dy, rel_dz
    )

    assert new_dr.shape == dr.shape
    assert np.allclose(new_dr, dr)

    assert new_phi0.shape == phi0.shape
    assert np.allclose(new_phi0, phi0)

    assert new_dz.shape == dz.shape
    assert np.allclose(new_dz, dz)


def test__helix_to_xy():
    flat_helix = ak.to_numpy(ak.flatten(mdc_trks.m_helix))

    dr = flat_helix[:, 0]
    phi0 = flat_helix[:, 1]

    x, y = p3nb._helix_to_xy(dr, phi0)

    assert x.shape == dr.shape
    assert y.shape == dr.shape

    assert np.allclose(x, dr * np.cos(phi0))
    assert np.allclose(y, dr * np.sin(phi0))


def test__helix_to_ptphipz():
    flat_helix = ak.to_numpy(ak.flatten(mdc_trks.m_helix))

    phi0 = flat_helix[:, 1]
    kappa = flat_helix[:, 2]
    tanl = flat_helix[:, 4]

    pt, phi, pz = p3nb._helix_to_ptphipz(phi0, kappa, tanl)

    assert pt.shape == phi0.shape
    assert phi.shape == phi0.shape
    assert pz.shape == phi0.shape

    assert np.allclose(pt, np.abs(1 / kappa))
    assert np.allclose(phi, phi0 + np.pi / 2)
    assert np.allclose(pz, np.abs(1 / kappa) * tanl)


@pytest.mark.skip(reason="Not implemented")
def test__helix_to_ptphipz__zero_kappa():
    flat_helix = ak.to_numpy(ak.flatten(mdc_trks.m_helix))

    phi0 = flat_helix[:, 1]
    kappa = np.zeros_like(phi0)
    tanl = flat_helix[:, 4]

    pt, phi, pz = p3nb._helix_to_ptphipz(phi0, kappa, tanl)

    assert pt.shape == phi0.shape
    assert phi.shape == phi0.shape
    assert pz.shape == phi0.shape

    assert np.allclose(pt, np.abs(1 / kappa))
    assert np.allclose(phi, phi0 + np.pi / 2)
    assert np.allclose(pz, np.abs(1 / kappa) * tanl)
