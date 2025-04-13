import os
from glob import glob
from pathlib import Path
from typing import Union

cur_dir = Path(__file__).parent
geom_dir = cur_dir / "detectors/geometry"

src_cache_list = [
    (geom_dir / "mdc_geom.npz", geom_dir / "__pycache__/mdc.*.nb[ci]"),
    (geom_dir / "emc_geom.npz", geom_dir / "__pycache__/emc.*.nb[ci]"),
]


def cache_auto_clear(
    sources: Union[Union[Path, str], list[Union[Path, str]]],
    caches: Union[Union[Path, str], list[Union[Path, str]]],
    silent: bool = True,
    force: bool = False,
) -> list[str]:
    """
    Automatically clear the Numba cache if the source files have changed.

    Due to limitation of numba cache, modification of external files like
    geometry data will not trigger the cache clearing. This function is
    designed to trigger the cache clearing when those external files are
    modified.

    This function compares the modification times of the source files with the
    modification times of the cached files. If any source file is newer than
    the cached files, the numba cache in cache directory will be cleared.

    !!! note
        There is no need to trace `*.py` files, as numba will automatically
        clear the cache when the source code is modified.

    Args:
        sources: A glob pattern or a list of glob patterns to match the source files.
        caches: A glob pattern or a list of glob patterns to match the cached files.
        silent: If True, suppresses the output messages.
        force: If True, forces the cache clearing even if the source files are not newer.

    Returns:
        list[str]: A list of cache files that were removed.
    """
    # Transform sources and caches to lists of strings
    sources: list[str] = (
        glob(str(sources))
        if isinstance(sources, (Path, str))
        else sum([glob(str(s)) for s in sources], [])
    )

    caches: list[str] = (
        glob(str(caches))
        if isinstance(caches, (Path, str))
        else sum([glob(str(c)) for c in caches], [])
    )

    # Check if sources and caches are empty
    if not sources:
        raise ValueError("No source files found.")

    if not caches:
        return []

    # Compare modification times
    removed_caches = []
    failed_removed_caches = []

    src_latest_mtime = max([os.path.getmtime(s) for s in sources if os.path.isfile(s)])
    cache_earliest_mtime = min([os.path.getmtime(c) for c in caches if os.path.isfile(c)])

    if src_latest_mtime > cache_earliest_mtime or force:
        # Remove the cache files
        for c in caches:
            try:
                os.remove(c)
                removed_caches.append(c)
            except FileNotFoundError:
                pass
            except Exception:
                failed_removed_caches.append(c)

    # Check failure of removing
    if failed_removed_caches:
        error_msg = "Cannot remove cache files:\n"
        for c in failed_removed_caches:
            error_msg += f" - {c}\n"
        error_msg += "This may cause wrong results from corresponding functions. "
        error_msg += "Please check their permissions or remove them manually."
        raise ImportError(error_msg)

    # Print messages if not silent
    if not silent:
        if removed_caches:
            removed_caches_str = "\n - ".join(removed_caches)
            print(f"Removed cache files: {removed_caches_str}")

    # Return the list of removed caches
    return removed_caches


def check_numba_cache():
    """
    Check the cache files and remove them if the source files are newer.
    This function should be called when the module is imported.

    When environment variable `PYBES3_NUMBA_CACHE_SILENT` is set to 1,
    the function will print out removal messages.
    """
    silent = os.getenv("PYBES3_NUMBA_CACHE_SILENT", "0") == "0"
    for src, cache in src_cache_list:
        cache_auto_clear(
            sources=src,
            caches=cache,
            silent=silent,
            force=False,
        )


def clear_numba_cache():
    """
    Clear the cache files regardless of the source files.

    When environment variable `PYBES3_NUMBA_CACHE_SILENT` is set to 1,
    the function will print out removal messages.
    """
    silent = os.getenv("PYBES3_NUMBA_CACHE_SILENT", "0") == "0"
    for src, cache in src_cache_list:
        cache_auto_clear(
            sources=src,
            caches=cache,
            silent=silent,
            force=True,
        )
