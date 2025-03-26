# Geometry

`pybes3` provides a set of methods to retrieve theoretical geometry information of detectors.

**The unit of length is `cm`.**

## MDC

### GID conversion

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

### Wires position

To get west/east x, y, z of wires:

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

To get x, y of wires at a specific z:

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

You can get the whole wires position table of MDC:

```python
# get table in `dict[str, np.ndarray]`
wire_position_np = p3.get_mdc_wire_position() 

# get table in `ak.Array`
wire_position_ak = p3.get_mdc_wire_position(library="ak")

# get table in `pd.DataFrame`
wire_position_pd = p3.get_mdc_wire_position(library="pd")
```

## EMC

### GID conversion

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

### Crystals position

To get front center, center x, y, z of crystals:

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

There are total 8 points on a crystal, you can get x, y, z of these points:

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

You can get the whole crystals position table of EMC:

```python
# get table in `dict[str, np.ndarray]`
crystal_position_np = p3.get_emc_crystal_position()

# get table in `ak.Array`
crystal_position_ak = p3.get_emc_crystal_position(library="ak")

# get table in `pd.DataFrame`
crystal_position_pd = p3.get_emc_crystal_position(library="pd")
```

### Barrel geometry

Some geometry constants of EMC barrel can be obtained:

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
