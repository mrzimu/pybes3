# MUC

The MUC has 9152 strips in total: 5056 in the barrel (8 segments × 9 layers, 48-112 strips per
layer) and 2048 in each of the two endcaps (4 segments × 8 layers × 64 strips).

## GID conversion

All `muc_gid_to_*` and `get_muc_gid` are backed by compiled NumPy ufuncs.
The calling convention is identical for scalar, NumPy array, and Awkward Array inputs:

=== "Scalar"

    ```python
    import pybes3 as p3

    gid = 0
    part = p3.muc_gid_to_part(gid)          # 0
    segment = p3.muc_gid_to_segment(gid)    # 0
    layer = p3.muc_gid_to_layer(gid)        # 0
    strip = p3.muc_gid_to_strip(gid)        # 0

    gid = p3.get_muc_gid(part, segment, layer, strip)
    ```

=== "NumPy array"

    ```python
    import numpy as np
    import pybes3 as p3

    gid = np.array([0, 2048, 7104])
    part = p3.muc_gid_to_part(gid)          # array([0, 1, 2])
    segment = p3.muc_gid_to_segment(gid)
    layer = p3.muc_gid_to_layer(gid)
    strip = p3.muc_gid_to_strip(gid)

    gid = p3.get_muc_gid(part, segment, layer, strip)
    ```

=== "Awkward Array"

    ```python
    import awkward as ak
    import pybes3 as p3

    gid = ak.Array([[0, 2048], [7104]])
    part = p3.muc_gid_to_part(gid)          # <Array [[0, 1], [2]] type='...'>
    segment = p3.muc_gid_to_segment(gid)
    layer = p3.muc_gid_to_layer(gid)
    strip = p3.muc_gid_to_strip(gid)

    gid = p3.get_muc_gid(part, segment, layer, strip)
    ```

`part` is 0 and 2 for the two endcaps and 1 for the barrel. `segment` is the segment number,
`layer` is the layer (gap) number starting from 0, and `strip` is the strip (channel) number
within the layer.

Use `parse_muc_gid` to parse all fields from a gid at once:

```python
# parse all fields; returns a dict (or ak.Array when the input is an ak.Array)
res = p3.parse_muc_gid(gid)
part = res["part"]
segment = res["segment"]
layer = res["layer"]
strip = res["strip"]

# with geometry information (center and half-lengths)
res_geom = p3.parse_muc_gid(gid, geometry=True)
center_x = res_geom["center_x"]
center_y = res_geom["center_y"]
center_z = res_geom["center_z"]
dx = res_geom["dx"]
dy = res_geom["dy"]
dz = res_geom["dz"]
```

!!! info
    The 8 corner points of strips are **not** returned by `parse_muc_gid`.
    Use `muc_gid_to_point_x`, `muc_gid_to_point_y`, and `muc_gid_to_point_z` to get them individually.

When the input is an `ak.Array`, the result is also an `ak.Array` with record fields.

## Strip position

All `muc_gid_to_center_*`, `muc_gid_to_dx`, `muc_gid_to_dy`, `muc_gid_to_dz` and
`muc_gid_to_point_*` are also backed by compiled NumPy ufuncs.

=== "Scalar"

    ```python
    import pybes3 as p3

    gid = 0
    center_x = p3.muc_gid_to_center_x(gid)
    center_y = p3.muc_gid_to_center_y(gid)
    center_z = p3.muc_gid_to_center_z(gid)

    dx = p3.muc_gid_to_dx(gid)
    dy = p3.muc_gid_to_dy(gid)
    dz = p3.muc_gid_to_dz(gid)
    ```

=== "NumPy array"

    ```python
    import numpy as np
    import pybes3 as p3

    gid = np.array([0, 2048, 7104])
    center_x = p3.muc_gid_to_center_x(gid)
    center_y = p3.muc_gid_to_center_y(gid)
    center_z = p3.muc_gid_to_center_z(gid)

    dx = p3.muc_gid_to_dx(gid)
    dy = p3.muc_gid_to_dy(gid)
    dz = p3.muc_gid_to_dz(gid)
    ```

=== "Awkward Array"

    ```python
    import awkward as ak
    import pybes3 as p3

    gid = ak.Array([[0, 2048], [7104]])
    center_x = p3.muc_gid_to_center_x(gid)
    center_y = p3.muc_gid_to_center_y(gid)
    center_z = p3.muc_gid_to_center_z(gid)

    dx = p3.muc_gid_to_dx(gid)
    dy = p3.muc_gid_to_dy(gid)
    dz = p3.muc_gid_to_dz(gid)
    ```

`dx`, `dy` and `dz` are the half-lengths of the strip box along the x, y and z axes.

---

Each strip has 8 corner points. `muc_gid_to_point_*` take two arguments (`gid` and `point`),
both support scalar/array inputs independently:

=== "Scalar"

    ```python
    import pybes3 as p3

    gid = 0
    x = p3.muc_gid_to_point_x(gid, 0)   # strip 0, point 0
    y = p3.muc_gid_to_point_y(gid, 0)
    z = p3.muc_gid_to_point_z(gid, 0)

    x = p3.muc_gid_to_point_x(gid, 7)   # strip 0, point 7
    y = p3.muc_gid_to_point_y(gid, 7)
    z = p3.muc_gid_to_point_z(gid, 7)
    ```

=== "NumPy array"

    ```python
    import numpy as np
    import pybes3 as p3

    gid = np.array([0, 2048, 7104])

    x = p3.muc_gid_to_point_x(gid, 0)       # multiple strips, point 0
    y = p3.muc_gid_to_point_y(gid, 0)
    z = p3.muc_gid_to_point_z(gid, 0)

    point_id = np.arange(8)
    x = p3.muc_gid_to_point_x(0, point_id)  # strip 0, all 8 points
    y = p3.muc_gid_to_point_y(0, point_id)
    z = p3.muc_gid_to_point_z(0, point_id)
    ```

=== "Awkward Array"

    ```python
    import awkward as ak
    import pybes3 as p3

    gid = ak.Array([[0, 2048], [7104]])
    point = ak.Array([0, 1, 2])

    x = p3.muc_gid_to_point_x(gid, 0)       # jagged strips, point 0
    x = p3.muc_gid_to_point_x(0, point)     # strip 0, jagged points
    ```

---

Retrieve the full strip position table:

```python
# get table in `dict[str, np.ndarray]`
strip_position_np = p3.get_muc_geom_table()

# get table in `ak.Array`
strip_position_ak = p3.get_muc_geom_table(library="ak")

# get table in `pd.DataFrame`
strip_position_pd = p3.get_muc_geom_table(library="pd")
```

The table holds `gid`, `part`, `segment`, `layer`, `strip`, `center_x`, `center_y`, `center_z`,
`dx`, `dy`, `dz`, and the 8 corner points of each strip (`x0`-`x7`, `y0`-`y7`, `z0`-`z7`).
