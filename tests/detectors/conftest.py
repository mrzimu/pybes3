import pytest

import uproot


@pytest.fixture(scope="session")
def cgem_idx_dict(test_data_dir):
    yield uproot.open(test_data_dir / "ref-idx.root")["cgem"].arrays(library="np")


@pytest.fixture(scope="session")
def tof_idx_dict(test_data_dir):
    yield uproot.open(test_data_dir / "ref-idx.root")["tof"].arrays(library="np")
