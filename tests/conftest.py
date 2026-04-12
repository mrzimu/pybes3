from pathlib import Path

import pytest
import uproot

import pybes3  # noqa: F401
import pybes3.data


@pytest.fixture(scope="session")
def test_data_dir():
    yield Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def geom_dir():
    yield pybes3.data.DATA_DIR


@pytest.fixture(scope="session")
def rtraw_event(test_data_dir):
    yield uproot.open(test_data_dir / "test_full_mc_evt_1.rtraw")[
        "Event/TDigiEvent"
    ].arrays()
