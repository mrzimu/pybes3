from pathlib import Path

import uproot

import pybes.besio as besio

besio.wrap_uproot()

cur_dir = Path(__file__).parent


def test_uproot_branches():
    f_full = uproot.open(cur_dir / "test_full_mc_evt_1.rtraw")
    assert len(f_full["Event/TMcEvent"].branches) == 5

    f_only_mc_particles = uproot.open(cur_dir / "test_only_mc_particles.rtraw")
    assert len(f_only_mc_particles["Event/TMcEvent"].branches) == 1


def test_mc_full():
    f_rtraw = uproot.open(cur_dir / "test_full_mc_evt_1.rtraw")
    arr = f_rtraw["Event/TMcEvent"].arrays()
    assert len(arr) == 10


def test_mc_only_particles():
    f_rtraw = uproot.open(cur_dir / "test_only_mc_particles.rtraw")
    arr = f_rtraw["Event/TMcEvent"].arrays()
    assert len(arr) == 10


def test_nav():
    f_rtraw = uproot.open(cur_dir / "test_only_mc_particles.rtraw")
    arr = f_rtraw["Event/EventNavigator"].arrays()
    assert len(arr) == 10


def test_dst():
    f_dst = uproot.open(cur_dir / "test_full_mc_evt_1.dst")
    arr_dst = f_dst["Event/TDstEvent"].arrays()
    assert len(arr_dst) == 10


def test_digi():
    f_dst = uproot.open(cur_dir / "test_full_mc_evt_1.rec")
    arr_digi = f_dst["Event/TDigiEvent"].arrays()
    assert len(arr_digi) == 10


def test_rec():
    f_rec = uproot.open(cur_dir / "test_full_mc_evt_1.rec")
    arr_rec = f_rec["Event/TRecEvent"].arrays()
    assert len(arr_rec) == 10


def test_cgem_rtraw():
    f_rtraw = uproot.open(cur_dir / "test_cgem.rtraw")
    arr = f_rtraw["Event/TMcEvent"].arrays()
    assert len(arr) == 200


def test_uproot_concatenate():
    arr_concat1 = uproot.concatenate(
        {
            cur_dir / "test_full_mc_evt_1.rtraw": "Event/TMcEvent",
            cur_dir / "test_full_mc_evt_2.rtraw": "Event/TMcEvent",
        }
    )
    assert len(arr_concat1) == 20

    arr_concat2 = uproot.concatenate(
        {
            cur_dir / "test_full_mc_evt_1.rtraw": "Event/TMcEvent/m_mcParticleCol",
            cur_dir / "test_full_mc_evt_2.rtraw": "Event/TMcEvent/m_mcParticleCol",
        }
    )
    assert len(arr_concat2) == 20


def test_bes_open():
    f = besio.open(cur_dir / "test_full_mc_evt_1.rtraw")
    assert len(f["Event/TMcEvent"].branches) == 5

    f = besio.open(cur_dir / "test_only_mc_particles.rtraw")
    assert len(f["Event/TMcEvent"].branches) == 1


def test_bes_concatenate():
    arr_concat1 = besio.concatenate(
        [cur_dir / "test_full_mc_evt_1.rtraw", cur_dir / "test_full_mc_evt_2.rtraw"],
        "Event/TMcEvent",
    )
    assert len(arr_concat1) == 20

    arr_concat2 = besio.concatenate(
        [cur_dir / "test_full_mc_evt_1.rtraw", cur_dir / "test_full_mc_evt_2.rtraw"],
        "Event/TMcEvent/m_mcParticleCol",
    )
    assert len(arr_concat2) == 20
