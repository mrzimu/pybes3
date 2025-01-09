import awkward as ak
import numba as nb
import numpy as np

from .DatabaseConnector import DatabaseConnector


@nb.njit
def _expand_vertex(
    header_runs: np.ndarray, vtx_runNo: np.ndarray, vtx_info: np.ndarray
) -> np.ndarray:
    abs_header_runs = np.abs(header_runs)
    res = np.ones(shape=(len(header_runs), 6), dtype=np.float64) * 99999

    for run, info in zip(vtx_runNo, vtx_info):
        idx = abs_header_runs == run
        res[idx] = info

    return res


def query_vertex(header_runs: ak.Array, boss_ver: str, db_conn: DatabaseConnector) -> ak.Array:
    abs_runs = np.abs(header_runs)
    run_from = ak.min(abs_runs)
    run_to = ak.max(abs_runs)

    query = f"""
        SELECT
            RunNo,
            Vx,
            Vy,
            Vz,
            SigmaVx,
            SigmaVy,
            SigmaVz
        FROM
            offlinedb.BeamPar
        WHERE
            RunNo >= {run_from} AND RunNo <= {run_to} AND SftVer = '{boss_ver}'
    """

    result = db_conn.query(query)
    assert (
        len(result) > 0
    ), "No data found in the database, check the run numbers and software version"

    res_runNo = np.array([x[0] for x in result])
    res_vtx = np.array([x[1:] for x in result]).reshape(-1, 6)

    expanded_vtx = _expand_vertex((header_runs).to_numpy(), res_runNo, res_vtx)

    return ak.Array(
        {
            "x": expanded_vtx[:, 0],
            "y": expanded_vtx[:, 1],
            "z": expanded_vtx[:, 2],
            "sigma_x": expanded_vtx[:, 3],
            "sigma_y": expanded_vtx[:, 4],
            "sigma_z": expanded_vtx[:, 5],
        }
    )
