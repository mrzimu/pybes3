import subprocess

import pytest

pytest.importorskip("mkdocs")


def test_mkdocs_build():
    """Test that mkdocs build runs without errors."""
    try:
        result = subprocess.run(
            ["mkdocs", "build"], check=True, capture_output=True, text=True
        )
        assert result.returncode == 0, "mkdocs build failed"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"mkdocs build failed with error: {e.stderr}")
