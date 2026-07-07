#include "numpy/ndarraytypes.h"
#include "numpy/ufuncobject.h"

#include "mod.hh"

static PyMethodDef MyMethods[] = {
    { "_init_emc_geom", _init_emc_geom, METH_VARARGS,
      "Initialize EMC geometry arrays from numpy arrays." },
    { "_init_mdc_geom", _init_mdc_geom, METH_VARARGS,
      "Initialize MDC geometry arrays from numpy arrays." },
    { NULL, NULL, 0, NULL } /* Sentinel */
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT, "_ufuncs", NULL, -1, MyMethods, NULL, NULL, NULL, NULL };

PyMODINIT_FUNC PyInit__ufuncs( void ) {
    import_array();
    import_umath();

    PyObject* m = PyModule_Create( &moduledef );
    if ( m == NULL ) { return NULL; }

    PyObject* d = PyModule_GetDict( m );

    declare_cgem( d );
    declare_mdc( d );
    declare_tof( d );
    declare_emc( d );

    declare_helix( d );
    declare_identifier( d );

    return m;
}
