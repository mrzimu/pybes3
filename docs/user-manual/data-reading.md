# Data Reading

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

:::{tip}
It is recommended to read only the branches you need for better performance.
:::

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
>>> file_path = "run_0087397_All_merge0_file001_SFO-1.raw"
>>> raw_file = p3.open_raw(file_path)
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
'run_0087397_All_merge0_file001_SFO-1.raw'
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
['m_intId', 'm_chargeChannel', 'm_timeChannel', 'm_time_ns', 'm_charge_fc']
```

To read a portion of the file:

```python
>>> some_digi = raw_file.arrays(entry_start=50, entry_stop=100)
>>> some_digi
<Array [{evt_header: {...}, ...}, ..., {...}] type='50 * {evt_header: {evt_...'>
```

:::{warning}
Reading a portion of a file still has to scan the events before `entry_start`. On a Lustre-backed 2 GB file this costs about 1.5 s per long prefix, while reading the events themselves stays at the sequential bandwidth. Opening a file never scans it: the entry offsets are built lazily while reading and kept in the open reader, so later reads through the same object do not scan again.
:::

To read only specific fields:

```python
>>> cgem_mdc_digi = raw_file.arrays(filter_name=['cgem', 'mdc'])
>>> cgem_mdc_digi.fields
['evt_header', 'cgem', 'mdc']
```

:::{note}
Available fields are: `cgem`, `mdc`, `tof`, `emc`, `muc`, `trigGTD`.

`evt_header` is always read and cannot be filtered out.
:::

### Iterate over entries

For files that do not fit in memory, read them in batches with `iterate`:

```python
>>> for batch in raw_file.iterate(step_size=5000):
...     print(len(batch))
```

Each batch is an independent `ak.Array`. `entry_start` and `entry_stop` work as in `arrays`, and `report=True` yields `(start, stop, array)` tuples:

```python
>>> for start, stop, batch in raw_file.iterate(step_size=1000, entry_start=100, entry_stop=3000, report=True):
...     print(start, stop, len(batch))
```

Batches are read with a single sequential pass over the same open file handle, so iterating is as fast as reading the file at once and only holds one batch in memory.

### Entry offsets

The raw format stores the number of entries but not their offsets, so a partial read scans the preceding events once. `entry_byte_offsets` exposes that scan and keeps the result in the reader:

```python
>>> raw_file.entry_byte_offsets[:3]
array([     108,    10480,    22340])
```

Nothing is written to disk. Opening a file only parses its header and tail, and the entry index is extended lazily as reads move forward.


Close the file when done:

```python
>>> raw_file.close()
```

:::{warning}
Always close the file after reading to free up system resources.
:::

Open the file using a context manager to automatically close it after reading:

```python
>>> with p3.open_raw(file_path) as f:
...     raw_data = f.arrays()
```

### Concatenate multiple files

To read multiple files and concatenate them into a single array, use `pybes3.concatenate_raw`:

```python
>>> files = [
...     "run_0087397_All_merge0_file001_SFO-1.raw",
...     "run_0087397_All_merge0_file002_SFO-1.raw",
... ]
>>> raw_data = p3.concatenate_raw(files)
>>> raw_data
<Array [{evt_header: {...}, ...}, ..., {...}] type='363492 * {evt_header: {...'>
```

Set `verbose=True` to print progress:

```python
>>> raw_data = p3.concatenate_raw(files, verbose=True)
Reading file run_0087397_All_merge0_file001_SFO-1.raw: 0 -> 180322 entries ...
Reading file run_0087397_All_merge0_file001_SFO-1.raw: 180322 -> 363492 entries ...
```

`entry_start`, `entry_stop` and `filter_name` can also be used in `concatenate_raw` to read only a portion of the files or specific fields:

```python
>>> raw_data = p3.concatenate_raw(files, entry_start=100, entry_stop=200, filter_name=['cgem', 'mdc'])
>>> raw_data
<Array [{evt_header: {...}, ...}, ..., {...}] type='100 * {evt_header: {evt...'>
```

Set `workers` to read several files at once. Each worker opens its own reader and keeps its own read buffer of up to 64 MB, so memory grows with the number of workers:

```python
>>> raw_data = p3.concatenate_raw(files, workers=2)
```

To process several files in batches, use `pybes3.iterate_raw`. `entry_start` and `entry_stop` count entries across all files, and a batch never spans two files:

```python
>>> for batch in p3.iterate_raw(files, step_size=5000, entry_start=100, entry_stop=300000):
...     print(len(batch))
```
