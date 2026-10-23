import pytest
import uproot


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
