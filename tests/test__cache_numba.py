import importlib
import os
from pathlib import Path

import pybes3 as p3


def test_detector_geometry_mdc(capsys, monkeypatch):
    monkeypatch.setenv("PYBES3_NUMBA_CACHE_SILENT", "1")

    geom_dir = Path(p3.detectors.geometry.__file__).parent

    # Change mdc_geom.npz mtime
    mdc_geom_path = geom_dir / "mdc_geom.npz"
    os.utime(mdc_geom_path)

    # Reload pybes3
    importlib.reload(p3)

    # Check output
    captured = capsys.readouterr()
    assert captured.out.startswith("Removed cache files:")


def test_detector_geometry_emc(capsys, monkeypatch):
    monkeypatch.setenv("PYBES3_NUMBA_CACHE_SILENT", "1")

    geom_dir = Path(p3.detectors.geometry.__file__).parent

    # Change emc_geom.npz mtime
    emc_geom_path = geom_dir / "emc_geom.npz"
    os.utime(emc_geom_path)

    # Reload pybes3
    importlib.reload(p3)

    # Check output
    captured = capsys.readouterr()
    assert captured.out.startswith("Removed cache files:")


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v", "-s"])
