# Documentation for pybes3

`pybes3` is an **unofficial** python module that aims to make BES3 user easier to work with Python.

!!! abstract "Help us improve `pybes3`!"
    If you have any suggestions, questions, or issues, please feel free to open an [issue](https://github.com/mrzimu/pybes3/issues/new/choose).

!!! tip "See Also"
    It is highly recommended to take a look at these Python modules before using `pybes3`:

    - [`awkward`](https://awkward-array.org/doc/stable/index.html): A Python module that can handle ragged-like array.
    - [`uproot`](https://uproot.readthedocs.io/en/stable/): A ROOT I/O Python module. `pybes3` uses `uproot` to read BES3 ROOT files.

<div class="grid cards" markdown>

- <a href="installation" style="text-decoration: none; color: inherit;">
    :material-download: __Install `pybes3`__ using `pip`
  </a>

- <a href="#user-manual" style="text-decoration: none; color: inherit;">
    :material-run-fast: __Get started__ with user manual
  </a>

</div>

## User manual

<div class="grid cards" markdown>
- <a href="user-manual/bes3-data-reading" style="text-decoration: none; color: inherit;">
    :material-import: __BES3 data reading__
    
    Read `rtraw`, `rec`, `dst`, and even `raw` files.
  </a>
</div>

<div class="grid cards" markdown>
- <a href="user-manual/digi-identifier" style="text-decoration: none; color: inherit;">
    :material-scatter-plot: __Digi identifier__

    Convert digi identifier id number to a human-readable format.
  </a>
</div>

<div class="grid cards" markdown>
- <a href="user-manual/detector/global-id" style="text-decoration: none; color: inherit;">
    :material-identifier: __Global ID__

    Global ID numbers for each detector element in `pybes3`.
  </a>
</div>

<div class="grid cards" markdown>
- <a href="user-manual/detector/geometry" style="text-decoration: none; color: inherit;">
    :material-crosshairs-gps: __Geometry__

    Retrieve and compute geometry information of detectors.
  </a>
</div>

<div class="grid cards" markdown>
- <a href="user-manual/helix" style="text-decoration: none; color: inherit;">
    :material-vector-curve: __Helix operations__

    Parse and transform track parameters, such as helix, etc.
  </a>
</div>
