# CGEM

## GID Conversion

All `cgem_gid_to_*` and `get_cgem_gid` are decorated with `@nb.vectorize`.
The calling convention is identical for scalar, NumPy array, and Awkward Array inputs:

=== "Scalar"

    ```python
    import pybes3 as p3

    gid = 0
    layer = p3.cgem_gid_to_layer(gid)       # 0
    sheet = p3.cgem_gid_to_sheet(gid)
    strip_type = p3.cgem_gid_to_strip_type(gid)
    strip = p3.cgem_gid_to_strip(gid)

    is_xstrip = p3.cgem_gid_to_is_xstrip(gid)
    is_vstrip = p3.cgem_gid_to_is_vstrip(gid)

    gid = p3.get_cgem_gid(layer, sheet, strip_type, strip)
    ```

=== "NumPy array"

    ```python
    import numpy as np
    import pybes3 as p3

    gid = np.array([0, 100, 5000])
    layer = p3.cgem_gid_to_layer(gid)       # array([0, 0, 1])
    sheet = p3.cgem_gid_to_sheet(gid)
    strip_type = p3.cgem_gid_to_strip_type(gid)
    strip = p3.cgem_gid_to_strip(gid)

    is_xstrip = p3.cgem_gid_to_is_xstrip(gid)
    is_vstrip = p3.cgem_gid_to_is_vstrip(gid)

    gid = p3.get_cgem_gid(layer, sheet, strip_type, strip)
    ```

=== "Awkward Array"

    ```python
    import awkward as ak
    import pybes3 as p3

    gid = ak.Array([[0, 100], [5000]])
    layer = p3.cgem_gid_to_layer(gid)       # <Array [[0, 0], [1]] type='...'>
    sheet = p3.cgem_gid_to_sheet(gid)
    strip_type = p3.cgem_gid_to_strip_type(gid)
    strip = p3.cgem_gid_to_strip(gid)

    is_xstrip = p3.cgem_gid_to_is_xstrip(gid)
    is_vstrip = p3.cgem_gid_to_is_vstrip(gid)

    gid = p3.get_cgem_gid(layer, sheet, strip_type, strip)
    ```

!!! info
    `strip_type=0` for x-strips and `strip_type=1` for v-strips.

## GID parser

Use `parse_cgem_gid` to parse all fields from a gid at once:

```python
# parse all fields; returns a dict (or ak.Array when gid is an ak.Array)
res = p3.parse_cgem_gid(gid)
layer = res["layer"]
sheet = res["sheet"]
strip_type = res["strip_type"]
strip = res["strip"]
is_xstrip = res["is_xstrip"]
is_vstrip = res["is_vstrip"]
```

When the input is an `ak.Array`, the result is also an `ak.Array` with record fields.
