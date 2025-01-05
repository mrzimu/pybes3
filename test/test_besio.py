import awkward as ak
import numpy as np
import pytest
from pathlib import Path

TEST_DIR = Path(__file__).parent


def test_Bes3EventReader():
    from pybes.besio import Bes3EventReader

    # Test case 1: Multiple files
    reader1 = Bes3EventReader([str(TEST_DIR / '*.rtraw')])
    assert reader1.entries == 20
    assert reader1.available_fields == ['/Event/Digi/Emc',
                                        '/Event/Digi/FromMc',
                                        '/Event/Digi/Lumi',
                                        '/Event/Digi/Mdc',
                                        '/Event/Digi/Muc',
                                        '/Event/Digi/Tof',
                                        '/Event/Header',
                                        '/Event/Mc/Emc',
                                        '/Event/Mc/McParticle',
                                        '/Event/Mc/Mdc',
                                        '/Event/Mc/Muc',
                                        '/Event/Mc/Tof']
    ioevt1 = reader1.arrays()
    assert ioevt1.entries == 20
    assert set(ioevt1.files) == {str(TEST_DIR / 'test_besio1.rtraw'),
                                 str(TEST_DIR / 'test_besio2.rtraw')}
    assert ioevt1.available_subevents == ['header', 'mc', 'digi']

    # Test event header
    header_keys = ['runNo', 'evtNo', 'time', 'tag', 'flag1', 'flag2', 'etsT1', 'etsT2']
    for k in header_keys:
        v = ioevt1.header[k]
        assert isinstance(v, ak.Array)
        assert len(v) == 20

    # Test MC subevent
    assert ioevt1.mc.available_fields == ['mdc', 'emc', 'tof', 'muc', 'particle']
    for f in ioevt1.mc.available_fields:
        f_obj = getattr(ioevt1.mc, f)
        for k, v in f_obj.items():
            assert isinstance(v, ak.Array)
            assert len(v) == 20

    # Test Digi subevent
    assert ioevt1.digi.available_fields == ['mdc', 'emc', 'tof', 'muc', 'from_mc']
    for f in ioevt1.digi.available_fields:
        f_arr = getattr(ioevt1.digi, f)
        for k, v in f_arr.items():
            assert isinstance(v, ak.Array)
            assert len(v) == 20

    # Test other arrays method arguments
    ioevt2 = reader1.arrays(entry_start=1, entry_stop=5)
    assert ioevt2.entries == 4

    ioevt3 = reader1.arrays(fields=['/Event/Header', '/Event/Mc/Mdc', '/Event/Digi/Mdc'])
    assert ioevt3.available_subevents == ['header', 'mc', 'digi']
    assert list(ioevt3.header.keys()) == ['runNo', 'evtNo', 'time', 'tag', 'flag1', 'flag2', 'etsT1', 'etsT2']
    assert ioevt3.mc.available_fields == ['mdc']
    assert ioevt3.digi.available_fields == ['mdc']

    ioevt4 = reader1.arrays(return_dict=True)
    assert isinstance(ioevt4, dict)

    # Test case 2: Single files
    reader2 = Bes3EventReader(str(TEST_DIR / 'test_besio1.rtraw'))
    reader3 = Bes3EventReader(TEST_DIR / 'test_besio1.rtraw')

    for r in [reader2, reader3]:
        assert r.entries == 10
        assert r.available_fields == ['/Event/Digi/Emc',
                                      '/Event/Digi/FromMc',
                                      '/Event/Digi/Lumi',
                                      '/Event/Digi/Mdc',
                                      '/Event/Digi/Muc',
                                      '/Event/Digi/Tof',
                                      '/Event/Header',
                                      '/Event/Mc/Emc',
                                      '/Event/Mc/McParticle',
                                      '/Event/Mc/Mdc',
                                      '/Event/Mc/Muc',
                                      '/Event/Mc/Tof']
        assert r.files == [str(TEST_DIR / 'test_besio1.rtraw')]


def test_get_sim_matrix_idx():
    from pybes.besio.IOEvent import get_sim_matrix_idx
    # Test case 1: Single indices
    i = 0
    j = 0
    ndim = 3
    expected_result = 0
    assert get_sim_matrix_idx(i, j, ndim) == expected_result

    # Test case 2: Single indices with different types
    i = 1
    j = np.array([0, 1, 2])
    ndim = 3
    expected_result = np.array([1, 2, 4])
    assert np.array_equal(get_sim_matrix_idx(i, j, ndim), expected_result)

    # Test case 3: Array indices
    i = ak.Array([[0, 1], [0, 1, 2]])
    j = ak.Array([[1, 0], [1, 1, 1]])
    ndim = 3
    expected_result = ak.Array([[1, 1], [1, 2, 4]])
    assert ak.all(get_sim_matrix_idx(i, j, ndim) == expected_result)

    # Test case 4: Array indices with different types, expected ValueError
    i = np.array([0, 1, 2])
    j = ak.Array([0, 1, 0])
    ndim = 3
    with pytest.raises(ValueError):
        get_sim_matrix_idx(i, j, ndim)
