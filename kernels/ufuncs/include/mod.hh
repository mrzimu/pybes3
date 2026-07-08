#pragma once

#define PY_SSIZE_T_CLEAN
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#define NPY_TARGET_VERSION NPY_2_0_API_VERSION

#include <Python.h>

void declare_cgem( PyObject* d );
void declare_emc( PyObject* d );
void declare_helix( PyObject* d );
void declare_identifier( PyObject* d );
void declare_mdc( PyObject* d );
void declare_tof( PyObject* d );

PyObject* _init_emc_geom( PyObject* self, PyObject* args );
PyObject* _init_mdc_geom( PyObject* self, PyObject* args );
