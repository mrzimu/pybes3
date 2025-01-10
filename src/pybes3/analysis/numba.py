import numba as nb
import numpy as np


@nb.njit
def _regularize_phi(phi: np.ndarray, phi_min: float, phi_max: float) -> None:
    for i in range(len(phi)):
        if phi[i] < phi_min:
            phi[i] = phi[i] + 2 * np.pi

        if phi[i] > phi_max:
            phi[i] = phi[i] - 2 * np.pi


@nb.njit
def _pivot(
    dr: np.ndarray,
    phi0: np.ndarray,
    kappa: np.ndarray,
    dz: np.ndarray,
    tanl: np.ndarray,
    Bz: float,
    rel_dx: np.ndarray,
    rel_dy: np.ndarray,
    rel_dz: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    alpha = 1000 / 2.99792458 / Bz  # Tesla

    r = np.abs(alpha / kappa)
    rpdr = r + dr
    x_center = rpdr * np.cos(phi0)
    y_center = rpdr * np.sin(phi0)

    new_dx = x_center - rel_dx
    new_dy = y_center - rel_dy
    new_dr = np.sqrt(new_dx**2 + new_dy**2) - r

    new_phi0 = np.arctan2(new_dy, new_dx)
    _regularize_phi(new_phi0, 0, 2 * np.pi)

    # new dz
    delta_phi0 = new_phi0 - phi0
    _regularize_phi(delta_phi0, -np.pi, np.pi)

    new_dz = dz - delta_phi0 * r * tanl - rel_dz

    return new_dr, new_phi0, new_dz


@nb.njit
def _helix_to_xy(dr: np.ndarray, phi0: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    x = dr * np.cos(phi0)
    y = dr * np.sin(phi0)
    return x, y


@nb.njit
def _helix_to_ptphipz(
    phi0: np.ndarray, kappa: np.ndarray, tanl: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    pt = np.abs(1 / kappa)
    phi = phi0 + np.pi / 2
    pz = pt * tanl
    return pt, phi, pz


@nb.njit
def _good_trk_selection(
    dr: np.ndarray, dz: np.ndarray, dr_cut: float, dz_cut: float
) -> np.ndarray:
    res1 = np.abs(dr) < dr_cut
    res2 = np.abs(dz) < dz_cut
    return res1 & res2
