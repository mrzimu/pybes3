# DST reading performance

Measures how long three readers need to decode the same DST file: a BOSS 8 job, a plain `ROOT` C++ program and pybes3. The numbers quoted in `README.md` and `docs/index.md` come from this harness.

All three read the seven Dst collections of `TDstEvent` (`m_mdcTrackCol`, `m_mdcKalTrackCol`, `m_mdcDedxCol`, `m_extTrackCol`, `m_tofTrackCol`, `m_emcTrackCol`, `m_mucTrackCol`) and throw the result away, so only the reading and decoding cost is measured. The other branches of the `Event` tree are not read.

## Layout

- `src/AccessTdsAlg.cc`: the BOSS algorithm, built into the `AccessTds` module. What it reads is a compile-time choice, see the access config block at the top of the file.
- `src/ReadEvent.cc`: the plain `ROOT` reader. Takes the input file and the number of events on the command line.
- `opts/AccessTDS.txt`: example job options file; `scripts/gen-jobs.py` writes the ones actually used.
- `scripts/`: the harness, see below.

## Harness

| File | Purpose |
| :--- | :--- |
| `bench.sh <dst>` | times the three readers for every event count in `nevt_list` with `hyperfine` (two warm-up runs, five measured runs) and exports `results/hyperfine_<nevt>.json` |
| `gen-jobs.py <dst>` | expands `pure-dst.txt` into `jobs/job_<nevt>.txt`, one per event count |
| `read-boss.sh <nevt>` | one BOSS measurement, running that job options file |
| `read-root.sh <dst> <nevt>` | one plain `ROOT` measurement |
| `read-pybes3.py <dst> <nevt> <backend>` | one pybes3 measurement; `cpp` is the backend measured in the docs |
| `fit.py [results-dir]` | fits `t = a + b * N` to the exported results and prints the table below |

`jobs/` and `results/` are generated and stay out of git.

## Running

The benchmark needs a BOSS 8 environment. Source it, then build and install the two targets, and source the `InstallArea` that belongs to your platform (for example `dev/boss-algs/InstallArea/x86_64-el9-gcc13-dbg`), because a plain `make` does not update it, see the traps below:

```bash
make -C dev/boss-algs/build AccessTds ReadEvent
make -C dev/boss-algs/build install
source dev/boss-algs/InstallArea/<platform>/setup/set_runtime.sh
```

Generate the job options and measure:

```bash
python3 dev/boss-algs/Performance/scripts/gen-jobs.py <dst-file>
bash dev/boss-algs/Performance/scripts/bench.sh <dst-file>
```

`bench.sh` needs `boss.exe` and `ReadEvent` in `PATH`, and uses the repository `.venv` for the pybes3 part unless `PYTHON` is set. Print the table that the documentation quotes with:

```bash
python3 dev/boss-algs/Performance/scripts/fit.py dev/boss-algs/Performance/scripts/results
```

## Results

AMD EPYC 9654 (96 cores), two warm-up runs and five measured runs per point, weighted fit of `t = a + b * N`:

| Reader       | Start-up time (ms) | Time per event (µs) |
| :----------- | -----------------: | ------------------: |
| `BOSS8`      | 658                | 55.2                |
| Plain `ROOT` | 429                | 23.6                |
| Pybes3       | 566                | 24.3                |

BOSS is more than twice as expensive per event as the other two, because the Gaudi converters rebuild every collection in the transient data store; the file is read once either way, so the difference is conversion, not I/O. pybes3 decodes about as fast as plain `ROOT`: the C++ kernels are generated for the BES3 event layout and cost no more than the generic `ROOT` object streamer, so the few percent between the two rows is the awkward arrays built on top of the decoded data.

## Traps found while building this

**Sub-branches of `TDstEvent` need their full name.** `TBranch::SetBranchStatus( "*", false )` also disables the `TDstEvent.m_*` sub-branches that hold the collections, and neither `"TDstEvent"`, `"TDstEvent*"` nor `"TDstEvent.*"` turns them back on (`"TDstEvent.*"` even reports "No branch name is matching wildcard"). The symptom is a `ReadEvent` whose runtime stays at the file-open cost for any event count, with empty collections. `ReadEvent.cc` enables every collection by its full name `TDstEvent.m_xxx` and checks the `found` counter of `SetBranchStatus`, because a name that matches nothing is otherwise ignored silently.

**uproot ignores an unknown `filter_name`.** A reader that asks for a misspelled branch does less work than the other two without any visible sign, which is exactly how the first version of this benchmark compared six collections against seven. `read-pybes3.py` verifies that every requested branch came back.

**A filled `TDstEvent` cannot be destroyed.** `TBranchElement` takes over the collections of the object it fills, and `TDstEvent::~TDstEvent()` deletes them again, so deleting an event that was read segfaults inside the destructor. `ReadEvent.cc` therefore keeps its `TDstEvent` for the lifetime of the process; a stack object or a `unique_ptr` crashes.

**`make` alone is not enough for a BOSS run.** The module has to be installed into the InstallArea as well, a stale `libAccessTds.so` silently turns an "access" run into a "no access" run. `finalize()` prints `Processed N events, M TDS object(s) retrieved`, with `M == 7 * N` when all seven collections were read.
