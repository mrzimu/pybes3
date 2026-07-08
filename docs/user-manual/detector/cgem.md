# CGEM

## Index conversion

All `cgem_idx_to_*` and `get_cgem_idx` are decorated with `@nb.vectorize`.
The calling convention is identical for scalar, NumPy array, and Awkward Array inputs:

=== "Scalar"

    ```python
    import pybes3 as p3

    idx = 0
    layer = p3.cgem_idx_to_layer(idx)       # 0
    sheet = p3.cgem_idx_to_sheet(idx)
    strip_type = p3.cgem_idx_to_strip_type(idx)
    strip = p3.cgem_idx_to_strip(idx)

    is_xstrip = p3.cgem_idx_to_is_xstrip(idx)
    is_vstrip = p3.cgem_idx_to_is_vstrip(idx)

    idx = p3.get_cgem_idx(layer, sheet, strip_type, strip)
    ```

=== "NumPy array"

    ```python
    import numpy as np
    import pybes3 as p3

    idx = np.array([0, 100, 5000])
    layer = p3.cgem_idx_to_layer(idx)       # array([0, 0, 1])
    sheet = p3.cgem_idx_to_sheet(idx)
    strip_type = p3.cgem_idx_to_strip_type(idx)
    strip = p3.cgem_idx_to_strip(idx)

    is_xstrip = p3.cgem_idx_to_is_xstrip(idx)
    is_vstrip = p3.cgem_idx_to_is_vstrip(idx)

    idx = p3.get_cgem_idx(layer, sheet, strip_type, strip)
    ```

=== "Awkward Array"

    ```python
    import awkward as ak
    import pybes3 as p3

    idx = ak.Array([[0, 100], [5000]])
    layer = p3.cgem_idx_to_layer(idx)       # <Array [[0, 0], [1]] type='...'>
    sheet = p3.cgem_idx_to_sheet(idx)
    strip_type = p3.cgem_idx_to_strip_type(idx)
    strip = p3.cgem_idx_to_strip(idx)

    is_xstrip = p3.cgem_idx_to_is_xstrip(idx)
    is_vstrip = p3.cgem_idx_to_is_vstrip(idx)

    idx = p3.get_cgem_idx(layer, sheet, strip_type, strip)
    ```

!!! info
    `strip_type=0` for x-strips and `strip_type=1` for v-strips.

## Index parser

Use `parse_cgem_idx` to parse all fields from an index at once:

```python
# parse all fields; returns a dict (or ak.Array when the input is an ak.Array)
res = p3.parse_cgem_idx(idx)
layer = res["layer"]
sheet = res["sheet"]
strip_type = res["strip_type"]
strip = res["strip"]
is_xstrip = res["is_xstrip"]
is_vstrip = res["is_vstrip"]
```

When the input is an `ak.Array`, the result is also an `ak.Array` with record fields.
