#pragma once

#define PY_SSIZE_T_CLEAN
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#define NPY_TARGET_VERSION NPY_2_0_API_VERSION

#include <Python.h>

namespace helix {
    void declare_helix( PyObject* d );
}

namespace identifier {
    void declare_identifier( PyObject* d );
}

namespace cgem {
    void declare_cgem( PyObject* d );
}

namespace mdc {
    void declare_mdc( PyObject* d );
    PyObject* _init_mdc_geom( PyObject* self, PyObject* args );
} // namespace mdc

namespace tof {
    void declare_tof( PyObject* d );
    PyObject* _init_tof_geom( PyObject* self, PyObject* args );
} // namespace tof

namespace emc {
    void declare_emc( PyObject* d );
    PyObject* _init_emc_geom( PyObject* self, PyObject* args );
} // namespace emc

namespace muc {
    void declare_muc( PyObject* d );
    PyObject* _init_muc_geom( PyObject* self, PyObject* args );
} // namespace muc
