# AGENTS.md — Pybes3

## Language

**This is an English-only project. All code, comments, documentation, commit messages, and AI-generated responses must be in English. Do not use Chinese or any other language.**

The only exception is the translation catalogs under `docs/locale/<language>/` and their handbook `docs/locale/README.md`, which are Chinese by design (see [Documentation Translations](#documentation-translations)).

## Virtual Environment (Critical)

**Always check for and activate the virtual environment before running any Python command.**

- A `.venv/` virtual environment exists at the project root.
- All Python commands (`python`, `pytest`, `sphinx`, `ruff`, `pip`, etc.) must use executables under `.venv/bin/`, or first `source .venv/bin/activate`.
- Some commands rely on PATH resolution and will raise `FileNotFoundError` if the virtual environment is not activated, so **always activate first**:

```bash
source .venv/bin/activate
```

- If `.venv/` does not exist, the current worktree has not been initialized for development. Remind the user to create a virtual environment first.

## Common Commands

| Action | Command |
|--------|---------|
| Run tests | `source .venv/bin/activate && python -m pytest` |
| Run single test | `source .venv/bin/activate && python -m pytest tests/test_xxx.py -k test_name` |
| Lint | `source .venv/bin/activate && ruff check` |
| Build docs | `source .venv/bin/activate && python -m sphinx -b dirhtml docs build/docs` |
| Preview docs | `source .venv/bin/activate && sphinx-autobuild docs build/docs -b dirhtml` |
| Build Chinese docs | `source .venv/bin/activate && python -m sphinx -b dirhtml -W -D language=zh_CN docs build/docs-zh` |
| Update doc translations | `source .venv/bin/activate && bash dev/update-docs-translations.sh` |
| Build package | `source .venv/bin/activate && python -m build` |
| Install in dev mode | `source .venv/bin/activate && pip install -e .` |

## Documentation Translations

`docs/` holds the English sources, which stay the only source of truth. Chinese lives in gettext catalogs under `docs/locale/zh_CN/LC_MESSAGES/`, maintained with `sphinx-intl` and selected at build time (`-D language=zh_CN` locally, `READTHEDOCS_LANGUAGE` on Read the Docs, where `zh-cn` is a separate project added under the English project's Translations).

- **Do not edit the English `.md` files to make the Chinese build work.** Edit the translations; untranslated messages fall back to English.
- **Regenerate the catalogs with `bash dev/update-docs-translations.sh`** after changing anything under `docs/` (it also prints per-catalog coverage). Then translate the new or `fuzzy` entries; `--no-obsolete` removes entries that disappeared. Rewording or reflowing a paragraph changes its `msgid` and drops the matching translation, so reflow before translating.
- **Docstrings are not translated.** `dev/strip-docstring-messages.py` strips autodoc messages from the catalogs, so API reference pages stay English.
- **Translator rules** (what to keep, terminology) are in `docs/locale/README.md`.

## Project Overview

Pybes3 is a Python module for the BES3 particle physics experiment, providing data reading, detector identifier conversion, geometry information, and helix operations. C++ extensions are bound via pybind11, located in the `kernels/` directory.

- **Package manager**: `uv` (configured in `pyproject.toml` `[tool.uv]`)
- **Build system**: `scikit-build-core` + CMake (C++ extensions in `kernels/CMakeLists.txt`)
- **Python version**: `>=3.9, <3.15`
- **Test framework**: pytest + pytest-subtests
- **Code style**: ruff (line width 95, target py39)

## Project Structure

```
src/pybes3/          # Python source code
kernels/             # C++ extensions (pybind11 + CMake)
tests/               # Tests
docs/                # Documentation (Sphinx + Furo)
docs/locale/         # Translation catalogs (zh_CN) + translator handbook
_tmp/                # Temporary/experimental scripts
```

## Key Conventions

- **gid naming**: The public API consistently uses `gid` (global ID). The underlying C++ kernel internally uses `idx`. See `docs/convention/gid.md`.
- **Deprecation pattern**: Use `warnings.warn` + `DeprecationWarning`, and keep deprecated function references in documentation.
- **No absolute paths**: All file paths in documentation, comments, code, and configuration files must be relative to the project root. Absolute paths (i.e., paths starting with `/`) are not allowed, as they are machine-specific and non-portable.
- **NumPy C-API**: Every translation unit that uses the NumPy C-API must call `_import_array` / `_import_umath` for initialization, otherwise it will crash at `PyUFunc_FromFuncAndData`.
- **C++ compilation**: Uses `-Wall -Werror`, C++20 standard.

## Python Style

- **Google-style docstrings**: Every public module, class, and function documents its inputs, outputs, and errors in `Parameters:`, `Returns:`, and `Raises:` sections, which `docs/conf.py` parses through `sphinx.ext.napoleon`.
- **Docstrings are Markdown-formatted**: use single backticks for inline code (conf.py sets `default_role = "code"`), `**bold**`, `-` bullet lists, and Markdown tables. Autodoc still feeds docstrings to reStructuredText, so block-level constructs that Markdown cannot express there stay RST: `.. note::`, `.. deprecated::`, `.. code-block:: python`, and the `:func:` / `:class:` roles.
- **Triple quotes stand on their own lines**: A triple-quoted string never starts or ends with text on the delimiter line. This applies to one-line docstrings as well.

  ```python
  def tof_gid_to_part(gid: IntLike) -> IntLike:
      """
      Get the TOF part from gid.

      Parameters:
          gid: The TOF strip global ID, ranging from 0 to 1135.

      Returns:
          The part of the TOF strip.
      """
      return _ufuncs.tof_gid_to_part(gid)
  ```

  Not allowed:

  ```python
  def tof_gid_to_part(gid: IntLike) -> IntLike:
      """Get the TOF part from gid."""
      return _ufuncs.tof_gid_to_part(gid)
  ```

## Markdown and Documentation

- **Markdown only**: All files under `docs/` are written in MyST Markdown (`myst_parser`); do not add reStructuredText sources to `docs/`.
- **One paragraph, one line**: Do not hard-wrap prose in `.md` files. A paragraph, and each list item, is a single physical line, and a blank line separates paragraphs; let the editor soft-wrap instead. Editing a sentence then touches one line, so diffs stay small and translation `msgid`s stay stable.
- **Syntax keeps its layout**: tables, code blocks, `:::` directive bodies, block quotes, and nested or indented blocks follow what Markdown/MyST requires, not the one-line rule.

## More Information

- User documentation: `docs/`
- Project configuration: `pyproject.toml`
