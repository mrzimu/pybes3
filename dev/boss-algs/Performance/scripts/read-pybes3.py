"""
Read the Dst collections of a DST file with pybes3, for one benchmark point.

Usage:
    python read-pybes3.py <dst-file> <n-evt> <backend>

`backend` selects the uproot-custom backend: `cpp` for the generated kernels measured in the
documentation, or `detree`. The seven collections are the same ones `AccessTdsAlg` and
`ReadEvent` read, and the result is thrown away.
"""

import sys

import uproot as urt
import uproot_custom as uc

import pybes3  # noqa: F401  # registers the BES3 readers with uproot-custom

# The sub-branches of TDstEvent, by the names used inside TDstEvent.
BRANCHES = [
    "m_mdcTrackCol",
    "m_mdcKalTrackCol",
    "m_mdcDedxCol",
    "m_extTrackCol",
    "m_tofTrackCol",
    "m_emcTrackCol",
    "m_mucTrackCol",
]


def main():
    """
    Read one benchmark point and exit.

    Raises:
        SystemExit: If the arguments are wrong, the event count exceeds the file, or uproot did
            not return every requested branch.
    """
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)

    path = sys.argv[1]
    n_evt = int(sys.argv[2])
    uc.set_backend(sys.argv[3])

    event = urt.open(path)["Event"]
    if n_evt > event.num_entries:
        raise SystemExit(
            f"Requested number of events ({n_evt}) exceeds available entries ({event.num_entries})"
        )

    data = event.arrays(filter_name=BRANCHES, entry_stop=n_evt)

    # uproot drops a filter name that matches no branch silently, which would make this reader do
    # less work than the other two without any visible sign.
    missing = sorted(set(BRANCHES) - set(data.fields))
    if missing:
        raise SystemExit(f"Branches not read: {missing}")


if __name__ == "__main__":
    main()
