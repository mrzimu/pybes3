#!/usr/bin/env bash
#
# One plain ROOT measurement: read-root.sh <dst-file> <n-evt>.
#
# `ReadEvent` has to be in PATH, which is what the InstallArea setup script does.

set -euo pipefail

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <dst-file> <n-evt>" >&2
    exit 1
fi

ReadEvent "$1" "$2"
