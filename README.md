# Pybes3

Pybes3 is a Python module that aims to make it easier for BES3 users to work with Python.

> [!TIP]
> If you have any suggestions, questions, or issues, please feel free to open an [issue](https://github.com/mrzimu/pybes3/issues/new/choose).

It is highly recommended to take a look at these Python modules before using Pybes3:

- [`awkward`](https://awkward-array.org/doc/stable/index.html): A Python module that can handle ragged-like array.
- [`uproot`](https://uproot.readthedocs.io/en/stable/): A ROOT I/O Python module. Pybes3 uses `uproot` to read BES3 ROOT files.

Visit the [documentation](https://pybes3.readthedocs.io/en/stable/) for more information about installation, usage, and examples.

## Installation

> [!NOTE]
> Pybes3 requires Python 3.9 or higher.

### Install Pybes3 using pip

```bash
python3 -m pip install pybes3
```

### Users on lxlogin server

"lxlogin server" means the login server of computation clusters of IHEP. If you are not using lxlogin server, you can skip this section.

Since there is a quota limitation on the user's home directory (`~/`), you need to create symlinks for `~/.local` and `~/.cache`, which contain pip packages and caches installed in "user mode":

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

### Using Pybes3 under `BOSS8` environment

If you are using Pybes3 under `BOSS8` environment, you MUST run following commands after setting up `BOSS8` environment:

```bash
export PYTHONPATH=`python -m site --user-site`:$PYTHONPATH
export PATH=`python -m site --user-base`/bin:$PATH
```

> [!WARNING]
> DO NOT add these commands to your shell configuration file (e.g. `~/.bashrc`), since they will conflict with the default python environment (without `BOSS8`).

## Features

At the moment, Pybes3 provides:

- **BES3 data reading**: Read `rtraw`, `rec`, `dst`, and even `raw` files.

- **Identifier**: Convert BOSS detector identifier number to a human-readable format.

- **Indexing**: Each detector element in Pybes3 is assigned a zero-based index, useful for array indexing and mapping detector elements.

- **Geometry**: Retrieve and compute geometry information of detectors.

- **Helix operations**: Parse and transform helix parameters.

## Performance

Pybes3 is designed to be fast and efficient. It uses C++ to accelerate some of the operations, such as helix operations, detector identifier conversion, etc.

### Data reading

The benchmark compares three readers on identical work: the seven Dst collections of every event are decoded and nothing is written back. The other branches of the `Event` tree (`TEvtHeader`, `TTrigEvent`, `TEvtRecObject`, `THltEvent`) are not read.

All readers read the same sub-branches of `TDstEvent`:

| Branch                       | Collection          |
| :--------------------------- | :------------------ |
| `TDstEvent/m_mdcTrackCol`    | `DstMdcTrackCol`    |
| `TDstEvent/m_mdcKalTrackCol` | `DstMdcKalTrackCol` |
| `TDstEvent/m_mdcDedxCol`     | `DstMdcDedxCol`     |
| `TDstEvent/m_extTrackCol`    | `DstExtTrackCol`    |
| `TDstEvent/m_tofTrackCol`    | `DstTofTrackCol`    |
| `TDstEvent/m_emcTrackCol`    | `DstEmcShowerCol`   |
| `TDstEvent/m_mucTrackCol`    | `DstMucTrackCol`    |

- Pybes3 reads those sub-branches with `uproot`:

    ```python
    import uproot
    import pybes3

    n_evt = ...  # number of events to read
    files = [...]  # list of ROOT files to read
    branches = [
        "TDstEvent/m_mdcTrackCol",
        "TDstEvent/m_mdcKalTrackCol",
        "TDstEvent/m_mdcDedxCol",
        "TDstEvent/m_extTrackCol",
        "TDstEvent/m_tofTrackCol",
        "TDstEvent/m_emcTrackCol",
        "TDstEvent/m_mucTrackCol",
    ]

    data = uproot.concatenate({f: "Event" for f in files}, expressions=branches, entry_stop=n_evt)
    ```

- A plain `ROOT` C++ program opens the same file, points a branch address at the `TDstEvent` object, enables the same sub-branches and loops over `TTree::GetEntry`. This is the fastest reading available without an experiment framework.

- A `BOSS8` job loops over all events and reads the same collections through the transient data store, so each collection is first converted from its ROOT representation into data-store objects by the Gaudi converters.

Each point is measured with `hyperfine`, using two warm-up runs and five measured runs, for `1000`, `5000`, `10000`, `50000` and `100000` events.

The benchmark machine is an `AMD EPYC 9654` (96 cores) and the input file is `/bes3fs/offline/data/712-1/psipp/round17/dst/231029/run_0078615_All_file001_SFO-1.dst`.

The results are shown below:

<div align="center">
    <picture>
        <source srcset="./docs/_static/image/io-benchmarking-dark.png" media="(prefers-color-scheme: dark)">
        <img src="./docs/_static/image/io-benchmarking-light.png" alt="DST reading performance" width="50%">
    </picture>
</div>

Fitting the reading time with `t = a + b * N` separates the fixed start-up cost from the per-event cost:

| Reader       | Start-up time (ms) | Time per event (µs) |
| :----------- | -----------------: | ------------------: |
| `BOSS8`      | 658                | 55.2                |
| Plain `ROOT` | 429                | 23.6                |
| Pybes3       | 566                | 24.3                |

`BOSS8` pays 55.2 µs per event, more than twice what the other readers pay, because the Gaudi converters rebuild every collection in the transient data store. The file is read once in all cases; the extra time is the conversion, not the I/O.

Pybes3 is almost on top of plain `ROOT` at 24.3 µs per event against 23.6 µs. The few percent in between is the cost of building the awkward arrays on top of the decoded data, while the decoding itself costs no more than the generic ROOT object streamer, since the C++ kernels are generated for the BES3 event layout.

Start-up goes the other way: Pybes3 spends 566 ms before the first event against 429 ms for plain `ROOT`, mostly importing the module and loading its kernels, and 658 ms for `BOSS8`, which also configures the event loop and the persistency services. Start-up is paid once per job, so the per-event column decides long jobs and this column decides short ones; either way Pybes3 is twice as cheap per event as `BOSS8` and within a few percent of plain `ROOT`.
