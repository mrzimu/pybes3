#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <pybind11/stl.h>

#include <string>
#include <vector>

#include "raw_io.hh"
#include "root_io.hh"

PYBIND11_MODULE( besio_cpp, m ) {
    m.doc() = "Binary Event Structure I/O";

    m.def( "read_data", &py_read_data, "Read data from a BinaryParser", py::arg( "data" ),
           py::arg( "offsets" ), py::arg( "reader" ) );

    m.def( "read_bes_raw", &py_read_bes_raw, "Read BES raw data", py::arg( "data" ),
           py::arg( "sub_detectors" ) = std::vector<std::string>() );

    py::class_<BaseReader, shared_ptr<BaseReader>>( m, "BaseReader" );

    // CTypeReader classes
    register_reader<CTypeReader<int8_t>>( m, "Int8Reader" );
    register_reader<CTypeReader<int16_t>>( m, "Int16Reader" );
    register_reader<CTypeReader<int32_t>>( m, "Int32Reader" );
    register_reader<CTypeReader<int64_t>>( m, "Int64Reader" );
    register_reader<CTypeReader<uint8_t>>( m, "UInt8Reader" );
    register_reader<CTypeReader<uint16_t>>( m, "UInt16Reader" );
    register_reader<CTypeReader<uint32_t>>( m, "UInt32Reader" );
    register_reader<CTypeReader<uint64_t>>( m, "UInt64Reader" );
    register_reader<CTypeReader<float>>( m, "FloatReader" );
    register_reader<CTypeReader<double>>( m, "DoubleReader" );

    // STL Readers
    register_reader<STLSeqReader, bool, shared_ptr<BaseReader>>( m, "STLSeqReader" );
    register_reader<STLMapReader, bool, shared_ptr<BaseReader>, shared_ptr<BaseReader>>(
        m, "STLMapReader" );
    register_reader<STLStringReader, bool>( m, "STLStringReader" );

    // TArrayReader classes
    register_reader<TArrayReader<int8_t>>( m, "TArrayCReader" );
    register_reader<TArrayReader<int16_t>>( m, "TArraySReader" );
    register_reader<TArrayReader<int32_t>>( m, "TArrayIReader" );
    register_reader<TArrayReader<int64_t>>( m, "TArrayLReader" );
    register_reader<TArrayReader<float>>( m, "TArrayFReader" );
    register_reader<TArrayReader<double>>( m, "TArrayDReader" );

    // Other readers
    register_reader<TStringReader>( m, "TStringReader" );
    register_reader<TObjectReader>( m, "TObjectReader" );
    register_reader<CArrayReader, bool, uint32_t, shared_ptr<BaseReader>>( m, "CArrayReader" );
    register_reader<BaseObjectReader, std::vector<shared_ptr<BaseReader>>>(
        m, "BaseObjectReader" );
    register_reader<ObjectHeaderReader, std::vector<shared_ptr<BaseReader>>>(
        m, "ObjectHeaderReader" );
    register_reader<EmptyReader>( m, "EmptyReader" );

    // BES3 reader
    register_reader<Bes3TObjArrayReader, shared_ptr<BaseReader>>( m, "Bes3TObjArrayReader" );
}
