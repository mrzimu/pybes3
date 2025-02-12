from pathlib import Path

import awkward
import pytest
import uproot

import pybes3
import pybes3.besio as besio

besio.wrap_uproot()

data_dir = Path(__file__).parent.parent / "data"


def test_uproot_branches():
    f_full = uproot.open(data_dir / "test_full_mc_evt_1.rtraw")
    assert len(f_full["Event/TMcEvent"].branches) == 5

    f_only_mc_particles = uproot.open(data_dir / "test_only_mc_particles.rtraw")
    assert len(f_only_mc_particles["Event/TMcEvent"].branches) == 1


def test_mc_full():
    f_rtraw = uproot.open(data_dir / "test_full_mc_evt_1.rtraw")
    arr = f_rtraw["Event/TMcEvent"].arrays()
    assert len(arr) == 10


def test_mc_only_particles():
    f_rtraw = uproot.open(data_dir / "test_only_mc_particles.rtraw")
    arr = f_rtraw["Event/TMcEvent"].arrays()
    assert len(arr) == 10


def test_nav():
    f_rtraw = uproot.open(data_dir / "test_only_mc_particles.rtraw")
    arr = f_rtraw["Event/EventNavigator"].arrays()
    assert len(arr) == 10


def test_evtrec():
    f_dst = uproot.open(data_dir / "test_full_mc_evt_1.dst")
    arr_evtrec = f_dst["Event/TEvtRecObject"].arrays()
    assert len(arr_evtrec) == 10


def test_dst():
    f_dst = uproot.open(data_dir / "test_full_mc_evt_1.dst")
    arr_dst = f_dst["Event/TDstEvent"].arrays()
    assert len(arr_dst) == 10


def test_digi():
    f_dst = uproot.open(data_dir / "test_full_mc_evt_1.rec")
    arr_digi = f_dst["Event/TDigiEvent"].arrays()
    assert len(arr_digi) == 10


def test_rec():
    f_rec = uproot.open(data_dir / "test_full_mc_evt_1.rec")
    arr_rec = f_rec["Event/TRecEvent"].arrays()
    assert len(arr_rec) == 10


def test_cgem_rtraw():
    f_rtraw = uproot.open(data_dir / "test_cgem.rtraw")
    arr = f_rtraw["Event/TMcEvent"].arrays()
    assert len(arr) == 200


def test_uproot_concatenate():
    arr_concat1 = uproot.concatenate(
        {
            data_dir / "test_full_mc_evt_1.rtraw": "Event/TMcEvent",
            data_dir / "test_full_mc_evt_2.rtraw": "Event/TMcEvent",
        }
    )
    assert len(arr_concat1) == 20

    arr_concat2 = uproot.concatenate(
        {
            data_dir / "test_full_mc_evt_1.rtraw": "Event/TMcEvent/m_mcParticleCol",
            data_dir / "test_full_mc_evt_2.rtraw": "Event/TMcEvent/m_mcParticleCol",
        }
    )
    assert len(arr_concat2) == 20


def test_bes_open():
    f = besio.open(data_dir / "test_full_mc_evt_1.rtraw")
    assert len(f["Event/TMcEvent"].branches) == 5

    f = besio.open(data_dir / "test_only_mc_particles.rtraw")
    assert len(f["Event/TMcEvent"].branches) == 1


def test_bes_concatenate():
    arr_concat1 = besio.concatenate(
        [data_dir / "test_full_mc_evt_1.rtraw", data_dir / "test_full_mc_evt_2.rtraw"],
        "Event/TMcEvent",
    )
    assert len(arr_concat1) == 20

    arr_concat2 = besio.concatenate(
        [data_dir / "test_full_mc_evt_1.rtraw", data_dir / "test_full_mc_evt_2.rtraw"],
        "Event/TMcEvent/m_mcParticleCol",
    )
    assert len(arr_concat2) == 20


def test_symetric_matrix_expansion():
    def test_symetric_matrix(arr):
        arr = awkward.flatten(arr)
        n_dim = int(arr.typestr.split("*")[-2].strip())

        # Check if the matrix is square
        assert n_dim == int(arr.typestr.split("*")[-3].strip())

        for i in range(n_dim):
            for j in range(i, n_dim):
                assert awkward.all(arr[:, i, j] == arr[:, j, i])

    f_dst = uproot.open(data_dir / "test_full_mc_evt_1.dst")
    arr_dst = f_dst["Event/TDstEvent"].arrays()

    f_rec = uproot.open(data_dir / "test_full_mc_evt_1.rec")
    arr_rec = f_rec["Event/TRecEvent"].arrays()

    for tmp_arr in [
        arr_dst.m_mdcTrackCol.m_err,
        arr_dst.m_emcTrackCol.m_err,
        arr_dst.m_extTrackCol.myEmcErrorMatrix,
        arr_dst.m_extTrackCol.myMucErrorMatrix,
        arr_dst.m_extTrackCol.myTof1ErrorMatrix,
        arr_dst.m_extTrackCol.myTof2ErrorMatrix,
        arr_rec.m_recMdcTrackCol.m_err,
        arr_rec.m_recEmcShowerCol.m_err,
        arr_rec.m_recMdcKalTrackCol.m_terror,
    ]:
        test_symetric_matrix(tmp_arr)


def test_digi_expand_TRawData():
    f_rec = uproot.open(data_dir / "test_full_mc_evt_1.rec")
    arr_digi = f_rec["Event/TDigiEvent"].arrays()
    for field in arr_digi.fields:
        if field == "m_fromMc":
            continue

        assert "TRawData" not in arr_digi[field].fields


@pytest.mark.skipif(
    not Path(
        "/bes3fs/offline/data/raw/round17/231117/run_0079017_All_file001_SFO-1.raw"
    ).exists(),
    reason="Test data is not available",
)
def test_raw():
    f_raw: pybes3.besio.RawBinaryReader = pybes3.open_raw(
        "/bes3fs/offline/data/raw/round17/231117/run_0079017_All_file001_SFO-1.raw"
    )

    n_mdc_digis = awkward.Array([1872, 2768, 1641, 2542, 3331, 2672, 2257, 2470, 3635, 3689])

    arr_full = f_raw.arrays(n_blocks=10)
    assert set(arr_full.fields) == {"evt_header", "mdc", "tof", "emc", "muc"}
    assert awkward.all(awkward.count(arr_full.mdc.id, axis=1) == n_mdc_digis)

    arr_mdc = f_raw.arrays(n_blocks=10, sub_detectors=["mdc"])
    assert set(arr_mdc.fields) == {"evt_header", "mdc"}
    assert awkward.all(awkward.count(arr_mdc.mdc.id, axis=1) == n_mdc_digis)

    arr_batch = f_raw.arrays(n_blocks=10, n_block_per_batch=5)
    assert set(arr_batch.fields) == {"evt_header", "mdc", "tof", "emc", "muc"}
    assert awkward.all(awkward.count(arr_batch.mdc.id, axis=1) == n_mdc_digis)

    arr_workers = f_raw.arrays(n_blocks=10, max_workers=4)
    assert set(arr_workers.fields) == {"evt_header", "mdc", "tof", "emc", "muc"}
    assert awkward.all(awkward.count(arr_workers.mdc.id, axis=1) == n_mdc_digis)
