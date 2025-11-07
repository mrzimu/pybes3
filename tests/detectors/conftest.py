import pytest
import uproot
import pybes3  # noqa: F401


@pytest.fixture(scope="session")
def rtraw_event(data_dir):
    yield uproot.open(data_dir / "test_full_mc_evt_1.rtraw")["Event/TDigiEvent"].arrays()
