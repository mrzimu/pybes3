from __future__ import annotations

from pathlib import Path

DATA_DIR = Path(__file__).parent

MDC_GEOM = DATA_DIR / "mdc_geom.npz"
TOF_GEOM = DATA_DIR / "tof_geom.npz"
EMC_GEOM = DATA_DIR / "emc_geom.npz"
MUC_GEOM = DATA_DIR / "muc_geom.npz"

CGEM_ELEC_TABLE = DATA_DIR / "cgem_elec_table.npz"
