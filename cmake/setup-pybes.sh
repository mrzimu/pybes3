#!/bin/bash

base_path="$(realpath "$(dirname "$(realpath "${BASH_SOURCE[0]}")")"/..)"

if [[ -d "${base_path}/lib" ]]; then
    export LD_LIBRARY_PATH="${base_path}/lib:${LD_LIBRARY_PATH}"
fi

if [[ -d "${base_path}/lib64" ]]; then
    export LD_LIBRARY_PATH="${base_path}/lib64:${LD_LIBRARY_PATH}"
fi

if [[ -n "$PYTHONPATH" ]]; then
    export PYTHONPATH="${base_path}/python:${PYTHONPATH}"
else
    export PYTHONPATH="${base_path}/python"
fi
