## v0.2.0
* Add `pybes3.detectors.global_id` with MDC global index methods
* Add `pybes3.detectors.geometry` with MDC wire position methods
* Add `r_trk` field in `pybes3.tracks.parse_helix`
* Move `pybes3.detectors.identify` to `pybes3.detectors.digi_id`, rename `parse_xxx_id` to `parse_xxx_digi_id`
* Fix `theta` calculation in `pybes3.tracks.parse_helix`

## v0.1.3
* Add `pybes3.tracks` with function `parse_helix` to transform 5 helix parameters to physical variables

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
