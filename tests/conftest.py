from pathlib import Path

import pytest

import pybes3.data


@pytest.fixture(scope="session")
def test_data_dir():
    yield Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def geom_dir():
    yield pybes3.data.DATA_DIR
