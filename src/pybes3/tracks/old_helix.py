import warnings
from typing import Literal, Union

import awkward as ak
import numba as nb
import numpy as np

from ..typing import FloatLike, IntLike


@nb.vectorize(cache=True)
def _helix01_to_x(helix0: FloatLike, helix1: FloatLike) -> FloatLike:
    """
    Convert helix parameters to x location.

    Parameters:
        helix0: helix[0] parameter, dr.
        helix1: helix[1] parameter, phi0.

    Returns:
        x location of the helix.
    """
    return helix0 * np.cos(helix1)


@nb.vectorize(cache=True)
def _helix01_to_y(helix0: FloatLike, helix1: FloatLike) -> FloatLike:
    """
    Convert helix parameters to y location.

    Parameters:
        helix0: helix[0] parameter, dr.
        helix1: helix[1] parameter, phi0.

    Returns:
        y location of the helix.
    """
    return helix0 * np.sin(helix1)


@nb.vectorize(cache=True)
def _helix2_to_pt(
    helix2: FloatLike,
) -> FloatLike:
    """
    Convert helix parameter to pt.

    Parameters:
        helix2: helix[2] parameter, kappa.

    Returns:
        pt of the helix.
    """
    return 1 / np.abs(helix2)


@nb.vectorize(cache=True)
def _helix2_to_charge(
    helix2: FloatLike,
) -> FloatLike:
    """
    Convert helix parameter to charge.

    Parameters:
        helix2: helix[2] parameter, kappa.

    Returns:
        charge of the helix.
    """
    if -1e-10 < helix2 < 1e-10:
        return np.int8(0)
    return np.int8(1) if helix2 > 0 else np.int8(-1)


@nb.vectorize(cache=True)
def _pt_helix1_to_px(pt: FloatLike, helix1: FloatLike) -> FloatLike:
    """
    Convert pt and helix1 to px.

    Parameters:
        pt: pt of the helix.
        helix1: helix[1] parameter, phi0.

    Returns:
        px of the helix.
    """
    return -pt * np.sin(helix1)


@nb.vectorize(cache=True)
def _pt_helix1_to_py(pt: FloatLike, helix1: FloatLike) -> FloatLike:
    """
    Convert pt and helix1 to py.

    Parameters:
        pt: pt of the helix.
        helix1: helix[1] parameter, phi0.

    Returns:
        py of the helix.
    """
    return pt * np.cos(helix1)


@nb.vectorize(cache=True)
def _pt_helix4_to_p(pt: FloatLike, helix4: FloatLike) -> FloatLike:
    """
    Convert pt and helix4 to p.

    Parameters:
        pt: pt of the helix.
        helix4: helix[4] parameter, tanl.

    Returns:
        p of the helix.
    """
    return pt * np.sqrt(1 + helix4**2)


@nb.vectorize(cache=True)
def _pz_p_to_theta(pz: FloatLike, p: FloatLike) -> FloatLike:
    """
    Convert pz and p to theta.

    Parameters:
        pz: pz of the helix.
        p: p of the helix.

    Returns:
        theta of the helix.
    """
    return np.arccos(pz / p)


def parse_helix(
    helix: Union[ak.Array, np.ndarray],
    library: Literal["ak", "auto"] = "auto",
) -> Union[ak.Array, dict[str, np.ndarray]]:
    """
    Parse helix parameters to physical parameters.

    Parameters:
        helix: helix parameters, the last dimension should be 5.
        library: the library to use, if "auto", return a dict when input is np.ndarray, \
            return an ak.Array when input is ak.Array. If "ak", return an ak.Array.

    Returns:
        parsed physical parameters. "x", "y", "z", "r" for position, \
            "pt", "px", "py", "pz", "p", "theta", "phi" for momentum, \
            "charge" for charge, "r_trk" for track radius.
    """

    warnings.warn(
        "'parse_helix' is deprecated and will be removed in the future, "
        "use 'helix_obj' and 'helix_awk' instead.",
        DeprecationWarning,
    )

    helix0 = helix[..., 0]
    helix1 = helix[..., 1]
    helix2 = helix[..., 2]
    helix3 = helix[..., 3]
    helix4 = helix[..., 4]

    x = _helix01_to_x(helix0, helix1)
    y = _helix01_to_y(helix0, helix1)
    z = helix3
    r = np.abs(helix0)

    pt = _helix2_to_pt(helix2)
    px = _pt_helix1_to_px(pt, helix1)
    py = _pt_helix1_to_py(pt, helix1)
    pz = pt * helix4
    p = _pt_helix4_to_p(pt, helix4)
    theta = _pz_p_to_theta(pz, p)
    phi = np.arctan2(py, px)

    charge = _helix2_to_charge(helix2)

    r_trk = pt * (10 / 2.99792458)  # |pt| * [GeV/c] / 1[e] / 1[T] = |pt| * 10/3 [m]
    r_trk = r_trk * 100  # to [cm]

    res_dict = {
        "x": x,
        "y": y,
        "z": z,
        "r": r,
        "px": px,
        "py": py,
        "pz": pz,
        "pt": pt,
        "p": p,
        "theta": theta,
        "phi": phi,
        "charge": charge,
        "r_trk": r_trk,
    }

    if isinstance(helix, ak.Array) or library == "ak":
        return ak.zip(res_dict)
    else:
        return res_dict


@nb.vectorize(cache=True)
def _xy_to_helix0(x: FloatLike, y: FloatLike) -> FloatLike:
    """
    Convert x and y to helix[0] parameter, dr.

    Parameters:
        x: x location of the helix.
        y: y location of the helix.

    Returns:
        helix[0] parameter, dr.
    """
    return np.sqrt(x**2 + y**2)


@nb.vectorize(cache=True)
def _xy_to_helix1(x: FloatLike, y: FloatLike) -> FloatLike:
    """
    Convert x and y to helix[1] parameter, phi0.

    Parameters:
        x: x location of the helix.
        y: y location of the helix.

    Returns:
        helix[1] parameter, phi0.
    """
    return (np.arctan2(y, x) + 2 * np.pi) % (2 * np.pi)  # make sure that phi0 is in [0, 2pi)


@nb.vectorize(cache=True)
def _ptcharge_to_helix2(pt: FloatLike, charge: IntLike) -> FloatLike:
    """
    Convert pt, charge to helix[2] parameter, kappa.

    Parameters:
        pt: pt of the helix.
        charge: charge of the helix.

    Returns:
        helix[2] parameter, kappa.
    """
    return np.sign(charge) / pt if pt != 0 else 0


@nb.vectorize(cache=True)
def _pxpy_to_pt(px: FloatLike, py: FloatLike) -> FloatLike:
    """
    Convert px and py to pt.

    Parameters:
        px: px of the helix.
        py: py of the helix.

    Returns:
        pt of the helix.
    """
    return np.sqrt(px**2 + py**2)


def compute_helix(
    data: Union[ak.Array, dict[str, np.ndarray]],
    library: Literal["ak", "auto"] = "auto",
) -> Union[ak.Array, np.ndarray]:
    """
    Compute helix parameters from charge, position and momentum.

    Parameters:
        data: data to compute helix parameters from, should contain "x", "y", "z", "px", \
            "py", "pz" and "charge" keys.
        library: the library to use, if "auto", return an np.ndarray when input is a dictionary \
            of np.ndarray, return an ak.Array when input is ak.Array. If "ak", return an ak.Array.

    Returns:
        helix parameters, the shape is (..., 5), where the last dimension is (dr, phi0, kappa, z, tanl).
    """
    warnings.warn(
        "'compute_helix' is deprecated and will be removed in the future, "
        "use 'helix_obj' and 'helix_awk' instead.",
        DeprecationWarning,
    )

    x = data["x"]
    y = data["y"]
    z = data["z"]
    px = data["px"]
    py = data["py"]
    pz = data["pz"]
    charge = data["charge"]

    pt = _pxpy_to_pt(px, py)

    helix0 = _xy_to_helix0(x, y)
    helix1 = _xy_to_helix1(x, y)
    helix2 = _ptcharge_to_helix2(pt, charge)
    helix3 = z
    helix4 = pz / pt

    if isinstance(data, ak.Array) or library == "ak":
        return ak.concatenate(
            [
                ak.unflatten(helix0, 1, axis=-1),
                ak.unflatten(helix1, 1, axis=-1),
                ak.unflatten(helix2, 1, axis=-1),
                ak.unflatten(helix3, 1, axis=-1),
                ak.unflatten(helix4, 1, axis=-1),
            ],
            axis=-1,
        )  # make the shape be (..., 5)
    else:
        return np.vstack([helix0, helix1, helix2, helix3, helix4]).T


@nb.vectorize(cache=True)
def _regularize_phi0(dr: FloatLike, phi0: FloatLike) -> FloatLike:
    """
    Regularize phi0 to make sure that dr is positive.

    Parameters:
        dr: helix[0] parameter, dr.
        phi0: helix[1] parameter, phi0.

    Returns:
        phi0: helix[1] parameter, phi0. Always in [0, 2pi).
    """
    if dr < 0:
        phi0 += 3 * np.pi
    return phi0 % (2 * np.pi)  # make sure that phi0 is in [0, 2pi)


def regularize_helix(helix: Union[ak.Array, np.ndarray]) -> Union[ak.Array, np.ndarray]:
    """
    Sometimes, the `dr` may be negative, which is not allowed. This function will make sure \
    that the `dr` is positive by rotating `phi0`.

    Parameters:
        helix: helix parameters, the last dimension should be 5.

    Returns:
        helix: helix parameters, the last dimension should be 5, and the `dr` is positive.
        The `phi0` is rotated to make sure that the `dr` is positive.
    """

    warnings.warn(
        "'regularize_helix' is deprecated and will be removed in the future, "
        "use 'helix_obj' and 'helix_awk' instead.",
        DeprecationWarning,
    )

    helix0 = helix[..., 0]
    helix1 = helix[..., 1]
    helix2 = helix[..., 2]
    helix3 = helix[..., 3]
    helix4 = helix[..., 4]

    helix1 = _regularize_phi0(helix0, helix1)
    helix0 = np.abs(helix0)

    if isinstance(helix, ak.Array):
        return ak.concatenate(
            [
                ak.unflatten(helix0, 1, axis=-1),
                ak.unflatten(helix1, 1, axis=-1),
                ak.unflatten(helix2, 1, axis=-1),
                ak.unflatten(helix3, 1, axis=-1),
                ak.unflatten(helix4, 1, axis=-1),
            ],
            axis=-1,
        )
    else:
        return np.vstack([helix0, helix1, helix2, helix3, helix4]).T
