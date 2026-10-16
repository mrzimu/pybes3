"""Sphinx configuration for the pybes3 documentation."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as get_version

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
exclude_patterns = ["_build"]

# Render single backticks as inline code, as in Markdown files.
default_role = "code"

# Language used to highlight code blocks without an explicit language.
highlight_language = "python"

myst_enable_extensions = [
    "colon_fence",  # ::: fenced directives and admonitions
    "dollarmath",  # $...$ and $$...$$ math
]

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
