## v0.3.4

* Fix: When reading 0 entry, `besio` will break because `ak.unflatten` doesn't support empty input.

## v0.3.3

* Fix: Call `ak.zip` when creating `Helix` array.
* Modify: Make `nb.vectorize` AOT to JIT.

## v0.3.2

* Optimize `besio`: Better reconstruct `ak.Array` from raw data.
* Add `_utils.py` to store utility methods.

## v0.3.1

* Optimize `besio`:
  * Fix some reading bugs.
  * Better reconstruct `ak.Array` from raw data.

## v0.3.0

* Add `pybes3.tracks.helix`, support:

  - Helix parameter conversion to/from physical variables.
  - Helix comparison.
  - Pivot transformation.
* Deprecate old helix operations, move it to `pybes3.tracks.old_helix`.

## v0.2.1.2

* Modify `pybes3.tracks`: Replace `np.acos` with `np.arccos`, `np.atan2` with `np.arctan2` to improve compatibility with `numpy`
* Fix mistake in `superlayer` field of `mdc_geom.npz` in `pybes3.detectors.geometry` again

## v0.2.1.1

* Fix mistake in `superlayer` field of `mdc_geom.npz` in `pybes3.detectors.geometry`
* Extend position filed of `mdc_geom.npz` from `np.float32` to `np.float64`

## v0.2.1

* Add EMC geometry methods to `pybes3.detectors.geometry`
* Add MDC `superlayer` and `stereo` fields to `pybes3.detectors.geometry`
* Modify: Expose `pybes3.detectors` methods to `pybes3` namespace

## v0.2.0.1

* Fix `phi` calculation in `pybes3.tracks.parse_helix`
* Improve `theta` calculation in `pybes3.tracks.parse_helix`

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

## v0.1.2.2 - v0.1.2.3

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
