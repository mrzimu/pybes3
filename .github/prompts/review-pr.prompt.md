---
description: "Review changes on the current branch as a squash-merge PR against main"
argument-hint: "Review branch diff..."
agent: "agent"
---

Review the current branch changes as if they were a single squash-merged PR targeting `main`.
All commits will be squashed into one, so review the **entire diff holistically** — not commit-by-commit.

## Step 1: Gather the diff

Run these commands to get the full diff and context:

```bash
git diff main...HEAD --stat
git diff main...HEAD
git log main..HEAD --oneline
```

If there are renamed or binary files, use `git diff main...HEAD --diff-filter=R --name-only` to find renames and adjust accordingly.

## Step 2: Summarize the change

Provide a concise overview:
- **What** does this PR do? (1-2 sentences)
- **Why** is it needed? (motivation, linked issue if any)
- **Scope**: which modules / packages are affected?

## Step 3: Review against project conventions

Check adherence to the conventions documented in `.github/` and the repo:

- **Deprecation pattern**: When renaming a public function, keep the old name with a `DeprecationWarning` and `stacklevel=2`, and preserve the docstring reference in `docs/api/pybes3.md`.
- **Docstrings**: All public functions must have NumPy-style docstrings. New modules must be registered in `docs/api/pybes3.md`.
- **Tests**: New features need tests in `tests/`. Run `uv run pytest ./tests/` to verify.

## Step 4: Python code quality review

- **Correctness**: Any logic errors, off-by-one, edge cases?
- **Performance**: Unnecessary copies, loops that could be vectorized, C++/Cython interaction overhead?
- **Error handling**: Are exceptions appropriate and informative? Are edge inputs handled?
- **Type annotations**: Public functions should have type hints.
- **Imports**: Clean, no unused imports, no circular dependencies.

## Step 5: C++ code quality review

If the diff touches any files under `kernels/`, `src/` (C++ sources), `build/`, or `CMakeLists.txt`:

- **Memory safety**: No bare `new`/`delete` — prefer RAII, smart pointers, or stack allocation. Check for potential leaks, use-after-free, buffer overflows.
- **UFunc registration**: Every translation unit that uses NumPy C-API (`_import_array` / `_import_umath`) must call the import function during module initialization. Missing init causes crashes in `PyUFunc_FromFuncAndData`.
- **Cython bindings**: `.pyx` / `.pxd` files must correctly declare C++ interfaces. Check for `except +` on functions that may raise, correct `cimport` paths, and `nogil` usage where appropriate.
- **CMake consistency**: New `.cpp` / `.cxx` / `.pyx` files must be listed in the relevant `CMakeLists.txt`. Check that target names and dependencies are correct.
- **Code style**: Follow `.clang-format` in the repo root. Consistent naming (snake_case for functions, PascalCase for classes), header guards or `#pragma once`.
- **Error handling**: C++ functions called from Python must not abort/terminate — translate errors into Python exceptions via Cython or the C-API.
- **Performance**: Watch for unnecessary copies in tight loops, missed `const &` opportunities, and vectorization potential in numeric kernels.

## Step 6: CI & build configuration

- **Workflows**: Check `.github/workflows/` and `.github/release.yml`. Do any existing workflows need to be updated to cover new files, new dependencies, or new build steps?
- **pre-commit**: Check `.pre-commit-config.yaml`. If new file types or linters are introduced, should pre-commit hooks be updated?
- **Dependencies**: If new Python packages or system libraries are required, are they reflected in `pyproject.toml` and CI install steps?
- **Build matrix**: If the change is platform-specific (Linux-only, Python-version-specific), verify the CI build matrix still covers the right targets.

## Step 7: Documentation & changelog

- Is `CHANGELOG.md` updated with a user-facing summary?
- Are new APIs documented in `docs/api/`?
- Does the docstring clearly explain parameters, return values, and raised exceptions?

## Step 8: Final assessment

Give a verdict with actionable items:
- ✅ **Ready to merge** — or —
- ⚠️ **Approve with suggestions** (list specific changes needed)
- ❌ **Changes requested** (blocking issues, list each)

For each issue found, categorize as:
- 🔴 **Blocking** (must fix before merge)
- 🟡 **Should fix** (important but not a merge-blocker)
- 🟢 **Nice to have** (optional improvement)
