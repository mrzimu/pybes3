from pathlib import Path

import awkward as ak
import pytest
import uproot

import pybes3
import pybes3.data


@pytest.fixture(scope="session")
def test_data_dir():
    yield Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def geom_dir():
    yield pybes3.data.DATA_DIR


@pytest.fixture(scope="session")
def digi_event(test_data_dir):
    yield uproot.open(test_data_dir / "test_full_mc_evt_1.rtraw")["Event/TDigiEvent"].arrays()


@pytest.fixture(scope="session")
def cgem_digi_event(test_data_dir):
    yield uproot.open(test_data_dir / "test_cgem.rtraw")["Event/TDigiEvent"].arrays()


@pytest.fixture(scope="session")
def raw_event(test_data_dir):
    yield pybes3.open_raw(test_data_dir / "test_raw_data.raw").arrays()


@pytest.fixture(scope="session")
def mdc_trk(test_data_dir):
    yield uproot.open(test_data_dir / "test_full_mc_evt_1.dst")[
        "Event/TDstEvent/m_mdcTrackCol"
    ].array()


@pytest.fixture(scope="session")
def raw_helix_arr(mdc_trk):
    yield mdc_trk["m_helix"]


@pytest.fixture(scope="session")
def raw_helix_err_arr(mdc_trk):
    yield mdc_trk["m_err"]


@pytest.fixture(scope="session")
def flat_helix_arr(raw_helix_arr):
    yield ak.flatten(raw_helix_arr)


@pytest.fixture(scope="session")
def flat_helix_err_arr(raw_helix_err_arr):
    yield ak.flatten(raw_helix_err_arr)


@pytest.fixture(scope="session")
def init_pivot(request, raw_helix_arr):
    if request.param == "ak":
        yield ak.zip(
            {
                "x": ak.zeros_like(raw_helix_arr[..., 0]),
                "y": ak.zeros_like(raw_helix_arr[..., 0]),
                "z": ak.zeros_like(raw_helix_arr[..., 0]),
            },
            with_name="Vector3D",
        )
    else:
        yield (0.0, 0.0, 0.0)


@pytest.fixture(scope="session")
def raw_pivot(request, raw_helix_arr):
    if request.param == "ak":
        yield (
            ak.zip(
                {
                    "x": ak.zeros_like(raw_helix_arr[..., 0]),
                    "y": ak.zeros_like(raw_helix_arr[..., 0]),
                    "z": ak.zeros_like(raw_helix_arr[..., 0]),
                },
                with_name="Vector3D",
            ),
        )
    elif request.param == "tuple":
        yield (0.0, 0.0, 0.0)
    else:
        raise ValueError(f"Unknown raw_pivot type: {request.param}")


@pytest.fixture(scope="session")
def new_pivot(request, raw_helix_arr):
    if request.param == "ak":
        yield (
            ak.zip(
                {
                    "x": ak.ones_like(raw_helix_arr[..., 0]) * 10,
                    "y": ak.ones_like(raw_helix_arr[..., 0]) * 10,
                    "z": ak.ones_like(raw_helix_arr[..., 0]) * 10,
                },
                with_name="Vector3D",
            ),
        )
    else:
        yield (10, 10, 10)


@pytest.fixture(scope="session")
def cgem_gid_dict(test_data_dir):
    yield uproot.open(test_data_dir / "ref-gid.root")["cgem"].arrays(library="np")


@pytest.fixture(scope="session")
def tof_gid_dict(test_data_dir):
    yield uproot.open(test_data_dir / "ref-gid.root")["tof"].arrays(library="np")


@pytest.fixture(scope="session")
def cgem_geom_dict(test_data_dir):
    yield uproot.open(test_data_dir / "ref_cgem_geom.root")["cgem_strip"].arrays(library="np")


@pytest.fixture(scope="session")
def raw_data_util_ref(test_data_dir):
    res = {}
    with uproot.open(test_data_dir / "ref_raw_data_util.root") as f:
        for key in ["mdc", "tof", "emc"]:
            res[key] = f[key].arrays(library="np")
    yield res


@pytest.fixture(scope="session")
def particle_status_ref(test_data_dir):
    yield uproot.open(test_data_dir / "ref_particle_status.root")["particle_status"].arrays(
        filter_name=["status", "is*", "decay*"]
    )
