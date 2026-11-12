"""
Sphinx configuration for the pybes3 documentation.
"""

from __future__ import annotations

import os
import sys
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as get_version
from pathlib import Path

# Local Sphinx helpers (`docs/_ext/`); Sphinx does not add the configuration
# directory to `sys.path`.
sys.path.insert(0, str(Path(__file__).resolve().parent / "_ext"))

from zh_search import SearchChineseWithSplitter

# -- Project information -----------------------------------------------------

project = "Pybes3"
author = "Mingrun Li"

try:
    release = get_version("pybes3")
except PackageNotFoundError:  # pragma: no cover - the package is not installed
    release = "0.0.0"

version = ".".join(release.split(".")[:2])

# -- General configuration ---------------------------------------------------

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
]

source_suffix = {".md": "markdown"}
root_doc = "index"
# `locale/` holds the translation catalogs and their handbook, not documents.
exclude_patterns = ["_build", "locale"]

# Render single backticks as inline code, as in Markdown files.
default_role = "code"

# Language used to highlight code blocks without an explicit language.
highlight_language = "python"

myst_enable_extensions = [
    "colon_fence",  # ::: fenced directives and admonitions
    "dollarmath",  # $...$ and $$...$$ math
]

# -- Internationalization ----------------------------------------------------
# The sources under `docs/` are English. Translations live in `docs/locale/`
# and are selected at build time:
#
#   - Read the Docs sets READTHEDOCS_LANGUAGE to the project language (`zh-cn`),
#   - locally, pass `-D language=zh_CN` to sphinx-build.
#
# Untranslated messages fall back to the English source, so a partially
# translated catalog still builds.
#
# Read the Docs reports lowercase, dash-separated codes (`zh-cn`), while Sphinx
# wants the locale name (`zh_CN`).
_LANGUAGES = {"en": "en", "zh_cn": "zh_CN"}

language = _LANGUAGES.get(
    os.environ.get("READTHEDOCS_LANGUAGE", "en").lower().replace("-", "_"), "en"
)

locale_dirs = ["locale"]
gettext_compact = False  # one catalog per document
gettext_uuid = True  # track moved messages when updating catalogs

if language.startswith("zh"):
    # Chinese search needs the jieba tokenizer (installed with the docs group).
    html_search_language = "zh"
    html_search_options = {"type": "jieba"}

# -- Options for extensions --------------------------------------------------

add_module_names = False
autodoc_member_order = "bysource"
autodoc_typehints = "signature"

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_preprocess_types = True
napoleon_use_rtype = True

viewcode_follow_imported_members = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "awkward": ("https://awkward-array.org/doc/main", None),
    "uproot": ("https://uproot.readthedocs.io/en/latest", None),
    "vector": ("https://vector.readthedocs.io/en/latest", None),
}

copybutton_prompt_text = r">>> |\.\.\. "
copybutton_prompt_is_regexp = True

# -- Options for HTML output -------------------------------------------------

html_theme = "furo"
html_title = "Pybes3"
html_static_path = ["_static"]

html_theme_options = {
    "source_repository": "https://github.com/mrzimu/pybes3/",
    "source_branch": "main",
    "source_directory": "docs/",
}

# -- Extension setup ---------------------------------------------------------


def setup(app):
    """
    Register the Chinese search language with a browser-side splitter.
    """
    app.add_search_language(SearchChineseWithSplitter)
