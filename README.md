# pybes

This project aims to make BES3 user easier to work with Python.

**This is an unofficial project.**

## besio

`besio` is an I/O module for BES3. It wraps `uproot` so that user can directly read BES3 `rtraw`, `dst` and  `rec` files, and transfer them to `awkward` array. See [uproot documentation](https://uproot.readthedocs.io/en/stable/) and [awkward documentation](https://awkward-array.org/doc/stable/index.html) for further details.

### Usage

To make `uproot` know about BES3 files,  call `pybes.wrap_uproot()` before opening any file:

```python
>>> import uproot
>>> import pybes
>>> pybes.wrap_uproot()
```

Then, open file as using `uproot`:

```python
>>> f = uproot.open("test.rtraw")
>>> evt = f["Event"]
```

There is a shorthand:

```python
>>> import pybes
>>> f = pybes.open("test.rtraw") # will automatically call `pybes.wrap_uproot()`
>>> evt = f["Event"]
```

Print information about this "event" tree:

```python
>>> evt.show(name_width=40)
name                                     | typename                 | interpretation                
-----------------------------------------+--------------------------+-------------------------------
TEvtHeader                               | TEvtHeader               | AsGroup(<TBranchElement 'TE...
TEvtHeader/m_eventId                     | int32_t                  | AsDtype('>i4')
TEvtHeader/m_runId                       | int32_t                  | AsDtype('>i4')
...
TMcEvent                                 | TMcEvent                 | AsGroup(<TBranchElement 'TM...
TMcEvent/m_mdcMcHitCol                   | BES::TObjArray<TMdcMc>   | BES::As(BES::TObjArray<TMdc...
TMcEvent/m_emcMcHitCol                   | BES::TObjArray<TEmcMc>   | BES::As(BES::TObjArray<TEmc...
TMcEvent/m_tofMcHitCol                   | BES::TObjArray<TTofMc>   | BES::As(BES::TObjArray<TTof...
TMcEvent/m_mucMcHitCol                   | BES::TObjArray<TMucMc>   | BES::As(BES::TObjArray<TMuc...
TMcEvent/m_mcParticleCol                 | BES::TObjArray<TMcPar... | BES::As(BES::TObjArray<TMcP...
TDigiEvent                               | TDigiEvent               | AsGroup(<TBranchElement 'TD...
TDigiEvent/m_fromMc                      | bool                     | AsDtype('bool')
...
>>> 
```

---

To read `TMcEvent` (Note: use `arrays()` instead of `array()` here):

```python
>>> mc_evt = evt["TMcEvent"].arrays()
>>> mc_evt.fields
['m_mdcMcHitCol', 'm_emcMcHitCol', 'm_tofMcHitCol', 'm_mucMcHitCol', 'm_mcParticleCol']
```

Now go to event 0:

```python
>>> evt0 = mc_evt[0]
>>> evt0.m_mcParticleCol.m_particleID
<Array [23, 4, -4, 91, 443, 11, ..., 111, 211, -211, 22, 22] type='12 * int32'>

>>> mc_evt[0].m_mcParticleCol.m_eInitialMomentum
<Array [3.1, 1.55, 1.55, 3.1, ..., 1.23, 0.178, 1.28] type='12 * float64'>
```

This indicates that in event 0, there are 12 MC particles. Their pdgIDs are `23, 4, -3, ...` and initial energies are `3.1, 1.55, 1.55, ... (GeV)`.

---

**Is is recommended that only read the branches you need, otherwise your memory may overflow.** 

To read a specific branch (Note: use `array()` instead of `arrays()` here):

```python
>>> pdgid_arr = evt["TMcEvent/m_mcParticleCol/m_particleID"].array()
>>> e_init_arr = evt["TMcEvent/m_mcParticleCol/m_eInitialMomentum"].array()
```

or you can retrieve branches from `mc_evt`:

```python
>>> pdgid_arr = mc_evt["m_mcParticleCol/m_particleID"].array()
>>> e_init_arr = mc_evt["m_mcParticleCol/m_eInitialMomentum"].array()
```

