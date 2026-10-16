import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("sphinx")

ROOT = Path(__file__).resolve().parent.parent


def test_sphinx_build(tmp_path):
    """Test that the Sphinx documentation builds without warnings."""

    out_dir = tmp_path / "site"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sphinx",
            "-b",
            "dirhtml",
            "-W",
            "--keep-going",
            str(ROOT / "docs"),
            str(out_dir),
        ],
        capture_output=True,
        check=False,
        text=True,
    )
    assert result.returncode == 0, f"sphinx build failed:\n{result.stdout}\n{result.stderr}"

    # check that the generated pages contain the expected content
    api_index = out_dir / "api" / "pybes3" / "index.html"
    api_page = api_index.read_text(encoding="utf-8")
    assert "mdc_gid_to_layer" in api_page
    assert "helix_awk" in api_page

    manual_page = (out_dir / "user-manual" / "mdc" / "index.html").read_text(encoding="utf-8")
    assert "mdc_gid_to_west_x" in manual_page
