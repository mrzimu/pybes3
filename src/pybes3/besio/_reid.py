"""
REID (Raw Electronics ID) to TEID (digi_id) conversion tables.

In raw binary data, each sub-detector hit uses a hardware-specific electronics ID (REID).
This module provides lookup tables to convert REIDs to the standard detector geometry IDs
(TEIDs, i.e. digi_ids) used by `pybes3.detectors.digi_id`.

The conversion logic is ported from the BOSS offline software:
    Event/RawDataCnv/src/EventManagement/{Mdc,Tof,Emc,Muc}Builder.cxx

References:
    - RawDataCnvConf.conf for MDC/TOF/EMC bit-field definitions
    - MucFec2Id.map for MUC FEC-to-ID mapping
"""

from __future__ import annotations

from functools import lru_cache

import numpy as np

# ============================================================================
# Constants from BesDetectorID / Identifier classes
# ============================================================================

# --- MDC ---
_MDC_ID = np.uint32(0x10)
_MDC_INDEX = 24
_MDC_WIRETYPE_INDEX = 15
_MDC_LAYER_INDEX = 9
_MDC_WIRE_INDEX = 0
_MDC_INNER_STEREO_LAYER_MAX = 8  # layers 0-7
_MDC_INNER_AXIAL_LAYER_MAX = 12  # layers 8-19
_MDC_OUTER_STEREO_LAYER_MAX = 16  # layers 20-35
# layers 36-42 are outer axial
_MDC_STEREO_WIRE = np.uint32(1)
_MDC_AXIAL_WIRE = np.uint32(0)
_MDC_TE_LAYER_MAX = 42  # 0..42 total 43 layers
_MDC_AXIAL_WIRE_MAX = 287

# --- TOF ---
_TOF_ID = np.uint32(0x20)
_TOF_INDEX = 24
_TOF_BARREL_EC_INDEX = 14
_TOF_LAYER_INDEX = 8
_TOF_PHI_INDEX = 1
_TOF_END_INDEX = 0
_TOF_BARREL_EC_MIN = 0
_TOF_BARREL_EC_MAX = 2
_TOF_LAYER_BARREL_MAX = 1
_TOF_PHI_BARREL_MAX = 87
_TOF_LAYER_ENDCAP_MAX = 0
_TOF_PHI_ENDCAP_MAX = 48  # for luminosity; normally 47

# --- EMC ---
_EMC_ID = np.uint32(0x30)
_EMC_INDEX = 24
_EMC_BARREL_EC_INDEX = 16
_EMC_THETA_INDEX = 8
_EMC_PHI_INDEX = 0
_EMC_ENDCAP_EAST = 0
_EMC_BARREL = 1
_EMC_ENDCAP_WEST = 2
_EMC_THETA_BARREL_MAX = 43
_EMC_THETA_ENDCAP_MAX = 5
_EMC_PHI_BARREL_MAX = 119
_EMC_PHI_ENDCAP_MIN = 0

# --- MUC ---
_MUC_ID = np.uint32(0x40)
_MUC_INDEX = 24
_MUC_BARREL_EC_INDEX = 16
_MUC_SEGMENT_INDEX = 12
_MUC_LAYER_INDEX = 8
_MUC_CHANNEL_INDEX = 0

# ============================================================================
# RE config from RawDataCnvConf.conf
# ============================================================================

# MDC RE bit-fields
_MDC_RE_WIRE_POS = 2
_MDC_RE_WIRE_MASK = 0x3FC
_MDC_RE_LAYER_POS = 10
_MDC_RE_LAYER_MASK = 0xFC00

# TOF RE bit-fields
_TOF_RE_CELL_POS = 0
_TOF_RE_CELL_MASK = 0x7F
_TOF_RE_LAYER_POS = 7
_TOF_RE_LAYER_MASK = 0x180
_TOF_RE_EAWE_POS = 9
_TOF_RE_EAWE_MASK = 0x200

# EMC RE bit-fields
_EMC_RE_PHI_POS = 0
_EMC_RE_PHI_MASK = 0x7F
_EMC_RE_THETA_POS = 7
_EMC_RE_THETA_MASK = 0xF80
_EMC_RE_EAWE_POS = 12
_EMC_RE_EAWE_MASK = 0x1000


# ============================================================================
# Helpers
# ============================================================================


def _mdc_wire_type(layer: int) -> int:
    """Determine MDC wire type from layer number (0=axial, 1=stereo)."""
    if layer < _MDC_INNER_STEREO_LAYER_MAX:
        return 1  # inner stereo: 0-7
    if layer < _MDC_INNER_STEREO_LAYER_MAX + _MDC_INNER_AXIAL_LAYER_MAX:
        return 0  # inner axial: 8-19
    if layer < (
        _MDC_INNER_STEREO_LAYER_MAX + _MDC_INNER_AXIAL_LAYER_MAX + _MDC_OUTER_STEREO_LAYER_MAX
    ):
        return 1  # outer stereo: 20-35
    return 0  # outer axial: 36-42


def _mdc_get_int_id(te_layer: int, te_wire: int) -> np.uint32:
    """Compute MDC teid (digi_id) from TE layer and wire numbers."""
    wt = _mdc_wire_type(te_layer)
    return np.uint32(
        (_MDC_ID << _MDC_INDEX)
        | (wt << _MDC_WIRETYPE_INDEX)
        | (te_layer << _MDC_LAYER_INDEX)
        | (te_wire << _MDC_WIRE_INDEX)
    )


def _tof_get_int_id(barrel_ec: int, te_layer: int, te_phi: int, end: int) -> np.uint32:
    """Compute TOF scintillator teid (digi_id)."""
    return np.uint32(
        (_TOF_ID << _TOF_INDEX)
        | (barrel_ec << _TOF_BARREL_EC_INDEX)
        | (te_layer << _TOF_LAYER_INDEX)
        | (te_phi << _TOF_PHI_INDEX)
        | (end << _TOF_END_INDEX)
    )


def _emc_get_int_id(barrel_ec: int, te_theta: int, te_phi: int) -> np.uint32:
    """Compute EMC teid (digi_id)."""
    return np.uint32(
        (_EMC_ID << _EMC_INDEX)
        | (barrel_ec << _EMC_BARREL_EC_INDEX)
        | (te_theta << _EMC_THETA_INDEX)
        | (te_phi << _EMC_PHI_INDEX)
    )


def _muc_get_int_id(part: int, seg: int, layer: int, channel: int) -> np.uint32:
    """Compute MUC teid (digi_id)."""
    return np.uint32(
        (_MUC_ID << _MUC_INDEX)
        | (part << _MUC_BARREL_EC_INDEX)
        | (seg << _MUC_SEGMENT_INDEX)
        | (layer << _MUC_LAYER_INDEX)
        | (channel << _MUC_CHANNEL_INDEX)
    )


def _emc_phi_endcap_max(theta: int) -> int:
    """Get the maximum phi for EMC endcap at given theta."""
    if theta <= 1:
        return 63
    elif theta <= 3:
        return 79
    else:
        return 95


# ============================================================================
# RE2TE Table Builders
# ============================================================================

_INVALID_TEID = np.uint32(0xFFFFFFFF)


@lru_cache(maxsize=1)
def build_mdc_re2te() -> np.ndarray:
    """
    Build MDC REID → TEID lookup table.

    Ported from ``MdcBuilder::initialize()`` in BOSS.

    Returns:
        numpy uint32 array of shape (16384,).
        ``table[reid]`` gives the corresponding teid (digi_id).
        Invalid entries are 0xFFFFFFFF.
    """
    re2te = np.full(16384, _INVALID_TEID, dtype=np.uint32)

    cur_layer_mask = _MDC_RE_LAYER_MASK
    cur_wire_mask = _MDC_RE_WIRE_MASK
    i = 0

    for te_layer in range(_MDC_TE_LAYER_MAX + 1):
        layer = te_layer + 1

        if layer >= 0x20:  # >= 32, i.e. te_layer >= 31
            layer = layer + i
            i += 1
            cur_layer_mask = cur_layer_mask & ~0x400  # clear bit 10
            cur_wire_mask = cur_wire_mask | 0x400  # set bit 10
            te_wire_max = _MDC_AXIAL_WIRE_MAX  # 287
        else:
            te_wire_max = 240

        for te_wire in range(te_wire_max + 1):
            wire = te_wire + 1
            reid = (
                ((layer << _MDC_RE_LAYER_POS) & cur_layer_mask)
                | ((wire << _MDC_RE_WIRE_POS) & cur_wire_mask)
            ) >> 2

            teid = _mdc_get_int_id(te_layer, te_wire)

            if reid < 16384:
                re2te[reid] = teid

    return re2te


@lru_cache(maxsize=1)
def build_tof_re2te() -> np.ndarray:
    """
    Build TOF (scintillator) REID → TEID lookup table.

    Ported from ``TofBuilder::initialize()`` in BOSS.

    Returns:
        numpy uint32 array of shape (16384,).
        ``table[reid]`` gives the corresponding teid (digi_id).
        Invalid entries are 0xFFFFFFFF.
    """
    re2te = np.full(16384, _INVALID_TEID, dtype=np.uint32)

    for barrel_ec in range(_TOF_BARREL_EC_MIN, _TOF_BARREL_EC_MAX + 1):
        if barrel_ec == 1:  # barrel
            te_layer_max = _TOF_LAYER_BARREL_MAX
            te_phi_max = _TOF_PHI_BARREL_MAX
        else:  # endcap
            te_layer_max = _TOF_LAYER_ENDCAP_MAX
            te_phi_max = _TOF_PHI_ENDCAP_MAX

        for te_ba_ea_we in range(2):
            if barrel_ec != 1 and te_ba_ea_we > 0:
                break
            eawe = te_ba_ea_we + (barrel_ec // 2)

            for te_layer in range(te_layer_max + 1):
                if barrel_ec == 1:
                    layer = te_layer + 1
                else:
                    layer = 3

                if layer <= 3:
                    for te_phi in range(te_phi_max + 1):
                        cell = te_phi + 1
                        reid = (
                            ((eawe << _TOF_RE_EAWE_POS) & _TOF_RE_EAWE_MASK)
                            | ((layer << _TOF_RE_LAYER_POS) & _TOF_RE_LAYER_MASK)
                            | ((cell << _TOF_RE_CELL_POS) & _TOF_RE_CELL_MASK)
                        )

                        teid = _tof_get_int_id(barrel_ec, te_layer, te_phi, te_ba_ea_we)

                        if reid < 16384:
                            re2te[reid] = teid

    return re2te


@lru_cache(maxsize=1)
def build_emc_re2te() -> np.ndarray:
    """
    Build EMC REID → TEID lookup table.

    Ported from ``EmcBuilder::initialize()`` in BOSS.

    Returns:
        numpy uint32 array of shape (8192,).
        ``table[reid]`` gives the corresponding teid (digi_id).
        Invalid entries are 0xFFFFFFFF.
    """
    re2te = np.full(8192, _INVALID_TEID, dtype=np.uint32)

    for barrel_ec in range(3):
        if barrel_ec == _EMC_BARREL:
            te_theta_max = _EMC_THETA_BARREL_MAX
            te_theta_min = 0
        else:
            te_theta_max = _EMC_THETA_ENDCAP_MAX
            te_theta_min = 0
            eawe = 0 if barrel_ec == _EMC_ENDCAP_EAST else 1

        for te_theta in range(te_theta_min, te_theta_max + 1):
            if barrel_ec == _EMC_BARREL:
                half = _EMC_THETA_BARREL_MAX // 2  # 21
                if te_theta <= half:
                    eawe = 0  # east
                    theta = half + 1 - te_theta
                else:
                    eawe = 1  # west
                    theta = te_theta - half
                te_phi_max = _EMC_PHI_BARREL_MAX
                te_phi_min = 0
            else:
                theta = te_theta + _EMC_THETA_BARREL_MAX // 2 + 2
                te_phi_max = _emc_phi_endcap_max(te_theta)
                te_phi_min = _EMC_PHI_ENDCAP_MIN

            for te_phi in range(te_phi_min, te_phi_max + 1):
                phi = te_phi + 1
                reid = (
                    ((eawe << _EMC_RE_EAWE_POS) & _EMC_RE_EAWE_MASK)
                    | ((theta << _EMC_RE_THETA_POS) & _EMC_RE_THETA_MASK)
                    | ((phi << _EMC_RE_PHI_POS) & _EMC_RE_PHI_MASK)
                )

                teid = _emc_get_int_id(barrel_ec, te_theta, te_phi)

                if reid < 8192:
                    re2te[reid] = teid

    return re2te


# Embedded MucFec2Id.map data: (VmeInt, Part, Seg, Lay, 1stStr)
# fmt: off
_MUC_FEC2ID_MAP = [
    (0,0,0,3,48),(1,0,0,3,32),(2,0,0,3,16),(3,0,0,3,0),
    (4,0,0,2,48),(5,0,0,2,32),(6,0,0,2,16),(7,0,0,2,0),
    (8,0,0,1,48),(9,0,0,1,32),(10,0,0,1,16),(11,0,0,1,0),
    (12,0,0,0,48),(13,0,0,0,32),(14,0,0,0,16),(15,0,0,0,0),
    (16,0,0,7,48),(17,0,0,7,32),(18,0,0,7,16),(19,0,0,7,0),
    (20,0,0,6,48),(21,0,0,6,32),(22,0,0,6,16),(23,0,0,6,0),
    (24,0,0,5,48),(25,0,0,5,32),(26,0,0,5,16),(27,0,0,5,0),
    (28,0,0,4,48),(29,0,0,4,32),(30,0,0,4,16),(31,0,0,4,0),
    (32,0,3,7,48),(33,0,3,7,32),(34,0,3,7,16),(35,0,3,7,0),
    (36,0,3,6,48),(37,0,3,6,32),(38,0,3,6,16),(39,0,3,6,0),
    (40,0,3,5,48),(41,0,3,5,32),(42,0,3,5,16),(43,0,3,5,0),
    (44,0,3,4,48),(45,0,3,4,32),(46,0,3,4,16),(47,0,3,4,0),
    (48,0,3,3,48),(49,0,3,3,32),(50,0,3,3,16),(51,0,3,3,0),
    (52,0,3,2,48),(53,0,3,2,32),(54,0,3,2,16),(55,0,3,2,0),
    (56,0,3,1,48),(57,0,3,1,32),(58,0,3,1,16),(59,0,3,1,0),
    (60,0,3,0,48),(61,0,3,0,32),(62,0,3,0,16),(63,0,3,0,0),
    (64,0,2,3,48),(65,0,2,3,32),(66,0,2,3,16),(67,0,2,3,0),
    (68,0,2,2,48),(69,0,2,2,32),(70,0,2,2,16),(71,0,2,2,0),
    (72,0,2,1,48),(73,0,2,1,32),(74,0,2,1,16),(75,0,2,1,0),
    (76,0,2,0,48),(77,0,2,0,32),(78,0,2,0,16),(79,0,2,0,0),
    (80,0,2,7,48),(81,0,2,7,32),(82,0,2,7,16),(83,0,2,7,0),
    (84,0,2,6,48),(85,0,2,6,32),(86,0,2,6,16),(87,0,2,6,0),
    (88,0,2,5,48),(89,0,2,5,32),(90,0,2,5,16),(91,0,2,5,0),
    (92,0,2,4,48),(93,0,2,4,32),(94,0,2,4,16),(95,0,2,4,0),
    (96,0,1,3,48),(97,0,1,3,32),(98,0,1,3,16),(99,0,1,3,0),
    (100,0,1,2,48),(101,0,1,2,32),(102,0,1,2,16),(103,0,1,2,0),
    (104,0,1,1,48),(105,0,1,1,32),(106,0,1,1,16),(107,0,1,1,0),
    (108,0,1,0,48),(109,0,1,0,32),(110,0,1,0,16),(111,0,1,0,0),
    (112,0,1,7,48),(113,0,1,7,32),(114,0,1,7,16),(115,0,1,7,0),
    (116,0,1,6,48),(117,0,1,6,32),(118,0,1,6,16),(119,0,1,6,0),
    (120,0,1,5,48),(121,0,1,5,32),(122,0,1,5,16),(123,0,1,5,0),
    (124,0,1,4,48),(125,0,1,4,32),(126,0,1,4,16),(127,0,1,4,0),
    (128,1,7,1,80),(129,1,7,1,64),(130,1,7,1,48),
    (131,1,7,3,48),(132,1,7,3,64),(133,1,7,3,80),
    (134,1,7,5,80),(135,1,7,5,64),(136,1,7,5,48),
    (137,1,7,7,48),(138,1,7,7,64),(139,1,7,7,80),
    (144,1,0,1,48),(145,1,0,1,64),(146,1,0,1,80),
    (147,1,0,3,80),(148,1,0,3,64),(149,1,0,3,48),
    (150,1,0,5,48),(151,1,0,5,64),(152,1,0,5,80),
    (153,1,0,7,80),(154,1,0,7,64),(155,1,0,7,48),
    (160,1,1,1,48),(161,1,1,1,64),(162,1,1,1,80),
    (163,1,1,3,80),(164,1,1,3,64),(165,1,1,3,48),
    (166,1,1,5,48),(167,1,1,5,64),(168,1,1,5,80),
    (169,1,1,7,80),(170,1,1,7,64),(171,1,1,7,48),
    (176,1,2,1,64),(177,1,2,1,96),(178,1,2,1,80),(179,1,2,1,48),
    (180,1,2,3,48),(181,1,2,3,80),(182,1,2,3,96),(183,1,2,3,64),
    (184,1,2,5,64),(185,1,2,5,96),(186,1,2,5,80),(187,1,2,5,48),
    (188,1,2,7,48),(189,1,2,7,80),(190,1,2,7,96),(191,1,2,7,64),
    (192,1,3,1,80),(193,1,3,1,64),(194,1,3,1,48),
    (195,1,3,3,48),(196,1,3,3,64),(197,1,3,3,80),
    (198,1,3,5,80),(199,1,3,5,64),(200,1,3,5,48),
    (201,1,3,7,48),(202,1,3,7,64),(203,1,3,7,80),
    (208,1,4,1,80),(209,1,4,1,64),(210,1,4,1,48),
    (211,1,4,3,48),(212,1,4,3,64),(213,1,4,3,80),
    (214,1,4,5,80),(215,1,4,5,64),(216,1,4,5,48),
    (217,1,4,7,48),(218,1,4,7,64),(219,1,4,7,80),
    (224,1,5,1,48),(225,1,5,1,64),(226,1,5,1,80),
    (227,1,5,3,80),(228,1,5,3,64),(229,1,5,3,48),
    (230,1,5,5,48),(231,1,5,5,64),(232,1,5,5,80),
    (233,1,5,7,80),(234,1,5,7,64),(235,1,5,7,48),
    (240,1,6,1,80),(241,1,6,1,64),(242,1,6,1,48),
    (243,1,6,3,48),(244,1,6,3,64),(245,1,6,3,80),
    (246,1,6,5,80),(247,1,6,5,64),(248,1,6,5,48),
    (249,1,6,7,48),(250,1,6,7,64),(251,1,6,7,80),
    (256,1,1,0,0),(257,1,1,0,16),(258,1,1,0,32),
    (259,1,1,2,32),(260,1,1,2,16),(261,1,1,2,0),
    (262,1,1,4,0),(263,1,1,4,16),(264,1,1,4,32),
    (265,1,1,6,32),(266,1,1,6,16),(267,1,1,6,0),
    (268,1,1,8,0),(269,1,1,8,16),(270,1,1,8,32),
    (272,1,1,1,32),(273,1,1,1,16),(274,1,1,1,0),
    (275,1,1,3,0),(276,1,1,3,16),(277,1,1,3,32),
    (278,1,1,5,32),(279,1,1,5,16),(280,1,1,5,0),
    (281,1,1,7,0),(282,1,1,7,16),(283,1,1,7,32),
    (288,1,2,1,32),(289,1,2,1,16),(290,1,2,1,0),
    (291,1,2,3,0),(292,1,2,3,16),(293,1,2,3,32),
    (294,1,2,5,32),(295,1,2,5,16),(296,1,2,5,0),
    (297,1,2,7,0),(298,1,2,7,16),(299,1,2,7,32),
    (304,1,2,0,0),(305,1,2,0,16),(306,1,2,0,32),
    (307,1,2,2,32),(308,1,2,2,16),(309,1,2,2,0),
    (310,1,2,4,0),(311,1,2,4,16),(312,1,2,4,32),
    (313,1,2,6,32),(314,1,2,6,16),(315,1,2,6,0),
    (316,1,2,8,0),(317,1,2,8,16),(318,1,2,8,32),
    (320,1,7,0,32),(321,1,7,0,16),(322,1,7,0,0),
    (323,1,7,2,0),(324,1,7,2,16),(325,1,7,2,32),
    (326,1,7,4,32),(327,1,7,4,16),(328,1,7,4,0),
    (329,1,7,6,0),(330,1,7,6,16),(331,1,7,6,32),
    (332,1,7,8,32),(333,1,7,8,16),(334,1,7,8,0),
    (336,1,7,1,0),(337,1,7,1,16),(338,1,7,1,32),
    (339,1,7,3,32),(340,1,7,3,16),(341,1,7,3,0),
    (342,1,7,5,0),(343,1,7,5,16),(344,1,7,5,32),
    (345,1,7,7,32),(346,1,7,7,16),(347,1,7,7,0),
    (352,1,0,1,32),(353,1,0,1,16),(354,1,0,1,0),
    (355,1,0,3,0),(356,1,0,3,16),(357,1,0,3,32),
    (358,1,0,5,32),(359,1,0,5,16),(360,1,0,5,0),
    (361,1,0,7,0),(362,1,0,7,16),(363,1,0,7,32),
    (368,1,0,0,0),(369,1,0,0,16),(370,1,0,0,32),
    (371,1,0,2,32),(372,1,0,2,16),(373,1,0,2,0),
    (374,1,0,4,0),(375,1,0,4,16),(376,1,0,4,32),
    (377,1,0,6,32),(378,1,0,6,16),(379,1,0,6,0),
    (380,1,0,8,0),(381,1,0,8,16),(382,1,0,8,32),
    (384,1,5,1,32),(385,1,5,1,16),(386,1,5,1,0),
    (387,1,5,3,0),(388,1,5,3,16),(389,1,5,3,32),
    (390,1,5,5,32),(391,1,5,5,16),(392,1,5,5,0),
    (393,1,5,7,0),(394,1,5,7,16),(395,1,5,7,32),
    (400,1,5,0,0),(401,1,5,0,16),(402,1,5,0,32),
    (403,1,5,2,32),(404,1,5,2,16),(405,1,5,2,0),
    (406,1,5,4,0),(407,1,5,4,16),(408,1,5,4,32),
    (409,1,5,6,32),(410,1,5,6,16),(411,1,5,6,0),
    (412,1,5,8,0),(413,1,5,8,16),(414,1,5,8,32),
    (416,1,6,1,0),(417,1,6,1,16),(418,1,6,1,32),
    (419,1,6,3,32),(420,1,6,3,16),(421,1,6,3,0),
    (422,1,6,5,0),(423,1,6,5,16),(424,1,6,5,32),
    (425,1,6,7,32),(426,1,6,7,16),(427,1,6,7,0),
    (432,1,6,0,32),(433,1,6,0,16),(434,1,6,0,0),
    (435,1,6,2,0),(436,1,6,2,16),(437,1,6,2,32),
    (438,1,6,4,32),(439,1,6,4,16),(440,1,6,4,0),
    (441,1,6,6,0),(442,1,6,6,16),(443,1,6,6,32),
    (444,1,6,8,32),(445,1,6,8,16),(446,1,6,8,0),
    (448,1,4,0,32),(449,1,4,0,16),(450,1,4,0,0),
    (451,1,4,2,0),(452,1,4,2,16),(453,1,4,2,32),
    (454,1,4,4,32),(455,1,4,4,16),(456,1,4,4,0),
    (457,1,4,6,0),(458,1,4,6,16),(459,1,4,6,32),
    (460,1,4,8,32),(461,1,4,8,16),(462,1,4,8,0),
    (464,1,4,1,0),(465,1,4,1,16),(466,1,4,1,32),
    (467,1,4,3,32),(468,1,4,3,16),(469,1,4,3,0),
    (470,1,4,5,0),(471,1,4,5,16),(472,1,4,5,32),
    (473,1,4,7,32),(474,1,4,7,16),(475,1,4,7,0),
    (480,1,3,1,0),(481,1,3,1,16),(482,1,3,1,32),
    (483,1,3,3,32),(484,1,3,3,16),(485,1,3,3,0),
    (486,1,3,5,0),(487,1,3,5,16),(488,1,3,5,32),
    (489,1,3,7,32),(490,1,3,7,16),(491,1,3,7,0),
    (496,1,3,0,32),(497,1,3,0,16),(498,1,3,0,0),
    (499,1,3,2,0),(500,1,3,2,16),(501,1,3,2,32),
    (502,1,3,4,32),(503,1,3,4,16),(504,1,3,4,0),
    (505,1,3,6,0),(506,1,3,6,16),(507,1,3,6,32),
    (508,1,3,8,32),(509,1,3,8,16),(510,1,3,8,0),
    (512,2,1,3,48),(513,2,1,3,32),(514,2,1,3,16),(515,2,1,3,0),
    (516,2,1,2,48),(517,2,1,2,32),(518,2,1,2,16),(519,2,1,2,0),
    (520,2,1,1,48),(521,2,1,1,32),(522,2,1,1,16),(523,2,1,1,0),
    (524,2,1,0,48),(525,2,1,0,32),(526,2,1,0,16),(527,2,1,0,0),
    (528,2,1,7,48),(529,2,1,7,32),(530,2,1,7,16),(531,2,1,7,0),
    (532,2,1,6,48),(533,2,1,6,32),(534,2,1,6,16),(535,2,1,6,0),
    (536,2,1,5,48),(537,2,1,5,32),(538,2,1,5,16),(539,2,1,5,0),
    (540,2,1,4,48),(541,2,1,4,32),(542,2,1,4,16),(543,2,1,4,0),
    (544,2,2,3,48),(545,2,2,3,32),(546,2,2,3,16),(547,2,2,3,0),
    (548,2,2,2,48),(549,2,2,2,32),(550,2,2,2,16),(551,2,2,2,0),
    (552,2,2,1,48),(553,2,2,1,32),(554,2,2,1,16),(555,2,2,1,0),
    (556,2,2,0,48),(557,2,2,0,32),(558,2,2,0,16),(559,2,2,0,0),
    (560,2,2,7,48),(561,2,2,7,32),(562,2,2,7,16),(563,2,2,7,0),
    (564,2,2,6,48),(565,2,2,6,32),(566,2,2,6,16),(567,2,2,6,0),
    (568,2,2,5,48),(569,2,2,5,32),(570,2,2,5,16),(571,2,2,5,0),
    (572,2,2,4,48),(573,2,2,4,32),(574,2,2,4,16),(575,2,2,4,0),
    (576,2,0,7,48),(577,2,0,7,32),(578,2,0,7,16),(579,2,0,7,0),
    (580,2,0,6,48),(581,2,0,6,32),(582,2,0,6,16),(583,2,0,6,0),
    (584,2,0,5,48),(585,2,0,5,32),(586,2,0,5,16),(587,2,0,5,0),
    (588,2,0,4,48),(589,2,0,4,32),(590,2,0,4,16),(591,2,0,4,0),
    (592,2,3,3,48),(593,2,3,3,32),(594,2,3,3,16),(595,2,3,3,0),
    (596,2,3,2,48),(597,2,3,2,32),(598,2,3,2,16),(599,2,3,2,0),
    (600,2,3,1,48),(601,2,3,1,32),(602,2,3,1,16),(603,2,3,1,0),
    (604,2,3,0,48),(605,2,3,0,32),(606,2,3,0,16),(607,2,3,0,0),
    (608,2,3,7,48),(609,2,3,7,32),(610,2,3,7,16),(611,2,3,7,0),
    (612,2,3,6,48),(613,2,3,6,32),(614,2,3,6,16),(615,2,3,6,0),
    (616,2,3,5,48),(617,2,3,5,32),(618,2,3,5,16),(619,2,3,5,0),
    (620,2,3,4,48),(621,2,3,4,32),(622,2,3,4,16),(623,2,3,4,0),
    (624,2,0,3,48),(625,2,0,3,32),(626,2,0,3,16),(627,2,0,3,0),
    (628,2,0,2,48),(629,2,0,2,32),(630,2,0,2,16),(631,2,0,2,0),
    (632,2,0,1,48),(633,2,0,1,32),(634,2,0,1,16),(635,2,0,1,0),
    (636,2,0,0,48),(637,2,0,0,32),(638,2,0,0,16),(639,2,0,0,0),
]
# fmt: on


@lru_cache(maxsize=1)
def build_muc_re2te() -> np.ndarray:
    """
    Build MUC REID → TEID lookup table from embedded MucFec2Id.map data.

    Each MUC raw-data word represents one FEC (front-end card) that covers
    16 strip channels.  The returned teid encodes the *base* digi_id
    (part, segment, layer, firstStrip) for that FEC card.

    Ported from ``MucBuilder::initialize()`` in BOSS.

    Returns:
        numpy uint32 array of shape (2048,).
        ``table[reid]`` gives the corresponding base teid (digi_id).
        Invalid entries are 0xFFFFFFFF.
    """
    re2te = np.full(2048, _INVALID_TEID, dtype=np.uint32)

    for fec, part, seg, layer, first_str in _MUC_FEC2ID_MAP:
        teid = _muc_get_int_id(part, seg, layer, first_str)
        if fec < 2048:
            re2te[fec] = teid

    return re2te


# ============================================================================
# Conversion function (applies to raw dict before building awkward array)
# ============================================================================


def convert_reid_to_teid(raw_dict: dict) -> dict:
    """
    Convert REID (raw electronics ID) to TEID (digi_id) in-place for all
    sub-detectors present in ``raw_dict``.

    After conversion, the ``id`` field of each sub-detector contains standard
    digi_id values compatible with :mod:`pybes3.detectors.digi_id`.

    Parameters:
        raw_dict: The raw dict returned by the C++ ``read_bes_raw`` function.
            Modified in-place.

    Returns:
        The same dict (modified in-place) for convenience.
    """

    if "mdc" in raw_dict:
        table = build_mdc_re2te()
        offsets, data_dict = raw_dict["mdc"]
        reid = data_dict["id"]
        data_dict["id"] = table[reid.astype(np.intp)]

    if "tof" in raw_dict:
        table = build_tof_re2te()
        offsets, data_dict = raw_dict["tof"]
        reid = data_dict["id"]
        data_dict["id"] = table[reid.astype(np.intp)]

    if "emc" in raw_dict:
        table = build_emc_re2te()
        offsets, data_dict = raw_dict["emc"]
        reid = data_dict["id"]
        data_dict["id"] = table[reid.astype(np.intp)]

    if "muc" in raw_dict:
        table = build_muc_re2te()
        offsets, data_dict = raw_dict["muc"]
        reid = data_dict["id"]
        data_dict["id"] = table[reid.astype(np.intp)]

    return raw_dict
