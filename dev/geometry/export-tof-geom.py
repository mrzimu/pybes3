"""Export the TOF geometry to `src/pybes3/data/tof_geom.npz`.

The BOSS algorithms `ExportTofScintGeom` / `ExportTofMrpcGeom` (from `dev/boss-algs`) have
to be run in a BOSS environment, where `GDMLMANAGEMENTDATAROOT` is set. This script runs
them directly, or reuses CSV files exported earlier (e.g. by `dump_tof_scin_vtx` and
`dump_tof_mrpc` of this directory):

    python dev/geometry/export-tof-geom.py                    # run the BOSS algorithms
    python dev/geometry/export-tof-geom.py scint.csv mrpc.csv # reuse exported CSVs
"""

import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

OUTPUT = Path(__file__).resolve().parents[2] / "src" / "pybes3" / "data" / "tof_geom.npz"

if len(sys.argv) > 2:
    scint_df = pd.read_csv(sys.argv[1])
    mrpc_df = pd.read_csv(sys.argv[2])
else:
    with tempfile.TemporaryDirectory() as temp_dir:
        scint_csv = Path(temp_dir) / "tof_scint_geom.csv"
        mrpc_csv = Path(temp_dir) / "tof_mrpc_geom.csv"

        subprocess.run(["ExportTofScintGeom", str(scint_csv)], check=True)
        subprocess.run(["ExportTofMrpcGeom", str(mrpc_csv)], check=True)

        scint_df = pd.read_csv(scint_csv)
        mrpc_df = pd.read_csv(mrpc_csv)

geom_df = pd.concat([scint_df, mrpc_df.query("part!=1")], ignore_index=True)

points_x = np.stack([geom_df[f"x{i}"].to_numpy() for i in range(8)]).T
points_y = np.stack([geom_df[f"y{i}"].to_numpy() for i in range(8)]).T
points_z = np.stack([geom_df[f"z{i}"].to_numpy() for i in range(8)]).T


np_dict = {
    "gid": geom_df["gid"].to_numpy(),
    "part": geom_df["part"].to_numpy(),
    "layer_or_module": geom_df["layer_or_module"].to_numpy(),
    "phi_or_strip": geom_df["phi_or_strip"].to_numpy(),
    "points_x": np.ascontiguousarray(points_x),
    "points_y": np.ascontiguousarray(points_y),
    "points_z": np.ascontiguousarray(points_z),
}

np.savez_compressed(OUTPUT, **np_dict)
print(f"Wrote {OUTPUT} ({len(geom_df)} elements)")
