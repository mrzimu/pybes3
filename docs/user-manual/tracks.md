# Tracks

## Helix

In BESIII, helix is represented by 5 parameters: `dr`, `phi0`, `kappa`, `dz`, `tanl`. `pybes3` provides a convenient way to parse these parameters, and do pivot transformation.

### Python object

If you are working with a single track, you can use `pybes3.helix_obj` to create a helix object:

```python
import pybes3 as p3

helix = p3.helix_obj(params=(dr, phi0, kappa, dz, tanl))
```

you can parse a  a `numpy` array of shape `(5, 5)` as error matrix of the helix:

```python
helix = p3.helix_obj(params=(dr, phi0, kappa, dz, tanl), err_matrix=err_matrix)
```

you can specify the initial pivot point of the helix by passing `pivot` argument:

```python
helix = p3.helix_obj(params=(dr, phi0, kappa, dz, tanl), pivot=(x0, y0, z0))
```

A full list of parameter types is listed below:

??? note

    * Helix parameters:

        ```python
        # specify parameters as a tuple
        p3.helix_obj(params=(dr, phi0, kappa, dz, tanl), ...)
        ```

        ```python
        # directly specify each parameter
        p3.helix_obj(dr=dr, phi0=phi0, kappa=kappa, dz=dz, tanl=tanl, ...)
        ```

    * Error matrix: Can only be a `numpy` array of shape `(5, 5)`.

        ```python
        # error is a numpy array of shape (5, 5)
        p3.helix_obj(..., error=error)
        ```

    * Pivot point:
        
        ```python
        # pivot is a tuple of (x0, y0, z0)
        p3.helix_obj(..., pivot=(x0, y0, z0))
        ```

        ```python
        # pivot is a Vector3D object
        p3.helix_obj(..., pivot=vector.obj(x=x0, y=y0, z=z0))
        ```

### Awkward array

```python
>>> import pybes3 as p3
>>> mdc_trk = p3.open("test.dst")["Event/TDstEvent/m_mdcTrackCol"].array()
>>> helix = mdc_trk["m_helix"]
>>> helix
<Array [[[0.0342, 0.736, ..., 0.676], ...], ...] type='10 * var * 5 * float64'>

>>> phy_helix = p3.parse_helix(helix)
>>> phy_helix.fields
['x', 'y', 'z', 'r', 'px', 'py', 'pz', 'pt', 'p', 'theta', 'phi', 'charge', 'r_trk']
```

!!! tip
    You can use `parse_helix` to decode any helix array with 5 elements in the last dimension, such as
    `m_mdcKalTrackCol["m_zhelix"]`, `m_mdcKalTrackCol["m_zhelix_e"]`, etc.


The formulas to transform helix parameters to physical parameters are:

- position:
    - $x = x_0 + dr \times \cos \varphi_0$
    - $y = y_0 + dr \times \sin \varphi_0$
    - $z = z_0 + dz$
    - $r = \left| dr \right|$

- momentum:
    - $p_t = \frac{1}{\left| \kappa \right|}$
    - $\varphi = \varphi_0 + \frac{\pi}{2}$
    - $p_x = p_t \times \cos(\varphi)$
    - $p_y = p_t \times \sin(\varphi)$
    - $p_z = p_t \times \tan\lambda$
    - $p = p_t \times \sqrt{1 + \tan^2\lambda}$
    - $\theta = \arccos\left(\frac{p_z}{p}\right)$

- others:
    - $\mathrm{charge} = \mathrm{sign}(\kappa)$
    - $r_{\mathrm{trk}} =\left| \frac{p_t}{qB} \right| = \left| \frac{p_t~[\mathrm{GeV}/c]}{1 e \times 1 \mathrm{T}} \right|$

Where `r_trk` is the radius of curvature of the track, and the magnetic field equals to `1T` in BESIII.
