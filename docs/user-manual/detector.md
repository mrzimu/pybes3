# Detector

## MDC

### GID Conversion

Convert between gid and superlayer/layer/wire/stereo/is_stereo numbers:

```python
import numpy as np
import pybes3 as p3

# generate random wire gid
gid = np.random.randint(0, 6796, 100)

# get layer, wire, stereo, is_stereo
layer = p3.mdc_gid_to_layer(gid)
wire = p3.mdc_gid_to_wire(gid)
stereo = p3.mdc_gid_to_stereo(gid)
is_stereo = p3.mdc_gid_to_is_stereo(gid)
superlayer = p3.mdc_gid_to_superlayer(gid)

# is_stereo can also be obtained by layer
is_stereo = p3.mdc_layer_to_is_stereo(layer)

# superlayer can also be obtained by layer
superlayer = p3.mdc_layer_to_superlayer(layer)

# get gid
gid = p3.get_mdc_gid(layer, wire)
```

!!! note
    `mdc_gid_to_stereo` returns the stereo type of the wire, which can be `0` (axial), `-1` for `west_phi < east_phi` and `1` for `west_phi > east_phi`.

Use `parse_mdc_gid` to parse all fields from a gid at once:

```python
import numpy as np
import pybes3 as p3

# generate random wire gid
gid = np.random.randint(0, 6796, 100)

# parse all fields; values are NumPy scalars for scalar gids and arrays for array-like gids
res = p3.parse_mdc_gid(gid)
layer = res["layer"]
wire = res["wire"]
stereo = res["stereo"]
is_stereo = res["is_stereo"]
superlayer = res["superlayer"]

# with geometry information (west/east endpoints and mid-point at z=0)
res_geom = p3.parse_mdc_gid(gid, geometry=True)
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

### Wires position

Get the west/east endpoint coordinates of wires:

```python
# get west x, y, z
west_x = p3.mdc_gid_to_west_x(gid)
west_y = p3.mdc_gid_to_west_y(gid)
west_z = p3.mdc_gid_to_west_z(gid)

# get east x, y, z
east_x = p3.mdc_gid_to_east_x(gid)
east_y = p3.mdc_gid_to_east_y(gid)
east_z = p3.mdc_gid_to_east_z(gid)
```

---

Get the x, y coordinates of a wire at a specific z position:

```python
# get x, y of wire 0 at z = -1, 0, 1 cm
z = np.array([-1, 0, 1])
x = p3.mdc_gid_z_to_x(0, z)
y = p3.mdc_gid_z_to_y(0, z)

# get x, y of wires at z = 10 cm
x_z10 = p3.mdc_gid_z_to_x(gid, 10)
y_z10 = p3.mdc_gid_z_to_y(gid, 10)
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

## TOF

### GID Conversion

Convert between gid and part/layer_or_module/phi_or_strip numbers:

```python
import numpy as np
import pybes3 as p3

# generate random gid
gid = np.random.randint(0, 1136, 100)

# get part, layer_or_module, phi_or_strip
part = p3.tof_gid_to_part(gid)
layer_or_module = p3.tof_gid_to_layer_or_module(gid)
phi_or_strip = p3.tof_gid_to_phi_or_strip(gid)

# get gid
gid = p3.get_tof_gid(part, layer_or_module, phi_or_strip)
```

!!! note
    The convention of `part` field is different from BOSS:

    - 0, 1, 2: scintillator endcap 0, barrel, endcap 1
    - 3, 4: MRPC endcap 0, endcap 1

    The scintillator `layer` and MRPC `module` share the same axis, and the `phi` and `strip` fields also share the same axis.

Use `parse_tof_gid` to parse all fields from a gid at once:

```python
# parse all fields, returns a dict[str, np.ndarray]
res = p3.parse_tof_gid(gid)
part = res["part"]
layer_or_module = res["layer_or_module"]
phi_or_strip = res["phi_or_strip"]
```

When the input is an `ak.Array`, the result is also an `ak.Array` with record fields.

## EMC

### GID Conversion

Convert between gid and part/theta/phi numbers:

```python
import numpy as np
import pybes3 as p3

# generate random crystal gid
gid = np.random.randint(0, 6240, 100)

# get part, theta, phi
part = p3.emc_gid_to_part(gid)
theta = p3.emc_gid_to_theta(gid)
phi = p3.emc_gid_to_phi(gid)

# get gid
gid = p3.get_emc_gid(part, theta, phi)
```

Use `parse_emc_gid` to parse all fields from a gid at once:

```python
# parse all fields, returns a dict[str, np.ndarray]
res = p3.parse_emc_gid(gid)
part = res["part"]
theta = res["theta"]
phi = res["phi"]

# with geometry information (front center and center)
res_geom = p3.parse_emc_gid(gid, geometry=True)
front_center_x = res_geom["front_center_x"]
front_center_y = res_geom["front_center_y"]
front_center_z = res_geom["front_center_z"]
center_x = res_geom["center_x"]
center_y = res_geom["center_y"]
center_z = res_geom["center_z"]
```

!!! info
    The 8 corner points of crystals are **not** returned by `parse_emc_gid`.
    Use `emc_gid_to_point_x/y/z` to get them individually.

When the input is an `ak.Array`, the result is also an `ak.Array` with record fields.

### Crystals position

Get front center and center coordinates of crystals:

```python
# get front center x, y, z
front_center_x = p3.emc_gid_to_front_center_x(gid)
front_center_y = p3.emc_gid_to_front_center_y(gid)
front_center_z = p3.emc_gid_to_front_center_z(gid)

# get center x, y, z
center_x = p3.emc_gid_to_center_x(gid)
center_y = p3.emc_gid_to_center_y(gid)
center_z = p3.emc_gid_to_center_z(gid)
```

---

Each crystal has 8 corner points. You can retrieve their coordinates:

```python
# get x, y, z of point-0 of crystals
x0 = p3.emc_gid_to_point_x(gid, 0)
y0 = p3.emc_gid_to_point_y(gid, 0)
z0 = p3.emc_gid_to_point_z(gid, 0)

# get x, y, z of point-7 of crystals
x7 = p3.emc_gid_to_point_x(gid, 7)
y7 = p3.emc_gid_to_point_y(gid, 7)
z7 = p3.emc_gid_to_point_z(gid, 7)

# get x, y, z of all 8 points of crystal 0
point_id = np.arange(8)
x = p3.emc_gid_to_point_x(0, point_id)
y = p3.emc_gid_to_point_y(0, point_id)
z = p3.emc_gid_to_point_z(0, point_id)
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

### Barrel geometry

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

## MUC

!!! note "Under development"

## CGEM

### GID Conversion

Convert between gid and layer/sheet/strip_type/strip numbers:

```python
import numpy as np
import pybes3 as p3

# generate random gid
gid = np.random.randint(0, 9897, 100)

# get layer, sheet, strip_type, strip
layer = p3.cgem_gid_to_layer(gid)
sheet = p3.cgem_gid_to_sheet(gid)
strip_type = p3.cgem_gid_to_strip_type(gid)
strip = p3.cgem_gid_to_strip(gid)

# check strip type
is_xstrip = p3.cgem_gid_to_is_xstrip(gid)
is_vstrip = p3.cgem_gid_to_is_vstrip(gid)

# get gid
gid = p3.get_cgem_gid(layer, sheet, strip_type, strip)
```

!!! info
    `strip_type=0` for x-strips and `strip_type=1` for v-strips.

Use `parse_cgem_gid` to parse all fields from a gid at once:

```python
res = p3.parse_cgem_gid(gid)
layer = res["layer"]
sheet = res["sheet"]
strip_type = res["strip_type"]
strip = res["strip"]
is_xstrip = res["is_xstrip"]
is_vstrip = res["is_vstrip"]
```

When the input is an `ak.Array`, the result is also an `ak.Array` with record fields.
