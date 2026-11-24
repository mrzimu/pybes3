#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <pybind11/stl.h>
#include <uproot-custom/uproot-custom.hh>

#include <string>
#include <vector>

#include "raw_file.hh"
#include "raw_io.hh"
#include "root_io.hh"

PYBIND11_MODULE( _io, m ) {
    IMPORT_UPROOT_CUSTOM_CPP;

    m.doc() = "Binary Event Structure I/O";

    m.def( "read_bes_raw", &py_read_bes_raw, "Read BES raw data", py::arg( "data" ),
           py::arg( "fields" )      = std::vector<std::string>(),
           py::arg( "info_tables" ) = std::map<std::string, py::array>() );

    py::class_<RawFileReader>( m, "RawFileReader" )
        .def( py::init<const std::string&>(), py::arg( "path" ) )
        .def( "read", &RawFileReader::read, py::arg( "entry_start" ), py::arg( "n_events" ),
              py::arg( "fields" ), py::arg( "info_tables" ) )
        .def( "build_entry_index", &RawFileReader::build_entry_index,
              py::call_guard<py::gil_scoped_release>() )
        .def( "index_valid", &RawFileReader::index_valid )
        .def( "entry_starts", &RawFileReader::entry_starts )
        .def( "entry_stops", &RawFileReader::entry_stops )
        .def( "read_block", &RawFileReader::read_block, py::arg( "n_blocks" ) )
        .def( "close", &RawFileReader::close )
        .def_property_readonly( "closed", &RawFileReader::closed )
        .def_property_readonly( "file_version", &RawFileReader::file_version )
        .def_property_readonly( "file_number", &RawFileReader::file_number )
        .def_property_readonly( "file_date", &RawFileReader::file_date )
        .def_property_readonly( "file_time", &RawFileReader::file_time )
        .def_property_readonly( "file_name", &RawFileReader::file_name )
        .def_property_readonly( "file_tag", &RawFileReader::file_tag )
        .def_property_readonly( "run_number", &RawFileReader::run_number )
        .def_property_readonly( "max_events", &RawFileReader::max_events )
        .def_property_readonly( "rec_enable", &RawFileReader::rec_enable )
        .def_property_readonly( "trigger_type", &RawFileReader::trigger_type )
        .def_property_readonly( "detector_mask", &RawFileReader::detector_mask )
        .def_property_readonly( "beam_type", &RawFileReader::beam_type )
        .def_property_readonly( "beam_energy", &RawFileReader::beam_energy )
        .def_property_readonly( "entries", &RawFileReader::entries )
        .def_property_readonly( "data_start", &RawFileReader::data_start )
        .def_property_readonly( "data_end", &RawFileReader::data_end )
        .def_property_readonly( "size", &RawFileReader::size );

    // BES3 reader
    declare_reader<Bes3TObjArrayReader, std::string, SharedReader>( m, "Bes3TObjArrayReader" );
    declare_reader<Bes3SymMatrixArrayReader<double>, std::string, uint32_t, uint32_t>(
        m, "Bes3SymMatrixArrayReader" );
    declare_reader<Bes3CgemClusterColReader, std::string>( m, "Bes3CgemClusterColReader" );
}
