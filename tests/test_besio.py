import struct

import awkward as ak
import numpy as np
import pytest
import uproot
import uproot_custom

import pybes3 as p3


def test_uproot_branches(test_data_dir):
    f_full = uproot.open(test_data_dir / "test_full_mc_evt_1.rtraw")
    assert len(f_full["Event/TMcEvent"].branches) == 6

    f_only_mc_particles = uproot.open(test_data_dir / "test_only_mc_particles.rtraw")
    assert len(f_only_mc_particles["Event/TMcEvent"].branches) == 6


@pytest.mark.parametrize("backend", ["cpp", "python", "detree"])
def test_mc_full(test_data_dir, backend):
    f_rtraw = uproot.open(test_data_dir / "test_full_mc_evt_1.rtraw")
    truth_arr = ak.from_parquet(test_data_dir / "test_full_mc_evt_1.rtraw.parquet")
    with uproot_custom.use_backend(backend):
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


def test_mrpc_rtraw(test_data_dir):
    f_rtraw = uproot.open(test_data_dir / "test_mrpc.rtraw")
    truth_arr = ak.from_parquet(test_data_dir / "test_mrpc.rtraw.parquet")
    arr = f_rtraw["Event"].arrays()
    assert len(arr) == 10
    assert ak.array_equal(arr, truth_arr, equal_nan=True)


def test_mrpc_dst(test_data_dir):
    f_dst = uproot.open(test_data_dir / "test_mrpc.dst")
    truth_arr = ak.from_parquet(test_data_dir / "test_mrpc.dst.parquet")
    arr = f_dst["Event"].arrays()
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


@pytest.mark.parametrize("backend", ["cpp", "python", "detree"])
def test_cgem_rec(test_data_dir, backend):
    f_dst = uproot.open(test_data_dir / "test_cgem.rec")
    truth_arr = ak.from_parquet(test_data_dir / "test_cgem.rec.parquet")
    with uproot_custom.use_backend(backend):
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


def test_raw_iterate_matches_arrays(test_data_dir):
    with p3.open_raw(test_data_dir / "test_raw_data.raw") as reader:
        full = reader.arrays()

        for step in (1, 3, 7, 5000):
            parts = list(reader.iterate(step_size=step))
            assert sum(len(p) for p in parts) == len(full)
            assert ak.array_equal(ak.concatenate(parts), full)

        filtered = list(reader.iterate(step_size=4, filter_name=["cgem", "mdc"]))
        assert filtered[0].fields == ["evt_header", "cgem", "mdc"]


def test_raw_iterate_report(test_data_dir):
    with p3.open_raw(test_data_dir / "test_raw_data.raw") as reader:
        report = [(start, stop) for start, stop, _ in reader.iterate(step_size=4, report=True)]
        assert report == [(0, 4), (4, 8), (8, 10)]

        report = [
            (start, stop)
            for start, stop, _ in reader.iterate(
                step_size=2,
                entry_start=3,
                entry_stop=8,
                report=True,
            )
        ]
        assert report == [(3, 5), (5, 7), (7, 8)]


def test_raw_iterate_ranges(test_data_dir):
    with p3.open_raw(test_data_dir / "test_raw_data.raw") as reader:
        full = reader.arrays()

        tail = list(reader.iterate(entry_start=4, step_size=3))
        assert ak.array_equal(ak.concatenate(tail), full[4:])

        head = list(reader.iterate(entry_stop=5, step_size=2))
        assert ak.array_equal(ak.concatenate(head), full[:5])

        assert list(reader.iterate(entry_start=10)) == []
        assert list(reader.iterate(entry_start=10, entry_stop=5)) == []
        assert len(reader.arrays(entry_stop=-1)) == len(full)

        with pytest.raises(ValueError):
            reader.iterate(step_size=0)
        with pytest.raises(ValueError):
            reader.arrays(entry_start=-1)


def test_raw_entry_byte_offsets(test_data_dir):
    with p3.open_raw(test_data_dir / "test_raw_data.raw") as reader:
        offsets = reader.entry_byte_offsets
        assert len(offsets) == reader.entries + 1
        assert offsets[-1] == reader._data_end
        assert list(offsets[:-1]) == sorted(offsets[:-1])


def test_raw_entry_index_is_lazy(test_data_dir):
    with p3.open_raw(test_data_dir / "test_raw_data.raw") as reader:
        assert reader.index_status == "missing"

        # starting at entry 0 needs no scan
        reader.arrays(entry_start=0, entry_stop=1)
        assert reader.index_status == "missing"

        # a partial read scans only up to the requested entry
        reader.arrays(entry_start=4, entry_stop=5)
        assert reader.index_status == "partial"

        reader.entry_byte_offsets
        assert reader.index_status == "complete"


def test_raw_closed_reader(test_data_dir):
    reader = p3.open_raw(test_data_dir / "test_raw_data.raw")
    assert not reader.closed

    reader.close()
    assert reader.closed

    with pytest.raises(ValueError):
        reader.arrays()
    with pytest.raises(ValueError):
        reader.entry_byte_offsets
    with pytest.raises(ValueError):
        reader.read_block(1)


def test_raw_read_block(test_data_dir):
    with p3.open_raw(test_data_dir / "test_raw_data.raw") as reader:
        whole = reader.read_block(-1)
        assert whole.dtype == np.uint32
        assert whole.size * 4 == reader._data_end - reader._data_start

        first = reader.read_block(1)
        assert 0 < first.size < whole.size
        assert np.array_equal(first, whole[: first.size])

        assert reader.read_block(0).size == 0


def test_raw_rejects_bad_entry_count(test_data_dir, tmp_path):
    data = bytearray((test_data_dir / "test_raw_data.raw").read_bytes())
    struct.pack_into("<I", data, len(data) - 40 + 16, 0xFFFFFFFF)

    path = tmp_path / "bad_entries.raw"
    path.write_bytes(data)

    with pytest.raises(RuntimeError, match="Invalid number of entries"):
        p3.open_raw(path)


def test_raw_recovers_after_failed_read(test_data_dir, tmp_path):
    with p3.open_raw(test_data_dir / "test_raw_data.raw") as reader:
        offsets = reader.entry_byte_offsets

    data = bytearray((test_data_dir / "test_raw_data.raw").read_bytes())
    struct.pack_into("<I", data, int(offsets[4]) + 4, 0x00FFFFFF)  # size of event 4

    path = tmp_path / "corrupt_event.raw"
    path.write_bytes(data)

    with p3.open_raw(path) as reader:
        expected = reader.arrays(entry_start=2, entry_stop=4)

        with pytest.raises(RuntimeError):
            reader.arrays(entry_start=2, entry_stop=5)

        # the failed read must not leave a stale cursor behind
        assert ak.array_equal(reader.arrays(entry_start=2, entry_stop=4), expected)


def test_concatenate_raw_workers(test_data_dir):
    files = [str(test_data_dir / "test_raw_data.raw")] * 3
    serial = p3.concatenate_raw(files)
    parallel = p3.concatenate_raw(files, workers=3)
    assert ak.array_equal(serial, parallel)

    sliced = p3.concatenate_raw(files, entry_start=5, entry_stop=23)
    assert ak.array_equal(sliced, serial[5:23])

    crossing = p3.concatenate_raw(files, entry_start=8, entry_stop=12)
    assert ak.array_equal(crossing, serial[8:12])

    assert len(p3.concatenate_raw(files, entry_start=30)) == 0

    with pytest.raises(ValueError):
        p3.concatenate_raw(files, workers=0)


def test_iterate_raw_boundaries(test_data_dir):
    files = [str(test_data_dir / "test_raw_data.raw")] * 3
    full = p3.concatenate_raw(files)

    parts = list(p3.iterate_raw(files, step_size=4))
    assert [len(p) for p in parts] == [4, 4, 2, 4, 4, 2, 4, 4, 2]
    assert ak.array_equal(ak.concatenate(parts), full)

    report = [
        (start, stop)
        for start, stop, _ in p3.iterate_raw(
            files,
            step_size=6,
            entry_start=7,
            entry_stop=24,
            report=True,
        )
    ]
    assert report[0][0] == 7
    assert report[-1][1] == 24
    for start, stop in report:
        assert start // 10 == (stop - 1) // 10


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v", "-s"])
