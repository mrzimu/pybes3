from pathlib import Path

import awkward as ak
import numpy as np
import pytest
import vector

import pybes3 as p3

data_dir = Path(__file__).parent.parent / "data"
mdc_trk = p3.open(data_dir / "test_full_mc_evt_1.dst")["Event/TDstEvent/m_mdcTrackCol"].array()

raw_helix_arr = mdc_trk["m_helix"]
raw_helix_err_arr = mdc_trk["m_err"]

flat_helix_arr = ak.flatten(raw_helix_arr)
flat_helix_err_arr = ak.flatten(raw_helix_err_arr)


def _make_arr_pivot(base_arr, x, y, z):
    x = ak.flatten(ak.ones_like(base_arr) * x, axis=None)
    y = ak.flatten(ak.ones_like(base_arr) * y, axis=None)
    z = ak.flatten(ak.ones_like(base_arr) * z, axis=None)


@pytest.mark.parametrize("error", [None, flat_helix_err_arr])
def test_helix_obj_1(error):
    """Test initialization, momentum, position, charge, and pivot of helix_obj."""
    raw_pivot = (0, 0, 0)

    for i in range(len(flat_helix_arr)):
        dr, phi0, kappa, dz, tanl = flat_helix_arr[i]
        np_error = error[i].to_numpy() if error is not None else None

        # case 1
        h1 = p3.helix_obj(
            dr,
            phi0,
            kappa,
            dz,
            tanl,
            error=np_error,
            pivot=raw_pivot,
        )

        # case 2
        h2 = p3.helix_obj(
            params=(dr, phi0, kappa, dz, tanl),
            error=np_error,
            pivot=raw_pivot,
        )

        momentum = h1.momentum
        position = h1.position

        # case 3-1: momentum and position are both vector
        h3_1 = p3.helix_obj(
            momentum=momentum,
            position=position,
            charge=h1.charge,
            error=np_error,
            pivot=raw_pivot,
        )

        # case 3-2: momentum as tuple, position as vector
        h3_2 = p3.helix_obj(
            momentum=(momentum.px, momentum.py, momentum.pz),
            position=position,
            charge=h1.charge,
            error=np_error,
            pivot=raw_pivot,
        )

        # case 3-3: momentum as vector, position as tuple
        h3_3 = p3.helix_obj(
            momentum=momentum,
            position=(position.x, position.y, position.z),
            charge=h1.charge,
            error=np_error,
            pivot=raw_pivot,
        )

        # case 3-4: momentum and position as tuple
        h3_4 = p3.helix_obj(
            momentum=(momentum.px, momentum.py, momentum.pz),
            position=(position.x, position.y, position.z),
            charge=h1.charge,
            error=np_error,
            pivot=raw_pivot,
        )

        for h in [h1, h2, h3_1, h3_2, h3_3, h3_4]:
            assert h.dr == pytest.approx(dr, rel=1e-6)
            assert h.phi0 == pytest.approx(phi0, rel=1e-6)
            assert h.kappa == pytest.approx(kappa, rel=1e-6)
            assert h.dz == pytest.approx(dz, rel=1e-6)
            assert h.tanl == pytest.approx(tanl, rel=1e-6)
            assert h.pivot.x == raw_pivot[0]
            assert h.pivot.y == raw_pivot[1]
            assert h.pivot.z == raw_pivot[2]

            if error is not None:
                assert h.error is not None
                assert np.all(h.error == np_error)
            else:
                assert h.error is None


def test_helix_obj_2():
    """Test change_pivot and isclose methods of helix_obj."""
    new_pivots = [
        (10, 10, 10),
        (10, -10, 10),
        (-10, -10, 10),
        (-10, 10, 10),
        (10, 10, 10),  # --- z > 0 / z < 0 ---
        (10, 10, -10),
        (10, -10, -10),
        (-10, -10, -10),
        (-10, 10, -10),
    ]

    for i in range(len(flat_helix_arr)):
        dr, phi0, kappa, dz, tanl = flat_helix_arr[i]
        helix_err = flat_helix_err_arr[i].to_numpy()

        h1_raw = p3.helix_obj(params=(dr, phi0, kappa, dz, tanl), error=helix_err)
        h2_raw = p3.helix_obj(params=(dr, phi0, kappa, dz, tanl), error=helix_err)
        h3_raw = p3.helix_obj(params=(dr, phi0, kappa, dz, tanl))
        h4_raw = p3.helix_obj(params=(dr, phi0, kappa, dz, tanl))

        h1 = h1_raw
        h2 = h2_raw
        h3 = h3_raw
        h4 = h4_raw

        for new_pivot in new_pivots:
            h1 = h1.change_pivot(*new_pivot)
            h2 = h2.change_pivot(*new_pivot)

            vec_new_pivot = vector.obj(x=new_pivot[0], y=new_pivot[1], z=new_pivot[2])
            h3 = h3.change_pivot(vec_new_pivot)
            h4 = h4.change_pivot(vec_new_pivot)

        # changed pivot, should be still close because of the automatic transformation
        assert h1.isclose(h1_raw)
        assert h2.isclose(h2_raw)
        assert h3.isclose(h3_raw)
        assert h4.isclose(h4_raw)

        # check strict criteria
        assert not h1.isclose(h1_raw, rtol=0, atol=0)

    # test with-error and no-error helix comparison
    with pytest.warns(UserWarning, match="Ignoring error matrix for isclose check."):
        h1_raw.isclose(h3_raw)


@pytest.mark.parametrize(
    "init_pivot",
    [
        (0, 0, 0),
        vector.obj(x=0, y=0, z=0),
        vector.obj(rho=0, phi=0, z=0),
    ],
)
@pytest.mark.parametrize(
    "raw_pivot",
    [
        (0, 0, 0),
        (vector.obj(x=0, y=0, z=0),),
    ],
)
@pytest.mark.parametrize(
    "new_pivot",
    [
        (10, 10, 10),
        (vector.obj(x=10, y=10, z=10),),
    ],
)
def test_helix_obj_3(init_pivot, raw_pivot, new_pivot):
    """Test different pivot arguments."""
    for i in range(len(flat_helix_arr)):
        h1 = p3.helix_obj(params=flat_helix_arr[i].tolist(), pivot=init_pivot)
        assert h1.change_pivot(*new_pivot).change_pivot(*raw_pivot).isclose(h1)


def test_helix_awk_1():
    """Test helix_awk, change_pivot, and isclose methods."""
    raw_pivot = ak.zip(
        {
            "x": ak.zeros_like(raw_helix_arr[..., 0]),
            "y": ak.zeros_like(raw_helix_arr[..., 0]),
            "z": ak.zeros_like(raw_helix_arr[..., 0]),
        },
        with_name="Vector3D",
    )

    new_pivot = ak.zip(
        {
            "x": ak.ones_like(raw_helix_arr[..., 0]) * 10,
            "y": ak.ones_like(raw_helix_arr[..., 0]) * 10,
            "z": ak.ones_like(raw_helix_arr[..., 0]) * 10,
        },
        with_name="Vector3D",
    )

    # directly constructing the helix array
    h0 = ak.Array(
        {
            "dr": raw_helix_arr[..., 0],
            "phi0": raw_helix_arr[..., 1],
            "kappa": raw_helix_arr[..., 2],
            "dz": raw_helix_arr[..., 3],
            "tanl": raw_helix_arr[..., 4],
            "pivot": raw_pivot,
            "error": raw_helix_err_arr,
        },
        with_name="Bes3Helix",
    )

    assert ak.all(h0.change_pivot(new_pivot).change_pivot(raw_pivot).isclose(h0))

    # test helix_awk and change_pivot

    # case 1-1: positional helix and error arguments
    h1_1 = p3.helix_awk(raw_helix_arr, raw_helix_err_arr)
    assert ak.all(h0.isclose(h1_1))
    assert ak.all(h1_1.change_pivot(new_pivot).change_pivot(raw_pivot).isclose(h1_1))

    # case 1-2: keyword arguments helix, error
    h1_2 = p3.helix_awk(helix=raw_helix_arr, error=raw_helix_err_arr)
    assert ak.all(h0.isclose(h1_2))

    # case 2: keyword arguments dr, phi0, kappa, dz, tanl
    h2 = p3.helix_awk(
        dr=raw_helix_arr[..., 0],
        phi0=raw_helix_arr[..., 1],
        kappa=raw_helix_arr[..., 2],
        dz=raw_helix_arr[..., 3],
        tanl=raw_helix_arr[..., 4],
        error=raw_helix_err_arr,
    )
    assert ak.all(h0.isclose(h2))

    # case 3: keyword arguments momentum, position, charge
    momentum = h0.momentum
    position = h0.position
    charge = h0.charge
    h3 = p3.helix_awk(
        momentum=momentum,
        position=position,
        charge=charge,
        error=raw_helix_err_arr,
    )
    assert ak.all(h0.isclose(h3))

    # test isclose method, no-error and with-error helix comparison
    h4 = p3.helix_awk(raw_helix_arr)
    with pytest.warns(UserWarning, match="Ignoring error matrix for isclose check."):
        assert ak.all(h1_1.isclose(h4))

    # check strict criteria
    assert not ak.all(
        h0.change_pivot(new_pivot).change_pivot(raw_pivot).isclose(h0, atol=0, rtol=0)
    )

    # changed pivot
    h4 = p3.helix_awk(helix=raw_helix_arr, error=raw_helix_err_arr).change_pivot(new_pivot)
    assert ak.all(h4.isclose(h0))

    # different pivot arguments
    assert ak.all(h0.change_pivot(new_pivot).change_pivot(0, 0, 0).isclose(h0))


@pytest.mark.parametrize(
    "init_pivot",
    [
        ak.zip(
            {
                "x": ak.zeros_like(raw_helix_arr[..., 0]),
                "y": ak.zeros_like(raw_helix_arr[..., 0]),
                "z": ak.zeros_like(raw_helix_arr[..., 0]),
            },
            with_name="Vector3D",
        ),
        (0, 0, 0),
    ],
)
@pytest.mark.parametrize(
    "raw_pivot",
    [
        (
            ak.zip(
                {
                    "x": ak.zeros_like(raw_helix_arr[..., 0]),
                    "y": ak.zeros_like(raw_helix_arr[..., 0]),
                    "z": ak.zeros_like(raw_helix_arr[..., 0]),
                },
                with_name="Vector3D",
            ),
        ),
        (0, 0, 0),
    ],
)
@pytest.mark.parametrize(
    "new_pivot",
    [
        (
            ak.zip(
                {
                    "x": ak.ones_like(raw_helix_arr[..., 0]) * 10,
                    "y": ak.ones_like(raw_helix_arr[..., 0]) * 10,
                    "z": ak.ones_like(raw_helix_arr[..., 0]) * 10,
                },
                with_name="Vector3D",
            ),
        ),
        (10, 10, 10),
    ],
)
def test_helix_awk_2(init_pivot, raw_pivot, new_pivot):
    """Test helix_awk with different pivot arguments."""
    h = p3.helix_awk(
        helix=raw_helix_arr,
        error=raw_helix_err_arr,
        pivot=init_pivot,
    )
    assert ak.all(h.change_pivot(*new_pivot).change_pivot(*raw_pivot).isclose(h))


@pytest.mark.parametrize(
    "new_pivot",
    [
        (10, 10, 10),
        (vector.obj(x=10, y=10, z=10),),
    ],
)
def test_HelixAwkwardRecord_1(new_pivot):
    """Test HelixAwkwardRecord class with 1 track."""
    helix_arr = p3.helix_awk(helix=raw_helix_arr, error=raw_helix_err_arr)
    helix_rec = helix_arr[0, 0]
    helix_obj = p3.helix_obj(
        dr=helix_rec.dr,
        phi0=helix_rec.phi0,
        kappa=helix_rec.kappa,
        dz=helix_rec.dz,
        tanl=helix_rec.tanl,
        pivot=(helix_rec.pivot.x, helix_rec.pivot.y, helix_rec.pivot.z),
        error=helix_rec.error,
    )

    # test isclose
    assert helix_rec.change_pivot(*new_pivot).change_pivot(0, 0, 0).isclose(helix_rec)
    assert helix_rec.change_pivot(*new_pivot).isclose(helix_rec)

    # test attributes
    assert isinstance(helix_rec.position, ak.Record)
    assert isinstance(helix_rec.momentum, ak.Record)
    assert helix_rec.position.isclose(helix_obj.position)
    assert helix_rec.momentum.isclose(helix_obj.momentum)
    assert helix_rec.charge == helix_obj.charge
    assert helix_rec.radius == pytest.approx(helix_obj.radius, rel=1e-6)


@pytest.mark.parametrize(
    "new_pivot",
    [
        (10, 10, 10),
        (vector.obj(x=10, y=10, z=10),),
    ],
)
def test_helix_awk_3(new_pivot):
    """Test HelixAwkwardArray slices."""

    helix_arr = p3.helix_awk(helix=raw_helix_arr, error=raw_helix_err_arr)
    helix_rec = helix_arr[0]

    # test isclose
    assert ak.all(helix_rec.change_pivot(*new_pivot).change_pivot(0, 0, 0).isclose(helix_rec))
    assert ak.all(helix_rec.change_pivot(*new_pivot).isclose(helix_rec))

    # test attributes
    assert isinstance(helix_rec.position, ak.Array)
    assert isinstance(helix_rec.momentum, ak.Array)
    assert ak.all(helix_rec.position.isclose(helix_arr.position[0]))
    assert ak.all(helix_rec.momentum.isclose(helix_arr.momentum[0]))
    assert ak.all(helix_rec.charge == helix_arr.charge[0])
    assert ak.all(np.isclose(helix_rec.radius, helix_arr.radius[0]))


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
