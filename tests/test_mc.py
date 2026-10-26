import awkward as ak
import numpy as np

import pybes3 as p3
from pybes3 import mc


def test_particle_status(particle_status_ref):
    ak_status: ak.Array = particle_status_ref["status"]
    ak_is_primary: ak.Array = particle_status_ref["is_primary"]
    ak_is_leaf: ak.Array = particle_status_ref["is_leaf"]
    ak_decay_from_generator: ak.Array = particle_status_ref["decay_from_generator"]
    ak_decay_in_flight: ak.Array = particle_status_ref["decay_in_flight"]

    assert ak.all(p3.particle_is_primary(ak_status) == ak_is_primary)
    assert ak.all(p3.particle_is_leaf(ak_status) == ak_is_leaf)
    assert ak.all(p3.particle_decay_from_generator(ak_status) == ak_decay_from_generator)
    assert ak.all(p3.particle_decay_in_flight(ak_status) == ak_decay_in_flight)

    np_status = ak.flatten(ak_status).to_numpy()
    np_is_primary = ak.flatten(ak_is_primary).to_numpy()
    np_is_leaf = ak.flatten(ak_is_leaf).to_numpy()
    np_decay_from_generator = ak.flatten(ak_decay_from_generator).to_numpy()
    np_decay_in_flight = ak.flatten(ak_decay_in_flight).to_numpy()
    for d in [
        np.int8,
        np.uint8,
        np.int16,
        np.uint16,
        np.int32,
        np.uint32,
        np.int64,
        np.uint64,
    ]:
        cur_status = np_status.astype(d)
        assert np.all(p3.particle_is_primary(cur_status) == np_is_primary)
        assert np.all(p3.particle_is_leaf(cur_status) == np_is_leaf)
        assert np.all(p3.particle_decay_from_generator(cur_status) == np_decay_from_generator)
        assert np.all(p3.particle_decay_in_flight(cur_status) == np_decay_in_flight)


def test_parse_particle_status(particle_status_ref):
    ak_status: ak.Array = particle_status_ref["status"]
    np_status = ak.flatten(ak_status).to_numpy()
    flags = ["is_primary", "is_leaf", "decay_from_generator", "decay_in_flight"]

    # Test awkward: an ak.Array of records, with one field per flag
    ak_res = mc.parse_particle_status(ak_status)
    assert ak_res.fields == flags
    for flag in flags:
        assert ak.all(ak_res[flag] == particle_status_ref[flag])

    # Test numpy: a dict, with one array per flag
    np_res = mc.parse_particle_status(np_status)
    assert list(np_res.keys()) == flags
    for flag in flags:
        np_flag = ak.flatten(particle_status_ref[flag]).to_numpy()
        assert np.all(np_res[flag] == np_flag)
