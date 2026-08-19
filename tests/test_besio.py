import awkward as ak
import pytest
import uproot

import pybes3 as p3


def test_uproot_branches(test_data_dir):
    f_full = uproot.open(test_data_dir / "test_full_mc_evt_1.rtraw")
    assert len(f_full["Event/TMcEvent"].branches) == 6

    f_only_mc_particles = uproot.open(test_data_dir / "test_only_mc_particles.rtraw")
    assert len(f_only_mc_particles["Event/TMcEvent"].branches) == 6


def test_mc_full(test_data_dir):
    f_rtraw = uproot.open(test_data_dir / "test_full_mc_evt_1.rtraw")
    truth_arr = ak.from_parquet(test_data_dir / "test_full_mc_evt_1.rtraw.parquet")
    arr = f_rtraw["Event"].arrays()
    assert len(arr) == 10
    assert ak.array_equal(arr, truth_arr, equal_nan=True)


def test_mc_only_particles(test_data_dir):
    f_rtraw = uproot.open(test_data_dir / "test_only_mc_particles.rtraw")
    truth_arr = ak.from_parquet(test_data_dir / "test_only_mc_particles.rtraw.parquet")
    arr = f_rtraw["Event"].arrays()
    assert len(arr) == 10
    assert ak.array_equal(arr, truth_arr, equal_nan=True)


def test_dst(test_data_dir):
    f_dst = uproot.open(test_data_dir / "test_full_mc_evt_1.dst")
    truth_arr = ak.from_parquet(test_data_dir / "test_full_mc_evt_1.dst.parquet")
    arr = f_dst["Event"].arrays()
    assert len(arr) == 10
    assert ak.array_equal(arr, truth_arr, equal_nan=True)


def test_rec(test_data_dir):
    f_rec = uproot.open(test_data_dir / "test_full_mc_evt_1.rec")
    truth_arr = ak.from_parquet(test_data_dir / "test_full_mc_evt_1.rec.parquet")
    arr = f_rec["Event"].arrays()
    assert len(arr) == 10
    assert ak.array_equal(arr, truth_arr, equal_nan=True)


def test_cgem_rtraw(test_data_dir):
    f_rtraw = uproot.open(test_data_dir / "test_cgem.rtraw")
    truth_arr = ak.from_parquet(test_data_dir / "test_cgem.rtraw.parquet")
    arr = f_rtraw["Event"].arrays()
    assert len(arr) == 10
    assert ak.array_equal(arr, truth_arr, equal_nan=True)


def test_cgem_dst(test_data_dir):
    f_dst = uproot.open(test_data_dir / "test_cgem.dst")
    truth_arr = ak.from_parquet(test_data_dir / "test_cgem.dst.parquet")
    arr = f_dst["Event"].arrays()
    assert len(arr) == 10
    assert ak.array_equal(arr, truth_arr, equal_nan=True)


def test_cgem_rec(test_data_dir):
    f_dst = uproot.open(test_data_dir / "test_cgem.rec")
    truth_arr = ak.from_parquet(test_data_dir / "test_cgem.rec.parquet")
    arr = f_dst["Event"].arrays()
    assert len(arr) == 10
    assert ak.array_equal(arr, truth_arr, equal_nan=True)


def test_uproot_concatenate(test_data_dir):
    arr_concat1 = uproot.concatenate(
        {
            test_data_dir / "test_full_mc_evt_1.rtraw": "Event",
            test_data_dir / "test_full_mc_evt_2.rtraw": "Event",
        }
    )
    assert len(arr_concat1) == 20

    arr_concat2 = uproot.concatenate(
        {
            test_data_dir / "test_full_mc_evt_1.rtraw": "Event/TMcEvent/m_mcParticleCol",
            test_data_dir / "test_full_mc_evt_2.rtraw": "Event/TMcEvent/m_mcParticleCol",
        }
    )
    assert len(arr_concat2) == 20


def test_symetric_matrix_expansion(test_data_dir):
    def test_symetric_matrix(arr):
        arr = ak.flatten(arr)
        n_dim = int(arr.typestr.split("*")[-2].strip())

        # Check if the matrix is square
        assert n_dim == int(arr.typestr.split("*")[-3].strip())

        for i in range(n_dim):
            for j in range(i, n_dim):
                assert ak.all(arr[:, i, j] == arr[:, j, i])

    f_dst = uproot.open(test_data_dir / "test_full_mc_evt_1.dst")
    arr_dst = f_dst["Event/TDstEvent"].arrays()

    f_rec = uproot.open(test_data_dir / "test_full_mc_evt_1.rec")
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


def test_bes3_tobjarray_factory_dask(test_data_dir):
    dask_arr = uproot.dask({test_data_dir / "test_full_mc_evt_1.rtraw": "Event/m_mdcDigiCol"})

    dask_arr.compute()


def test_symetric_matrix_expansion_dask(test_data_dir):
    dask_arr = uproot.dask(
        {test_data_dir / "test_full_mc_evt_1.dst": "Event/TDstEvent/m_mdcTrackCol"}
    )

    dask_arr.compute()


def test_digi_expand_TRawData(test_data_dir):
    f_rec = uproot.open(test_data_dir / "test_full_mc_evt_1.rec")
    arr_digi = f_rec["Event/TDigiEvent"].arrays()
    for field in arr_digi.fields:
        if field == "m_fromMc":
            continue

        assert "TRawData" not in arr_digi[field].fields


def test_raw_content(test_data_dir, subtests):
    f_ref = uproot.open(test_data_dir / "ref_raw_data.root")

    test_fields = ["cgem", "mdc", "tof", "emc", "muc", "trigGTD"]

    ref_arr_dict = {}
    for field in test_fields:
        cur_ref_arr = f_ref[field].arrays()
        cur_ref_arr = ak.zip({k: cur_ref_arr[k] for k in cur_ref_arr.fields if k != "index"})
        cur_ref_arr = ak.zip({k: cur_ref_arr[k] for k in cur_ref_arr.fields})
        ref_arr_dict[field] = cur_ref_arr

    f_raw = p3.open_raw(test_data_dir / "test_raw_data.raw")
    raw_arr = f_raw.arrays()

    assert len(raw_arr) == f_raw.entries

    for field in test_fields:
        with subtests.test(field=field):
            assert ak.array_equal(raw_arr[field], ref_arr_dict[field], equal_nan=True)


def test_RawBinaryParser(test_data_dir):
    f_test = test_data_dir / "test_raw_data.raw"
    raw_reader = p3.open_raw(f_test)

    arr = raw_reader.arrays()
    assert len(arr) == 10

    arr = raw_reader.arrays(entry_start=4)
    assert len(arr) == 6

    arr = raw_reader.arrays(entry_stop=4)
    assert len(arr) == 4

    arr = raw_reader.arrays(entry_start=5, entry_stop=10)
    assert len(arr) == 5

    arr = raw_reader.arrays(entry_start=9)
    assert len(arr) == 1

    arr = raw_reader.arrays(entry_start=0, entry_stop=0)
    assert len(arr) == 0

    arr = raw_reader.arrays(entry_start=10)
    assert len(arr) == 0

    arr = raw_reader.arrays(entry_start=10, entry_stop=5)
    assert len(arr) == 0

    raw_reader.close()


def test_RawBinaryParser_context(test_data_dir):
    f_test = test_data_dir / "test_raw_data.raw"

    with p3.open_raw(f_test) as f:
        arr = f.arrays()
        assert len(arr) == 10


def test_concatenate_raw(test_data_dir):
    f_test = test_data_dir / "test_raw_data.raw"
    files = [f_test, f_test, f_test]

    arr = p3.concatenate_raw(files)
    assert len(arr) == 30

    arr = p3.concatenate_raw(files, entry_start=5, entry_stop=23)
    assert len(arr) == 18

    arr = p3.concatenate_raw(files, entry_start=25)
    assert len(arr) == 5

    arr = p3.concatenate_raw(files, entry_stop=7)
    assert len(arr) == 7

    arr = p3.concatenate_raw(files, entry_start=10, entry_stop=21)
    assert len(arr) == 11

    arr = p3.concatenate_raw(files, entry_start=0, entry_stop=0)
    assert len(arr) == 0

    arr = p3.concatenate_raw(files, entry_start=15, entry_stop=15)
    assert len(arr) == 0

    arr = p3.concatenate_raw(files, entry_start=35)
    assert len(arr) == 0


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v", "-s"])
