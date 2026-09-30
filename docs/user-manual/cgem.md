# CGEM

## GID conversion

All `cgem_gid_to_*` and `get_cgem_gid` are backed by compiled NumPy ufuncs.
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

Use `parse_cgem_gid` to parse all fields from a gid at once:

```python
# parse all fields; returns a dict (or ak.Array when the input is an ak.Array)
res = p3.parse_cgem_gid(gid)
layer = res["layer"]
sheet = res["sheet"]
strip_type = res["strip_type"]
strip = res["strip"]
is_xstrip = res["is_xstrip"]
is_vstrip = res["is_vstrip"]
```

When the input is an `ak.Array`, the result is also an `ak.Array` with record fields.

## Strip geometry

All `cgem_gid_to_width`, `cgem_gid_to_radius`, `cgem_gid_to_phi0`, `cgem_gid_to_dphi`,
`cgem_gid_to_z0` and `cgem_gid_to_dz` are also backed by compiled NumPy ufuncs.
The calling convention is identical for scalar, NumPy array, and Awkward Array inputs:

=== "Scalar"

    ```python
    import pybes3 as p3

    gid = 0
    width = p3.cgem_gid_to_width(gid)
    radius = p3.cgem_gid_to_radius(gid)

    phi0 = p3.cgem_gid_to_phi0(gid)
    dphi = p3.cgem_gid_to_dphi(gid)
    z0 = p3.cgem_gid_to_z0(gid)
    dz = p3.cgem_gid_to_dz(gid)
    ```

=== "NumPy array"

    ```python
    import numpy as np
    import pybes3 as p3

    gid = np.array([0, 856, 5000])
    width = p3.cgem_gid_to_width(gid)
    radius = p3.cgem_gid_to_radius(gid)

    phi0 = p3.cgem_gid_to_phi0(gid)
    dphi = p3.cgem_gid_to_dphi(gid)
    z0 = p3.cgem_gid_to_z0(gid)
    dz = p3.cgem_gid_to_dz(gid)
    ```

=== "Awkward Array"

    ```python
    import awkward as ak
    import pybes3 as p3

    gid = ak.Array([[0, 856], [5000]])
    width = p3.cgem_gid_to_width(gid)
    radius = p3.cgem_gid_to_radius(gid)

    phi0 = p3.cgem_gid_to_phi0(gid)
    dphi = p3.cgem_gid_to_dphi(gid)
    z0 = p3.cgem_gid_to_z0(gid)
    dz = p3.cgem_gid_to_dz(gid)
    ```

The centre line of a strip is described in the global cylindrical coordinate system.
`radius` is the distance (cm) of the strip from the beam axis, and `width` is the width (cm)
of the strip, which is measured along the arc direction for an x-strip and perpendicular to
the strip for a v-strip.

The other four values parametrise the centre line from its start point ($t = 0$), which is the
end with the most negative z, to its other end ($t = 1$):

$$\phi(t) = \phi_0 + t \cdot \Delta\phi, \qquad z(t) = z_0 + t \cdot \Delta z, \qquad 0 \le t \le 1$$

- `phi0`, `z0`: azimuth (rad) and z (cm) of the start point;
- `dphi`, `dz`: changes of the azimuth (rad) and of the z (cm) along the strip, from the start
  point to the other end; their signs give the direction of the strip (`dz` is always positive,
  because the start point is the negative z end).

`dphi` is 0 for x-strips, which run along the beam axis, and non-zero for v-strips, which are
tilted by the stereo angle.

!!! info
    `radius` and `width` only depend on the strip type and the layer, so they take a few distinct
    values, whereas `phi0`, `dphi`, `z0` and `dz` vary from strip to strip.

---

The position along a strip can be converted between the azimuth and the z coordinate with
`cgem_gid_phi_to_z` and `cgem_gid_z_to_phi`. They take two arguments (`gid` and `phi` or `z`),
both supporting scalar/array inputs independently:

=== "Scalar"

    ```python
    import pybes3 as p3

    gid = 1297

    z = p3.cgem_gid_phi_to_z(gid, 0.0)      # z (cm) of the strip at phi = 0
    phi = p3.cgem_gid_z_to_phi(gid, 0.0)    # phi (rad) of the strip at z = 0 cm
    ```

=== "NumPy array"

    ```python
    import numpy as np
    import pybes3 as p3

    gid = np.array([1297, 1300, 1301])
    phi = np.array([-3.0, 0.0, 1.0])

    z = p3.cgem_gid_phi_to_z(1297, phi)     # strip 1297 at multiple phi
    z = p3.cgem_gid_phi_to_z(gid, 0.0)      # multiple strips at phi = 0

    phi = p3.cgem_gid_z_to_phi(1297, np.array([-10.0, 0.0, 10.0]))
    phi = p3.cgem_gid_z_to_phi(gid, 0.0)    # multiple strips at z = 0 cm
    ```

=== "Awkward Array"

    ```python
    import awkward as ak
    import pybes3 as p3

    gid = ak.Array([[1297, 1300], [1301]])
    phi = ak.Array([[-3.0, 0.0], [1.0]])

    z = p3.cgem_gid_phi_to_z(1297, phi)     # strip 1297 at jagged phi
    z = p3.cgem_gid_phi_to_z(gid, 0.0)      # jagged strips at phi = 0
    ```

Both functions are backed by compiled NumPy ufuncs and use linear interpolation between the
two ends of the strip, without any range check, so a `phi` or `z` outside the strip is
extrapolated.

!!! info
    An x-strip runs along the z axis, so `cgem_gid_z_to_phi` always returns its `phi0`, whereas
    `cgem_gid_phi_to_z` returns NaN, since its phi does not give any z.

---

Retrieve the full strip geometry table:

```python
# get table in `dict[str, np.ndarray]`
strip_geom_np = p3.get_cgem_geom_table()

# get table in `ak.Array`
strip_geom_ak = p3.get_cgem_geom_table(library="ak")

# get table in `pd.DataFrame`
strip_geom_pd = p3.get_cgem_geom_table(library="pd")
```

The table holds `gid`, `layer`, `sheet`, `strip_type`, `strip`, `r`, `width`, `phi0`, `dphi`,
`z0` and `dz`. Here `r` and `width` are the same values as the ones returned by
`cgem_gid_to_radius` and `cgem_gid_to_width`.
