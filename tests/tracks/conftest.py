import awkward as ak
import pytest
import uproot


@pytest.fixture(scope="session")
def mdc_trk(data_dir):
    yield uproot.open(data_dir / "test_full_mc_evt_1.dst")[
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
