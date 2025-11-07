from pathlib import Path

import pytest

import pybes3


@pytest.fixture(scope="session")
def data_dir():
    yield Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def geom_dir():
    yield Path(pybes3.detectors.geometry.__file__).parent
