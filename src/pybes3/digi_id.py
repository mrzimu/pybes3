"""
Backward compatibility shim. Use :mod:`pybes3.identifier` instead.

.. deprecated::
    This module will be removed in a future release.
    Import from :mod:`pybes3.identifier` directly.
"""

from __future__ import annotations

import warnings

warnings.warn(
    "pybes3.digi_id is deprecated and will be removed in a future release. "
    "Use pybes3.identifier instead.",
    DeprecationWarning,
    stacklevel=2,
)

from pybes3.identifier import _tof_id_to_layer_or_module_1 as _tof_id_to_layer_or_module_1
from pybes3.identifier import _tof_id_to_layer_or_module_2 as _tof_id_to_layer_or_module_2
from pybes3.identifier import _tof_id_to_phi_or_strip_1 as _tof_id_to_phi_or_strip_1
from pybes3.identifier import _tof_id_to_phi_or_strip_2 as _tof_id_to_phi_or_strip_2
from pybes3.identifier import cgem_id_to_gid as cgem_id_to_gid
from pybes3.identifier import cgem_id_to_layer as cgem_id_to_layer
from pybes3.identifier import cgem_id_to_sheet as cgem_id_to_sheet
from pybes3.identifier import cgem_id_to_strip as cgem_id_to_strip
from pybes3.identifier import cgem_id_to_strip_type as cgem_id_to_strip_type
from pybes3.identifier import check_cgem_id as check_cgem_id
from pybes3.identifier import check_emc_id as check_emc_id
from pybes3.identifier import check_mdc_id as check_mdc_id
from pybes3.identifier import check_muc_id as check_muc_id
from pybes3.identifier import check_tof_id as check_tof_id
from pybes3.identifier import emc_id_to_gid as emc_id_to_gid
from pybes3.identifier import emc_id_to_module as emc_id_to_module
from pybes3.identifier import emc_id_to_phi as emc_id_to_phi
from pybes3.identifier import emc_id_to_theta as emc_id_to_theta
from pybes3.identifier import get_cgem_id as get_cgem_digi_id
from pybes3.identifier import get_emc_id as get_emc_digi_id
from pybes3.identifier import get_mdc_id as get_mdc_digi_id
from pybes3.identifier import get_muc_id as get_muc_digi_id
from pybes3.identifier import get_tof_id as get_tof_digi_id
from pybes3.identifier import mdc_id_to_gid as mdc_id_to_gid
from pybes3.identifier import mdc_id_to_is_stereo as mdc_id_to_is_stereo
from pybes3.identifier import mdc_id_to_layer as mdc_id_to_layer
from pybes3.identifier import mdc_id_to_wire as mdc_id_to_wire
from pybes3.identifier import muc_id_to_channel as muc_id_to_channel
from pybes3.identifier import muc_id_to_gap as muc_id_to_gap
from pybes3.identifier import muc_id_to_layer as muc_id_to_layer
from pybes3.identifier import muc_id_to_part as muc_id_to_part
from pybes3.identifier import muc_id_to_segment as muc_id_to_segment
from pybes3.identifier import muc_id_to_strip as muc_id_to_strip
from pybes3.identifier import parse_cgem_id as parse_cgem_digi_id
from pybes3.identifier import parse_emc_digi as parse_emc_digi
from pybes3.identifier import parse_emc_id as parse_emc_digi_id
from pybes3.identifier import parse_mdc_digi as parse_mdc_digi
from pybes3.identifier import parse_mdc_id as parse_mdc_digi_id
from pybes3.identifier import parse_muc_id as parse_muc_digi_id
from pybes3.identifier import parse_tof_id as parse_tof_digi_id
from pybes3.identifier import tof_id_to_end as tof_id_to_end
from pybes3.identifier import tof_id_to_gid as tof_id_to_gid
from pybes3.identifier import tof_id_to_layer_or_module as tof_id_to_layer_or_module
from pybes3.identifier import tof_id_to_part as tof_id_to_part
from pybes3.identifier import tof_id_to_phi_or_strip as tof_id_to_phi_or_strip

__all__ = [
    "_tof_id_to_layer_or_module_1",
    "_tof_id_to_layer_or_module_2",
    "_tof_id_to_phi_or_strip_1",
    "_tof_id_to_phi_or_strip_2",
    "cgem_id_to_gid",
    "cgem_id_to_layer",
    "cgem_id_to_sheet",
    "cgem_id_to_strip",
    "cgem_id_to_strip_type",
    "check_cgem_id",
    "check_emc_id",
    "check_mdc_id",
    "check_muc_id",
    "check_tof_id",
    "emc_id_to_gid",
    "emc_id_to_module",
    "emc_id_to_phi",
    "emc_id_to_theta",
    "get_cgem_digi_id",
    "get_emc_digi_id",
    "get_mdc_digi_id",
    "get_muc_digi_id",
    "get_tof_digi_id",
    "mdc_id_to_gid",
    "mdc_id_to_is_stereo",
    "mdc_id_to_layer",
    "mdc_id_to_wire",
    "muc_id_to_channel",
    "muc_id_to_gap",
    "muc_id_to_layer",
    "muc_id_to_part",
    "muc_id_to_segment",
    "muc_id_to_strip",
    "parse_cgem_digi_id",
    "parse_emc_digi",
    "parse_emc_digi_id",
    "parse_mdc_digi",
    "parse_mdc_digi_id",
    "parse_muc_digi_id",
    "parse_tof_digi_id",
    "tof_id_to_end",
    "tof_id_to_gid",
    "tof_id_to_layer_or_module",
    "tof_id_to_part",
    "tof_id_to_phi_or_strip",
]
