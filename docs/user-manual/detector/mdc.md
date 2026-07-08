# MDC

## Index conversion

All `mdc_idx_to_*`, `mdc_layer_to_*` and `get_mdc_idx` are decorated with `@nb.vectorize`.
The calling convention is identical for scalar, NumPy array, and Awkward Array inputs:

=== "Scalar"

    ```python
    import pybes3 as p3

    idx = 0
    layer = p3.mdc_idx_to_layer(idx)        # 0
    wire = p3.mdc_idx_to_wire(idx)
    stereo = p3.mdc_idx_to_stereo(idx)
    is_stereo = p3.mdc_idx_to_is_stereo(idx)
    superlayer = p3.mdc_idx_to_superlayer(idx)

    # also available from layer directly
    is_stereo = p3.mdc_layer_to_is_stereo(layer)
    superlayer = p3.mdc_layer_to_superlayer(layer)

    idx = p3.get_mdc_idx(layer, wire)
    ```

=== "NumPy array"

    ```python
    import numpy as np
    import pybes3 as p3

    idx = np.array([0, 100, 5000])
    layer = p3.mdc_idx_to_layer(idx)        # array([ 0,  2, 36])
    wire = p3.mdc_idx_to_wire(idx)
    stereo = p3.mdc_idx_to_stereo(idx)
    is_stereo = p3.mdc_idx_to_is_stereo(idx)
    superlayer = p3.mdc_idx_to_superlayer(idx)

    # also available from layer directly
    is_stereo = p3.mdc_layer_to_is_stereo(layer)
    superlayer = p3.mdc_layer_to_superlayer(layer)

    idx = p3.get_mdc_idx(layer, wire)
    ```

=== "Awkward Array"

    ```python
    import awkward as ak
    import pybes3 as p3

    idx = ak.Array([[0, 100], [5000]])
    layer = p3.mdc_idx_to_layer(idx)        # <Array [[0, 2], [36]] type='...'>
    wire = p3.mdc_idx_to_wire(idx)
    stereo = p3.mdc_idx_to_stereo(idx)
    is_stereo = p3.mdc_idx_to_is_stereo(idx)
    superlayer = p3.mdc_idx_to_superlayer(idx)

    # also available from layer directly
    is_stereo = p3.mdc_layer_to_is_stereo(layer)
    superlayer = p3.mdc_layer_to_superlayer(layer)

    idx = p3.get_mdc_idx(layer, wire)
    ```

!!! note
    `mdc_idx_to_stereo` returns the stereo type of the wire, which can be `0` (axial), `-1` for `west_phi < east_phi` and `1` for `west_phi > east_phi`.

## Wires position

All `mdc_idx_to_west_*`, `mdc_idx_to_east_*`, `mdc_idx_z_to_*` are also `@nb.vectorize` functions.

=== "Scalar"

    ```python
    import pybes3 as p3

    idx = 0
    west_x = p3.mdc_idx_to_west_x(idx)
    west_y = p3.mdc_idx_to_west_y(idx)
    west_z = p3.mdc_idx_to_west_z(idx)

    east_x = p3.mdc_idx_to_east_x(idx)
    east_y = p3.mdc_idx_to_east_y(idx)
    east_z = p3.mdc_idx_to_east_z(idx)
    ```

=== "NumPy array"

    ```python
    import numpy as np
    import pybes3 as p3

    idx = np.array([0, 100, 5000])
    west_x = p3.mdc_idx_to_west_x(idx)
    west_y = p3.mdc_idx_to_west_y(idx)
    west_z = p3.mdc_idx_to_west_z(idx)

    east_x = p3.mdc_idx_to_east_x(idx)
    east_y = p3.mdc_idx_to_east_y(idx)
    east_z = p3.mdc_idx_to_east_z(idx)
    ```

=== "Awkward Array"

    ```python
    import awkward as ak
    import pybes3 as p3

    idx = ak.Array([[0, 100], [5000]])
    west_x = p3.mdc_idx_to_west_x(idx)
    west_y = p3.mdc_idx_to_west_y(idx)
    west_z = p3.mdc_idx_to_west_z(idx)

    east_x = p3.mdc_idx_to_east_x(idx)
    east_y = p3.mdc_idx_to_east_y(idx)
    east_z = p3.mdc_idx_to_east_z(idx)
    ```

---

Get the x, y coordinates of a wire at a specific z position.
`mdc_idx_z_to_x` / `mdc_idx_z_to_y` take two arguments (`idx` and `z`), both support scalar/array inputs independently:

=== "Scalar"

    ```python
    import pybes3 as p3

    idx = 0
    x = p3.mdc_idx_z_to_x(idx, 10.0)    # wire 0 at z=10 cm
    y = p3.mdc_idx_z_to_y(idx, 10.0)

    idx = 100
    x = p3.mdc_idx_z_to_x(idx, 10.0)    # wire 100 at z=10 cm
    ```

=== "NumPy array"

    ```python
    import numpy as np
    import pybes3 as p3

    idx = np.array([0, 100, 5000])
    z = np.array([-1.0, 0.0, 1.0])

    x = p3.mdc_idx_z_to_x(0, z)         # wire 0 at multiple z
    y = p3.mdc_idx_z_to_y(0, z)

    x = p3.mdc_idx_z_to_x(idx, 10.0)    # multiple wires at z=10 cm
    y = p3.mdc_idx_z_to_y(idx, 10.0)
    ```

=== "Awkward Array"

    ```python
    import awkward as ak
    import pybes3 as p3

    idx = ak.Array([[0, 100], [5000]])
    z = ak.Array([[-1.0, 0.0], [1.0]])

    x = p3.mdc_idx_z_to_x(0, z)         # wire 0 at jagged z
    x = p3.mdc_idx_z_to_x(idx, 10.0)    # jagged wires at z=10 cm
    ```

---

Retrieve the full wire position table:

```python
# get table in `dict[str, np.ndarray]`
wire_position_np = p3.get_mdc_geom_table()

# get table in `ak.Array`
wire_position_ak = p3.get_mdc_geom_table(library="ak")

# get table in `pd.DataFrame`
wire_position_pd = p3.get_mdc_geom_table(library="pd")
```

## Index parser

Use `parse_mdc_idx` to parse all fields from an index at once:

```python
import numpy as np
import pybes3 as p3

# generate random wire index
idx = np.random.randint(0, 6796, 100)

# parse all fields; returns a dict (or ak.Array when the input is an ak.Array)
res = p3.parse_mdc_idx(idx)
layer = res["layer"]
wire = res["wire"]
stereo = res["stereo"]
is_stereo = res["is_stereo"]
superlayer = res["superlayer"]

# with geometry information (west/east endpoints and mid-point at z=0)
res_geom = p3.parse_mdc_idx(idx, geometry=True)
mid_x = res_geom["mid_x"]
mid_y = res_geom["mid_y"]
west_x = res_geom["west_x"]
west_y = res_geom["west_y"]
west_z = res_geom["west_z"]
east_x = res_geom["east_x"]
east_y = res_geom["east_y"]
east_z = res_geom["east_z"]
```

When the input is an `ak.Array`, the result is also an `ak.Array` with record fields.
