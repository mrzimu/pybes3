#include "mod.hh"

#include "numpy/ndarraytypes.h"
#include "numpy/ufuncobject.h"

static PyMethodDef MyMethods[] = {
    { "_init_emc_geom", emc::_init_emc_geom, METH_VARARGS,
      "Initialize EMC geometry arrays from numpy arrays." },
    { "_init_tof_geom", tof::_init_tof_geom, METH_VARARGS,
      "Initialize TOF geometry arrays from numpy arrays." },
    { "_init_mdc_geom", mdc::_init_mdc_geom, METH_VARARGS,
      "Initialize MDC geometry arrays from numpy arrays." },
    { "_init_muc_geom", muc::_init_muc_geom, METH_VARARGS,
      "Initialize MUC geometry arrays from numpy arrays." },
    { NULL, NULL, 0, NULL } /* Sentinel */
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT, "ufuncs", NULL, -1, MyMethods, NULL, NULL, NULL, NULL };

PyMODINIT_FUNC PyInit_ufuncs( void ) {
    import_array();
    import_umath();

    PyObject* m = PyModule_Create( &moduledef );
    if ( m == NULL ) { return NULL; }

    PyObject* d = PyModule_GetDict( m );

    cgem::declare_cgem( d );
    mdc::declare_mdc( d );
    tof::declare_tof( d );
    emc::declare_emc( d );
    muc::declare_muc( d );

    helix::declare_helix( d );
    identifier::declare_identifier( d );

    return m;
}
