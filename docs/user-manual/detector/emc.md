# EMC

## Index conversion

All `emc_idx_to_*` and `get_emc_idx` are decorated with `@nb.vectorize`.
The calling convention is identical for scalar, NumPy array, and Awkward Array inputs:

=== "Scalar"

    ```python
    import pybes3 as p3

    idx = 0
    part = p3.emc_idx_to_part(idx)          # 0
    theta = p3.emc_idx_to_theta(idx)
    phi = p3.emc_idx_to_phi(idx)

    idx = p3.get_emc_idx(part, theta, phi)
    ```

=== "NumPy array"

    ```python
    import numpy as np
    import pybes3 as p3

    idx = np.array([0, 100, 5000])
    part = p3.emc_idx_to_part(idx)          # array([0, 0, 1])
    theta = p3.emc_idx_to_theta(idx)
    phi = p3.emc_idx_to_phi(idx)

    idx = p3.get_emc_idx(part, theta, phi)
    ```

=== "Awkward Array"

    ```python
    import awkward as ak
    import pybes3 as p3

    idx = ak.Array([[0, 100], [5000]])
    part = p3.emc_idx_to_part(idx)          # <Array [[0, 0], [1]] type='...'>
    theta = p3.emc_idx_to_theta(idx)
    phi = p3.emc_idx_to_phi(idx)

    idx = p3.get_emc_idx(part, theta, phi)
    ```

## Crystals position

All `emc_idx_to_front_center_*`, `emc_idx_to_center_*`, `emc_idx_to_point_*` are also `@nb.vectorize` functions.

=== "Scalar"

    ```python
    import pybes3 as p3

    idx = 0
    front_center_x = p3.emc_idx_to_front_center_x(idx)
    front_center_y = p3.emc_idx_to_front_center_y(idx)
    front_center_z = p3.emc_idx_to_front_center_z(idx)

    center_x = p3.emc_idx_to_center_x(idx)
    center_y = p3.emc_idx_to_center_y(idx)
    center_z = p3.emc_idx_to_center_z(idx)
    ```

=== "NumPy array"

    ```python
    import numpy as np
    import pybes3 as p3

    idx = np.array([0, 100, 5000])
    front_center_x = p3.emc_idx_to_front_center_x(idx)
    front_center_y = p3.emc_idx_to_front_center_y(idx)
    front_center_z = p3.emc_idx_to_front_center_z(idx)

    center_x = p3.emc_idx_to_center_x(idx)
    center_y = p3.emc_idx_to_center_y(idx)
    center_z = p3.emc_idx_to_center_z(idx)
    ```

=== "Awkward Array"

    ```python
    import awkward as ak
    import pybes3 as p3

    idx = ak.Array([[0, 100], [5000]])
    front_center_x = p3.emc_idx_to_front_center_x(idx)
    front_center_y = p3.emc_idx_to_front_center_y(idx)
    front_center_z = p3.emc_idx_to_front_center_z(idx)

    center_x = p3.emc_idx_to_center_x(idx)
    center_y = p3.emc_idx_to_center_y(idx)
    center_z = p3.emc_idx_to_center_z(idx)
    ```

---

Each crystal has 8 corner points. `emc_idx_to_point_*` take two arguments (`idx` and `point`),
both support scalar/array inputs independently:

=== "Scalar"

    ```python
    import pybes3 as p3

    idx = 0
    x = p3.emc_idx_to_point_x(idx, 0)   # crystal 0, point 0
    y = p3.emc_idx_to_point_y(idx, 0)
    z = p3.emc_idx_to_point_z(idx, 0)

    x = p3.emc_idx_to_point_x(idx, 7)   # crystal 0, point 7
    y = p3.emc_idx_to_point_y(idx, 7)
    z = p3.emc_idx_to_point_z(idx, 7)
    ```

=== "NumPy array"

    ```python
    import numpy as np
    import pybes3 as p3

    idx = np.array([0, 100, 5000])

    x = p3.emc_idx_to_point_x(idx, 0)       # multiple crystals, point 0
    y = p3.emc_idx_to_point_y(idx, 0)
    z = p3.emc_idx_to_point_z(idx, 0)

    point_id = np.arange(8)
    x = p3.emc_idx_to_point_x(0, point_id)  # crystal 0, all 8 points
    y = p3.emc_idx_to_point_y(0, point_id)
    z = p3.emc_idx_to_point_z(0, point_id)
    ```

=== "Awkward Array"

    ```python
    import awkward as ak
    import pybes3 as p3

    idx = ak.Array([[0, 100], [5000]])
    point = ak.Array([0, 1, 2])

    x = p3.emc_idx_to_point_x(idx, 0)       # jagged crystals, point 0
    x = p3.emc_idx_to_point_x(0, point)     # crystal 0, jagged points
    ```

---

Retrieve the full crystal position table:

```python
# get table in `dict[str, np.ndarray]`
crystal_position_np = p3.get_emc_geom_table()

# get table in `ak.Array`
crystal_position_ak = p3.get_emc_geom_table(library="ak")

# get table in `pd.DataFrame`
crystal_position_pd = p3.get_emc_geom_table(library="pd")
```

## Barrel geometry

Some geometry constants of the EMC barrel are available:

```python
p3.emc_barrel_h1
p3.emc_barrel_h2
p3.emc_barrel_h3
p3.emc_barrel_l
p3.emc_barrel_r
p3.emc_barrel_offset_1
p3.emc_barrel_offset_2
```

These constants are exported from `EmcRecGeoSvc` in `BOSS`.

## Index parser

Use `parse_emc_idx` to parse all fields from an index at once:

```python
# parse all fields; returns a dict (or ak.Array when the input is an ak.Array)
res = p3.parse_emc_idx(idx)
part = res["part"]
theta = res["theta"]
phi = res["phi"]

# with geometry information (front center and center)
res_geom = p3.parse_emc_idx(idx, geometry=True)
front_center_x = res_geom["front_center_x"]
front_center_y = res_geom["front_center_y"]
front_center_z = res_geom["front_center_z"]
center_x = res_geom["center_x"]
center_y = res_geom["center_y"]
center_z = res_geom["center_z"]
```

!!! info
    The 8 corner points of crystals are **not** returned by `parse_emc_idx`.
    Use `emc_idx_to_point_x`, `emc_idx_to_point_y`, and `emc_idx_to_point_z` to get them individually.

When the input is an `ak.Array`, the result is also an `ak.Array` with record fields.
