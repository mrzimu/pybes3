# pybes3

## Overview

`pybes3` is an **unofficial** python module that aims to make BES3 user easier to work with Python.


It is recommended to take a look at [awkward](https://awkward-array.org/doc/stable/index.html) and [uproot](https://uproot.readthedocs.io/en/stable/) documentations before using `pybes3`. See [Further information](#further-information) for more details.

---

## Installation

### on lxlogin

Since there is a quota limitation on user's home path (`~/`), you may also need to create a symbolink for `~/.local`, which will contain pip packages that installed in "user mode":

```bash
# Check whether a `.local` directory and `.cache` already exists.
# If so, move it to somewhere else.
ls -a ~
mv ~/.local /path/to/somewhere/
mv ~/.cache /path/to/somewhere

# If no `.local` or `.cache` exists, create them
mkdir /path/to/somewhere/.local
mkdir /path/to/somewhere/.cache

# After moving or creating them, link them back to `~`
ln -s /path/to/somewhere/.local ~/.local
ln -s /path/to/somewhere/.cache ~/.cache
```

Then install `pybes3` in user mode:

```bash
pip install --user pybes3
```

> If you are using different python version, you need to install `pybes3` for each of major version.

### on PC

For PC users, it is sufficient to directly execute:

```bash
pip install pybes3
```


## BESIII data files reading

### read ROOT file (rtraw, dst, rec)

To make `uproot` know about BES3 ROOT files,  call `pybes3.wrap_uproot()` before opening any file:

```python
>>> import uproot
>>> import pybes3
>>> pybes3.wrap_uproot()
```

Then, open file as using `uproot`:

```python
>>> f = uproot.open("test.rtraw")
>>> evt = f["Event"]
```

There is a shorthand:

```python
>>> import pybes3
>>> f = pybes3.open("test.rtraw") # will automatically call `pybes3.wrap_uproot()`
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

This indicates that in event 0, there are 12 MC particles. Their PDGIDs are `23, 4, -3, ...` and initial energies are `3.1, 1.55, 1.55, ... (GeV)`.

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

### read raw data file

BES3 raw data files contain only digits information. To read a raw data file, use `pybes3.open_raw`:

```python
>>> import pybes3
>>> reader = pybes3.open_raw("/bes3fs/offline/data/raw/round17/231117/run_0079017_All_file001_SFO-1.raw")
>>> reader
BesRawReader
- File: /bes3fs/offline/data/raw/round17/231117/run_0079017_All_file001_SFO-1.raw
- Run Number: 79017
- Entries: 100112
- File Size: 2010 MB
```

To read all data out:

```python
>>> all_digi = reader.arrays()
>>> all_digi
<Array [{evt_header: {...}, ...}, ..., {...}] type='100112 * {evt_header: {...'>
>>> all_digi.fields
['evt_header', 'mdc', 'tof', 'emc', 'muc']
>>> all_digi.mdc.fields
['id', 'adc', 'tdc', 'overflow']
```

To only read some sub-detectors:

```python
>>> mdc_tof_digi = reader.arrays(sub_detectors=['mdc', 'tof']) # 'emc', 'muc' are also available
>>> mdc_tof_digi.fields
['evt_header', 'mdc', 'tof']
```

To read part of file:

```python
>>> some_digi = reader.arrays(n_blocks=1000)
>>> some_digi
<Array [{evt_header: {...}, ...}, ..., {...}] type='1000 * {evt_header: {ev...'>
```

> `n_blocks` instead of `n_entries` is used here because only data blocks are continuous in memory. Most of the time, there is one event in a data block.


## Further information

* `awkward` is a Python module that can handle ragged-like array. See [awkward-doc](https://awkward-array.org/doc/stable/index.html) to learn how to work with ragged-like array.
* `uproot` is a ROOT I/O Python module. If you want to write something into ROOT file (not as BES3 format!), see [uproot-doc](https://uproot.readthedocs.io/en/stable/) for help.
