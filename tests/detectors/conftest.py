import pytest
import uproot


@pytest.fixture(scope="session")
def cgem_gid_dict(test_data_dir):
    yield uproot.open(test_data_dir / "ref-gid.root")["cgem"].arrays(library="np")


@pytest.fixture(scope="session")
def tof_gid_dict(test_data_dir):
    yield uproot.open(test_data_dir / "ref-gid.root")["tof"].arrays(library="np")
