# Documentation for pybes3

`pybes3` is a Python module that aims to make it easier for BES3 users to work with Python.

:::{note} Help us improve `pybes3`!
If you have any suggestions, questions, or issues, please feel free to
[open an issue](https://github.com/mrzimu/pybes3/issues/new/choose).
:::

:::{tip} See Also
It is highly recommended to take a look at these Python modules before using `pybes3`:

- [`awkward`](https://awkward-array.org/doc/stable/index.html): A Python module that can handle ragged-like array.
- [`uproot`](https://uproot.readthedocs.io/en/stable/): A ROOT I/O Python module. `pybes3` uses `uproot` to read BES3 ROOT files.
:::

::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} Install `pybes3` using `pip`
:link: installation
:link-type: doc

Get `pybes3` from PyPI.
:::

:::{grid-item-card} Get started with user manual
:link: user-manual/data-reading
:link-type: doc

Learn how to read data and use detector utilities.
:::
::::

## User manual

::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} Data reading
:link: user-manual/data-reading
:link-type: doc

Read `rtraw`, `rec`, `dst`, and even `raw` files.
:::

:::{grid-item-card} Global ID (gid)
:link: convention/gid
:link-type: doc

Zero-based global ID (gid) for detector elements in `pybes3`.
:::

:::{grid-item-card} BOSS identifier
:link: user-manual/identifier
:link-type: doc

Convert BOSS detector identifier number to a human-readable format.
:::

:::{grid-item-card} Helix operations
:link: user-manual/helix
:link-type: doc

Parse and transform helix parameters.
:::
::::

## Performance

`pybes3` is designed to be fast and efficient. It uses C++ to accelerate some of the operations, such as helix operations, detector identifier conversion, etc.

### Data reading

A simple benchmark compares the performance of `pybes3` and `BOSS8` in reading `dst` files:

- For `pybes3`, we directly read out the `Event` tree:

    ```python
    import uproot
    import pybes3

    n_evt = ... # number of events to read
    files = [...] # list of ROOT files to read

    data_array = uproot.concatenate({f: "Event" for f in files}, entry_stop=n_evt)
    ```

- For `BOSS8`, reading reconstruction data with the default job-options loads `RecMakerAlg` for each event, which slows down the reading performance significantly (4–5× slower than pure reading). We test 2 cases:

    - A loop on all events **with** `RecMakerAlg` (default job-options):

        ```
        #include "$ROOTIOROOT/share/jobOptions_ReadRec.txt"
        #include "$OFFLINEEVENTLOOPMGRROOT/share/OfflineEventLoopMgr_Option.txt"

        EventCnvSvc.digiRootInputFile = { ... }; // list of ROOT files to read
        ApplicationMgr.EvtMax = ...; // number of events to read
        MessageSvc.OutputLevel = 7; // suppress messages
        ```

    - A loop on all events **without** `RecMakerAlg`. This is similar to reading `rtraw` files and is the closest case to raw ROOT reading:

        ```
        ApplicationMgr.ExtSvc += {"EvtPersistencySvc/EventPersistencySvc"};
        ApplicationMgr.ExtSvc +={"RootEvtSelector/EventSelector","RootCnvSvc/EventCnvSvc"};
        EventPersistencySvc.CnvServices += {"EventCnvSvc"};
        #include "$OFFLINEEVENTLOOPMGRROOT/share/OfflineEventLoopMgr_Option.txt"

        EventCnvSvc.digiRootInputFile = { ... }; // list of ROOT files to read
        ApplicationMgr.EvtMax = ...; // number of events to read
        MessageSvc.OutputLevel = 7; // suppress messages
        ```

The benchmark machine is an Intel i7-12700 with Great Wall GW7000 4TB SSD, running AlmaLinux OS 9 on WSL2. The number of events varies from 1,000 to 1,000,000.

The results are shown below:

<div align="center">
    <picture>
        <source srcset="_static/image/io-benchmarking-dark.svg" media="(prefers-color-scheme: dark)">
        <img src="_static/image/io-benchmarking-light.svg" alt="Dummy Reading Performance">
    </picture>
</div>

The linear fit results are:

|                            | Initialization time (s) | Slope (s/10k-event) |
| :------------------------: | :---------------------: | :-----------------: |
| BOSS8 (with `RecMakerAlg`) | 0.615                   | 2.766               |
| BOSS8 (no `RecMakerAlg`)   | 0.451                   | 0.338               |
| pybes3                     | 1.135                   | 0.326               |

The results show that `pybes3` achieves comparable performance to `BOSS8` when `RecMakerAlg` is not loaded—its reading speed is close to raw ROOT I/O. With default `BOSS8` settings (including `RecMakerAlg`), `pybes3` is several times faster. The only exception is very small datasets (~1,000 events), where Python module import and initialization overhead becomes noticeable.

:::{toctree}
:hidden:
:maxdepth: 2

installation
:::

:::{toctree}
:hidden:
:caption: Convention
:maxdepth: 1

convention/unit
convention/gid
:::

:::{toctree}
:hidden:
:caption: User manual
:maxdepth: 1

user-manual/data-reading
user-manual/mdc
user-manual/tof
user-manual/emc
user-manual/muc
user-manual/cgem
user-manual/helix
user-manual/identifier
:::

:::{toctree}
:hidden:
:caption: API Reference
:maxdepth: 1

api/pybes3
api/pybes3.io
api/pybes3.mdc
api/pybes3.tof
api/pybes3.emc
api/pybes3.muc
api/pybes3.cgem
api/pybes3.helix
api/pybes3.identifier
api/pybes3.digi_id
:::
