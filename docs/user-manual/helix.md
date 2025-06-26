# Helix operations

In BES3, helix is represented by 5 parameters: `dr`, `phi0`, `kappa`, `dz`, `tanl`. `pybes3` provides a convenient way to parse these parameters, and do pivot transformation with parameters and error matrix.

The implementation of helix depends on [`vector`](https://vector.readthedocs.io/en/latest/). It is recommended to take a look at [Vector objects](https://vector.readthedocs.io/en/latest/src/object.html) and [Awkward Arrays of vectors](https://vector.readthedocs.io/en/latest/src/awkward.html) before using helix objects, as they are used to represent helix position, momentum and pivot point.

## Transformation rules

The implementation follows formulas below:

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

The magnetic field in BES3 is assumed to be `1T`.

## Create helix

### Create helix object

If you are working with a single track, you can use `pybes3.helix_obj` to create a helix object:

```python
import pybes3 as p3

helix = p3.helix_obj(
    params=(dr, phi0, kappa, dz, tanl), # helix parameters
    error=error,                        # error matrix (optional
    pivot=(x0, y0, z0),                 # initial pivot point (optional)
)
```

When `error` is not provided, it defaults to `None`. When `pivot` is not provided, it defaults to `(0, 0, 0)`.


!!! note "Overload of `helix_obj`"

    When calling `helix_obj`, you can pass the helix parameters and initial pivot point in different ways:

    === "Helix parameters"

        You can specify the helix parameters in two ways:

        === "Directly specify each parameter"

            ```python
            p3.helix_obj(dr, phi0, kappa, dz, tanl, ...)
            # or
            p3.helix_obj(dr=dr, phi0=phi0, kappa=kappa, dz=dz, tanl=tanl, ...)
            ```

        === "As a tuple"

            ```python
            p3.helix_obj(params=(dr, phi0, kappa, dz, tanl), ...)
            ```

    === "Pivot point"

        You can specify the initial pivot point in different ways:

        === "As a tuple"
        
            ```python
            p3.helix_obj(..., pivot=(x0, y0, z0))
            ```

        === "As a Vector3D object"

            ```python
            pivot = p3.vector.obj(x=x0, y=y0, z=z0)
            p3.helix_obj(..., pivot=pivot)
            ```

### Create helix array

!!! warning
    You must import `pybes3` before creating a helix array, even though the creation may not involve any `pybes3` functions.

The helix array is implemented with awkward ["behavior" machanism](https://awkward-array.org/doc/main/reference/ak.behavior.html). One can create a helix array via `pybes3.helix_awk`, or directly create an awkward array with the `Bes3Helix` behavior.

A very common case is to read helix parameters from a BES3 file, and create a helix array:

```python
import pybes3 as p3

# Open a BES3 file and read the helix parameters
dst_evt = p3.open("test.dst")["Event/TDstEvent"]
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

If you want to specify the helix parameters directly, just pass them as keyword arguments:

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

    === "As a tuple or `Vector3D` object"

        This will set all tracks to have such pivot point:

        ```python
        # As a tuple
        helix = p3.helix_awk(..., pivot=(x0, y0, z0))

        # As a Vector3D object
        pivot = p3.vector.obj(x=x0, y=y0, z=z0)
        helix = p3.helix_awk(..., pivot=pivot)
        ```
    
    === "As an awkward array"

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

Sometimes you may need to create a helix from position, momentum and charge. You can pass these parameters to `pybes3.helix_obj` or `pybes3.helix_awk` to create a helix object or array. `pybes3` will automatically calculate the helix parameters for you.

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

!!! tip "Create helix from MC truth"

    If you are creating helix from MC truth, you should let `pivot` be the same as the MC truth position, then change the pivot point to `(0, 0, 0)` later with `change_pivot` method:

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

    Then you can retrieve helix parameters of truth via `dr`, `phi0`, `kappa`, `dz`, `tanl` properties of the helix.

## Physics information

Once you have an object or an awkward array of helix, you can retrieve the physical parameters such as position, momentum, charge and circular radius of the track.

### Position

The position is defined as the closest point to the pivot point on the helix. You can retrieve the position with:

```python
position = helix.position
```

This will return a `Vector3D` object with the position of the track. You can access the `x`, `y`, and `z` coordinates with:

```python
x = position.x
y = position.y
z = position.z
```

!!! tip "See Also"
    See [Interface for 3D vectors](https://vector.readthedocs.io/en/latest/src/vector3d.html) for more properties.

### Momentum

The momentum is defined as the momentum at the closest point to the pivot point on the helix. You can retrieve the momentum with:

```python
momentum = helix.momentum
```

This will return a `Momentum3D` object with the momentum of the track. You can access the many components of the momentum with:

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

!!! warning "Momentum changes with pivot point"
    When changing pivot point, the momentum will also change. This is because the momentum is defined at the closest point to the pivot point on the helix.

### Pivot point

You can retrieve the pivot point of the helix with:

```python
pivot = helix.pivot
```

Similar to the position, this will return a `Vector3D` object with the pivot point of the track.

### Charge

The charge of the track can be retrieved with:

```python
charge = helix.charge
```

This will return `1` or `-1`, or an awkward array of these values if the helix is an awkward array.

### Circular radius

The circular radius is defined as the radius of the 2D circle in the XY plane that the track follows. You can retrieve the circular radius with:

```python
r = helix.radius
```

This will return a scalar value or an awkward array of values, depending on whether the helix is an object or an awkward array.

## Pivot transformation

To change pivot point of helix, use `change_pivot` method. This will transform the helix parameters and error matrix to the new pivot point:

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
    `change_pivot` will not modify the original helix object or array, but return a new one with the pivot point changed.

## Helix comparison

You can compare two helix objects or awkward arrays of helix using `isclose` method. If two helix objects have different pivot points, the second helix will be transformed to the first helix's pivot point before comparison.

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

The comparison uses `numpy.isclose` to check if the helix parameters and error matrix are close enough. You can specify the `rtol`, `atol` and `equal_nan` parameters to control the comparison behavior:

```python
is_close = helix1.isclose(helix2, rtol=1e-5, atol=1e-8, equal_nan=False)
```

See [numpy.isclose](https://numpy.org/doc/stable/reference/generated/numpy.isclose.html) for more details on these parameters.
