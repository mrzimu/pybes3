#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <pybind11/stl.h>
#include <uproot-custom/uproot-custom.hh>

#include <string>
#include <vector>

#include "raw_io.hh"
#include "root_io.hh"

PYBIND11_MODULE( besio_cpp, m ) {
    IMPORT_UPROOT_CUSTOM_CPP;

    m.doc() = "Binary Event Structure I/O";

    m.def( "read_bes_raw", &py_read_bes_raw, "Read BES raw data", py::arg( "data" ),
           py::arg( "sub_detectors" ) = std::vector<std::string>() );

    // BES3 reader
    register_reader<Bes3TObjArrayReader, SharedReader>( m, "Bes3TObjArrayReader" );
    register_reader<Bes3SymMatrixArrayReader<double>, uint32_t, uint32_t>(
        m, "Bes3SymMatrixArrayReader" );
    register_reader<Bes3CgemClusterColReader>( m, "Bes3CgemClusterColReader" );
}
