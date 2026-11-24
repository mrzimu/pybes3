#!/usr/bin/env bash
#
# Benchmark BOSS, plain ROOT and pybes3 reading the same DST file with hyperfine.
#
# Usage: bash bench.sh <dst-file>
#
# Every event count in `nevt_list` is timed for all three readers in one hyperfine invocation
# (two warm-up runs, five measured runs) and exported to `results/hyperfine_<nevt>.json`, which
# `fit.py` turns into the table quoted in the documentation.
#
# Source the BOSS environment, build and install `AccessTds` and `ReadEvent` so that both are in
# PATH, and generate the job options with `gen-jobs.py` before running this.

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <dst-file>" >&2
    exit 1
fi

dst=$(realpath "$1")
nevt_list=(1000 5000 10000 50000 100000)

cd "$(dirname "$0")"
mkdir -p results

for exe in boss.exe ReadEvent; do
    if ! command -v "${exe}" >/dev/null; then
        echo "${exe} is not in PATH, source the BOSS environment first" >&2
        exit 1
    fi
done

python_bin=${PYTHON:-}
if [[ -z ${python_bin} ]]; then
    if [[ -x ../../../../.venv/bin/python ]]; then
        python_bin=../../../../.venv/bin/python
    else
        python_bin=python3
    fi
fi

for nevt in "${nevt_list[@]}"; do
    echo "=== ${nevt} events ==="
    hyperfine \
        --warmup 2 \
        --runs 5 \
        --export-json "results/hyperfine_${nevt}.json" \
        -n "boss (${nevt} events)" "bash read-boss.sh ${nevt}" \
        -n "root (${nevt} events)" "bash read-root.sh '${dst}' ${nevt}" \
        -n "pybes3 (c++ ${nevt} events)" "${python_bin} read-pybes3.py '${dst}' ${nevt} cpp"
done
