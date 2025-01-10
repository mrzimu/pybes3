import awkward as ak
import awkward.contents
import awkward.index
import numpy as np
import vector
import vector.backends.awkward

from pybes3.tools import make_jagged_array

from .numba import _helix_to_ptphipz, _helix_to_xy, _pivot, _good_trk_selection


def _regularize_helix_array(helix_arr: ak.Array, n_trks: ak.Array) -> ak.Array:
    """
    Regularizes the helix array by flattening it and creating a new layout.

    Transform a [n_trks, 5] helix array into a record array with fields
    "dr", "phi0", "kappa", "dz", and "tanl". This function is used to
    regularize the helix array read from the input file.

    Args:
        helix_arr (ak.Array): The input helix array.
        n_trks (ak.Array): The number of tracks.

    Returns:
        ak.Array: The regularized helix array.
    """
    flat_helix = ak.flatten(helix_arr)

    dr = flat_helix[:, 0]
    phi0 = flat_helix[:, 1]
    kappa = flat_helix[:, 2]
    dz = flat_helix[:, 3]
    tanl = flat_helix[:, 4]

    n_trks = ak.to_numpy(n_trks)
    offsets = np.zeros(len(n_trks) + 1, dtype=np.int64)
    offsets[1:] = np.cumsum(n_trks)

    layout = awkward.contents.ListOffsetArray(
        awkward.index.Index(offsets),
        awkward.contents.RecordArray(
            [
                awkward.contents.NumpyArray(dr),
                awkward.contents.NumpyArray(phi0),
                awkward.contents.NumpyArray(kappa),
                awkward.contents.NumpyArray(dz),
                awkward.contents.NumpyArray(tanl),
            ],
            ["dr", "phi0", "kappa", "dz", "tanl"],
        ),
    )

    return ak.Array(layout)


def pivot(helix: ak.Array, n_trks: ak.Array, Bz: float, pos_changes: ak.Array) -> ak.Array:
    flat_helix = ak.flatten(helix)

    dr = ak.to_numpy(flat_helix["dr"])
    phi0 = ak.to_numpy(flat_helix["phi0"])
    kappa = ak.to_numpy(flat_helix["kappa"])
    dz = ak.to_numpy(flat_helix["dz"])
    tanl = ak.to_numpy(flat_helix["tanl"])

    new_dr, new_phi0, new_dz = _pivot(
        dr,
        phi0,
        kappa,
        dz,
        tanl,
        Bz,
        ak.to_numpy(np.repeat(pos_changes.x, n_trks)),
        ak.to_numpy(np.repeat(pos_changes.y, n_trks)),
        ak.to_numpy(np.repeat(pos_changes.z, n_trks)),
    )

    return make_jagged_array(
        ak.Array(
            {
                "dr": new_dr,
                "phi0": new_phi0,
                "kappa": kappa,
                "dz": new_dz,
                "tanl": tanl,
            }
        ),
        n_trks,
    )


def select_good_tracks(
    helix: ak.Array, n_trks: np.ndarray, dr_cut: float, dz_cut: float
) -> ak.Array:
    flat_dr = ak.to_numpy(ak.flatten(helix["dr"]))
    flat_dz = ak.to_numpy(ak.flatten(helix["dz"]))
    flat_res = _good_trk_selection(flat_dr, flat_dz, dr_cut, dz_cut)
    return make_jagged_array(flat_res, n_trks)


def helix_to_position(helix: ak.Array, n_trks: np.ndarray) -> ak.Array:
    flat_dr = ak.to_numpy(ak.flatten(helix["dr"]))
    flat_phi0 = ak.to_numpy(ak.flatten(helix["phi0"]))

    flat_x, flat_y = _helix_to_xy(flat_dr, flat_phi0)
    flat_z = ak.to_numpy(ak.flatten(helix["dz"]))

    return make_jagged_array(
        ak.Array(
            {"x": flat_x, "y": flat_y, "z": flat_z},
            with_name="Vector3D",
            behavior=vector.backends.awkward.behavior,
        ),
        n_trks,
    )


def helix_to_momentum(helix: ak.Array, n_trks: np.ndarray) -> ak.Array:
    flat_phi0 = ak.to_numpy(ak.flatten(helix["phi0"]))
    flat_kappa = ak.to_numpy(ak.flatten(helix["kappa"]))
    flat_tanl = ak.to_numpy(ak.flatten(helix["tanl"]))

    # flat phi is the azimuthal angle of the momentum, i.e. phi = phi0 + pi/2
    flat_pt, flat_phi, flat_pz = _helix_to_ptphipz(flat_phi0, flat_kappa, flat_tanl)
    return make_jagged_array(
        ak.Array(
            {"pt": flat_pt, "phi": flat_phi, "pz": flat_pz},
            with_name="Momentum3D",
            behavior=vector.backends.awkward.behavior,
        ),
        n_trks,
    )
