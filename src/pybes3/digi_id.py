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

from pybes3.identifier import *  # noqa: F401, F403
from pybes3.identifier import (  # noqa: F401
    _tof_id_to_layer_or_module_1,
    _tof_id_to_layer_or_module_2,
    _tof_id_to_phi_or_strip_1,
    _tof_id_to_phi_or_strip_2,
)
