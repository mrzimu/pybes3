## v0.1.1
* Add: Check version of `pybes3` and warn if it is not the latest version
* Add: Automatically recover zipped symetric error matrix to full matrix
* Fix: `pybes3.besio.uproot_wrappers.tobject_np2ak` now correctly convert `TObject` to `ak.Array`

## 0.1.0.2
* Fix: repeatedly import `pybes3` wrap `TBranchElement.branches` multiple times
