#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <pybind11/stl.h>
#include <uproot-custom/uproot-custom.hh>

#include <string>
#include <vector>

#include "raw_io.hh"
#include "root_io.hh"

PYBIND11_MODULE( _io, m ) {
    IMPORT_UPROOT_CUSTOM_CPP;

    m.doc() = "Binary Event Structure I/O";

    m.def( "read_bes_raw", &py_read_bes_raw, "Read BES raw data", py::arg( "data" ),
           py::arg( "fields" )      = std::vector<std::string>(),
           py::arg( "info_tables" ) = std::map<std::string, py::array>() );

    // BES3 reader
    declare_reader<Bes3TObjArrayReader, std::string, SharedReader>( m, "Bes3TObjArrayReader" );
    declare_reader<Bes3SymMatrixArrayReader<double>, std::string, uint32_t, uint32_t>(
        m, "Bes3SymMatrixArrayReader" );
    declare_reader<Bes3CgemClusterColReader, std::string>( m, "Bes3CgemClusterColReader" );
}
