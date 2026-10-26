#!/usr/bin/env bash
# Build the BesVis-style geometry export programs of dev/geometry.
#
# A BOSS environment has to be configured first, by running the setup script of your
# installation: it must provide ROOT and BesVisLib, export ROOTSYS and
# GDMLMANAGEMENTDATAROOT, and put the include/library search paths used below
# (ROOTGEOROOT, BESVISLIBROOT, LD_LIBRARY_PATH) into the environment. No path is hard-coded
# here, so ./build.sh works from any BOSS installation.
set -e

HERE=$(cd "$(dirname "$0")" && pwd)
cd "$HERE"

if [ -z "${ROOTSYS:-}" ]; then
    echo "error: ROOTSYS is not set; source the BOSS environment setup script first" >&2
    exit 1
fi

# Search paths are taken from the BOSS environment: every directory of LD_LIBRARY_PATH is
# used for linking, and its sibling "include" directory (the InstallArea layout) is used
# for the headers of ROOTGeo / BesVisLib.
INCS=()
LIBS=()
IFS=':' read -r -a _ld_path <<< "${LD_LIBRARY_PATH:-}"
for d in "${_ld_path[@]}"; do
    [ -z "$d" ] && continue
    LIBS+=("-L$d")
    [ -d "$d/../include" ] && INCS+=("-I$d/../include")
done

# Header directories of the BOSS packages as they are checked out
for d in "${ROOTGEOROOT:-}" "${BESVISLIBROOT:-}"; do
    [ -n "$d" ] && [ -d "$d/include" ] && INCS+=("-I$d/include")
done

for src in dump_tof_scin_vtx dump_tof_mrpc dump_muc_strip_vtx dump_cgem_strip; do
    echo "compiling $src ..."
    g++ -std=c++20 -O2 -o "$src" "$src.cxx" \
        -I"$HERE" ${INCS[@]+"${INCS[@]}"} ${LIBS[@]+"${LIBS[@]}"} \
        -lROOTGeo -lGeom -lCore -lRIO -lThread -lMathCore
done

cat <<'EOF'
done. The four programs write the geometry tables pybes3 uses (all in cm, the inputs of
`export-tof-geom.py` / `export-muc-geom.py`):
  ./dump_tof_scin_vtx > tof-scint-vertices.csv   # TOF scintillators: 8 vertices
  ./dump_tof_mrpc     > tof-mrpc-vertices.csv    # TOF MRPC strips: 8 vertices
  ./dump_muc_strip_vtx > muc-vtx.csv             # MUC strips: 8 vertices
  ./dump_cgem_strip   > cgem_strip.csv           # CGEM X/V strip parameters [--model N]
EOF
