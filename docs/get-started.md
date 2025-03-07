## BESIII data files reading

### read ROOT file (rtraw, dst, rec)

To make `uproot` know about BES3 ROOT files,  call `pybes3.wrap_uproot()` before opening any file:

```python
>>> import uproot
>>> import pybes3 as p3
>>> p3.wrap_uproot()
```

Then, open file as using `uproot`:

```python
>>> f = uproot.open("test.rtraw")
>>> evt = f["Event"]
```

There is a shorthand:

```python
>>> import pybes3 as p3
>>> f = p3.open("test.rtraw") # will automatically call `pybes3.wrap_uproot()`
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

**It is recommended that only read the branches you need, otherwise your memory may overflow.** 

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
>>> import pybes3 as p3
>>> reader = p3.open_raw("/bes3fs/offline/data/raw/round17/231117/run_0079017_All_file001_SFO-1.raw")
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

!!! note
    `n_blocks` instead of `n_entries` is used here because only data blocks are continuous in memory. Most of the time, there is one event in a data block.

!!! warning
    By so far, `besio` can only read original raw data without any decoding. Read raw data with decoding is under development.



## Digi Identifier

When reading `TDigiEvent`, the `m_intId` field in `mdc`, `tof`, `emc`, `muc` branches are the electronics readout id (TEID), also known as `IntValue` of `Identifier` in `BOSS`. To decode the `m_intId`, use `parse_xxx_id` methods where `xxx` is the detector name (`cgem`, `mdc`, `tof`, `emc`, `muc`):

```python
>>> import pybes3 as p3
>>> digi_evt = p3.open("test.rtraw")["Event/TDigiEvent"].arrays()
>>> mdc_id = digi_evt.m_mdcDigiCol.m_intId
>>> mdc_id
<Array [[], [...], ..., [268439568, ..., 268457030]] type='200 * var * uint32'>

>>> parsed_mdc_id = p3.parse_mdc_id(mdc_id)
>>> parsed_mdc_id.fields
['wire', 'layer', 'is_stereo']
>>> parsed_mdc_id.typestr
'200 * var * {wire: uint16, layer: uint8, is_stereo: bool}'
```

`m_intId` can be calculated with `get_xxx_id` methods:

```python
>>> import awkward as ak
>>> wire = parsed_mdc_id["wire"]
>>> layer = parsed_mdc_id["layer"]
>>> is_stereo = parsed_mdc_id["is_stereo"]
>>> p3.get_mdc_id(wire, layer, is_stereo)
<Array [[], [...], ..., [268439568, ..., 268457030]] type='200 * var * uint32'>
>>> ak.all(mdc_id == p3.get_mdc_id(wire, layer, is_stereo))
np.True_
```

!!! note
    `pybes3` uses different convention for TOF `part` ID: `0~2` for scintillator endcap0/barrel/endcap1, `3~4` for MRPC endcap0/endcap1. In this case, TOF ID information can be decoded to 4 fields: `part`, `layerOrModule`, `phiOrStrip`, `end`.



## Tracks parsing

### Helix

In BESIII, helix is represented by 5 parameters: `dr`, `phi0`, `kappa`, `dz`, `tanl`. To transform these parameters to `x`, `y`, `z`, `px`, `py`, `pz`, etc., use `pybes3.parse_helix`:

```python
>>> import pybes3 as p3
>>> mdc_trk = p3.open("test.dst")["Event/TDstEvent/m_mdcTrackCol"].array()
>>> helix = mdc_trk["m_helix"]
>>> helix
<Array [[[0.0342, 0.736, ..., 0.676], ...], ...] type='10 * var * 5 * float64'>

>>> phy_helix = p3.parse_helix(helix)
>>> phy_helix.fields
['x', 'y', 'z', 'r', 'px', 'py', 'pz', 'pt', 'p', 'theta', 'phi', 'charge']
```

!!! note
    You can use `parse_helix` to decode any helix array with 5 elements in the last dimension, such as
    `m_mdcKalTrackCol["m_zhelix"]`, `m_mdcKalTrackCol["m_zhelix_e"]`, etc.
