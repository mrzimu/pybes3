# Tracks

## Helix

In BESIII, helix is represented by 5 parameters: `dr`, `phi0`, `kappa`, `dz`, `tanl`. To transform these parameters to `x`, `y`, `z`, `px`, `py`, `pz`, etc., use `pybes3.parse_helix`:

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
    - $x = dr \times \cos \varphi_0$
    - $y = dr \times \sin \varphi_0$
    - $z = dz$
    - $r = \left| dr \right|$

- momentum:
    - $p_t = \frac{1}{\left| \kappa \right|}$
    - $p_x = p_t \times \sin(- \varphi_0)$
    - $p_y = p_t \times \cos(- \varphi_0)$
    - $p_z = p_t \times \tan\lambda$
    - $p = p_t \times \sqrt{1 + \tan^2\lambda}$
    - $\theta = \arccos\left(\frac{p_z}{p}\right)$
    - $\varphi = -\varphi_0$

- others:
    - $\mathrm{charge} = \mathrm{sign}(\kappa)$
    - $r_{\mathrm{trk}} =\left| \frac{p_t}{qB} \right| = \left| \frac{p_t~[\mathrm{GeV}/c]}{1 e \times 1 \mathrm{T}} \right|$

Where `r_trk` is the radius of curvature of the track, and the magnetic field equals to `1T` in BESIII.
