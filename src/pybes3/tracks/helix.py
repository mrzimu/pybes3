import math
import warnings
from operator import xor
from typing import Literal, Optional, Union, overload

import awkward as ak
import numba as nb
import numpy as np
import vector
import vector.backends.awkward as vec_ak

vector.register_awkward()

from .._utils import _extract_index, _flat_to_numpy, _recover_shape
from ..typing import FloatLike, IntLike

TypeObjPosition = Union[vector.VectorObject3D, tuple[float, float, float]]
TypeObjMomentum = Union[vector.MomentumObject3D, tuple[float, float, float]]
TypeAwkPosition = Union[ak.Array, vector.VectorObject3D, tuple[float, float, float]]


def _regularize_obj_position(
    args: Union[TypeObjPosition, tuple[TypeObjPosition]],
) -> vector.VectorObject3D:
    """
    Regularizes the position argument to always return a VectorObject3D.

    Args:
        args: A tuple of (x, y, z), a VectorObject3D, an ak.Record, or a tuple
            containing one of them.

    Returns:
        A VectorObject3D representing the position point.
    """
    if isinstance(args, tuple) and len(args) == 1:
        args = args[0]

    if isinstance(args, vector.VectorObject3D):
        return args

    if isinstance(args, ak.Record):
        return vector.VectorObject3D(x=args["x"], y=args["y"], z=args["z"])

    # tuple
    point = args if args is not None else (0, 0, 0)

    assert len(point) == 3, "Pivot must be a tuple of (x, y, z)."
    return vector.VectorObject3D(x=point[0], y=point[1], z=point[2])


def _regularize_obj_momentum(
    args: Union[TypeObjMomentum, tuple[TypeObjMomentum]],
) -> vector.MomentumObject3D:
    """
    Regularizes the momentum argument to always return a MomentumObject3D.

    Args:
        args: A tuple of (px, py, pz), a MomentumObject3D, an ak.Record, or a tuple
            containing one of them.

    Returns:
        A MomentumObject3D representing the momentum vector.
    """
    if isinstance(args, tuple) and len(args) == 1:
        args = args[0]

    if isinstance(args, vector.MomentumObject3D):
        return args

    if isinstance(args, ak.Record):
        return vector.MomentumObject3D(
            px=args["px"],
            py=args["py"],
            pz=args["pz"],
        )

    # tuple
    momentum = args
    assert len(momentum) == 3, "Momentum must be a tuple of (px, py, pz)."
    return vector.MomentumObject3D(px=momentum[0], py=momentum[1], pz=momentum[2])


def _change_pivot(
    r,
    old_dr,
    old_phi0,
    old_dz,
    kappa,
    tanl,
    old_error,
    old_pivot,
    new_pivot,
):
    """
    Change the pivot point of the helix and transform its parameters accordingly.
    The transformation is based on the BOSS `Helix::pivot` method.

    This method will be called by the `change_pivot` method of `HelixObject`, `HelixAwkwardRecord` and `HelixAwkwardArray`.

    Args:
        r: Circular radius of the helix.
        old_dr: Current dr of the helix.
        old_phi0: Current phi0 of the helix.
        old_dz: Current dz of the helix.
        kappa: Current kappa of the helix.
        tanl: Current tanl of the helix.
        old_error: Current error matrix of the helix, if available.
        old_pivot: Current pivot point of the helix, either as a VectorObject3D or a tuple of (x, y, z).
        new_pivot: New pivot point of the helix, either as a VectorObject3D or a tuple of (x, y, z).

    Returns:
        A tuple containing the new dr, new phi0, new dz, and the transformed error matrix (if available).
    """
    if isinstance(old_pivot, vector.VectorObject3D):
        old_dist = vector.obj(rho=old_dr + r, phi=old_phi0)
    elif isinstance(old_pivot, vector.VectorNumpy3D):
        old_dist = vector.arr({"rho": old_dr + r, "phi": old_phi0})
    else:
        raise TypeError(f"Unsupported old_pivot type: {type(old_pivot)}. ")

    center = old_pivot.to_2D() + old_dist

    new_dist: vector.Vector2D = center - new_pivot.to_2D()

    new_dr = new_dist.rho - r
    new_phi0 = new_dist.phi % (2 * np.pi)

    if isinstance(new_phi0, np.ndarray):
        dphi = np.unwrap(new_phi0 - old_phi0)
    else:
        dphi = (new_phi0 - old_phi0) % (2 * np.pi)
        if dphi > np.pi:
            dphi -= 2 * np.pi
    new_dz = old_pivot.z + old_dz - r * tanl * dphi - new_pivot.z

    # transform error matrix
    if old_error is not None:
        cos_dphi = np.cos(dphi)
        sin_dphi = np.sin(dphi)

        rdr = r + old_dr
        rdrpr = 1 / (r + new_dr)

        jacobian: np.ndarray = np.zeros_like(old_error)  # (tracks, i, j)
        if jacobian.ndim == 3:
            jacobian = jacobian.transpose(1, 2, 0)  # (i, j, tracks)

        jacobian[0, 0] = cos_dphi
        jacobian[0, 1] = rdr * sin_dphi
        jacobian[0, 2] = r / kappa * (1 - cos_dphi)

        jacobian[1, 0] = -rdrpr * sin_dphi
        jacobian[1, 1] = rdr * rdrpr * cos_dphi
        jacobian[1, 2] = r / kappa * rdrpr * sin_dphi

        jacobian[2, 2] = 1

        jacobian[3, 0] = r * rdrpr * tanl * sin_dphi
        jacobian[3, 1] = r * tanl * (1 - rdr * rdrpr * cos_dphi)
        jacobian[3, 2] = r / kappa * tanl * (dphi - r * rdrpr * sin_dphi)
        jacobian[3, 3] = 1
        jacobian[3, 4] = -r * dphi

        jacobian[4, 4] = 1

        if jacobian.ndim == 3:
            jacobian = jacobian.transpose(2, 0, 1)  # (tracks, i, j)
            new_error = jacobian @ old_error @ jacobian.transpose(0, 2, 1)
        else:
            new_error = jacobian @ old_error @ jacobian.T
    else:
        new_error = None

    return new_dr, new_phi0, new_dz, new_error


def _obj_isclose(self, other, *, rtol: float, atol: float, equal_nan: bool) -> bool:
    kwargs = {"rtol": rtol, "atol": atol, "equal_nan": equal_nan}
    other = other.change_pivot(self.pivot)

    # when `self` is an ak.Record, its pivot needs to be converted to a VectorObject3D
    self_pivot = vector.obj(x=self.pivot.x, y=self.pivot.y, z=self.pivot.z)
    other_pivot = vector.obj(x=other.pivot.x, y=other.pivot.y, z=other.pivot.z)

    condition = (
        np.isclose(self.dr, other.dr, **kwargs)
        and np.isclose(self.phi0, other.phi0, **kwargs)
        and np.isclose(self.kappa, other.kappa, **kwargs)
        and np.isclose(self.tanl, other.tanl, **kwargs)
        and np.isclose(self.dz, other.dz, **kwargs)
        and np.isclose(np.abs(self_pivot - other_pivot), 0, **kwargs)
    )

    if self.error is not None and other.error is not None:
        condition = condition and np.allclose(self.error, other.error, **kwargs)

    return bool(condition)


def _arr_isclose(self, other, *, rtol: float, atol: float, equal_nan: bool) -> ak.Array:
    kwargs = {"rtol": rtol, "atol": atol, "equal_nan": equal_nan}
    other = other.change_pivot(self.pivot)

    condition = ak.ones_like(self.dr, dtype=bool)
    for f in [
        "dr",
        "phi0",
        "kappa",
        "tanl",
        "dz",
    ]:
        condition = condition & ak.isclose(self[f], other[f], **kwargs)

    # Check pivot separately
    if isinstance(self, ak.Record):
        self_pivot = ak.Record(
            {"x": self.pivot.x, "y": self.pivot.y, "z": self.pivot.z},
            with_name="Vector3D",
        )
        other_pivot = ak.Record(
            {"x": other.pivot.x, "y": other.pivot.y, "z": other.pivot.z},
            with_name="Vector3D",
        )
    else:
        self_pivot = self.pivot
        other_pivot = other.pivot

    condition = condition & ak.isclose(np.abs(self_pivot - other_pivot), 0, **kwargs)

    if "error" in self.fields and "error" in other.fields:
        condition = condition & ak.all(
            ak.all(ak.isclose(self.error, other.error, **kwargs), axis=-1), axis=-1
        )

    return condition


###############################################################################################


class HelixObject:
    def __init__(
        self,
        dr: float,
        phi0: float,
        kappa: float,
        dz: float,
        tanl: float,
        *,
        error: np.ndarray = None,
        pivot: TypeObjPosition = (0, 0, 0),
    ):
        self.dr = float(dr)
        self.phi0 = float(phi0)
        self.kappa = float(kappa)
        self.dz = float(dz)
        self.tanl = float(tanl)
        self.error = error
        self.pivot = _regularize_obj_position(pivot)

    @property
    def radius(self) -> float:
        """
        Circular radius of the helix (in cm).
        """
        return 1000 / 2.99792458 / np.abs(self.kappa)

    @property
    def momentum(self) -> vector.MomentumObject3D:
        """
        Momentum of the helix as a 3D vector.
        Note that the momentum is relative to the pivot, so once the pivot is changed,
        the momentum will also change accordingly.
        """
        pt = 1 / abs(self.kappa)
        pz = pt * self.tanl
        phi = (self.phi0 + np.pi / 2) % (2 * np.pi)
        return vector.obj(pt=pt, phi=phi, pz=pz)

    @property
    def position(self) -> vector.VectorObject3D:
        return vector.VectorObject3D(
            x=self.dr * math.cos(self.phi0),
            y=self.dr * math.sin(self.phi0),
            z=self.dz,
        )

    @property
    def charge(self) -> int:
        """
        Returns the charge of the helix.
        """
        return 1 if self.kappa > 1e-10 else -1 if self.kappa < -1e-10 else 0

    def change_pivot(self, *args):
        """
        Change the pivot point of the helix.
        The transformation refers to `Helix` class in `BOSS`.
        """
        # transform helix parameters
        r = self.radius

        old_dr = self.dr
        old_phi0 = self.phi0
        old_dz = self.dz
        tanl = self.tanl
        kappa = self.kappa

        old_pivot = self.pivot
        new_pivot = _regularize_obj_position(args)

        new_dr, new_phi0, new_dz, new_error = _change_pivot(
            r=r,
            old_dr=old_dr,
            old_phi0=old_phi0,
            old_dz=old_dz,
            kappa=kappa,
            tanl=tanl,
            old_error=self.error,
            old_pivot=old_pivot,
            new_pivot=new_pivot,
        )

        return HelixObject(
            dr=new_dr,
            phi0=new_phi0,
            kappa=kappa,
            dz=new_dz,
            tanl=tanl,
            error=new_error,
            pivot=new_pivot,
        )

    def __repr__(self) -> str:
        return f"Bes3Helix(dr={self.dr:.3f}, phi0={self.phi0:.3f}, kappa={self.kappa:.3f}, tanl={self.tanl:.3f}, dz={self.dz:.3f})"

    def isclose(
        self,
        other: "HelixObject",
        *,
        rtol: float = 1e-5,
        atol: float = 1e-8,
        equal_nan: bool = False,
    ) -> bool:
        if xor(
            (self.error is not None),
            (other.error is not None),
        ):
            warnings.warn(
                "One of the helix records has an error matrix, but the other does not. "
                "Ignoring error matrix for isclose check.",
                UserWarning,
            )

        return _obj_isclose(self, other, rtol=rtol, atol=atol, equal_nan=equal_nan)


###############################################################################################


def _check_kwargs_used_up(left_kwargs):
    if len(left_kwargs):
        warnings.warn(
            "Ignoring additional keyword arguments: " + ", ".join(left_kwargs.keys()),
            UserWarning,
        )


# case 1
@overload
def helix_obj(
    dr: float,
    phi0: float,
    kappa: float,
    dz: float,
    tanl: float,
    *,
    error: Optional[np.ndarray] = None,
    pivot: TypeObjPosition = (0, 0, 0),
) -> HelixObject: ...


# case 2
@overload
def helix_obj(
    *,
    params: tuple[float, float, float, float, float],
    error: Optional[np.ndarray] = None,
    pivot: TypeObjPosition = (0, 0, 0),
) -> HelixObject: ...


# case 3
@overload
def helix_obj(
    *,
    momentum: TypeObjMomentum,
    position: TypeObjPosition,
    charge: Literal[-1, 1],
    error: Optional[np.ndarray] = None,
    pivot: TypeObjPosition = (0, 0, 0),
) -> HelixObject: ...


def helix_obj(*args, **kwargs) -> HelixObject:
    pivot = _regularize_obj_position(kwargs.pop("pivot", (0, 0, 0)))

    error = kwargs.pop("error", None)
    if isinstance(error, ak.Array):
        error = error.to_numpy()

    # given helix parameters as positional arguments
    if len(args) > 0:
        _check_kwargs_used_up(kwargs)
        return HelixObject(*args, error=error, pivot=pivot)

    # given helix parameters as keyword arguments
    if "dr" in kwargs:
        dr = kwargs.pop("dr")
        phi0 = kwargs.pop("phi0")
        kappa = kwargs.pop("kappa")
        dz = kwargs.pop("dz")
        tanl = kwargs.pop("tanl")

        _check_kwargs_used_up(kwargs)
        return HelixObject(
            dr=dr, phi0=phi0, kappa=kappa, dz=dz, tanl=tanl, pivot=pivot, error=error
        )

    # given helix parameters as a tuple
    if "params" in kwargs:
        params = kwargs.pop("params")
        if len(params) != 5:
            raise ValueError("params must be a tuple of 5 elements")

        _check_kwargs_used_up(kwargs)
        return HelixObject(*params, pivot=pivot, error=error)

    # given momentum, position and charge
    charge: Literal[-1, 1] = int(kwargs.pop("charge"))
    assert charge in (-1, 1), "Charge must be either -1 or 1"

    momentum = _regularize_obj_momentum(kwargs.pop("momentum"))
    position = _regularize_obj_position(kwargs.pop("position"))

    # compute helix parameters
    kappa = charge / momentum.pt
    phi0 = (momentum.phi - np.pi / 2) % (2 * np.pi)

    dist = (position - pivot).to_2D()
    dr = dist.rho
    if not np.isclose(dist.phi % (2 * np.pi), phi0):
        dr *= -1

    dz = position.z - pivot.z
    tanl = momentum.pz / momentum.pt

    _check_kwargs_used_up(kwargs)
    return HelixObject(
        dr=dr,
        phi0=phi0,
        kappa=kappa,
        dz=dz,
        tanl=tanl,
        pivot=pivot,
        error=error,
    )


###############################################################################################


@nb.vectorize(cache=True)
def dr_phi0_to_x(dr: FloatLike, phi0: FloatLike) -> FloatLike:
    """
    Convert helix parameters to x location.

    Parameters:
        dr (float): helix[0] parameter, dr.
        phi0 (float): helix[1] parameter, phi0.

    Returns:
        x location of the helix.
    """
    return dr * np.cos(phi0)


@nb.vectorize(cache=True)
def dr_phi0_to_y(dr: FloatLike, phi0: FloatLike) -> FloatLike:
    """
    Convert helix parameters to y location.

    Parameters:
        dr: helix[0] parameter, dr.
        phi0: helix[1] parameter, phi0.

    Returns:
        y location of the helix.
    """
    return dr * np.sin(phi0)


@nb.vectorize(cache=True)
def phi0_to_phi(phi0: FloatLike) -> FloatLike:
    """
    Convert helix parameter phi0 to momentum phi.

    Parameters:
        phi0: helix[1] parameter, phi0.

    Returns:
        phi of the momentum vector.
    """
    return (phi0 + np.pi / 2) % (2 * np.pi)


@nb.vectorize(cache=True)
def kappa_to_pt(kappa: FloatLike) -> FloatLike:
    """
    Convert helix parameter to pt.

    Parameters:
        kappa: helix[2] parameter, kappa.

    Returns:
        pt of the helix.
    """
    return 1 / np.abs(kappa)


@nb.vectorize(cache=True)
def kappa_to_charge(kappa: IntLike) -> FloatLike:
    """
    Convert helix parameter to charge.

    Parameters:
        kappa: helix[2] parameter, kappa.

    Returns:
        charge of the helix.
    """
    return np.int8(1) if kappa > 1e-10 else np.int8(-1) if kappa < -1e-10 else np.int8(0)


@nb.vectorize(cache=True)
def kappa_to_radius(kappa: FloatLike) -> FloatLike:
    """
    Convert helix parameter kappa to circular radius.

    Parameters:
        kappa: helix[2] parameter, kappa.

    Returns:
        circular radius of the helix in cm.
    """
    return 1000 / 2.99792458 / np.abs(kappa)


###############################################################################################


def _compute_momentum(kappa, tanl, phi0):
    pt = kappa_to_pt(kappa)
    pz = pt * tanl
    phi = phi0_to_phi(phi0)
    return pt, phi, pz


def _compute_position(dr, phi0, dz):
    x = dr_phi0_to_x(dr, phi0)
    y = dr_phi0_to_y(dr, phi0)
    z = dz

    return x, y, z


###############################################################################################


class HelixAwkwardRecord(ak.Record):
    @property
    def momentum(self) -> vector.MomentumObject3D:
        """
        Returns the momentum of the helix as a 3D vector.

        Returns:
            vector.MomentumObject3D: The momentum vector of the helix.
        """
        pt, phi, pz = _compute_momentum(self.kappa, self.tanl, self.phi0)
        return ak.zip({"pt": pt, "phi": phi, "pz": pz}, with_name="Momentum3D")

    @property
    def position(self) -> vector.VectorObject3D:
        """
        Returns the position of the helix at a given azimuthal angle.

        Returns:
            vector.VectorObject3D: The position vector of the helix.
        """
        x, y, z = _compute_position(self.dr, self.phi0, self.dz)
        return ak.zip({"x": x, "y": y, "z": z}, with_name="Vector3D")

    @property
    def charge(self) -> int:
        """
        Returns the charge of the helix.

        Returns:
            int: The charge of the helix.
        """
        return kappa_to_charge(self.kappa)

    @property
    def radius(self) -> float:
        """
        Returns the radius of the helix.

        Returns:
            float: The radius of the helix in mm.
        """
        return kappa_to_radius(self.kappa)

    def change_pivot(self, *args):
        multi_trk = isinstance(self.pivot.x, ak.Array)

        # regularize pivot
        if multi_trk:
            if len(args) == 3:
                x, y, z = args
                new_pivot = None
            elif len(args) == 1:
                new_pivot = args[0]
                if isinstance(new_pivot, (vector.VectorObject3D, ak.Array, ak.Record)):
                    x = new_pivot.x
                    y = new_pivot.y
                    z = new_pivot.z
                    new_pivot = None
                else:
                    x = new_pivot[0]
                    y = new_pivot[1]
                    z = new_pivot[2]
                    new_pivot = None
            else:
                raise ValueError(
                    "change_pivot requires either 3 arguments (x, y, z) or 1 argument (pivot)."
                )

            if new_pivot is None:
                x = (
                    ak.ones_like(self.dr) * x
                    if not isinstance(x, (ak.Array, ak.Record))
                    else x
                )
                y = (
                    ak.ones_like(self.dr) * y
                    if not isinstance(y, (ak.Array, ak.Record))
                    else y
                )
                z = (
                    ak.ones_like(self.dr) * z
                    if not isinstance(z, (ak.Array, ak.Record))
                    else z
                )
                new_pivot = ak.Array({"x": x, "y": y, "z": z}, with_name="Vector3D")

            old_pivot_x = _flat_to_numpy(self.pivot.x)
            old_pivot_y = _flat_to_numpy(self.pivot.y)
            old_pivot_z = _flat_to_numpy(self.pivot.z)
            old_pivot = vector.arr({"x": old_pivot_x, "y": old_pivot_y, "z": old_pivot_z})

            new_pivot_x = _flat_to_numpy(new_pivot.x)
            new_pivot_y = _flat_to_numpy(new_pivot.y)
            new_pivot_z = _flat_to_numpy(new_pivot.z)
            new_pivot = vector.arr({"x": new_pivot_x, "y": new_pivot_y, "z": new_pivot_z})

        else:
            new_pivot = _regularize_obj_position(args)
            old_pivot = vector.obj(
                x=self.pivot.x,
                y=self.pivot.y,
                z=self.pivot.z,
            )

        # do transformation
        r = _flat_to_numpy(self.radius)
        old_dr = _flat_to_numpy(self.dr)
        old_phi0 = _flat_to_numpy(self.phi0)
        old_dz = _flat_to_numpy(self.dz)
        tanl = _flat_to_numpy(self.tanl)
        kappa = _flat_to_numpy(self.kappa)

        if "error" in self.fields:
            old_error = (
                _flat_to_numpy(self.error).reshape(-1, 5, 5)
                if multi_trk
                else _flat_to_numpy(self.error).reshape(5, 5)
            )
        else:
            old_error = None

        new_dr, new_phi0, new_dz, new_error = _change_pivot(
            r=r,
            old_dr=old_dr,
            old_phi0=old_phi0,
            old_dz=old_dz,
            kappa=kappa,
            tanl=tanl,
            old_error=old_error,
            old_pivot=old_pivot,
            new_pivot=new_pivot,
        )

        res_dict = {
            "dr": new_dr,
            "phi0": new_phi0,
            "kappa": kappa,
            "dz": new_dz,
            "tanl": tanl,
            "pivot": ak.Record(
                {"x": new_pivot.x, "y": new_pivot.y, "z": new_pivot.z},
                with_name="Vector3D",
            ),
        }

        if new_error is not None:
            res_dict["error"] = new_error

        res = ak.Record(res_dict, with_name="Bes3Helix")

        if multi_trk:
            raw_shape = _extract_index(self.dr.layout)
            for count in raw_shape:
                res = ak.unflatten(res, count)

        return res

    def isclose(
        self,
        value: "HelixAwkwardRecord",
        *,
        rtol: float = 1e-5,
        atol: float = 1e-8,
        equal_nan: bool = False,
    ) -> bool:
        """
        Check if two helix records are close to each other.

        Args:
            value (HelixAwkwardRecord): The helix record to compare with.

        Returns:
            bool: True if the records are close, False otherwise.
        """
        if xor(
            ("error" in self.fields),
            ("error" in value.fields),
        ):
            warnings.warn(
                "One of the helix records has an error matrix, but the other does not. "
                "Ignoring error matrix for isclose check.",
                UserWarning,
            )

        multi_trk = isinstance(self.pivot.x, ak.Array)
        if multi_trk:
            return _arr_isclose(self, value, rtol=rtol, atol=atol, equal_nan=equal_nan)
        else:
            return _obj_isclose(self, value, rtol=rtol, atol=atol, equal_nan=equal_nan)


ak.behavior["Bes3Helix"] = HelixAwkwardRecord


###############################################################################################


class HelixAwkwardArray(ak.Array):
    @property
    def momentum(self) -> vec_ak.MomentumAwkward3D:
        """
        Returns the momentum of the helix as an awkward array of 3D vectors.

        Returns:
            vector.MomentumNumpy3D: The momentum vectors of the helix.
        """
        pt, phi, pz = _compute_momentum(self.kappa, self.tanl, self.phi0)
        return ak.zip({"pt": pt, "phi": phi, "pz": pz}, with_name="Momentum3D")

    @property
    def position(self) -> vec_ak.VectorAwkward3D:
        """
        Returns the position of the helix at a given azimuthal angle as an awkward array of 3D vectors.

        Returns:
            vector.VectorNumpy3D: The position vectors of the helix.
        """
        x, y, z = _compute_position(self.dr, self.phi0, self.dz)
        return ak.zip({"x": x, "y": y, "z": z}, with_name="Vector3D")

    @property
    def charge(self) -> ak.Array:
        """
        Returns the charge of the helix as an awkward array.

        Returns:
            ak.Array: The charge of the helix.
        """
        return kappa_to_charge(self.kappa)

    @property
    def radius(self) -> ak.Array:
        """
        Returns the radius of the helix as an awkward array.

        Returns:
            ak.Array: The radius of the helix in mm.
        """
        return kappa_to_radius(self.kappa)

    def change_pivot(self, *args) -> "HelixAwkwardArray":
        """
        Changes the pivot point of the helix.
        """
        if len(args) == 3:
            x, y, z = args
            pivot = None
        elif len(args) == 1:
            pivot = args[0]
            if isinstance(pivot, vector.VectorObject3D):
                x = pivot.x
                y = pivot.y
                z = pivot.z
                pivot = None
            elif not isinstance(pivot, ak.Array):
                x = pivot[0]
                y = pivot[1]
                z = pivot[2]
                pivot = None
        else:
            raise ValueError(
                "change_pivot requires either 3 arguments (x, y, z) or 1 argument (pivot)."
            )

        if pivot is None:
            x = ak.ones_like(self.dr) * x if not isinstance(x, ak.Array) else x
            y = ak.ones_like(self.dr) * y if not isinstance(y, ak.Array) else y
            z = ak.ones_like(self.dr) * z if not isinstance(z, ak.Array) else z
            pivot = ak.Array({"x": x, "y": y, "z": z}, with_name="Vector3D")

        raw_shape = _extract_index(self.dr.layout)

        r = _flat_to_numpy(self.radius)

        old_dr = _flat_to_numpy(self.dr)
        old_phi0 = _flat_to_numpy(self.phi0)
        old_dz = _flat_to_numpy(self.dz)
        tanl = _flat_to_numpy(self.tanl)
        kappa = _flat_to_numpy(self.kappa)

        old_pivot_x = _flat_to_numpy(self.pivot.x)
        old_pivot_y = _flat_to_numpy(self.pivot.y)
        old_pivot_z = _flat_to_numpy(self.pivot.z)
        old_pivot = vector.arr({"x": old_pivot_x, "y": old_pivot_y, "z": old_pivot_z})

        new_pivot_x = _flat_to_numpy(pivot.x)
        new_pivot_y = _flat_to_numpy(pivot.y)
        new_pivot_z = _flat_to_numpy(pivot.z)
        new_pivot = vector.arr({"x": new_pivot_x, "y": new_pivot_y, "z": new_pivot_z})

        old_error = (
            _flat_to_numpy(self.error).reshape(-1, 5, 5) if "error" in self.fields else None
        )

        new_dr, new_phi0, new_dz, new_error = _change_pivot(
            r=r,
            old_dr=old_dr,
            old_phi0=old_phi0,
            old_dz=old_dz,
            kappa=kappa,
            tanl=tanl,
            old_error=old_error,
            old_pivot=old_pivot,
            new_pivot=new_pivot,
        )

        res_dict = {
            "dr": new_dr,
            "phi0": new_phi0,
            "kappa": kappa,
            "tanl": tanl,
            "dz": new_dz,
            "pivot": ak.zip(
                {"x": new_pivot.x, "y": new_pivot.y, "z": new_pivot.z},
                with_name="Vector3D",
            ),
        }

        if new_error is not None:
            res_dict["error"] = new_error

        raw_shape = _extract_index(self.dr.layout)
        res = ak.Array(res_dict, with_name="Bes3Helix")

        for count in raw_shape:
            res = ak.unflatten(res, count)

        return res

    def isclose(
        self,
        other: "HelixAwkwardRecord",
        *,
        rtol: float = 1e-5,
        atol: float = 1e-8,
        equal_nan: bool = False,
    ) -> ak.Array:
        """
        Check if two helix records are close to each other.

        Args:
            other (HelixAwkwardRecord): The helix record to compare with.

        Returns:
            ak.Array: A boolean array indicating if the records are close.
        """
        if xor(
            ("error" in self.fields),
            ("error" in other.fields),
        ):
            warnings.warn(
                "One of the helix records has an error matrix, but the other does not. "
                "Ignoring error matrix for isclose check.",
                UserWarning,
            )

        return _arr_isclose(self, other, rtol=rtol, atol=atol, equal_nan=equal_nan)


ak.behavior["*", "Bes3Helix"] = HelixAwkwardArray

###############################################################################################


# case 1
@overload
def helix_awk(
    helix: ak.Array,
    error: Optional[ak.Array] = None,
    pivot: TypeAwkPosition = (0, 0, 0),
) -> HelixAwkwardArray: ...


# case 2
@overload
def helix_awk(
    *,
    dr: ak.Array,
    phi0: ak.Array,
    kappa: ak.Array,
    dz: ak.Array,
    tanl: ak.Array,
    error: Optional[ak.Array] = None,
    pivot: TypeAwkPosition = (0, 0, 0),
) -> HelixAwkwardArray: ...


# case 3
@overload
def helix_awk(
    *,
    momentum: ak.Array,
    position: ak.Array,
    charge: Union[Literal[-1, 1], ak.Array],
    error: Optional[ak.Array] = None,
    pivot: TypeAwkPosition = (0, 0, 0),
) -> HelixAwkwardArray: ...


@nb.vectorize(cache=True)
def _fix_dr_sign(dr: FloatLike, phi0: FloatLike, dist_phi: FloatLike) -> FloatLike:
    """
    Fix the sign of dr based on the azimuthal angle.

    Parameters:
        dr (float): The radial distance.
        phi0 (float): The azimuthal angle.
        dist_phi (float): The difference between the azimuthal angle and phi0.

    Returns:
        float: The corrected radial distance.
    """
    if not np.isclose(dist_phi % (2 * np.pi), phi0):
        return -dr
    return dr


def helix_awk(*args, **kwargs) -> HelixAwkwardArray:
    error = None
    pivot = (0, 0, 0)

    if len(args) > 0:
        helix = args[0]

        if len(args) > 1:
            error = args[1]
            if "error" in kwargs:
                raise ValueError("Cannot pass both helix and error as positional arguments.")

        if len(args) > 2:
            pivot = args[2]
            if "pivot" in kwargs:
                raise ValueError("Cannot pass both helix and pivot as positional arguments.")

        dr = helix[..., 0]
        phi0 = helix[..., 1]
        kappa = helix[..., 2]
        dz = helix[..., 3]
        tanl = helix[..., 4]

    elif "helix" in kwargs:
        helix = kwargs.pop("helix")

        dr = helix[..., 0]
        phi0 = helix[..., 1]
        kappa = helix[..., 2]
        dz = helix[..., 3]
        tanl = helix[..., 4]

    elif "dr" in kwargs:
        dr = kwargs.pop("dr")
        phi0 = kwargs.pop("phi0")
        kappa = kwargs.pop("kappa")
        dz = kwargs.pop("dz")
        tanl = kwargs.pop("tanl")

    else:
        momentum = kwargs.pop("momentum")
        position = kwargs.pop("position")
        charge = kwargs.pop("charge")

        pivot = kwargs.pop("pivot", (0, 0, 0))
        if not isinstance(pivot, ak.Array):
            pivot = _regularize_obj_position(pivot)

        # compute helix parameters
        kappa = charge / momentum.pt
        phi0 = (momentum.phi - np.pi / 2) % (2 * np.pi)

        dist = (position - pivot).to_2D()
        dr = _fix_dr_sign(dist.rho, phi0, dist.phi)

        dz = position.z - pivot.z
        tanl = momentum.pz / momentum.pt

    error = kwargs.pop("error", error)
    pivot = kwargs.pop("pivot", pivot)

    if not isinstance(pivot, ak.Array):
        pivot = _regularize_obj_position(pivot)

        x0 = ak.ones_like(dr) * pivot.x
        y0 = ak.ones_like(dr) * pivot.y
        z0 = ak.ones_like(dr) * pivot.z
        pivot = ak.zip({"x": x0, "y": y0, "z": z0}, with_name="Vector3D")

    res_dict = {
        "dr": dr,
        "phi0": phi0,
        "kappa": kappa,
        "dz": dz,
        "tanl": tanl,
        "pivot": pivot,
    }

    if error is not None:
        res_dict["error"] = error

    _check_kwargs_used_up(kwargs)

    raw_shape = _extract_index(dr.layout)
    return ak.zip(res_dict, depth_limit=len(raw_shape) + 1, with_name="Bes3Helix")
