# Monte Carlo

## Particle status

The status of an MC particle is the `m_statusFlags` branch of `TMcEvent/m_mcParticleCol` in
a DST:

```python
>>> import pybes3
>>> import uproot
>>> evt = uproot.open("test.dst")["Event"]
>>> status = evt["TMcEvent"].arrays()["m_mcParticleCol", "m_statusFlags"]
>>> status[0]
<Array [5, 9, 1, 1, 1, 13, 1, 1, 9, 9, 9, 9] type='12 * uint32'>
```

It is a bit field defined by BOSS as `Event::McParticle::StatusBits`: bit 0 `DECAYED` (the
particle comes from the generator), bit 1 `DECAYFLT` (produced in flight by Geant4), bit 2
`PRIMARY` and bit 3 `LEAF` (no daughter). Several bits can be set at the same time, e.g. `5`
is `PRIMARY | DECAYED`.

`particle_is_primary`, `particle_is_leaf`, `particle_decay_from_generator` and
`particle_decay_in_flight` decode them one by one. The calling convention is identical for
scalar, NumPy array, and Awkward Array inputs:

::::{tab-set}

:::{tab-item} Scalar
:sync: scalar

```python
import pybes3 as p3

status = 5  # PRIMARY | DECAYED
is_primary = p3.particle_is_primary(status)                      # True
is_leaf = p3.particle_is_leaf(status)                            # False
decay_from_generator = p3.particle_decay_from_generator(status)  # True
decay_in_flight = p3.particle_decay_in_flight(status)            # False
```
:::

:::{tab-item} NumPy array
:sync: numpy

```python
import numpy as np
import pybes3 as p3

status = np.array([1, 4, 8], dtype=np.uint32)
is_primary = p3.particle_is_primary(status)                      # array([False,  True, False])
is_leaf = p3.particle_is_leaf(status)                            # array([False, False,  True])
decay_from_generator = p3.particle_decay_from_generator(status)  # array([ True, False, False])
decay_in_flight = p3.particle_decay_in_flight(status)            # array([False, False, False])
```
:::

:::{tab-item} Awkward Array
:sync: awkward

```python
import awkward as ak
import pybes3 as p3

status = ak.Array([[5, 9], [1]])
is_primary = p3.particle_is_primary(status)                      # <Array [[True, False], [False]] ...>
is_leaf = p3.particle_is_leaf(status)                            # <Array [[False, True], [False]] ...>
decay_from_generator = p3.particle_decay_from_generator(status)  # <Array [[True, True], [True]] ...>
decay_in_flight = p3.particle_decay_in_flight(status)            # <Array [[False, False], [False]] ...>
```
:::

::::

`parse_particle_status` (in `pybes3.mc`, not re-exported at the top level) decodes all flags
at once. It returns a `dict` for scalar and NumPy input, and an `ak.Array` with the fields
`is_primary`, `is_leaf`, `decay_from_generator` and `decay_in_flight` for Awkward input:

```python
import pybes3.mc as mc

flags = mc.parse_particle_status(status)
flags["is_primary"]
flags["is_leaf"]
flags["decay_from_generator"]
flags["decay_in_flight"]
```
