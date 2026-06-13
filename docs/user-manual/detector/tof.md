# TOF

## GID Conversion

All `tof_gid_to_*` and `get_tof_gid` are decorated with `@nb.vectorize`.
The calling convention is identical for scalar, NumPy array, and Awkward Array inputs:

=== "Scalar"

    ```python
    import pybes3 as p3

    gid = 0
    part = p3.tof_gid_to_part(gid)          # 0
    layer_or_module = p3.tof_gid_to_layer_or_module(gid)
    phi_or_strip = p3.tof_gid_to_phi_or_strip(gid)

    gid = p3.get_tof_gid(part, layer_or_module, phi_or_strip)
    ```

=== "NumPy array"

    ```python
    import numpy as np
    import pybes3 as p3

    gid = np.array([0, 100, 500])
    part = p3.tof_gid_to_part(gid)          # array([0, 1, 3])
    layer_or_module = p3.tof_gid_to_layer_or_module(gid)
    phi_or_strip = p3.tof_gid_to_phi_or_strip(gid)

    gid = p3.get_tof_gid(part, layer_or_module, phi_or_strip)
    ```

=== "Awkward Array"

    ```python
    import awkward as ak
    import pybes3 as p3

    gid = ak.Array([[0, 100], [500]])
    part = p3.tof_gid_to_part(gid)          # <Array [[0, 1], [3]] type='...'>
    layer_or_module = p3.tof_gid_to_layer_or_module(gid)
    phi_or_strip = p3.tof_gid_to_phi_or_strip(gid)

    gid = p3.get_tof_gid(part, layer_or_module, phi_or_strip)
    ```

!!! note
    The convention of `part` field is different from BOSS:

    - 0, 1, 2: scintillator endcap 0, barrel, endcap 1
    - 3, 4: MRPC endcap 0, endcap 1

    The scintillator `layer` and MRPC `module` share the same axis, and the `phi` and `strip` fields also share the same axis.

## GID parser

Use `parse_tof_gid` to parse all fields from a gid at once:

```python
# parse all fields; returns a dict (or ak.Array when gid is an ak.Array)
res = p3.parse_tof_gid(gid)
part = res["part"]
layer_or_module = res["layer_or_module"]
phi_or_strip = res["phi_or_strip"]
```

When the input is an `ak.Array`, the result is also an `ak.Array` with record fields.
