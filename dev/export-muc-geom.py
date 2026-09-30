"""Export the MUC strip geometry to `src/pybes3/data/muc_geom.npz`.

`ExportMucGeom` (from `dev/boss-algs`) has to be run in a BOSS environment, where
`GDMLMANAGEMENTDATAROOT` is set. This script runs it directly, or reuses a CSV file
exported earlier:

    python dev/export-muc-geom.py                # run ExportMucGeom
    python dev/export-muc-geom.py muc-vtx.csv    # reuse an exported CSV
"""

import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

OUTPUT = Path(__file__).resolve().parent.parent / "src" / "pybes3" / "data" / "muc_geom.npz"

if len(sys.argv) > 1:
    df = pd.read_csv(sys.argv[1])
else:
    with tempfile.TemporaryDirectory() as temp_dir:
        csv_path = Path(temp_dir) / "muc_vtx.csv"
        subprocess.run(["ExportMucGeom", str(csv_path)], check=True)
        df = pd.read_csv(csv_path)

points_x = np.stack([df[f"x{i}"].to_numpy() for i in range(8)]).T
points_y = np.stack([df[f"y{i}"].to_numpy() for i in range(8)]).T
points_z = np.stack([df[f"z{i}"].to_numpy() for i in range(8)]).T

np_dict = {
    "gid": df["gid"].to_numpy(),
    "part": df["part"].to_numpy(),
    "segment": df["segment"].to_numpy(),
    "layer": df["layer"].to_numpy(),
    "strip": df["strip"].to_numpy(),
    "points_x": np.ascontiguousarray(points_x),
    "points_y": np.ascontiguousarray(points_y),
    "points_z": np.ascontiguousarray(points_z),
    "center_x": df["cx"].to_numpy(),
    "center_y": df["cy"].to_numpy(),
    "center_z": df["cz"].to_numpy(),
    "dx": df["dx"].to_numpy(),
    "dy": df["dy"].to_numpy(),
    "dz": df["dz"].to_numpy(),
}

np.savez_compressed(OUTPUT, **np_dict)
print(f"Wrote {OUTPUT} ({len(df)} strips)")
