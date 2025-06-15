#include "root_io.hh"
#include <pybind11/pybind11.h>

py::object py_read_data( py::array_t<uint8_t> data, py::array_t<uint32_t> offsets,
                         shared_ptr<BaseReader> reader ) {
    BinaryParser parser( data, offsets );
    py::gil_scoped_release release;
    for ( uint64_t i_evt = 0; i_evt < parser.m_entries; i_evt++ ) { reader->read( parser ); }
    py::gil_scoped_acquire acquire;

    return reader->data();
}
