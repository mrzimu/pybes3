from typing import Literal, Union

import awkward as ak
import numba as nb
import numpy as np


@nb.vectorize([nb.float64(nb.float64, nb.float64)])
def _helix01_to_x(
    helix0: Union[ak.Array, np.ndarray, float], helix1: Union[ak.Array, np.ndarray, float]
) -> Union[ak.Array, np.ndarray, float]:
    """
    Convert helix parameters to x location.

    Parameters:
        helix0: helix[0] parameter, dr.
        helix1: helix[1] parameter, phi0.

    Returns:
        x location of the helix.
    """
    return helix0 * np.cos(helix1)


@nb.vectorize([nb.float64(nb.float64, nb.float64)])
def _helix01_to_y(
    helix0: Union[ak.Array, np.ndarray, float], helix1: Union[ak.Array, np.ndarray, float]
) -> Union[ak.Array, np.ndarray, float]:
    """
    Convert helix parameters to y location.

    Parameters:
        helix0: helix[0] parameter, dr.
        helix1: helix[1] parameter, phi0.

    Returns:
        y location of the helix.
    """
    return helix0 * np.sin(helix1)


@nb.vectorize([nb.float64(nb.float64)])
def _helix2_to_pt(
    helix2: Union[ak.Array, np.ndarray, float],
) -> Union[ak.Array, np.ndarray, float]:
    """
    Convert helix parameter to pt.

    Parameters:
        helix2: helix[2] parameter, kappa.

    Returns:
        pt of the helix.
    """
    return 1 / np.abs(helix2)


@nb.vectorize([nb.int8(nb.float64)])
def _helix2_to_charge(
    helix2: Union[ak.Array, np.ndarray, float],
) -> Union[ak.Array, np.ndarray, float]:
    """
    Convert helix parameter to charge.

    Parameters:
        helix2: helix[2] parameter, kappa.

    Returns:
        charge of the helix.
    """
    if -1e-10 < helix2 < 1e-10:
        return 0
    return 1 if helix2 > 0 else -1


@nb.vectorize([nb.float64(nb.float64)])
def _helix4_to_theta(
    helix4: Union[ak.Array, np.ndarray, float],
) -> Union[ak.Array, np.ndarray, float]:
    """
    Convert helix parameter to theta.

    Parameters:
        helix4: helix[4] parameter, tanl.

    Returns:
        theta of the helix.
    """
    return np.arctan(1 / helix4)


@nb.vectorize([nb.float64(nb.float64, nb.float64)])
def _pt_helix1_to_px(
    pt: Union[ak.Array, np.ndarray, float], helix1: Union[ak.Array, np.ndarray, float]
) -> Union[ak.Array, np.ndarray, float]:
    """
    Convert pt and helix1 to px.

    Parameters:
        pt: pt of the helix.
        helix1: helix[1] parameter, phi0.

    Returns:
        px of the helix.
    """
    return -pt * np.sin(helix1)


@nb.vectorize([nb.float64(nb.float64, nb.float64)])
def _pt_helix1_to_py(
    pt: Union[ak.Array, np.ndarray, float], helix1: Union[ak.Array, np.ndarray, float]
) -> Union[ak.Array, np.ndarray, float]:
    """
    Convert pt and helix1 to py.

    Parameters:
        pt: pt of the helix.
        helix1: helix[1] parameter, phi0.

    Returns:
        py of the helix.
    """
    return pt * np.cos(helix1)


@nb.vectorize([nb.float64(nb.float64, nb.float64)])
def _pt_helix4_to_p(
    pt: Union[ak.Array, np.ndarray, float], helix4: Union[ak.Array, np.ndarray, float]
) -> Union[ak.Array, np.ndarray, float]:
    """
    Convert pt and helix4 to p.

    Parameters:
        pt: pt of the helix.
        helix4: helix[4] parameter, tanl.

    Returns:
        p of the helix.
    """
    return pt * np.sqrt(1 + helix4**2)


def parse_helix(
    helix: Union[ak.Array, np.ndarray], library: Literal["ak", "auto"] = "auto"
) -> Union[ak.Array, dict[str, np.ndarray]]:
    """
    Parse helix parameters to physical parameters.

    Parameters:
        helix: helix parameters, the last dimension should be 5.
        library: the library to use, if "auto", return a dict when input is np.ndarray, \
            return an ak.Array when input is ak.Array. If "ak", return an ak.Array.

    Returns:
        parsed physical parameters. "x", "y", "z", "r" for position, \
            "pt", "px", "py", "pz", "p", "theta", "phi" for momentum.
    """
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
    theta = _helix4_to_theta(helix4)
    phi = -helix1

    charge = _helix2_to_charge(helix2)

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
    }

    if isinstance(helix, ak.Array) or library == "ak":
        return ak.zip(res_dict)
    else:
        return res_dict
