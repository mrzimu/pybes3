from __future__ import annotations

import awkward as ak
import numpy as np

from pybes3.typing import BoolLike, IntLike


def particle_is_primary(status: IntLike) -> BoolLike:
    """
    Convert the MC particle status to whether the particle is a primary particle.

    It tests the `PRIMARY` bit (`1 << 2`) of the status flags of BOSS
    `Event::McParticle`, which the simulation sets for the particles whose production vertex
    has no parent track, i.e. the particles without a mother in the MC particle tree.

    Parameters:
        status: Status flags of the MC particle.

    Returns:
        Whether the particle is a primary particle.
    """
    return (status & 4) > 0  # 1 << 2


def particle_is_leaf(status: IntLike) -> BoolLike:
    """
    Convert the MC particle status to whether the particle is a leaf particle.

    It tests the `LEAF` bit (`1 << 3`) of the status flags of BOSS `Event::McParticle`,
    which the simulation sets for the tracks without daughter, i.e. the leaves of the MC
    particle tree.

    Parameters:
        status: Status flags of the MC particle.

    Returns:
        Whether the particle is a leaf of the MC particle tree.
    """
    return (status & 8) > 0  # 1 << 3


def particle_decay_from_generator(status: IntLike) -> BoolLike:
    """
    Convert the MC particle status to whether the particle comes from the generator.

    It tests the `DECAYED` bit (`1 << 0`) of the status flags of BOSS `Event::McParticle`
    (the bit reported by `McParticle::decayFromGenerator()`), which the simulation sets for
    the tracks whose source is `"FromGenerator"`, i.e. the particle comes from the event
    generator (including the decays it performs) and not from Geant4.

    Parameters:
        status: Status flags of the MC particle.

    Returns:
        Whether the particle comes from the generator.
    """
    return (status & 1) > 0


def particle_decay_in_flight(status: IntLike) -> BoolLike:
    """
    Convert the MC particle status to whether the particle was produced in flight by Geant4.

    It tests the `DECAYFLT` bit (`1 << 1`) of the status flags of BOSS `Event::McParticle`
    (the bit reported by `McParticle::decayInFlight()`), which the simulation sets for the
    tracks whose source is `"FromG4"`, i.e. the particle comes from a decay or an
    interaction simulated in flight by Geant4.

    Parameters:
        status: Status flags of the MC particle.

    Returns:
        Whether the particle was produced in flight by Geant4.
    """
    return (status & 2) > 0  # 1 << 1


def parse_particle_status(status: IntLike) -> ak.Array | dict[str, np.ndarray | bool]:
    """
    Parse the MC particle status flags into one boolean per flag.

    When `status` is an `ak.Array`, the result is an `ak.Array`, otherwise it is a `dict`.
    The bits tested are those of `Event::McParticle::StatusBits`: bit 0 `DECAYED`,
    bit 1 `DECAYFLT`, bit 2 `PRIMARY` and bit 3 `LEAF` (the `ERROR` bit is not exposed).

    Keys of the output:

    - `is_primary`: Whether the particle is a primary particle.
    - `is_leaf`: Whether the particle is a leaf of the MC particle tree.
    - `decay_from_generator`: Whether the particle comes from the generator.
    - `decay_in_flight`: Whether the particle was produced in flight by Geant4.

    Parameters:
        status: Status flags of the MC particle.

    Returns:
        The parsed flags.
    """
    res = {
        "is_primary": particle_is_primary(status),
        "is_leaf": particle_is_leaf(status),
        "decay_from_generator": particle_decay_from_generator(status),
        "decay_in_flight": particle_decay_in_flight(status),
    }

    if isinstance(status, ak.Array):
        return ak.zip(res)
    else:
        return res
