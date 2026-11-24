#!/usr/bin/env bash
#
# One BOSS measurement: read-boss.sh <n-evt>.
#
# Runs the job options file generated for that event count by `gen-jobs.py`.

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <n-evt>" >&2
    exit 1
fi

cd "$(dirname "$0")"
mkdir -p results

job="jobs/job_${1}.txt"
if [[ ! -f ${job} ]]; then
    echo "${job} is missing, run gen-jobs.py first" >&2
    exit 1
fi

boss.exe "${job}" > "results/job_${1}.log" 2>&1
