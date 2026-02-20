import subprocess

import pytest

pytest.importorskip("mkdocs")


def test_mkdocs_build(monkeypatch):
    """Test that mkdocs build runs without errors."""

    # set environment variable to silence the MkDocs 2.0 warning
    monkeypatch.setenv("NO_MKDOCS_2_WARNING", "1")

    try:
        result = subprocess.run(
            ["mkdocs", "build"], check=True, capture_output=True, text=True
        )
        assert result.returncode == 0, "mkdocs build failed"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"mkdocs build failed with error: {e.stderr}")
