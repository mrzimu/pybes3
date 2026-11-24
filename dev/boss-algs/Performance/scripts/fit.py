"""
Fit ``t = a + b * N`` to the exported hyperfine results and print the table quoted in the docs.

Usage:
    python fit.py [results-dir]

`results-dir` defaults to the `results` directory next to this script and holds the
`hyperfine_<nevt>.json` files written by `bench.sh`. Each reader is fitted separately, with the
per-point standard deviations as weights, and reported as the fixed start-up cost `a` and the
per-event cost `b`.
"""

import json
import re
import sys
from pathlib import Path

import numpy as np

# The command names that `bench.sh` passes to hyperfine, and the names used in the documentation.
READERS = {"boss": "BOSS8", "root": "Plain ROOT", "pybes3 (c++": "Pybes3"}


def load(directory):
    """
    Collect the timings of every reader.

    Parameters:
        directory: The directory that holds the `hyperfine_<nevt>.json` files.

    Returns:
        A mapping from the names in `READERS` to a list of `(n-events, mean, stddev)` tuples in
        seconds, sorted by the number of events.
    """
    results = {name: [] for name in READERS.values()}
    for path in sorted(directory.glob("hyperfine_*.json")):
        match = re.fullmatch(r"hyperfine_(\d+)\.json", path.name)
        if match is None:
            continue
        n_events = int(match.group(1))
        with path.open(encoding="utf-8") as file:
            payload = json.load(file)
        for result in payload["results"]:
            for prefix, name in READERS.items():
                if result["command"].startswith(prefix):
                    results[name].append((n_events, result["mean"], result["stddev"]))
                    break

    for points in results.values():
        points.sort()

    return results


def fit(points):
    """
    Fit a straight line through one reader's timings.

    Parameters:
        points: The `(n-events, mean, stddev)` tuples of one reader, in seconds.

    Returns:
        A `(start-up-ms, per-event-us)` pair.
    """
    x = np.array([point[0] for point in points], dtype=float)
    y = np.array([point[1] for point in points], dtype=float)
    # A run whose timings did not vary has a zero deviation, which would give it an infinite
    # weight; the floor keeps the weights finite without changing the fit otherwise.
    sigma = np.array([max(point[2], 1e-6) for point in points], dtype=float)

    slope, intercept = np.polyfit(x, y, 1, w=1 / sigma)

    return intercept * 1e3, slope * 1e6


def main():
    """
    Print the fit table for the results directory given on the command line.

    Raises:
        SystemExit: If the directory does not exist or holds no usable results.
    """
    script_dir = Path(__file__).resolve().parent
    directory = Path(sys.argv[1]) if len(sys.argv) > 1 else script_dir / "results"

    if not directory.is_dir():
        raise SystemExit(f"No such directory: {directory}")

    results = load(directory)
    if not any(results.values()):
        raise SystemExit(f"No hyperfine results in {directory}")

    print("| Reader       | Start-up time (ms) | Time per event (µs) |")
    print("| :----------- | -----------------: | ------------------: |")
    for name, points in results.items():
        if not points:
            continue
        start_up, per_event = fit(points)
        print(f"| {name:<12} | {start_up:>18.0f} | {per_event:>19.1f} |")


if __name__ == "__main__":
    main()
