# pybes

This project aims to make BES3 user easier to work with Python.

**This is an unofficial project.**

## Requirements

This module requires `Python3` and `ROOT`. See [here](https://root.cern/install/) to getinformation about how to install `ROOT` on your local machine.

* `Python3`: `>=3.9` is recommended, no gurantee for `<=3.8`.
* `ROOT`: Only tested on `6.32.02`, but theoretically not strict.

Report of sucessfully run on any `OS`, `Python`, `ROOT` combinition is welcome!

## Installation

```bash
# clone the repository
git clone https://code.ihep.ac.cn/mrli/pybes.git

# build
cd pybes
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=<path/to/install>
make -j
make install
```

## Usage

Before importing this module in python, you need to setup environment first:

```bash
# environment setup
source <path/to/install>/bin/setup-pybes.sh
```

Then you can import `pybes` in python:

```python
>>> import pybes
```

### besio

You can read BES3 `rtraw`, `dst`, `rec` file with `pybes.io` module. All data will be returned as `awkward` arrays. For more information about `awkward`, see [awkward-array](https://awkward-array.org/).

```python
>>> reader = pybes.io.Bes3EventReader("demo.dst")
>>> reader
Bes3EventReader(entries=1000, files=['demo.dst'])
>>> evts = reader.arrays()
>>> evts
<Bes3Event with 1000 entries, sub-events: ['header', 'evt_rec', 'mc', 'dst']>
```

You can access arrays like:

```python
>>> evts.dst
<IODstEvent with available fields: ['mdc', 'emc', 'tof', 'muc', 'dedx', 'ext']>
>>> evts.dst.mdc
<DstMdc with attributions: trackIndex, helix, helixErr, stat, chi2, ndof, nster, nlayers, firstLayer, lastLayer>
>>> evts.dst.mdc.helix # nEvt * nTracks * 5
<Array [[[-0.291, ..., -0.552], ...], ...] type='1000 * var * 5 * float64'>
```

In general, there are too much information in `dst`, `rec` files. To suppress memory usage, you can specify the fields you want to read:

```python
>>> reader.available_fields # Get available fields
['/Event/Dst/Dedx', '/Event/Dst/Emc', '/Event/Dst/Ext', '/Event/Dst/Mdc', '/Event/Dst/Muc', '/Event/Dst/Tof', '/Event/EvtRec/DTag', '/Event/EvtRec/EtaToGG', '/Event/EvtRec/Evt', '/Event/EvtRec/Pi0', '/Event/EvtRec/PrimaryVertex', '/Event/EvtRec/Trk', '/Event/EvtRec/VeeVertex', '/Event/Header', '/Event/Mc/Emc', '/Event/Mc/McParticle', '/Event/Mc/Mdc', '/Event/Mc/Muc', '/Event/Mc/Tof']
>>> evts = reader.arrays(fields=['/Event/Dst/Mdc','/Event/Mc/McParticle'])
>>> evts
<Bes3Event with 1000 entries, sub-events: ['mc', 'dst']>
>>> evts.dst
<IODstEvent with available fields: ['mdc']>
```
