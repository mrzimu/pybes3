# BES3 Data Reading

## Read ROOT files (rtraw, dst, rec)

To enable `uproot` to read BES3 ROOT files, import `pybes3` before opening any file:

```python
>>> import pybes3
>>> import uproot
```

Then, open file using `uproot`:

```python
>>> f = uproot.open("test.rtraw")
>>> evt = f["Event"]
```

Print information about this event tree:

```python
>>> evt.show(name_width=30)
name                           | typename                 | interpretation
-------------------------------+--------------------------+-------------------------------
TEvtHeader                     | TEvtHeader               | AsGroup(<TBranchElement 'TE...
TEvtHeader/TObject             | unknown                  | <UnknownInterpretation 'non...
TEvtHeader/m_eventId           | int32_t                  | AsDtype('>i4')
TEvtHeader/m_runId             | int32_t                  | AsDtype('>i4')
...
TMcEvent                       | TMcEvent                 | AsGroup(<TBranchElement 'TM...
TMcEvent/TObject               | unknown                  | <UnknownInterpretation 'non...
TMcEvent/m_mdcMcHitCol         | TMdcMc                   | AsBes3(TObjArray[TMdcMc])
TMcEvent/m_emcMcHitCol         | TEmcMc                   | AsBes3(TObjArray[TEmcMc])
TMcEvent/m_tofMcHitCol         | TTofMc                   | AsBes3(TObjArray[TTofMc])
TMcEvent/m_mucMcHitCol         | TMucMc                   | AsBes3(TObjArray[TMucMc])
TMcEvent/m_mcParticleCol       | TMcParticle              | AsBes3(TObjArray[TMcParticle])
TDigiEvent                     | TDigiEvent               | AsGroup(<TBranchElement 'TD...
TDigiEvent/TObject             | unknown                  | <UnknownInterpretation 'non...
TDigiEvent/m_fromMc            | bool                     | AsDtype('bool')
TDigiEvent/m_mdcDigiCol        | TMdcDigi                 | AsBes3(TObjArray[TMdcDigi])
...
```

---

### Reading sub-trees

To read `TMcEvent` (note: use `arrays()` instead of `array()` here):

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

This indicates that event 0 contains 12 MC particles. Their PDGIDs are `23, 4, -3, ...` and initial energies are `3.1, 1.55, 1.55, ... (GeV)`.

### Reading specific branches

!!! tip
    It is recommended to read only the branches you need for better performance.

To read a specific branch (note: use `array()` instead of `arrays()` here):

```python
>>> pdgid_arr = evt["TMcEvent/m_mcParticleCol/m_particleID"].array()
>>> e_init_arr = evt["TMcEvent/m_mcParticleCol/m_eInitialMomentum"].array()
```

or retrieve branches from `mc_evt`:

```python
>>> pdgid_arr = mc_evt["m_mcParticleCol/m_particleID"].array()
>>> e_init_arr = mc_evt["m_mcParticleCol/m_eInitialMomentum"].array()
```

## Read raw data files

### Read a single file

To read a raw data file, use `pybes3.open_raw`:

```python
>>> import pybes3 as p3
>>> raw_file = p3.open_raw("/besfs8/offline/data/merge/raw/round19/250912/run_0087397_All_merge0_file001_SFO-1.raw")
>>> raw_file
<RawData filename='run_0087397_All_merge0_file001_SFO-1.raw' Entries=180322 Size='2368 MB'>
```

Get meta information:

```python
>>> raw_file.entries # Number of events
180322
>>> raw_file.run_number
87397
>>> raw_file.path
'/besfs8/offline/data/merge/raw/round19/250912/run_0087397_All_merge0_file001_SFO-1.raw'
>>> raw_file.size
2483177188 # Size in bytes
```

To read all data:

```python
>>> raw_data = raw_file.arrays()
>>> raw_data
<Array [{evt_header: {...}, ...}, ..., {...}] type='180322 * {evt_header: {...'>
>>> raw_data.fields
['evt_header', 'cgem', 'mdc', 'tof', 'emc', 'muc', 'trigGTD']
>>> raw_data.cgem.fields
['id', 'adc', 'tdc', 'time', 'charge']
```

To read a portion of the file:

```python
>>> some_digi = raw_file.arrays(entry_start=50, entry_stop=100)
>>> some_digi
<Array [{evt_header: {...}, ...}, ..., {...}] type='50 * {evt_header: {evt_...'>
```

!!! warning
    Explicitly specifying `entry_start` and `entry_stop` will slow down the reading speed ($\sim 0.33 \times$), as the reader needs to skip entries one by one until it reaches `entry_stop`.

To read only specific fields:

```python
>>> cgem_mdc_digi = raw_file.arrays(filter_name=['cgem', 'mdc'])
>>> cgem_mdc_digi.fields
['evt_header', 'cgem', 'mdc']
```

!!! info
    Available fields are: `cgem`, `mdc`, `tof`, `emc`, `muc`, `trigGTD`.

    `evt_header` is always read and cannot be filtered out.

### Concatenate multiple files

To read multiple files and concatenate them into a single array, use `pybes3.concatenate_raw`:

```python
>>> files = [
        "/besfs8/offline/data/merge/raw/round19/250912/run_0087397_All_merge0_file001_SFO-1.raw",
        "/besfs8/offline/data/merge/raw/round19/250912/run_0087397_All_merge0_file002_SFO-1.raw",
>>> ]
>>> raw_data = p3.concatenate_raw(files)
>>> raw_data
<Array [{evt_header: {...}, ...}, ..., {...}] type='363492 * {evt_header: {...'>
```

Set `verbose=True` to print progress:

```python
>>> raw_data = p3.concatenate_raw(files, verbose=True)
Reading file /mnt/f/pybes3/run_0087397_All_merge0_file001_SFO-1.raw: 0 -> 180322 entries ...
Reading file /mnt/f/pybes3/run_0087397_All_merge0_file001_SFO-1.raw: 180322 -> 363492 entries ...
```

`entry_start`, `entry_stop` and `filter_name` can also be used in `concatenate_raw` to read only a portion of the files or specific fields:

```python
>>> raw_data = p3.concatenate_raw(files, entry_start=100, entry_stop=200, filter_name=['cgem', 'mdc'])
>>> raw_data
<Array [{evt_header: {...}, ...}, ..., {...}] type='100 * {evt_header: {evt...'>
```
