# Geometry

`pybes3` provides a set of methods to retrieve theoretical geometry information of detectors.

**The unit of length is `cm`.**

## MDC

### GID conversion

```python
import numpy as np
from pybes3.detectors import geometry as geom

# generate random wire gid
gid = np.random.randint(0, 6796, 100)

# get layer, wire, is_stereo
layer = geom.mdc_gid_to_layer(gid)
wire = geom.mdc_gid_to_wire(gid)
is_stereo = geom.mdc_gid_to_is_stereo(gid)

# is_stereo can also be obtained by layer
is_stereo = geom.mdc_layer_to_is_stereo(layer)

# get gid
gid = geom.get_mdc_gid(layer, wire)
```

### Wires position

To get west/east x, y, z of wires:

```python
# get west x, y, z
west_x = geom.mdc_gid_to_west_x(gid)
west_y = geom.mdc_gid_to_west_y(gid)
west_z = geom.mdc_gid_to_west_z(gid)

# get east x, y, z
east_x = geom.mdc_gid_to_east_x(gid)
east_y = geom.mdc_gid_to_east_y(gid)
east_z = geom.mdc_gid_to_east_z(gid)
```

---

To get x, y of wires at a specific z:

```python
# get x, y of wire 0 at z = -1, 0, 1 cm
z = np.array([-1, 0, 1])
x, y = geom.mdc_gid_z_to_x_y(0, z)

# get x, y of wires at z = 10 cm
x_z10 = geom.mdc_gid_z_to_x(gid, 10)
y_z10 = geom.mdc_gid_z_to_y(gid, 10)
```

---

You can get the whole wires position table of MDC:

```python
# get table in `dict[str, np.ndarray]`
wire_position_np = geom.get_mdc_wire_position() 

# get table in `ak.Array`
wire_position_ak = geom.get_mdc_wire_position(library="ak")

# get table in `pd.DataFrame`
wire_position_pd = geom.get_mdc_wire_position(library="pd")
```

## EMC

### GID conversion

```python
import numpy as np
from pybes3.detectors import geometry as geom

# generate random crystal gid
gid = np.random.randint(0, 6240, 100)

# get part, theta, phi
part = geom.emc_gid_to_part(gid)
theta = geom.emc_gid_to_theta(gid)
phi = geom.emc_gid_to_phi(gid)

# get gid
gid = geom.get_emc_gid(part, theta, phi)
```

### Crystals position

To get front center, center x, y, z of crystals:

```python
# get front center x, y, z
front_center_x = geom.emc_gid_to_front_center_x(gid)
front_center_y = geom.emc_gid_to_front_center_y(gid)
front_center_z = geom.emc_gid_to_front_center_z(gid)

# get center x, y, z
center_x = geom.emc_gid_to_center_x(gid)
center_y = geom.emc_gid_to_center_y(gid)
center_z = geom.emc_gid_to_center_z(gid)
```

---

There are total 8 points on a crystal, you can get x, y, z of these points:

```python
# get x, y, z of point-0 of crystals
x0 = geom.emc_gid_to_point_x(gid, 0)
y0 = geom.emc_gid_to_point_y(gid, 0)
z0 = geom.emc_gid_to_point_z(gid, 0)

# get x, y, z of point-7 of crystals
x7 = geom.emc_gid_to_point_x(gid, 7)
y7 = geom.emc_gid_to_point_y(gid, 7)
z7 = geom.emc_gid_to_point_z(gid, 7)

# get x, y, z of all 8 points of crystal 0
point_id = np.arange(8)
x = geom.emc_gid_to_point_x(0, point_id)
y = geom.emc_gid_to_point_y(0, point_id)
z = geom.emc_gid_to_point_z(0, point_id)
```

---

You can get the whole crystals position table of EMC:

```python
# get table in `dict[str, np.ndarray]`
crystal_position_np = geom.get_emc_crystal_position()

# get table in `ak.Array`
crystal_position_ak = geom.get_emc_crystal_position(library="ak")

# get table in `pd.DataFrame`
crystal_position_pd = geom.get_emc_crystal_position(library="pd")
```
