"""
Expand `pure-dst.txt` into one BOSS job options file per event count.

Usage:
    python gen-jobs.py <dst-file>

Every `@nevt@` and `@dst@` placeholder in `pure-dst.txt` is replaced and the result is written to
`jobs/job_<nevt>.txt`, next to this script. `bench.sh` reads those files.
"""

import sys
from pathlib import Path

# The event counts measured in the documentation.
NEVT_LIST = [1000, 5000, 10000, 50000, 100000]


def main():
    """
    Write one job options file per event count.

    Raises:
        SystemExit: If the DST file is missing from the command line or does not exist, or if the
            template misses a placeholder.
    """
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)

    dst = Path(sys.argv[1])
    if not dst.is_file():
        raise SystemExit(f"No such file: {dst}")

    here = Path(__file__).resolve().parent
    template = (here / "pure-dst.txt").read_text(encoding="utf-8")
    for placeholder in ("@nevt@", "@dst@"):
        if placeholder not in template:
            raise SystemExit(f"pure-dst.txt does not contain the {placeholder} placeholder")

    job_dir = here / "jobs"
    job_dir.mkdir(exist_ok=True)

    for nevt in NEVT_LIST:
        path = job_dir / f"job_{nevt}.txt"
        path.write_text(
            template.replace("@nevt@", str(nevt)).replace("@dst@", str(dst.resolve())),
            encoding="utf-8",
        )
        print(path.relative_to(here))


if __name__ == "__main__":
    main()
