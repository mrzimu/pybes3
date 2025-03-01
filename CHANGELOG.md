## v0.1.2.4
* Modify `pybes3.detectors.identify`: Replace `nb.bool` with `nb.boolean` to improve compatibility with `numba`

## v0.1.2.2-v0.1.2.3
* Add github workflows `python-publish`
* Remove version checking in `__init__.py`
* Improve `pyproject.toml`
* Improve `README.md`

## v0.1.2.1
* Modify: `pybes3.detectors.identify` merge scintillator and MRPC information into same fields: `part`, `layerOrModule`, `phiOrStrip`, `end`.

## v0.1.2
* Add: `pybes3.detectors.identify` module to parse detector ids read from `TDigiEvent`.
* Add: Use `MkDocs` to generate documentation.

## v0.1.1
* Add: Check version of `pybes3` and warn if it is not the latest version
* Add: Automatically recover zipped symetric error matrix to full matrix
* Fix: `pybes3.besio.uproot_wrappers.tobject_np2ak` now correctly convert `TObject` to `ak.Array`

## 0.1.0.2
* Fix: repeatedly import `pybes3` wrap `TBranchElement.branches` multiple times
