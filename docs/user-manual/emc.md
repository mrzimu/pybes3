# EMC

## GID conversion

All `emc_gid_to_*` and `get_emc_gid` are backed by compiled NumPy ufuncs.
The calling convention is identical for scalar, NumPy array, and Awkward Array inputs:

::::{tab-set}

:::{tab-item} Scalar
:sync: scalar

```python
import pybes3 as p3

gid = 0
part = p3.emc_gid_to_part(gid)          # 0
theta = p3.emc_gid_to_theta(gid)
phi = p3.emc_gid_to_phi(gid)

gid = p3.get_emc_gid(part, theta, phi)
```
:::

:::{tab-item} NumPy array
:sync: numpy

```python
import numpy as np
import pybes3 as p3

gid = np.array([0, 100, 5000])
part = p3.emc_gid_to_part(gid)          # array([0, 0, 1])
theta = p3.emc_gid_to_theta(gid)
phi = p3.emc_gid_to_phi(gid)

gid = p3.get_emc_gid(part, theta, phi)
```
:::

:::{tab-item} Awkward Array
:sync: awkward

```python
import awkward as ak
import pybes3 as p3

gid = ak.Array([[0, 100], [5000]])
part = p3.emc_gid_to_part(gid)          # <Array [[0, 0], [1]] type='...'>
theta = p3.emc_gid_to_theta(gid)
phi = p3.emc_gid_to_phi(gid)

gid = p3.get_emc_gid(part, theta, phi)
```
:::

::::

Use `parse_emc_gid` to parse all fields from a gid at once:

```python
# parse all fields; returns a dict (or ak.Array when the input is an ak.Array)
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

:::{note}
The 8 corner points of crystals are **not** returned by `parse_emc_gid`.
Use `emc_gid_to_point_x`, `emc_gid_to_point_y`, and `emc_gid_to_point_z` to get them individually.
:::

When the input is an `ak.Array`, the result is also an `ak.Array` with record fields.

## Crystal position

All `emc_gid_to_front_center_*`, `emc_gid_to_center_*`, `emc_gid_to_point_*` are also backed by compiled NumPy ufuncs.

::::{tab-set}

:::{tab-item} Scalar
:sync: scalar

```python
import pybes3 as p3

gid = 0
front_center_x = p3.emc_gid_to_front_center_x(gid)
front_center_y = p3.emc_gid_to_front_center_y(gid)
front_center_z = p3.emc_gid_to_front_center_z(gid)

center_x = p3.emc_gid_to_center_x(gid)
center_y = p3.emc_gid_to_center_y(gid)
center_z = p3.emc_gid_to_center_z(gid)
```
:::

:::{tab-item} NumPy array
:sync: numpy

```python
import numpy as np
import pybes3 as p3

gid = np.array([0, 100, 5000])
front_center_x = p3.emc_gid_to_front_center_x(gid)
front_center_y = p3.emc_gid_to_front_center_y(gid)
front_center_z = p3.emc_gid_to_front_center_z(gid)

center_x = p3.emc_gid_to_center_x(gid)
center_y = p3.emc_gid_to_center_y(gid)
center_z = p3.emc_gid_to_center_z(gid)
```
:::

:::{tab-item} Awkward Array
:sync: awkward

```python
import awkward as ak
import pybes3 as p3

gid = ak.Array([[0, 100], [5000]])
front_center_x = p3.emc_gid_to_front_center_x(gid)
front_center_y = p3.emc_gid_to_front_center_y(gid)
front_center_z = p3.emc_gid_to_front_center_z(gid)

center_x = p3.emc_gid_to_center_x(gid)
center_y = p3.emc_gid_to_center_y(gid)
center_z = p3.emc_gid_to_center_z(gid)
```
:::

::::

---

Each crystal has 8 corner points. `emc_gid_to_point_*` take two arguments (`gid` and `point`),
both support scalar/array inputs independently:

::::{tab-set}

:::{tab-item} Scalar
:sync: scalar

```python
import pybes3 as p3

gid = 0
x = p3.emc_gid_to_point_x(gid, 0)   # crystal 0, point 0
y = p3.emc_gid_to_point_y(gid, 0)
z = p3.emc_gid_to_point_z(gid, 0)

x = p3.emc_gid_to_point_x(gid, 7)   # crystal 0, point 7
y = p3.emc_gid_to_point_y(gid, 7)
z = p3.emc_gid_to_point_z(gid, 7)
```
:::

:::{tab-item} NumPy array
:sync: numpy

```python
import numpy as np
import pybes3 as p3

gid = np.array([0, 100, 5000])

x = p3.emc_gid_to_point_x(gid, 0)       # multiple crystals, point 0
y = p3.emc_gid_to_point_y(gid, 0)
z = p3.emc_gid_to_point_z(gid, 0)

point_id = np.arange(8)
x = p3.emc_gid_to_point_x(0, point_id)  # crystal 0, all 8 points
y = p3.emc_gid_to_point_y(0, point_id)
z = p3.emc_gid_to_point_z(0, point_id)
```
:::

:::{tab-item} Awkward Array
:sync: awkward

```python
import awkward as ak
import pybes3 as p3

gid = ak.Array([[0, 100], [5000]])
point = ak.Array([0, 1, 2])

x = p3.emc_gid_to_point_x(gid, 0)       # jagged crystals, point 0
x = p3.emc_gid_to_point_x(0, point)     # crystal 0, jagged points
```
:::

::::

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

## Raw data conversion

The ADC measure/channel and the TDC channel numbers of a hit can be converted into charge (raw energy) and time with `emc_adc_to_charge` and `emc_tdc_to_time`:

```python
import numpy as np
import pybes3 as p3

measure = np.array([0, 1, 2, 3])
adc = np.array([100, 200, 300, 400])
charge = p3.emc_adc_to_charge(measure, adc)

tdc = np.array([10, 20, 30, 40])
time = p3.emc_tdc_to_time(tdc)
```

The conversion formula of the charge is:

$$
\text{charge} = \frac{\text{adc}}{1024} \times E_{\text{measure}}
$$

where $adc$ is the charge channel number, $E_{\text{measure}}$ is the maximum energy of the corresponding measure:

$$
E_{\text{measure}} =
    \begin{cases}
        0.078~\mathrm{GeV}, & \text{measure} = 0 \\
        0.625~\mathrm{GeV}, & \text{measure} = 1 \\
        2.5~\mathrm{GeV}, & \text{measure} = 2 \\
        2.5~\mathrm{GeV}, & \text{measure} = 3 \\
    \end{cases}
$$

Note that `measure=3` indicates that the hit is saturated, and the charge is calculated with the same formula as `measure=2`.

:::{admonition} Same as BOSS
:class: hint

EMC charge calculation is the same as the one given by `RawDataUtil::EmcCharge` in `BOSS`, except that the charge is in GeV in `pybes3`, while it is in MeV in `BOSS`.
:::

The conversion formula of the time is:

$$
\text{time} = \text{tdc} \times 50~\mathrm{ns}
$$

:::{admonition} Different from BOSS
:class: warning

EMC time calculation is different from the one given by `RawDataUtil` in `BOSS`. In `RawDataUtil` it simply multiplies the time channel number by 1 without any unit conversion, while in `pybes3` it multiplies by 50 ns.
:::
