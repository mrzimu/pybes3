#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>

#include "BesEventReader.hh"
#include "ModuleFunctions.hh"

namespace py = pybind11;

PYBIND11_MODULE( _cpp_besio, m ) {

    py::class_<BesEventReader>( m, "_Bes3EventReader" )
        .def( py::init<const std::vector<std::string>>() )
        .def( "get_entries", &BesEventReader::py_get_entries )
        .def( "get_available_fields", &BesEventReader::py_get_available_fields )
        .def( "arrays", &BesEventReader::py_arrays );

    m.def( "is_bes_format", &py_is_bes_format );
}