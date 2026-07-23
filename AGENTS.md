# AGENTS.md — pybes3

## Language

**This is an English-only project. All code, comments, documentation, commit messages, and AI-generated responses must be in English. Do not use Chinese or any other language.**

## Virtual Environment (Critical)

**Always check for and activate the virtual environment before running any Python command.**

- A `.venv/` virtual environment exists at the project root.
- All Python commands (`python`, `pytest`, `mkdocs`, `ruff`, `pip`, etc.) must use executables under `.venv/bin/`, or first `source .venv/bin/activate`.
- Some commands (e.g. `mkdocs`) rely on PATH resolution and will raise `FileNotFoundError` if the virtual environment is not activated, so **always activate first**:

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
| Build docs | `source .venv/bin/activate && mkdocs build` |
| Preview docs | `source .venv/bin/activate && mkdocs serve` |
| Build package | `source .venv/bin/activate && python -m build` |
| Install in dev mode | `source .venv/bin/activate && pip install -e .` |

## Project Overview

`pybes3` is a Python module for the BES3 particle physics experiment, providing data reading, detector identifier conversion, geometry information, and helix operations. C++ extensions are bound via pybind11, located in the `kernels/` directory.

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
docs/                # Documentation (mkdocs-material)
_tmp/                # Temporary/experimental scripts
```

## Key Conventions

- **gid naming**: The public API consistently uses `gid` (global ID). The underlying C++ kernel internally uses `idx`. See `docs/convention/global-id.md`.
- **Deprecation pattern**: Use `warnings.warn` + `DeprecationWarning`, and keep deprecated function references in documentation. See `/memories/repo/pybes3-conventions.md`.
- **NumPy C-API**: Every translation unit that uses the NumPy C-API must call `_import_array` / `_import_umath` for initialization, otherwise it will crash at `PyUFunc_FromFuncAndData`.
- **C++ compilation**: Uses `-Wall -Werror`, C++20 standard.

## More Information

- User documentation: `docs/`
- Repository conventions: `/memories/repo/pybes3-conventions.md`
- Project configuration: `pyproject.toml`
