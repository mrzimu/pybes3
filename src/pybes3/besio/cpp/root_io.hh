#pragma once

#include <cstdint>
#include <memory>
#include <pybind11/cast.h>
#include <pybind11/detail/common.h>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>

using std::shared_ptr;

namespace py = pybind11;

class BinaryParser {
  public:
    BinaryParser( py::array_t<uint8_t> data, py::array_t<uint32_t> offsets )
        : m_data( static_cast<uint8_t*>( data.request().ptr ) )
        , m_offsets( static_cast<uint32_t*>( offsets.request().ptr ) )
        , m_entries( offsets.request().size - 1 )
        , m_cursor( static_cast<uint8_t*>( data.request().ptr ) ) {}

    const uint64_t m_entries;

    /**
     * @brief Reads a value of type T from the data array.
     *
     * This function reads a value of type T from the data array and advances the cursor by the
     * size of T.
     *
     * @tparam T The type of the value to read.
     * @return The value read from the data array.
     */
    template <typename T>
    const T read() {
        union {
            T value;
            uint8_t bytes[sizeof( T )];
        } src, dst;

        src.value = *reinterpret_cast<const T*>( m_cursor );
        for ( size_t i = 0; i < sizeof( T ); i++ )
            dst.bytes[i] = src.bytes[sizeof( T ) - i - 1];

        m_cursor += sizeof( T );
        return dst.value;
    }

    /**
     * @brief Skips n_bytes in the data array.
     *
     * @param n_bytes The number of bytes to skip.
     */
    void skip( uint32_t n_bytes ) { m_cursor += n_bytes; }

    /**
     * @brief Reads a fNBytes value from the data array.
     *
     * An fNBytes value is a 32-bit unsigned integer, which equals to (nbytes & ~0x40000000) in
     * original data. To read an fNBytes value, we need to & the value with ~0x40000000.
     *
     * @return The value read from the data array.
     */
    const uint32_t read_fNBytes() {
        auto nbytes = read<uint32_t>();
        if ( !( nbytes & 0x40000000 ) )
            throw std::runtime_error( "Invalid fNBytes: " + std::to_string( nbytes ) );
        return nbytes & ~0x40000000;
    }

    /**
     * @brief Reads a fVersion value from the data array. Just a shorthand for
     * read<uint16_t>().
     *
     * An fVersion value is a 16-bit unsigned integer.
     *
     * @return The value read from the data array.
     */
    const uint16_t read_fVersion() { return read<uint16_t>(); }

    /**
     * @brief Reads a null-terminated string from the data array.
     *
     * @return The TString read from the data array.
     */
    const std::string read_null_terminated_string() {
        auto start = m_cursor;
        while ( 1 )
        {
            if ( *m_cursor == 0 ) break;
            m_cursor++;
        }
        m_cursor++;
        return std::string( start, m_cursor );
    }

  private:
    uint8_t* m_cursor;
    const uint8_t* m_data;
    const uint32_t* m_offsets;
};

class BaseReader {
  protected:
    const std::string m_name;

  public:
    BaseReader( std::string_view name ) : m_name( name ) {}
    virtual ~BaseReader()                      = default;
    virtual void read( BinaryParser& bparser ) = 0;
    virtual py::object data()                  = 0;
};

/**
 * @brief Reader for C types.
 *
 * This class reads C types from a binary parser. C types include bool, char, short, int, long,
 * float, double, unsigned char, unsigned short, unsigned int, and unsigned long.
 *
 * @tparam T The type of the C type. It can be bool, int8_t, int16_t, int32_t, int64_t, float,
 * double, uint8_t, uint16_t, uint32_t, or uint64_t.
 */
template <typename T>
class CTypeReader : public BaseReader {
  public:
    CTypeReader( std::string_view name ) : BaseReader( name ), m_data( 0 ) {}

    void read( BinaryParser& bparser ) override { m_data.push_back( bparser.read<T>() ); }

    py::object data() override {
        py::array_t<T> array( m_data.size() );
        auto ptr_data = array.mutable_data();
        std::copy( m_data.begin(), m_data.end(), ptr_data );
        return array;
    }

  private:
    std::vector<T> m_data;
};

/**
 * @brief Reader for STL Sequence.
 *
 * This class reads STL Sequence from a binary parser.
 */
class STLSeqReader : public BaseReader {
  public:
    STLSeqReader( std::string_view name, bool is_top, shared_ptr<BaseReader> element_reader )
        : BaseReader( name )
        , m_is_top( is_top )
        , m_element_reader( element_reader )
        , m_offsets( { 0 } ) {}

    /**
     * @brief Reads data from a BinaryParser object.
     *
     * If an STL Sequence is "top level", it will have fNBytes(4), fVersion(2) at the
     * beginning. Otherwise, it will not have these 2 fields.
     *
     * The case that "is_top" is false is when a sequence is an element of a sequence C-type
     * array (e.g. `vector<int>[N]`).
     *
     * @param bparser The BinaryParser object to read data from.
     */
    void read( BinaryParser& bparser ) override {
        if ( m_is_top )
        {
            bparser.read_fNBytes();
            bparser.read_fVersion();
        }

        auto fSize = bparser.read<uint32_t>();
        m_offsets.push_back( m_offsets.back() + fSize );
        for ( uint32_t i = 0; i < fSize; i++ ) { m_element_reader->read( bparser ); }
    }

    /**
     * @brief Returns the array data of the STL sequence.
     *
     * @return A tuple of counts array and element data.
     */
    py::object data() override {
        py::array_t<uint32_t> offsets_array( m_offsets.size() );
        auto ptr_offsets = offsets_array.mutable_data();
        std::copy( m_offsets.begin(), m_offsets.end(), ptr_offsets );

        py::object element_data = m_element_reader->data();
        return py::make_tuple( offsets_array, element_data );
    }

  private:
    bool m_is_top;

    shared_ptr<BaseReader> m_element_reader;
    std::vector<uint32_t> m_offsets;
};

/**
 * @brief Reader for map.
 *
 * This class reads map from a binary parser.
 */
class STLMapReader : public BaseReader {
  public:
    STLMapReader( std::string_view name, bool is_top, shared_ptr<BaseReader> key_reader,
                  shared_ptr<BaseReader> val_reader )
        : BaseReader( name )
        , m_is_top( is_top )
        , m_key_reader( key_reader )
        , m_val_reader( val_reader )
        , m_offsets( { 0 } ) {}

    /**
     * @brief Reads data from a BinaryParser object.
     *
     * If a map is "top level", it will have fNBytes(4), fVersion(2), Unknown(6) at the
     * beginning. Otherwise, it will not have these 3 fields.
     *
     * The case that "is_top" is false is when a map is an element of a map C-type array
     * (e.g. `map<int, int>[N]`).
     *
     * @param bparser The BinaryParser object to read data from.
     */
    void read( BinaryParser& bparser ) override {
        if ( m_is_top )
        {
            bparser.read_fNBytes();
            bparser.skip( 8 ); // I don't know what these 8 bytes are :(
        }

        auto fSize = bparser.read<uint32_t>();
        m_offsets.push_back( m_offsets.back() + fSize );

        if ( m_is_top )
        {
            for ( uint32_t i = 0; i < fSize; i++ ) { m_key_reader->read( bparser ); }
            for ( uint32_t i = 0; i < fSize; i++ ) { m_val_reader->read( bparser ); }
        }
        else
        {
            for ( uint32_t i = 0; i < fSize; i++ )
            {
                m_key_reader->read( bparser );
                m_val_reader->read( bparser );
            }
        }
    }

    /**
     * @brief Returns the array data of the map.
     *
     * @return A tuple of offsets array, key data, and value data.
     */
    py::object data() override {
        auto key_data = m_key_reader->data();
        auto val_data = m_val_reader->data();

        py::array_t<uint32_t> offsets_array( m_offsets.size() );
        auto ptr_offsets = offsets_array.mutable_data();
        std::copy( m_offsets.begin(), m_offsets.end(), ptr_offsets );

        return py::make_tuple( offsets_array, key_data, val_data );
    }

  private:
    bool m_is_top;

    shared_ptr<BaseReader> m_key_reader;
    shared_ptr<BaseReader> m_val_reader;
    std::vector<uint32_t> m_offsets;
};

class STLStringReader : public BaseReader {
  public:
    STLStringReader( std::string_view name, bool is_top )
        : BaseReader( name ), m_data( 0 ), m_is_top( is_top ), m_offsets( { 0 } ) {}

    void read( BinaryParser& bparser ) override {
        if ( m_is_top )
        {
            bparser.read_fNBytes();
            bparser.read_fVersion();
        }

        uint32_t fSize = bparser.read<uint8_t>();
        if ( fSize == 255 ) { fSize = bparser.read<uint32_t>(); }

        m_offsets.push_back( m_offsets.back() + fSize );
        for ( uint32_t i = 0; i < fSize; i++ ) { m_data.push_back( bparser.read<char>() ); }
    }

    py::object data() override {
        py::array_t<char> data_array( m_data.size() );
        auto ptr_data = data_array.mutable_data();
        std::copy( m_data.begin(), m_data.end(), ptr_data );

        py::array_t<uint32_t> offsets_array( m_offsets.size() );
        auto ptr_offsets = offsets_array.mutable_data();
        std::copy( m_offsets.begin(), m_offsets.end(), ptr_offsets );

        return py::make_tuple( offsets_array, data_array );
    }

  private:
    bool m_is_top;

    std::vector<char> m_data;
    std::vector<uint32_t> m_offsets;
};

/**
 * @brief Reader for TArray.
 *
 * This class reads TArray from a binary parser. TArray includes TArrayC, TArrayS, TArrayI,
 * TArrayL, TArrayF, and TArrayD.
 *
 * There is no limitation that requires the length of TArray to be the same.
 *
 * @tparam T The type of the TArray. It can be int8_t, int16_t, int32_t, int64_t, float, or
 * double.
 */
template <typename T>
class TArrayReader : public BaseReader {
  public:
    TArrayReader( std::string_view name )
        : BaseReader( name ), m_data( 0 ), m_offsets( { 0 } ) {}

    void read( BinaryParser& bparser ) override {
        uint32_t fSize = bparser.read<uint32_t>();
        for ( uint32_t i = 0; i < fSize; i++ ) m_data.push_back( bparser.read<T>() );
        m_offsets.push_back( m_offsets.back() + fSize );
    }

    py::object data() override {
        // prepare data
        py::array_t<T> data_array( m_data.size() );
        auto ptr_data = data_array.mutable_data();
        std::copy( m_data.begin(), m_data.end(), ptr_data );

        // prepare offsets
        py::array_t<uint32_t> offsets_array( m_offsets.size() );
        auto ptr_offsets = offsets_array.mutable_data();
        std::copy( m_offsets.begin(), m_offsets.end(), ptr_offsets );

        return py::make_tuple( offsets_array, data_array );
    }

  private:
    std::vector<T> m_data;
    std::vector<uint32_t> m_offsets;
};

/**
 * @brief Reader for TString.
 *
 * This class reads TString from a binary parser.
 */
class TStringReader : public BaseReader {
  public:
    TStringReader( std::string_view name )
        : BaseReader( name ), m_data( 0 ), m_offsets( { 0 } ) {}

    /**
     * @brief Reads data from a BinaryParser object.
     *
     * TString reading rules:
     * 1. Read an uint_8 as fSize.
     * 2. If fSize == 255, read an uint_32 as fSize
     * 3. Read fSize characters.
     *
     * @param bparser The BinaryParser object to read data from.
     */
    void read( BinaryParser& bparser ) override {
        uint32_t fSize = bparser.read<uint8_t>();
        if ( fSize == 255 ) fSize = bparser.read<uint32_t>();

        for ( uint32_t i = 0; i < fSize; i++ ) m_data.push_back( bparser.read<uint8_t>() );
        m_offsets.push_back( m_offsets.back() + fSize );
    }

    /**
     * @brief Returns the array data of the TString.
     *
     * @return A tuple of offsets array and data array.
     */
    py::object data() override {
        // prepare data
        py::array_t<uint8_t> data_array( m_data.size() );
        auto ptr_data = data_array.mutable_data();
        std::copy( m_data.begin(), m_data.end(), ptr_data );

        // prepare offsets
        py::array_t<uint32_t> offsets_array( m_offsets.size() );
        auto ptr_offsets = offsets_array.mutable_data();
        std::copy( m_offsets.begin(), m_offsets.end(), ptr_offsets );

        return py::make_tuple( offsets_array, data_array );
    }

  private:
    std::vector<uint8_t> m_data;
    std::vector<uint32_t> m_offsets;
};

/**
 * @brief Reader for TObject.
 *
 * This class reads TObject from a binary parser.
 */
class TObjectReader : public BaseReader {
  public:
    TObjectReader( std::string_view name ) : BaseReader( name ) {}

    /**
     * @brief Reads data from a BinaryParser object.
     *
     * TObject reading rules:
     * Read fNBytes(4), fVersion(2), fVersion(2), fUniqueID(4), fBits(4)
     *
     * This class does not store any data, since TObject is a base class.
     *
     * @param bparser The BinaryParser object to read data from.
     */
    void read( BinaryParser& bparser ) override {
        bparser.read_fVersion();
        auto fUniqueID = bparser.read<uint32_t>();
        auto fBits     = bparser.read<uint32_t>();
    }

    /**
     * @brief Returns an empty tuple.
     *
     * @return An empty tuple.
     */
    py::object data() override { return py::none(); }

  private:
};

class CArrayReader : public BaseReader {
  private:
    bool m_is_obj;
    uint32_t m_flat_size;
    shared_ptr<BaseReader> m_element_reader;

  public:
    CArrayReader( std::string_view name, bool is_obj, uint32_t flat_size,
                  shared_ptr<BaseReader> element_reader )
        : BaseReader( name )
        , m_is_obj( is_obj )
        , m_flat_size( flat_size )
        , m_element_reader( element_reader ) {}

    void read( BinaryParser& bparser ) override {
        if ( m_is_obj )
        {
            bparser.read_fNBytes();
            bparser.read_fVersion();
        }

        for ( uint32_t i = 0; i < m_flat_size; i++ ) { m_element_reader->read( bparser ); }
    }

    py::object data() override { return m_element_reader->data(); }
};

/**
 * @brief Reader for a base object.
 *
 * Base object is what a custom object inherits from. It has fNBytes(4), fVersion(2) at the
 * beginning.
 *
 */
class BaseObjectReader : public BaseReader {
  public:
    /**
     * @brief Constructs a BaseObjectReader object.
     *
     * BaseObjectReader reads an object with fNBytes(4), fVersion(2) at the beginning.
     *
     * @param name Reader's name.
     * @param sub_readers The readers for the object's members.
     */
    BaseObjectReader( std::string_view name, std::vector<shared_ptr<BaseReader>> sub_readers )
        : BaseReader( name ), m_sub_readers( sub_readers ) {}

    void read( BinaryParser& bparser ) override {
#ifdef PRINT_DEBUG_INFO
        std::cout << "BaseObjectReader " << m_name << "::read(): " << std::endl;
        for ( int i = 0; i < 40; i++ ) std::cout << (int)bparser.get_cursor()[i] << " ";
        std::cout << std::endl << std::endl;
#endif
        bparser.read_fNBytes();
        bparser.read_fVersion();
        for ( auto& reader : m_sub_readers )
        {
#ifdef PRINT_DEBUG_INFO
            std::cout << "BaseObjectReader " << m_name << ": " << reader->name() << ":"
                      << std::endl;
            for ( int i = 0; i < 40; i++ ) std::cout << (int)bparser.get_cursor()[i] << " ";
            std::cout << std::endl << std::endl;
#endif
            reader->read( bparser );
        }
    }

    /**
     * @brief Returns the data of the object
     *
     * @return A tuple with the data of sub-readers.
     */
    py::object data() override {
        py::list res;
        for ( auto& parser : m_sub_readers ) res.append( parser->data() );
        return res;
    }

  private:
    std::vector<shared_ptr<BaseReader>> m_sub_readers;
};

class ObjectHeaderReader : public BaseReader {
  private:
    std::vector<shared_ptr<BaseReader>> m_sub_readers;

  public:
    ObjectHeaderReader( std::string_view name,
                        std::vector<shared_ptr<BaseReader>> sub_readers )
        : BaseReader( name ), m_sub_readers( sub_readers ) {}

    void read( BinaryParser& bparser ) override {
        bparser.read_fNBytes();
        auto fTag = bparser.read<int32_t>();
        if ( fTag == -1 ) bparser.read_null_terminated_string();

        bparser.read_fNBytes();
        bparser.read_fVersion();
        for ( auto& reader : m_sub_readers ) { reader->read( bparser ); }
    }

    py::object data() override {
        py::list res;
        for ( auto& parser : m_sub_readers ) res.append( parser->data() );
        return res;
    }
};

class EmptyReader : public BaseReader {
  private:
  public:
    EmptyReader( std::string_view name ) : BaseReader( name ) {}

    void read( BinaryParser& bparser ) override {}
    py::object data() override { return py::none(); }
};

class Bes3TObjArrayReader : public BaseReader {
  private:
    shared_ptr<BaseReader> m_element_reader;
    std::vector<uint32_t> m_offsets;

  public:
    Bes3TObjArrayReader( std::string_view name, shared_ptr<BaseReader> element_reader )
        : BaseReader( name ), m_element_reader( element_reader ), m_offsets( { 0 } ) {}

    void read( BinaryParser& bparser ) override {
        bparser.read_fNBytes();
        bparser.read_fVersion();
        bparser.read_fVersion();
        bparser.read<uint32_t>(); // fUniqueID
        bparser.read<uint32_t>(); // fBits

        bparser.read<uint8_t>(); // fName
        auto fSize = bparser.read<uint32_t>();
        bparser.read<uint32_t>(); // fLowerBound

        m_offsets.push_back( m_offsets.back() + fSize );
        for ( uint32_t i = 0; i < fSize; i++ ) { m_element_reader->read( bparser ); }
    }

    py::object data() override {
        py::array_t<uint32_t> offsets_array( m_offsets.size() );
        auto ptr_offsets = offsets_array.mutable_data();
        std::copy( m_offsets.begin(), m_offsets.end(), ptr_offsets );

        py::object element_data = m_element_reader->data();
        return py::make_tuple( offsets_array, element_data );
    }
};

template <typename ReaderType, typename... Args>
shared_ptr<ReaderType> CreateReader( Args... args ) {
    return std::make_shared<ReaderType>( std::forward<Args>( args )... );
}

template <typename ReaderType, typename... Args>
void register_reader( py::module& m, const char* name ) {
    py::class_<ReaderType, shared_ptr<ReaderType>, BaseReader>( m, name ).def(
        py::init( &CreateReader<ReaderType, std::string, Args...> ) );
}

py::object py_read_data( py::array_t<uint8_t> data, py::array_t<uint32_t> offsets,
                         shared_ptr<BaseReader> reader );