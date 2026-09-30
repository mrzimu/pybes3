import subprocess
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

temp_dir = tempfile.TemporaryDirectory()

subprocess.run(
    ["ExportTofScintGeom", str(Path(temp_dir.name) / "tof_scint_geom.csv")],
    check=True,
)

subprocess.run(
    ["ExportTofMrpcGeom", str(Path(temp_dir.name) / "tof_mrpc_geom.csv")],
    check=True,
)

scint_df = pd.read_csv(Path(temp_dir.name) / "tof_scint_geom.csv")
mrpc_df = pd.read_csv(Path(temp_dir.name) / "tof_mrpc_geom.csv")

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

np.savez_compressed("tof_geom.npz", **np_dict)

temp_dir.cleanup()
