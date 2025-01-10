from typing import Union

import awkward as ak
import numpy as np

from .helix import _regularize_helix_array, helix_to_momentum, helix_to_position


class MdcTrackCol:
    def __init__(self, mdc_trks: ak.Array):

        self.trackId: ak.Array = mdc_trks["m_trackId"]
        self.n_trks = np.array(ak.count(mdc_trks["m_trackId"], axis=1))
        self.helix = _regularize_helix_array(mdc_trks["m_helix"], self.n_trks)
        self.err: ak.Array = mdc_trks["m_err"]
        self.stat: ak.Array = mdc_trks["m_stat"]
        self.chi2: ak.Array = mdc_trks["m_chi2"]
        self.ndof: ak.Array = mdc_trks["m_ndof"]
        self.nster: ak.Array = mdc_trks["m_nster"]
        self.nlayer: ak.Array = mdc_trks["m_nlayer"]
        self.firstLayer: ak.Array = mdc_trks["m_firstLayer"]
        self.lastLayer: ak.Array = mdc_trks["m_lastLayer"]

        self.position = helix_to_position(self.helix, self.n_trks)
        self.momentum = helix_to_momentum(self.helix, self.n_trks)

        self._pt: Union[ak.Array, None] = None
        self._pz: Union[ak.Array, None] = None
        self._phi: Union[ak.Array, None] = None
        self._theta: Union[ak.Array, None] = None
        self._costheta: Union[ak.Array, None] = None
        self._p: Union[ak.Array, None] = None

    def __repr__(self) -> str:
        n_evt = len(self.n_trks)
        tot_trks = np.sum(self.n_trks)
        return f"<MdcTrackCol: {n_evt} events, {tot_trks} tracks>"

    @property
    def pt(self) -> ak.Array:
        if self._pt is None:
            self._pt = np.abs(self.momentum["pt"])
        return self._pt

    @property
    def pz(self) -> ak.Array:
        if self._pz is None:
            self._pz = self.momentum["pz"]
        return self._pz

    @property
    def phi(self) -> ak.Array:
        if self._phi is None:
            self._phi = self.momentum["phi"]
        return self._phi

    @property
    def theta(self) -> ak.Array:
        if self._theta is None:
            self._theta = self.momentum["theta"]
        return self._theta

    @property
    def costheta(self) -> ak.Array:
        if self._costheta is None:
            self._costheta = np.cos(self.theta)
        return self._costheta

    @property
    def p(self) -> ak.Array:
        if self._p is None:
            self._p = np.abs(self.momentum["p"])
        return self._p
