import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("sphinx")

ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.parametrize(
    ("language", "manual_snippet", "index_snippet"),
    [
        pytest.param(None, "Wire position", "Data reading", id="en"),
        pytest.param("zh_CN", "丝的位置", "数据读取", id="zh-cn"),
    ],
)
def test_sphinx_build(tmp_path, language, manual_snippet, index_snippet):
    """
    Test that the Sphinx documentation builds without warnings.
    """

    out_dir = tmp_path / "site"
    command = [sys.executable, "-m", "sphinx", "-b", "dirhtml", "-W", "--keep-going"]
    if language is not None:
        command += ["-D", f"language={language}"]
    command += [str(ROOT / "docs"), str(out_dir)]

    result = subprocess.run(command, capture_output=True, check=False, text=True)
    assert result.returncode == 0, f"sphinx build failed:\n{result.stdout}\n{result.stderr}"

    # check that the generated pages contain the expected content
    api_index = out_dir / "api" / "pybes3" / "index.html"
    api_page = api_index.read_text(encoding="utf-8")
    assert "mdc_gid_to_layer" in api_page
    assert "helix_awk" in api_page

    manual_page = (out_dir / "user-manual" / "mdc" / "index.html").read_text(encoding="utf-8")
    assert "mdc_gid_to_west_x" in manual_page
    assert manual_snippet in manual_page

    index_page = (out_dir / "index.html").read_text(encoding="utf-8")
    assert index_snippet in index_page

    # The Chinese build must ship a browser-side query splitter; the default one
    # only splits on whitespace, so queries without spaces would never match.
    language_data = (out_dir / "_static" / "language_data.js").read_text(encoding="utf-8")
    if language == "zh_CN":
        assert "var splitQuery" in language_data
        # Sphinx appends `window.Stemmer = ChineseStemmer;` to the English stemmer
        # file, which only defines `EnglishStemmer`; that aborts the script.
        assert "ChineseStemmer" not in language_data
    else:
        assert "var splitQuery" not in language_data
