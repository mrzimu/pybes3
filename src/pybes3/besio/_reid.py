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

    re2te.flags.writeable = False
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

    re2te.flags.writeable = False
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

    re2te.flags.writeable = False
    return re2te


# Embedded MucFec2Id.map data: (VmeInt, Part, Seg, Lay, 1stStr)
# fmt: off
_MUC_FEC2ID_MAP = [
    (0, 0, 0, 3, 48, 1), (1, 0, 0, 3, 32, 1), (2, 0, 0, 3, 16, 1), (3, 0, 0, 3, 0, 1),
    (4, 0, 0, 2, 48, -1), (5, 0, 0, 2, 32, -1), (6, 0, 0, 2, 16, -1), (7, 0, 0, 2, 0, -1),
    (8, 0, 0, 1, 48, 1), (9, 0, 0, 1, 32, 1), (10, 0, 0, 1, 16, 1), (11, 0, 0, 1, 0, 1),
    (12, 0, 0, 0, 48, -1), (13, 0, 0, 0, 32, -1), (14, 0, 0, 0, 16, -1), (15, 0, 0, 0, 0, -1),
    (16, 0, 0, 7, 48, 1), (17, 0, 0, 7, 32, 1), (18, 0, 0, 7, 16, 1), (19, 0, 0, 7, 0, 1),
    (20, 0, 0, 6, 48, -1), (21, 0, 0, 6, 32, -1), (22, 0, 0, 6, 16, -1), (23, 0, 0, 6, 0, -1),
    (24, 0, 0, 5, 48, 1), (25, 0, 0, 5, 32, 1), (26, 0, 0, 5, 16, 1), (27, 0, 0, 5, 0, 1),
    (28, 0, 0, 4, 48, -1), (29, 0, 0, 4, 32, -1), (30, 0, 0, 4, 16, -1), (31, 0, 0, 4, 0, -1),
    (32, 0, 3, 7, 48, -1), (33, 0, 3, 7, 32, -1), (34, 0, 3, 7, 16, -1), (35, 0, 3, 7, 0, -1),
    (36, 0, 3, 6, 48, 1), (37, 0, 3, 6, 32, 1), (38, 0, 3, 6, 16, 1), (39, 0, 3, 6, 0, 1),
    (40, 0, 3, 5, 48, -1), (41, 0, 3, 5, 32, -1), (42, 0, 3, 5, 16, -1), (43, 0, 3, 5, 0, -1),
    (44, 0, 3, 4, 48, 1), (45, 0, 3, 4, 32, 1), (46, 0, 3, 4, 16, 1), (47, 0, 3, 4, 0, 1),
    (48, 0, 3, 3, 48, -1), (49, 0, 3, 3, 32, -1), (50, 0, 3, 3, 16, -1), (51, 0, 3, 3, 0, -1),
    (52, 0, 3, 2, 48, 1), (53, 0, 3, 2, 32, 1), (54, 0, 3, 2, 16, 1), (55, 0, 3, 2, 0, 1),
    (56, 0, 3, 1, 48, -1), (57, 0, 3, 1, 32, -1), (58, 0, 3, 1, 16, -1), (59, 0, 3, 1, 0, -1),
    (60, 0, 3, 0, 48, 1), (61, 0, 3, 0, 32, 1), (62, 0, 3, 0, 16, 1), (63, 0, 3, 0, 0, 1),
    (64, 0, 2, 3, 48, 1), (65, 0, 2, 3, 32, 1), (66, 0, 2, 3, 16, 1), (67, 0, 2, 3, 0, 1),
    (68, 0, 2, 2, 48, -1), (69, 0, 2, 2, 32, -1), (70, 0, 2, 2, 16, -1), (71, 0, 2, 2, 0, -1),
    (72, 0, 2, 1, 48, 1), (73, 0, 2, 1, 32, 1), (74, 0, 2, 1, 16, 1), (75, 0, 2, 1, 0, 1),
    (76, 0, 2, 0, 48, -1), (77, 0, 2, 0, 32, -1), (78, 0, 2, 0, 16, -1), (79, 0, 2, 0, 0, -1),
    (80, 0, 2, 7, 48, 1), (81, 0, 2, 7, 32, 1), (82, 0, 2, 7, 16, 1), (83, 0, 2, 7, 0, 1),
    (84, 0, 2, 6, 48, -1), (85, 0, 2, 6, 32, -1), (86, 0, 2, 6, 16, -1), (87, 0, 2, 6, 0, -1),
    (88, 0, 2, 5, 48, 1), (89, 0, 2, 5, 32, 1), (90, 0, 2, 5, 16, 1), (91, 0, 2, 5, 0, 1),
    (92, 0, 2, 4, 48, -1), (93, 0, 2, 4, 32, -1), (94, 0, 2, 4, 16, -1), (95, 0, 2, 4, 0, -1),
    (96, 0, 1, 3, 48, -1), (97, 0, 1, 3, 32, -1), (98, 0, 1, 3, 16, -1), (99, 0, 1, 3, 0, -1),
    (100, 0, 1, 2, 48, 1), (101, 0, 1, 2, 32, 1), (102, 0, 1, 2, 16, 1), (103, 0, 1, 2, 0, 1),
    (104, 0, 1, 1, 48, -1), (105, 0, 1, 1, 32, -1), (106, 0, 1, 1, 16, -1), (107, 0, 1, 1, 0, -1),
    (108, 0, 1, 0, 48, 1), (109, 0, 1, 0, 32, 1), (110, 0, 1, 0, 16, 1), (111, 0, 1, 0, 0, 1),
    (112, 0, 1, 7, 48, -1), (113, 0, 1, 7, 32, -1), (114, 0, 1, 7, 16, -1), (115, 0, 1, 7, 0, -1),
    (116, 0, 1, 6, 48, 1), (117, 0, 1, 6, 32, 1), (118, 0, 1, 6, 16, 1), (119, 0, 1, 6, 0, 1),
    (120, 0, 1, 5, 48, -1), (121, 0, 1, 5, 32, -1), (122, 0, 1, 5, 16, -1), (123, 0, 1, 5, 0, -1),
    (124, 0, 1, 4, 48, 1), (125, 0, 1, 4, 32, 1), (126, 0, 1, 4, 16, 1), (127, 0, 1, 4, 0, 1),
    (128, 1, 7, 1, 80, -1), (129, 1, 7, 1, 64, -1), (130, 1, 7, 1, 48, -1), (131, 1, 7, 3, 48, -1),
    (132, 1, 7, 3, 64, -1), (133, 1, 7, 3, 80, -1), (134, 1, 7, 5, 80, -1), (135, 1, 7, 5, 64, -1),
    (136, 1, 7, 5, 48, -1), (137, 1, 7, 7, 48, -1), (138, 1, 7, 7, 64, -1), (139, 1, 7, 7, 80, -1),
    (144, 1, 0, 1, 48, -1), (145, 1, 0, 1, 64, -1), (146, 1, 0, 1, 80, -1), (147, 1, 0, 3, 80, -1),
    (148, 1, 0, 3, 64, -1), (149, 1, 0, 3, 48, -1), (150, 1, 0, 5, 48, -1), (151, 1, 0, 5, 64, -1),
    (152, 1, 0, 5, 80, -1), (153, 1, 0, 7, 80, -1), (154, 1, 0, 7, 64, -1), (155, 1, 0, 7, 48, -1),
    (160, 1, 1, 1, 48, -1), (161, 1, 1, 1, 64, -1), (162, 1, 1, 1, 80, -1), (163, 1, 1, 3, 80, -1),
    (164, 1, 1, 3, 64, -1), (165, 1, 1, 3, 48, -1), (166, 1, 1, 5, 48, -1), (167, 1, 1, 5, 64, -1),
    (168, 1, 1, 5, 80, -1), (169, 1, 1, 7, 80, -1), (170, 1, 1, 7, 64, -1), (171, 1, 1, 7, 48, -1),
    (176, 1, 2, 1, 64, -1), (177, 1, 2, 1, 96, -1), (178, 1, 2, 1, 80, -1), (179, 1, 2, 1, 48, -1),
    (180, 1, 2, 3, 48, -1), (181, 1, 2, 3, 80, -1), (182, 1, 2, 3, 96, -1), (183, 1, 2, 3, 64, -1),
    (184, 1, 2, 5, 64, -1), (185, 1, 2, 5, 96, -1), (186, 1, 2, 5, 80, -1), (187, 1, 2, 5, 48, -1),
    (188, 1, 2, 7, 48, -1), (189, 1, 2, 7, 80, -1), (190, 1, 2, 7, 96, -1), (191, 1, 2, 7, 64, -1),
    (192, 1, 3, 1, 80, -1), (193, 1, 3, 1, 64, -1), (194, 1, 3, 1, 48, -1), (195, 1, 3, 3, 48, -1),
    (196, 1, 3, 3, 64, -1), (197, 1, 3, 3, 80, -1), (198, 1, 3, 5, 80, -1), (199, 1, 3, 5, 64, -1),
    (200, 1, 3, 5, 48, -1), (201, 1, 3, 7, 48, -1), (202, 1, 3, 7, 64, -1), (203, 1, 3, 7, 80, -1),
    (208, 1, 4, 1, 80, -1), (209, 1, 4, 1, 64, -1), (210, 1, 4, 1, 48, -1), (211, 1, 4, 3, 48, -1),
    (212, 1, 4, 3, 64, -1), (213, 1, 4, 3, 80, -1), (214, 1, 4, 5, 80, -1), (215, 1, 4, 5, 64, -1),
    (216, 1, 4, 5, 48, -1), (217, 1, 4, 7, 48, -1), (218, 1, 4, 7, 64, -1), (219, 1, 4, 7, 80, -1),
    (224, 1, 5, 1, 48, -1), (225, 1, 5, 1, 64, -1), (226, 1, 5, 1, 80, -1), (227, 1, 5, 3, 80, -1),
    (228, 1, 5, 3, 64, -1), (229, 1, 5, 3, 48, -1), (230, 1, 5, 5, 48, -1), (231, 1, 5, 5, 64, -1),
    (232, 1, 5, 5, 80, -1), (233, 1, 5, 7, 80, -1), (234, 1, 5, 7, 64, -1), (235, 1, 5, 7, 48, -1),
    (240, 1, 6, 1, 80, -1), (241, 1, 6, 1, 64, -1), (242, 1, 6, 1, 48, -1), (243, 1, 6, 3, 48, -1),
    (244, 1, 6, 3, 64, -1), (245, 1, 6, 3, 80, -1), (246, 1, 6, 5, 80, -1), (247, 1, 6, 5, 64, -1),
    (248, 1, 6, 5, 48, -1), (249, 1, 6, 7, 48, -1), (250, 1, 6, 7, 64, -1), (251, 1, 6, 7, 80, -1),
    (256, 1, 1, 0, 0, -1), (257, 1, 1, 0, 16, -1), (258, 1, 1, 0, 32, -1), (259, 1, 1, 2, 32, -1),
    (260, 1, 1, 2, 16, -1), (261, 1, 1, 2, 0, -1), (262, 1, 1, 4, 0, -1), (263, 1, 1, 4, 16, -1),
    (264, 1, 1, 4, 32, -1), (265, 1, 1, 6, 32, -1), (266, 1, 1, 6, 16, -1), (267, 1, 1, 6, 0, -1),
    (268, 1, 1, 8, 0, -1), (269, 1, 1, 8, 16, -1), (270, 1, 1, 8, 32, -1), (272, 1, 1, 1, 32, -1),
    (273, 1, 1, 1, 16, -1), (274, 1, 1, 1, 0, -1), (275, 1, 1, 3, 0, -1), (276, 1, 1, 3, 16, -1),
    (277, 1, 1, 3, 32, -1), (278, 1, 1, 5, 32, -1), (279, 1, 1, 5, 16, -1), (280, 1, 1, 5, 0, -1),
    (281, 1, 1, 7, 0, -1), (282, 1, 1, 7, 16, -1), (283, 1, 1, 7, 32, -1), (288, 1, 2, 1, 32, -1),
    (289, 1, 2, 1, 16, -1), (290, 1, 2, 1, 0, -1), (291, 1, 2, 3, 0, -1), (292, 1, 2, 3, 16, -1),
    (293, 1, 2, 3, 32, -1), (294, 1, 2, 5, 32, -1), (295, 1, 2, 5, 16, -1), (296, 1, 2, 5, 0, -1),
    (297, 1, 2, 7, 0, -1), (298, 1, 2, 7, 16, -1), (299, 1, 2, 7, 32, -1), (304, 1, 2, 0, 0, -1),
    (305, 1, 2, 0, 16, -1), (306, 1, 2, 0, 32, -1), (307, 1, 2, 2, 32, -1), (308, 1, 2, 2, 16, -1),
    (309, 1, 2, 2, 0, -1), (310, 1, 2, 4, 0, -1), (311, 1, 2, 4, 16, -1), (312, 1, 2, 4, 32, -1),
    (313, 1, 2, 6, 32, -1), (314, 1, 2, 6, 16, -1), (315, 1, 2, 6, 0, -1), (316, 1, 2, 8, 0, -1),
    (317, 1, 2, 8, 16, -1), (318, 1, 2, 8, 32, -1), (320, 1, 7, 0, 32, -1), (321, 1, 7, 0, 16, -1),
    (322, 1, 7, 0, 0, -1), (323, 1, 7, 2, 0, -1), (324, 1, 7, 2, 16, -1), (325, 1, 7, 2, 32, -1),
    (326, 1, 7, 4, 32, -1), (327, 1, 7, 4, 16, -1), (328, 1, 7, 4, 0, -1), (329, 1, 7, 6, 0, -1),
    (330, 1, 7, 6, 16, -1), (331, 1, 7, 6, 32, -1), (332, 1, 7, 8, 32, -1), (333, 1, 7, 8, 16, -1),
    (334, 1, 7, 8, 0, -1), (336, 1, 7, 1, 0, -1), (337, 1, 7, 1, 16, -1), (338, 1, 7, 1, 32, -1),
    (339, 1, 7, 3, 32, -1), (340, 1, 7, 3, 16, -1), (341, 1, 7, 3, 0, -1), (342, 1, 7, 5, 0, -1),
    (343, 1, 7, 5, 16, -1), (344, 1, 7, 5, 32, -1), (345, 1, 7, 7, 32, -1), (346, 1, 7, 7, 16, -1),
    (347, 1, 7, 7, 0, -1), (352, 1, 0, 1, 32, -1), (353, 1, 0, 1, 16, -1), (354, 1, 0, 1, 0, -1),
    (355, 1, 0, 3, 0, -1), (356, 1, 0, 3, 16, -1), (357, 1, 0, 3, 32, -1), (358, 1, 0, 5, 32, -1),
    (359, 1, 0, 5, 16, -1), (360, 1, 0, 5, 0, -1), (361, 1, 0, 7, 0, -1), (362, 1, 0, 7, 16, -1),
    (363, 1, 0, 7, 32, -1), (368, 1, 0, 0, 0, -1), (369, 1, 0, 0, 16, -1), (370, 1, 0, 0, 32, -1),
    (371, 1, 0, 2, 32, -1), (372, 1, 0, 2, 16, -1), (373, 1, 0, 2, 0, -1), (374, 1, 0, 4, 0, -1),
    (375, 1, 0, 4, 16, -1), (376, 1, 0, 4, 32, -1), (377, 1, 0, 6, 32, -1), (378, 1, 0, 6, 16, -1),
    (379, 1, 0, 6, 0, -1), (380, 1, 0, 8, 0, -1), (381, 1, 0, 8, 16, -1), (382, 1, 0, 8, 32, -1),
    (384, 1, 5, 1, 32, -1), (385, 1, 5, 1, 16, -1), (386, 1, 5, 1, 0, -1), (387, 1, 5, 3, 0, -1),
    (388, 1, 5, 3, 16, -1), (389, 1, 5, 3, 32, -1), (390, 1, 5, 5, 32, -1), (391, 1, 5, 5, 16, -1),
    (392, 1, 5, 5, 0, -1), (393, 1, 5, 7, 0, -1), (394, 1, 5, 7, 16, -1), (395, 1, 5, 7, 32, -1),
    (400, 1, 5, 0, 0, -1), (401, 1, 5, 0, 16, -1), (402, 1, 5, 0, 32, -1), (403, 1, 5, 2, 32, -1),
    (404, 1, 5, 2, 16, -1), (405, 1, 5, 2, 0, -1), (406, 1, 5, 4, 0, -1), (407, 1, 5, 4, 16, -1),
    (408, 1, 5, 4, 32, -1), (409, 1, 5, 6, 32, -1), (410, 1, 5, 6, 16, -1), (411, 1, 5, 6, 0, -1),
    (412, 1, 5, 8, 0, -1), (413, 1, 5, 8, 16, -1), (414, 1, 5, 8, 32, -1), (416, 1, 6, 1, 0, -1),
    (417, 1, 6, 1, 16, -1), (418, 1, 6, 1, 32, -1), (419, 1, 6, 3, 32, -1), (420, 1, 6, 3, 16, -1),
    (421, 1, 6, 3, 0, -1), (422, 1, 6, 5, 0, -1), (423, 1, 6, 5, 16, -1), (424, 1, 6, 5, 32, -1),
    (425, 1, 6, 7, 32, -1), (426, 1, 6, 7, 16, -1), (427, 1, 6, 7, 0, -1), (432, 1, 6, 0, 32, -1),
    (433, 1, 6, 0, 16, -1), (434, 1, 6, 0, 0, -1), (435, 1, 6, 2, 0, -1), (436, 1, 6, 2, 16, -1),
    (437, 1, 6, 2, 32, -1), (438, 1, 6, 4, 32, -1), (439, 1, 6, 4, 16, -1), (440, 1, 6, 4, 0, -1),
    (441, 1, 6, 6, 0, -1), (442, 1, 6, 6, 16, -1), (443, 1, 6, 6, 32, -1), (444, 1, 6, 8, 32, -1),
    (445, 1, 6, 8, 16, -1), (446, 1, 6, 8, 0, -1), (448, 1, 4, 0, 32, -1), (449, 1, 4, 0, 16, -1),
    (450, 1, 4, 0, 0, -1), (451, 1, 4, 2, 0, -1), (452, 1, 4, 2, 16, -1), (453, 1, 4, 2, 32, -1),
    (454, 1, 4, 4, 32, -1), (455, 1, 4, 4, 16, -1), (456, 1, 4, 4, 0, -1), (457, 1, 4, 6, 0, -1),
    (458, 1, 4, 6, 16, -1), (459, 1, 4, 6, 32, -1), (460, 1, 4, 8, 32, -1), (461, 1, 4, 8, 16, -1),
    (462, 1, 4, 8, 0, -1), (464, 1, 4, 1, 0, -1), (465, 1, 4, 1, 16, -1), (466, 1, 4, 1, 32, -1),
    (467, 1, 4, 3, 32, -1), (468, 1, 4, 3, 16, -1), (469, 1, 4, 3, 0, -1), (470, 1, 4, 5, 0, -1),
    (471, 1, 4, 5, 16, -1), (472, 1, 4, 5, 32, -1), (473, 1, 4, 7, 32, -1), (474, 1, 4, 7, 16, -1),
    (475, 1, 4, 7, 0, -1), (480, 1, 3, 1, 0, -1), (481, 1, 3, 1, 16, -1), (482, 1, 3, 1, 32, -1),
    (483, 1, 3, 3, 32, -1), (484, 1, 3, 3, 16, -1), (485, 1, 3, 3, 0, -1), (486, 1, 3, 5, 0, -1),
    (487, 1, 3, 5, 16, -1), (488, 1, 3, 5, 32, -1), (489, 1, 3, 7, 32, -1), (490, 1, 3, 7, 16, -1),
    (491, 1, 3, 7, 0, -1), (496, 1, 3, 0, 32, -1), (497, 1, 3, 0, 16, -1), (498, 1, 3, 0, 0, -1),
    (499, 1, 3, 2, 0, -1), (500, 1, 3, 2, 16, -1), (501, 1, 3, 2, 32, -1), (502, 1, 3, 4, 32, -1),
    (503, 1, 3, 4, 16, -1), (504, 1, 3, 4, 0, -1), (505, 1, 3, 6, 0, -1), (506, 1, 3, 6, 16, -1),
    (507, 1, 3, 6, 32, -1), (508, 1, 3, 8, 32, -1), (509, 1, 3, 8, 16, -1), (510, 1, 3, 8, 0, -1),
    (512, 2, 1, 3, 48, 1), (513, 2, 1, 3, 32, 1), (514, 2, 1, 3, 16, 1), (515, 2, 1, 3, 0, 1),
    (516, 2, 1, 2, 48, -1), (517, 2, 1, 2, 32, -1), (518, 2, 1, 2, 16, -1), (519, 2, 1, 2, 0, -1),
    (520, 2, 1, 1, 48, 1), (521, 2, 1, 1, 32, 1), (522, 2, 1, 1, 16, 1), (523, 2, 1, 1, 0, 1),
    (524, 2, 1, 0, 48, -1), (525, 2, 1, 0, 32, -1), (526, 2, 1, 0, 16, -1), (527, 2, 1, 0, 0, -1),
    (528, 2, 1, 7, 48, 1), (529, 2, 1, 7, 32, 1), (530, 2, 1, 7, 16, 1), (531, 2, 1, 7, 0, 1),
    (532, 2, 1, 6, 48, -1), (533, 2, 1, 6, 32, -1), (534, 2, 1, 6, 16, -1), (535, 2, 1, 6, 0, -1),
    (536, 2, 1, 5, 48, 1), (537, 2, 1, 5, 32, 1), (538, 2, 1, 5, 16, 1), (539, 2, 1, 5, 0, 1),
    (540, 2, 1, 4, 48, -1), (541, 2, 1, 4, 32, -1), (542, 2, 1, 4, 16, -1), (543, 2, 1, 4, 0, -1),
    (544, 2, 2, 3, 48, -1), (545, 2, 2, 3, 32, -1), (546, 2, 2, 3, 16, -1), (547, 2, 2, 3, 0, -1),
    (548, 2, 2, 2, 48, 1), (549, 2, 2, 2, 32, 1), (550, 2, 2, 2, 16, 1), (551, 2, 2, 2, 0, 1),
    (552, 2, 2, 1, 48, -1), (553, 2, 2, 1, 32, -1), (554, 2, 2, 1, 16, -1), (555, 2, 2, 1, 0, -1),
    (556, 2, 2, 0, 48, 1), (557, 2, 2, 0, 32, 1), (558, 2, 2, 0, 16, 1), (559, 2, 2, 0, 0, 1),
    (560, 2, 2, 7, 48, -1), (561, 2, 2, 7, 32, -1), (562, 2, 2, 7, 16, -1), (563, 2, 2, 7, 0, -1),
    (564, 2, 2, 6, 48, 1), (565, 2, 2, 6, 32, 1), (566, 2, 2, 6, 16, 1), (567, 2, 2, 6, 0, 1),
    (568, 2, 2, 5, 48, -1), (569, 2, 2, 5, 32, -1), (570, 2, 2, 5, 16, -1), (571, 2, 2, 5, 0, -1),
    (572, 2, 2, 4, 48, 1), (573, 2, 2, 4, 32, 1), (574, 2, 2, 4, 16, 1), (575, 2, 2, 4, 0, 1),
    (576, 2, 0, 7, 48, -1), (577, 2, 0, 7, 32, -1), (578, 2, 0, 7, 16, -1), (579, 2, 0, 7, 0, -1),
    (580, 2, 0, 6, 48, 1), (581, 2, 0, 6, 32, 1), (582, 2, 0, 6, 16, 1), (583, 2, 0, 6, 0, 1),
    (584, 2, 0, 5, 48, -1), (585, 2, 0, 5, 32, -1), (586, 2, 0, 5, 16, -1), (587, 2, 0, 5, 0, -1),
    (588, 2, 0, 4, 48, 1), (589, 2, 0, 4, 32, 1), (590, 2, 0, 4, 16, 1), (591, 2, 0, 4, 0, 1),
    (592, 2, 3, 3, 48, 1), (593, 2, 3, 3, 32, 1), (594, 2, 3, 3, 16, 1), (595, 2, 3, 3, 0, 1),
    (596, 2, 3, 2, 48, -1), (597, 2, 3, 2, 32, -1), (598, 2, 3, 2, 16, -1), (599, 2, 3, 2, 0, -1),
    (600, 2, 3, 1, 48, 1), (601, 2, 3, 1, 32, 1), (602, 2, 3, 1, 16, 1), (603, 2, 3, 1, 0, 1),
    (604, 2, 3, 0, 48, -1), (605, 2, 3, 0, 32, -1), (606, 2, 3, 0, 16, -1), (607, 2, 3, 0, 0, -1),
    (608, 2, 3, 7, 48, 1), (609, 2, 3, 7, 32, 1), (610, 2, 3, 7, 16, 1), (611, 2, 3, 7, 0, 1),
    (612, 2, 3, 6, 48, -1), (613, 2, 3, 6, 32, -1), (614, 2, 3, 6, 16, -1), (615, 2, 3, 6, 0, -1),
    (616, 2, 3, 5, 48, 1), (617, 2, 3, 5, 32, 1), (618, 2, 3, 5, 16, 1), (619, 2, 3, 5, 0, 1),
    (620, 2, 3, 4, 48, -1), (621, 2, 3, 4, 32, -1), (622, 2, 3, 4, 16, -1), (623, 2, 3, 4, 0, -1),
    (624, 2, 0, 3, 48, -1), (625, 2, 0, 3, 32, -1), (626, 2, 0, 3, 16, -1), (627, 2, 0, 3, 0, -1),
    (628, 2, 0, 2, 48, 1), (629, 2, 0, 2, 32, 1), (630, 2, 0, 2, 16, 1), (631, 2, 0, 2, 0, 1),
    (632, 2, 0, 1, 48, -1), (633, 2, 0, 1, 32, -1), (634, 2, 0, 1, 16, -1), (635, 2, 0, 1, 0, -1),
    (636, 2, 0, 0, 48, 1), (637, 2, 0, 0, 32, 1), (638, 2, 0, 0, 16, 1), (639, 2, 0, 0, 0, 1),
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
        numpy uint32 array of shape (1024,).
        ``table[reid]`` gives the corresponding base teid (digi_id).
        Invalid entries are 0xFFFFFFFF.
    """
    re2te = np.full(1024, _INVALID_TEID, dtype=np.uint32)

    for reid, part, seg, layer, first_str, strsqc in _MUC_FEC2ID_MAP:
        teid = _muc_get_int_id(part, seg, layer, first_str)
        if reid < 1024:
            re2te[reid] = teid

    re2te.flags.writeable = False
    return re2te


@lru_cache(maxsize=1)
def build_muc_strsqc() -> np.ndarray:
    """
    Build MUC StrSqc lookup table from embedded MucFec2Id.map data.

    Returns:
        numpy uint32 array of shape (1024,).
    """
    strsqc = np.zeros(1024, dtype=np.uint32)
    for reid, part, seg, layer, first_str, strsqc_val in _MUC_FEC2ID_MAP:
        if reid < 1024:
            strsqc[reid] = strsqc_val + 1

    strsqc.flags.writeable = False
    return strsqc


@lru_cache(maxsize=1)
def build_re2te_tables() -> dict[str, np.ndarray]:
    """
    Build all REID → TEID lookup tables and return as a dict.

    Returns:
        A dict mapping sub-detector names to their corresponding re2te tables.
        Each table is a numpy uint32 array where ``table[reid]`` gives the
        corresponding teid (digi_id), and invalid entries are 0xFFFFFFFF.
    """
    return {
        "mdc": build_mdc_re2te(),
        "tof": build_tof_re2te(),
        "emc": build_emc_re2te(),
        "muc": build_muc_re2te(),
    }
