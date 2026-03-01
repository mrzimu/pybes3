# Helix Operations

In BES3, a helix is represented by 5 parameters: `dr`, `phi0`, `kappa`, `dz`, `tanl`. `pybes3` provides a convenient way to parse these parameters and perform pivot transformations with parameters and error matrices.

The implementation depends on [`vector`](https://vector.readthedocs.io/en/latest/). It is recommended to review [Vector objects](https://vector.readthedocs.io/en/latest/src/object.html) and [Awkward Arrays of vectors](https://vector.readthedocs.io/en/latest/src/awkward.html) before using helix objects, as they are used to represent helix position, momentum, and pivot point.

## Transformation rules

The implementation follows these formulas:

- Position $[\mathrm{cm}]$:
    - $x = x_0 + dr \times \cos \varphi_0$
    - $y = y_0 + dr \times \sin \varphi_0$
    - $z = z_0 + dz$

- Momentum $[\mathrm{GeV}/c]$:
    - $p_t = \frac{1}{\left| \kappa \right|}$
    - $\varphi = \varphi_0 + \frac{\pi}{2}$
    - $p_x = p_t \times \cos(\varphi)$
    - $p_y = p_t \times \sin(\varphi)$
    - $p_z = p_t \times \tan\lambda$

- Others:
    - $\mathrm{charge} = \mathrm{sign}(\kappa)$
    - $r_{\mathrm{trk}} \ [\mathrm{cm}] = \frac{1000}{2.99792458} \times p_t \ [\mathrm{GeV}/c]$

The magnetic field in BES3 is assumed to be 1 T.

## Create helix

### From helix parameters (single track)

For a single track, use `pybes3.helix_obj`:

```python
import pybes3 as p3

helix = p3.helix_obj(
    params=(dr, phi0, kappa, dz, tanl), # helix parameters
    error=error,                        # error matrix (optional)
    pivot=(x0, y0, z0),                 # initial pivot point (optional)
)
```

When `error` is not provided, it defaults to `None`. When `pivot` is not provided, it defaults to `(0, 0, 0)`.


!!! note "Overload of `helix_obj`"

    When calling `helix_obj`, you can pass the helix parameters and initial pivot point in different ways:

    === "Helix parameters"

        You can specify the helix parameters in two ways:

        ```python
        p3.helix_obj(dr, phi0, kappa, dz, tanl, ...)
        # or
        p3.helix_obj(dr=dr, phi0=phi0, kappa=kappa, dz=dz, tanl=tanl, ...)
        # or
        p3.helix_obj(params=(dr, phi0, kappa, dz, tanl), ...)
        ```

    === "Pivot point"

        You can specify the initial pivot point in different ways:

        ```python
        # As a tuple
        p3.helix_obj(..., pivot=(x0, y0, z0))

        # As a Vector3D object
        pivot = p3.vector.obj(x=x0, y=y0, z=z0)
        p3.helix_obj(..., pivot=pivot)
        ```

### From helix parameters (array)

!!! warning
    You must import `pybes3` before creating a helix array, even if the creation does not directly use any `pybes3` functions.

The helix array is implemented with awkward's ["behavior" mechanism](https://awkward-array.org/doc/main/reference/ak.behavior.html). You can create a helix array via `pybes3.helix_awk`, or directly create an awkward array with the `Bes3Helix` behavior.

A common use case is reading helix parameters from a BES3 file:

```python
import pybes3 as p3
import uproot

# Open a BES3 file and read the helix parameters
dst_evt = uproot.open("test.dst")["Event/TDstEvent"]
mdc_trks = dst_evt["m_mdcTrackCol"].array()

# Extract the helix parameters and error matrix
raw_helix = mdc_trks["m_helix"]
raw_helix_err = mdc_trks["m_err"]

# Create a helix array
helix = p3.helix_awk(raw_helix, raw_helix_err)
```

!!! info

    This overload of `helix_awk` follows such convention:

    ```python
    dr = raw_helix[..., 0]
    phi0 = raw_helix[..., 1]
    kappa = raw_helix[..., 2]
    dz = raw_helix[..., 3]
    tanl = raw_helix[..., 4]
    ```

If you want to specify the helix parameters directly, pass them as keyword arguments:

```python
# Prepare helix parameters arrays
dr = ak.Array(...)
phi0 = ak.Array(...)
kappa = ak.Array(...)
dz = ak.Array(...)
tanl = ak.Array(...)

# Optional, if you have an error matrix
error = ak.Array(...)

# Create a helix array with the parameters
helix = p3.helix_awk(
    dr=dr,
    phi0=phi0,
    kappa=kappa,
    dz=dz,
    tanl=tanl,
    error=error, # Optional, if you have an error matrix
)
```

!!! note
    Since each track has a `5x5` error matrix, if a track array has shape `(n, var)`, the error matrix should have shape `(n, var, 5, 5)`.

You can also specify the initial pivot point:

```python
helix = p3.helix_awk(
    dr=dr,
    phi0=phi0,
    kappa=kappa,
    dz=dz,
    tanl=tanl,
    error=error,        # Optional, if you have an error matrix
    pivot=(x0, y0, z0)  # Initial pivot point
)
```

!!! note "Different types of pivot point"

    The `pivot` can be specified in different ways when using `helix_awk`:

    - As a tuple or `Vector3D` object

        If all tracks share the same pivot point, you can specify it as a tuple or a `Vector3D` object:

        ```python
        # As a tuple
        helix = p3.helix_awk(..., pivot=(x0, y0, z0))

        # As a Vector3D object
        pivot = p3.vector.obj(x=x0, y=y0, z=z0)
        helix = p3.helix_awk(..., pivot=pivot)
        ```

    - As an awkward array

        If you have different pivot points for each track, you can provide a `Vector3D` awkward array:

        ```python
        pivot = ak.Array({
            "x": ak.Array(...),
            "y": ak.Array(...),
            "z": ak.Array(...),
        }, with_name="Vector3D")

        helix = p3.helix_awk(..., pivot=pivot)
        ```

??? note "Directly create helix array"

    To create a helix array directly, first import necessary modules:

    ```python
    import pybes3
    import awkward as ak
    ```

    Prepare helix parameters:

    ```python
    dr = ak.Array(...)
    phi0 = ak.Array(...)
    kappa = ak.Array(...)
    dz = ak.Array(...)
    tanl = ak.Array(...)
    ```

    Prepare initial pivot point:

    ```python
    pivot = ak.Array({
        "x": ak.zeros_like(dr),
        "y": ak.zeros_like(dr),
        "z": ak.zeros_like(dr),
    }, with_name="Vector3D")
    ```

    Create helix array (with no error matrix)

    ```python
    helix = ak.Array({
        "dr": dr,
        "phi0": phi0,
        "kappa": kappa,
        "dz": dz,
        "tanl": tanl,
        "pivot": pivot,
    }, with_name="Bes3Helix")
    ```

    Optionally, you can also create an error matrix.

    ```python
    error = ak.Array(...)

    helix = ak.Array({
        "dr": dr,
        "phi0": phi0,
        "kappa": kappa,
        "dz": dz,
        "tanl": tanl,
        "error": error,
        "pivot": pivot,
    }, with_name="Bes3Helix")
    ```

### Create helix from physics parameters

You can also create a helix from position, momentum, and charge. Pass these parameters to `pybes3.helix_obj` or `pybes3.helix_awk`, and `pybes3` will automatically calculate the helix parameters.

=== "Object"

    To create a helix object, use:

    ```python
    p3.helix_obj(
        position=(x, y, z),     # position of the track
        momentum=(px, py, pz),  # momentum of the track
        charge=charge,          # charge of the track
        error=error,            # error matrix (optional)
        pivot=(x0, y0, z0)      # initial pivot point (optional)
    )
    ```

    where `charge` should be `1` or `-1`, and the `pivot` defaults to `(0, 0, 0)` if not provided.

=== "Array"

    To create a helix array, use:

    ```python
    position = ak.Array({
        "x": ak.Array(...),
        "y": ak.Array(...),
        "z": ak.Array(...),
    }, with_name="Vector3D")

    momentum = ak.Array({
        "px": ak.Array(...),
        "py": ak.Array(...),
        "pz": ak.Array(...),
    }, with_name="Vector3D")

    charge = ak.Array(...)  # values should be 1 or -1

    p3.helix_awk(
        position=position,
        momentum=momentum,
        charge=charge,
        error=error,    # error matrix (optional)
        pivot=pivot     # initial pivot point (optional)
    )
    ```

    where `charge` should be array of `1` or `-1`, and the `pivot` defaults to `(0, 0, 0)` if not provided.

### Create helix from MC truth

When creating a helix from MC truth, set `pivot` to the MC truth position, then change it to `(0, 0, 0)` using the `change_pivot` method:

```python
truth_helix = p3.helix_obj(
    position=(x, y, z),
    momentum=(px, py, pz),
    charge=charge,
    pivot=(x, y, z)  # use the MC truth position as pivot
).change_pivot(0, 0, 0)  # change pivot to (0, 0, 0)
```

or, for awkward array:

```python
truth_helix = p3.helix_awk(
    position=position,
    momentum=momentum,
    charge=charge,
    pivot=position  # use the MC truth position as pivot
).change_pivot(0, 0, 0)  # change pivot to (0, 0, 0)
```

Then you can retrieve the helix parameters via the `dr`, `phi0`, `kappa`, `dz`, `tanl` properties.

## Physics information

Once you have a helix object or awkward array, you can retrieve physical parameters such as position, momentum, charge, and circular radius.

### Position

The position is defined as the closest point on the helix to the pivot point:

```python
position = helix.position
```

This returns a `Vector3D` object. You can access individual coordinates with:

```python
x = position.x
y = position.y
z = position.z
```

!!! tip "See Also"
    See [Interface for 3D vectors](https://vector.readthedocs.io/en/latest/src/vector3d.html) for more properties.

### Momentum

The momentum is defined at the closest point on the helix to the pivot point:

```python
momentum = helix.momentum
```

This returns a `Momentum3D` object with many accessible components:

```python
px = momentum.px
py = momentum.py
pz = momentum.pz
pt = momentum.pt  # transverse momentum
p = momentum.p    # total momentum
costheta = momentum.costheta  # cosine of the polar angle
theta = momentum.theta  # polar angle
phi = momentum.phi  # azimuthal angle
```

!!! tip "See Also"
    See [Interface for 3D momentum](https://vector.readthedocs.io/en/latest/src/momentum3d.html) for more properties.

!!! warning "Momentum depends on the pivot point"
    When changing the pivot point, the momentum also changes, because it is evaluated at the closest point to the pivot.

### Pivot point

Retrieve the pivot point of the helix:

```python
pivot = helix.pivot
```

Similar to position, this returns a `Vector3D` object.

### Charge

Retrieve the charge of the track:

```python
charge = helix.charge
```

Returns `1` or `-1`, or an awkward array of these values for helix arrays.

### Circular radius

The circular radius is the radius of the 2D circle in the XY plane that the track follows:

```python
r = helix.radius
```

Returns a scalar value or an awkward array, depending on the helix type.

## Pivot transformation

Use `change_pivot` to transform the helix parameters and error matrix to a new pivot point:

=== "Object"

    ```python
    helix = p3.helix_obj(...)

    # Change pivot point to (3, 4, 5)
    helix = helix.change_pivot(3, 4, 5)
    ```

    or pass a `Vector3D` object:

    ```python
    pivot = p3.vector.obj(x=3, y=4, z=5)
    helix = helix.change_pivot(pivot)
    ```

=== "Array"

    You can change the pivot for each track in an awkward array of helix:

    ```python
    helix = p3.helix_awk(...)
    new_pivot = ak.Array({
        "x": ak.Array(...),
        "y": ak.Array(...),
        "z": ak.Array(...),
    }, with_name="Vector3D")

    helix = helix.change_pivot(new_pivot)
    ```

    or change the pivot point to a specific point for each track:

    ```python
    # Change pivot point to (3, 4, 5) for each track
    helix = helix.change_pivot(3, 4, 5)
    ```

!!! warning
    `change_pivot` returns a **new** helix object/array; it does not modify the original.

## Helix comparison

Compare two helix objects or arrays using the `isclose` method. If they have different pivot points, the second helix is automatically transformed to the first helix's pivot point before comparison.

=== "Object"

    ```python
    helix1 = p3.helix_obj(...)
    helix2 = p3.helix_obj(...)

    # Compare two helix objects, returns a boolean value
    is_close = helix1.isclose(helix2)
    ```

=== "Array"

    ```python
    helix1 = p3.helix_awk(...)
    helix2 = p3.helix_awk(...)

    # Compare two helix awkward arrays, returns an awkward array of boolean values
    is_close = helix1.isclose(helix2)
    ```

The comparison uses `numpy.isclose` to check whether the helix parameters and error matrix are close enough. You can customize the tolerance:

```python
is_close = helix1.isclose(helix2, rtol=1e-5, atol=1e-8, equal_nan=False)
```

See [numpy.isclose](https://numpy.org/doc/stable/reference/generated/numpy.isclose.html) for more details on these parameters.
