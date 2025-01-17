#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <pybind11/stl.h>

#include <string>
#include <vector>

#include "raw_io.hh"
#include "root_io.hh"

PYBIND11_MODULE( besio_cpp, m ) {
    m.doc() = "Binary Event Structure I/O";

    m.def( "read_bes_tobjarray", &py_read_bes_tobjarray,
           "Read BES TObjArray, which can only contain 1 type of class" );

    m.def( "read_bes_tobject", &py_read_bes_tobject, "Read BES TObject" );

    m.def( "read_bes_stl", &py_read_bes_stl, "Read BES STL" );

    m.def( "read_bes_raw", &py_read_bes_raw, "Read BES raw data", py::arg( "data" ),
           py::arg( "sub_detectors" ) = std::vector<std::string>() );
}