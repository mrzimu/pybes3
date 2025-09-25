from pathlib import Path
from typing import Literal, NamedTuple, Optional

import awkward as ak
import numpy as np
import pytest
import uproot

import pybes3
import pybes3.besio as besio

besio.wrap_uproot()

data_dir = Path(__file__).parent / "data"


class CompareResult(NamedTuple):
    item: str
    is_same: bool
    arr_dtype: Optional[str] = None
    diff_type: Optional[Literal["type mismatch", "length mismatch", "value unequal"]] = None


def compare_ak(arr1: ak.Array, arr2: ak.Array, item_path: str = "") -> list[CompareResult]:
    """
    Compare two awkward arrays and return a list of CompareResult.

    Args:
        arr1 (ak.Array): First array to compare.
        arr2 (ak.Array): Second array to compare.
        item_path (str): Path to the item being compared.

    Returns:
        list[CompareResult]: List of CompareResult objects containing comparison results.
    """
    if arr1.typestr != arr2.typestr:
        return [
            CompareResult(
                item=item_path,
                is_same=False,
                arr_dtype=arr1.typestr,
                diff_type="type mismatch",
            )
        ]

    # Record array
    if arr1.fields:
        res = []
        for field in arr1.fields:
            tmp_res = compare_ak(arr1[field], arr2[field], item_path=f"{item_path}/{field}")

            if (
                len(tmp_res) == 1
                and tmp_res[0].arr_dtype != "ak.Record"
                and tmp_res[0].diff_type == "length mismatch"
            ):
                return [
                    CompareResult(
                        item=item_path + "/*",
                        is_same=False,
                        arr_dtype="ak.Record",
                        diff_type="length mismatch",
                    )
                ]

            else:
                res += tmp_res
        return res

    # Get array dtype
    arr_dtype = arr1.typestr.split("*")[-1].strip()

    try:
        if "float" in arr_dtype and ak.all(np.isclose(arr1, arr2, equal_nan=True)):
            return [
                CompareResult(
                    item=item_path,
                    is_same=True,
                    arr_dtype=arr_dtype,
                )
            ]
        elif ak.all(arr1 == arr2):
            return [
                CompareResult(
                    item=item_path,
                    is_same=True,
                    arr_dtype=arr_dtype,
                )
            ]

        # Value non-equal
        else:
            return [
                CompareResult(
                    item=item_path,
                    is_same=False,
                    diff_type="value unequal",
                    arr_dtype=arr_dtype,
                )
            ]

    # Length mismatch
    except ValueError as e:
        if ak.any(ak.count(arr1, axis=1) != ak.count(arr2, axis=1)):
            return [
                CompareResult(
                    item=item_path,
                    is_same=False,
                    arr_dtype=arr_dtype,
                    diff_type="length mismatch",
                )
            ]
        else:
            print(arr1.typestr)
            print(ak.count(arr1), ak.count(arr2))
            raise e


def test_uproot_branches():
    f_full = uproot.open(data_dir / "test_full_mc_evt_1.rtraw")
    assert len(f_full["Event/TMcEvent"].branches) == 6

    f_only_mc_particles = uproot.open(data_dir / "test_only_mc_particles.rtraw")
    assert len(f_only_mc_particles["Event/TMcEvent"].branches) == 6


def test_mc_full():
    f_rtraw = uproot.open(data_dir / "test_full_mc_evt_1.rtraw")
    truth_arr = ak.from_parquet(data_dir / "test_full_mc_evt_1.rtraw.parquet")
    arr = f_rtraw["Event"].arrays()
    assert len(arr) == 10
    comp_res = compare_ak(arr, truth_arr)
    assert all(r.is_same for r in comp_res)


def test_mc_only_particles():
    f_rtraw = uproot.open(data_dir / "test_only_mc_particles.rtraw")
    truth_arr = ak.from_parquet(data_dir / "test_only_mc_particles.rtraw.parquet")
    arr = f_rtraw["Event"].arrays()
    assert len(arr) == 10
    comp_res = compare_ak(arr, truth_arr)
    assert all(r.is_same for r in comp_res)


def test_dst():
    f_dst = uproot.open(data_dir / "test_full_mc_evt_1.dst")
    truth_arr = ak.from_parquet(data_dir / "test_full_mc_evt_1.dst.parquet")
    arr = f_dst["Event"].arrays()
    assert len(arr) == 10
    comp_res = compare_ak(arr, truth_arr)
    assert all(r.is_same for r in comp_res)


def test_rec():
    f_rec = uproot.open(data_dir / "test_full_mc_evt_1.rec")
    truth_arr = ak.from_parquet(data_dir / "test_full_mc_evt_1.rec.parquet")
    arr = f_rec["Event"].arrays()
    assert len(arr) == 10
    comp_res = compare_ak(arr, truth_arr)
    assert all(r.is_same for r in comp_res)


def test_cgem_rtraw():
    f_rtraw = uproot.open(data_dir / "test_cgem.rtraw")
    truth_arr = ak.from_parquet(data_dir / "test_cgem.rtraw.parquet")
    arr = f_rtraw["Event"].arrays()
    assert len(arr) == 10
    comp_res = compare_ak(arr, truth_arr)
    assert all(r.is_same for r in comp_res)


def test_cgem_dst():
    f_dst = uproot.open(data_dir / "test_cgem.dst")
    truth_arr = ak.from_parquet(data_dir / "test_cgem.dst.parquet")
    arr = f_dst["Event"].arrays()
    assert len(arr) == 10
    comp_res = compare_ak(arr, truth_arr)
    assert all(r.is_same for r in comp_res)


def test_cgem_rec():
    f_dst = uproot.open(data_dir / "test_cgem.rec")
    truth_arr = ak.from_parquet(data_dir / "test_cgem.rec.parquet")
    arr = f_dst["Event"].arrays()
    assert len(arr) == 10
    comp_res = compare_ak(arr, truth_arr)
    assert all(r.is_same for r in comp_res)


def test_uproot_concatenate():
    arr_concat1 = uproot.concatenate(
        {
            data_dir / "test_full_mc_evt_1.rtraw": "Event",
            data_dir / "test_full_mc_evt_2.rtraw": "Event",
        }
    )
    assert len(arr_concat1) == 20

    arr_concat2 = uproot.concatenate(
        {
            data_dir / "test_full_mc_evt_1.rtraw": "Event/TMcEvent/m_mcParticleCol",
            data_dir / "test_full_mc_evt_2.rtraw": "Event/TMcEvent/m_mcParticleCol",
        }
    )
    assert len(arr_concat2) == 20


def test_bes_open():
    f = besio.open(data_dir / "test_full_mc_evt_1.rtraw")
    assert len(f["Event/TMcEvent"].branches) == 6

    f = besio.open(data_dir / "test_only_mc_particles.rtraw")
    assert len(f["Event/TMcEvent"].branches) == 6


def test_bes_concatenate():
    arr_concat1 = besio.concatenate(
        [data_dir / "test_full_mc_evt_1.rtraw", data_dir / "test_full_mc_evt_2.rtraw"],
        "Event/TMcEvent",
    )
    assert len(arr_concat1) == 20

    arr_concat2 = besio.concatenate(
        [data_dir / "test_full_mc_evt_1.rtraw", data_dir / "test_full_mc_evt_2.rtraw"],
        "Event/TMcEvent/m_mcParticleCol",
    )
    assert len(arr_concat2) == 20


def test_symetric_matrix_expansion():
    def test_symetric_matrix(arr):
        arr = ak.flatten(arr)
        n_dim = int(arr.typestr.split("*")[-2].strip())

        # Check if the matrix is square
        assert n_dim == int(arr.typestr.split("*")[-3].strip())

        for i in range(n_dim):
            for j in range(i, n_dim):
                assert ak.all(arr[:, i, j] == arr[:, j, i])

    f_dst = uproot.open(data_dir / "test_full_mc_evt_1.dst")
    arr_dst = f_dst["Event/TDstEvent"].arrays()

    f_rec = uproot.open(data_dir / "test_full_mc_evt_1.rec")
    arr_rec = f_rec["Event/TRecEvent"].arrays()

    for tmp_arr in [
        arr_dst.m_mdcTrackCol.m_err,
        arr_dst.m_emcTrackCol.m_err,
        arr_dst.m_extTrackCol.myEmcErrorMatrix,
        arr_dst.m_extTrackCol.myMucErrorMatrix,
        arr_dst.m_extTrackCol.myTof1ErrorMatrix,
        arr_dst.m_extTrackCol.myTof2ErrorMatrix,
        arr_rec.m_recMdcTrackCol.m_err,
        arr_rec.m_recEmcShowerCol.m_err,
        arr_rec.m_recMdcKalTrackCol.m_terror,
    ]:
        test_symetric_matrix(tmp_arr)


def test_digi_expand_TRawData():
    f_rec = uproot.open(data_dir / "test_full_mc_evt_1.rec")
    arr_digi = f_rec["Event/TDigiEvent"].arrays()
    for field in arr_digi.fields:
        if field == "m_fromMc":
            continue

        assert "TRawData" not in arr_digi[field].fields


@pytest.mark.skipif(
    not Path(
        "/bes3fs/offline/data/raw/round17/231117/run_0079017_All_file001_SFO-1.raw"
    ).exists(),
    reason="Test data is not available",
)
def test_raw():
    f_raw: pybes3.besio.RawBinaryReader = pybes3.open_raw(
        "/bes3fs/offline/data/raw/round17/231117/run_0079017_All_file001_SFO-1.raw"
    )

    n_mdc_digis = ak.Array([1872, 2768, 1641, 2542, 3331, 2672, 2257, 2470, 3635, 3689])

    arr_full = f_raw.arrays(n_blocks=10)
    assert set(arr_full.fields) == {"evt_header", "mdc", "tof", "emc", "muc"}
    assert ak.all(ak.count(arr_full.mdc.id, axis=1) == n_mdc_digis)

    arr_mdc = f_raw.arrays(n_blocks=10, sub_detectors=["mdc"])
    assert set(arr_mdc.fields) == {"evt_header", "mdc"}
    assert ak.all(ak.count(arr_mdc.mdc.id, axis=1) == n_mdc_digis)

    arr_batch = f_raw.arrays(n_blocks=10, n_block_per_batch=5)
    assert set(arr_batch.fields) == {"evt_header", "mdc", "tof", "emc", "muc"}
    assert ak.all(ak.count(arr_batch.mdc.id, axis=1) == n_mdc_digis)

    arr_workers = f_raw.arrays(n_blocks=10, max_workers=4)
    assert set(arr_workers.fields) == {"evt_header", "mdc", "tof", "emc", "muc"}
    assert ak.all(ak.count(arr_workers.mdc.id, axis=1) == n_mdc_digis)


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v", "-s"])
