#pragma once

#include <pybind11/cast.h>
#include <pybind11/detail/common.h>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>

#include <cstdint>
#include <iostream>
#include <memory>
#include <set>
#include <stdexcept>
#include <string>
#include <string_view>
#include <tuple>
#include <vector>

namespace py = pybind11;

class RootBinaryParser {
    //  fName(1), fSize(4), fLowerBound(4)
    using InfoTObjArray = const std::tuple<uint8_t, uint32_t, uint32_t>;

    // fNBytes(4), fTag(4), fClassName(n)
    using InfoObjHeader = const std::tuple<const uint32_t, const int32_t, const std::string>;

  public:
    /**
     * @brief Constructs a BinaryParser object.
     *
     * This constructor initializes a BinaryParser object with the provided data and offsets
     * arrays.
     *
     * @param data The basket data array.
     * @param offsets The entry byte offsets array.
     */
    RootBinaryParser( py::array_t<uint8_t> data, py::array_t<uint32_t> offsets )
        : m_data( static_cast<uint8_t*>( data.request().ptr ) )
        , m_offsets( static_cast<uint32_t*>( offsets.request().ptr ) )
        , m_entries( offsets.request().size - 1 )
        , m_cursor( static_cast<uint8_t*>( data.request().ptr ) ) {}

    /**
     * @brief The number of entries in the data structure.
     */
    const uint64_t m_entries;

    /**
     * @brief The current cursor position.
     */
    const uint8_t* get_cursor() const { return m_cursor; }

    /**
     * @brief The data array.
     */
    const uint8_t* get_data() const { return m_data; }

    /* ================================= Readers ================================== */

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
     * @brief Reads a fNBytes value from the data array.
     *
     * An fNBytes value is a 32-bit unsigned integer, which equals to (nbytes & ~0x40000000) in
     * original data. To read an fNBytes value, we need to & the value with ~0x40000000.
     *
     * @return The value read from the data array.
     */
    const uint32_t read_fNBytes() {
        auto nbytes = read<uint32_t>();
#ifdef SAFETY_PARSE
        if ( !( nbytes & 0x40000000 ) )
            throw std::runtime_error( "Invalid fNBytes: " + std::to_string( nbytes ) );
#endif
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
     * @brief Reads a TObjArray information from the data array.
     *
     * A TObjArray information consists of TObject, fName, fSize, and fLowerBound. This
     * function reads last three values from the data array and advances the cursor
     * accordingly.
     *
     * @return A tuple of fName, fSize, and fLowerBound.
     */
    InfoTObjArray read_TObjArray() {
        // Read TObject first
        auto fNBytes   = read_fNBytes();
        auto fVersion1 = read_fVersion();
        auto fVersion2 = read_fVersion();
        auto fUniqueID = read<uint32_t>();
        auto fBits     = read<uint32_t>();

        // Read TObjArray information
        auto fName       = read<uint8_t>();
        auto fSize       = read<uint32_t>();
        auto fLowerBound = read<uint32_t>();
        return std::make_tuple( fName, fSize, fLowerBound );
    }

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

    /**
     * @brief Reads an Object's header information from the data array.
     *
     * An Object's header information consists of fNBytes, fTag and fClassName(only when
     * fTag==-1).
     *
     * @return A tuple of fNBytes, fTag, and fClassName.
     */
    InfoObjHeader read_ObjHeader() {
        auto fNBytes           = read_fNBytes();
        auto fTag              = read<int32_t>();
        std::string fClassName = ( fTag == -1 ) ? read_null_terminated_string() : "";
        return std::make_tuple( fNBytes, fTag, fClassName );
    }

    /* ================================= Skippers ================================= */

    /**
     * @brief Skips n_bytes in the data array.
     *
     * @param n_bytes The number of bytes to skip.
     */
    void skip( uint32_t n_bytes ) { m_cursor += n_bytes; }

    /**
     * @brief Skips an fNBytes value in the data array.
     */
    void skip_fNBytes() {
#ifdef SAFETY_PARSE
        read_fNBytes();
#else
        skip( 4 );
#endif
    }

    /**
     * @brief Skips an fVersion value in the data array.
     */
    void skip_fVersion() { skip( 2 ); }

    /**
     * @brief Skips a null-terminated string in the data array.
     */
    void skip_null_terminated_string() {
        while ( *m_cursor++ )
            ;
    }

    /**
     * @brief Skips an Object's header information in the data array.
     */
    void skip_ObjHeader() {
        skip_fNBytes();
        auto fTag = read<int32_t>();
        if ( fTag == -1 ) skip_null_terminated_string();
    }

  private:
    /**
     * @brief The current cursor position.
     */
    uint8_t* m_cursor;

    /**
     * @brief The data array pointer.
     */
    const uint8_t* m_data;

    /**
     * @brief The entry byte offsets array pointer.
     */
    const uint32_t* m_offsets;
};

/**
 * @brief Interface for reading items.
 *
 * This interface defines the common methods for reading items.
 */
class IItemReader {
  public:
    virtual ~IItemReader() = default;

    /**
     * @brief Get the name of the item.
     *
     * @return The name of the item as a string view.
     */
    virtual std::string_view name() = 0;

    /**
     * @brief Read the item from a binary parser.
     *
     * @param bparser The binary parser to read from.
     */
    virtual void read( RootBinaryParser& bparser ) = 0;

    /**
     * @brief Get the data of the item.
     *
     * @return The data of the item as a Python tuple.
     */
    virtual py::tuple data() = 0;
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
class CTypeReader : public IItemReader {
  public:
    CTypeReader( std::string_view name ) : m_name( name ), m_data( 0 ) {}

    std::string_view name() override { return m_name; }

    void read( RootBinaryParser& bparser ) override { m_data.push_back( bparser.read<T>() ); }

    py::tuple data() override {
        py::array_t<T> array( m_data.size() );
        auto ptr_data = array.mutable_data();
        std::copy( m_data.begin(), m_data.end(), ptr_data );
        return py::make_tuple( array );
    }

  private:
    const std::string m_name;

    std::vector<T> m_data;
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
class TArrayReader : public IItemReader {
  public:
    TArrayReader( std::string_view name ) : m_name( name ), m_data( 0 ), m_offsets( { 0 } ) {}

    std::string_view name() override { return m_name; }

    void read( RootBinaryParser& bparser ) override {
        uint32_t fSize = bparser.read<uint32_t>();
        for ( uint32_t i = 0; i < fSize; i++ ) m_data.push_back( bparser.read<T>() );
        m_offsets.push_back( m_data.size() );
    }

    py::tuple data() override {
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
    const std::string m_name;

    std::vector<T> m_data;
    std::vector<uint32_t> m_offsets;
};

/**
 * @brief Reader for TString.
 *
 * This class reads TString from a binary parser.
 */
class TStringReader : public IItemReader {
  public:
    TStringReader( std::string_view name ) : m_name( name ), m_data( 0 ), m_offsets( { 0 } ) {}

    std::string_view name() override { return m_name; }

    /**
     * @brief Reads data from a BinaryParser object.
     *
     * TString reading rules:
     * 1. Read an uint_8 as n_chars.
     * 2. If n_chars == 255, read an uint_32 as n_chars
     * 3. Read n_chars characters.
     *
     * @param bparser The BinaryParser object to read data from.
     */
    void read( RootBinaryParser& bparser ) override {
        uint32_t n_chars = bparser.read<uint8_t>();
        if ( n_chars == 255 ) n_chars = bparser.read<uint32_t>();

        for ( uint32_t i = 0; i < n_chars; i++ ) m_data.push_back( bparser.read<char>() );
        m_offsets.push_back( m_data.size() );
    }

    /**
     * @brief Returns the array data of the TString.
     *
     * @return A tuple of offsets array and data array.
     */
    py::tuple data() override {
        // prepare data
        py::array_t<char> data_array( m_data.size() );
        auto ptr_data = data_array.mutable_data();
        std::copy( m_data.begin(), m_data.end(), ptr_data );

        // prepare offsets
        py::array_t<uint32_t> offsets_array( m_offsets.size() );
        auto ptr_offsets = offsets_array.mutable_data();
        std::copy( m_offsets.begin(), m_offsets.end(), ptr_offsets );

        return py::make_tuple( offsets_array, data_array );
    }

  private:
    const std::string m_name;

    std::vector<char> m_data;
    std::vector<uint32_t> m_offsets;
};

/**
 * @brief Reader for TObject.
 *
 * This class reads TObject from a binary parser.
 */
class TObjectReader : public IItemReader {
  public:
    TObjectReader( std::string_view name ) : m_name( name ) {}

    std::string_view name() override { return m_name; }

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
    void read( RootBinaryParser& bparser ) override {
        bparser.read_fVersion();
        auto fUniqueID = bparser.read<uint32_t>();
        auto fBits     = bparser.read<uint32_t>();
    }

    /**
     * @brief Returns an empty tuple.
     *
     * @return An empty tuple.
     */
    py::tuple data() override { return py::make_tuple(); }

  private:
    const std::string m_name;
};

/**
 * @brief Reader for vector.
 *
 * This class reads vector from a binary parser.
 */
class VectorReader : public IItemReader {
  public:
    VectorReader( std::string_view name, std::unique_ptr<IItemReader> element_reader )
        : m_name( name )
        , m_is_top( true )
        , m_element_reader( std::move( element_reader ) )
        , m_offsets( { 0 } ) {}

    std::string_view name() override { return m_name; }

    /**
     * @brief Reads data from a BinaryParser object.
     *
     * If a vector is "top level", it will have fNBytes(4), fVersion(2) at the beginning.
     * Otherwise, it will not have these 2 fields.
     *
     * The case that "is_top" is false is when a vector is an element of a vector C-type array
     * (e.g. `vector<int>[N]`).
     *
     * @param bparser The BinaryParser object to read data from.
     */
    void read( RootBinaryParser& bparser ) override {
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
     * @brief Set whether this reader is the top reader.
     *
     * @param is_top Whether this reader is the top reader.
     */
    void set_is_top( const bool is_top ) { m_is_top = is_top; }

    /**
     * @brief Returns the array data of the vector.
     *
     * @return A tuple of offsets array and element data.
     */
    py::tuple data() override {
        py::array_t<uint32_t> offsets_array( m_offsets.size() );
        auto ptr_offsets = offsets_array.mutable_data();
        std::copy( m_offsets.begin(), m_offsets.end(), ptr_offsets );

        py::tuple element_data = m_element_reader->data();

        return py::make_tuple( offsets_array, element_data );
    }

  private:
    const std::string m_name;
    bool m_is_top;

    std::unique_ptr<IItemReader> m_element_reader;
    std::vector<uint32_t> m_offsets;
};

/**
 * @brief Reader for map.
 *
 * This class reads map from a binary parser.
 */
class MapReader : public IItemReader {
  public:
    MapReader( std::string_view name, std::unique_ptr<IItemReader> key_reader,
               std::unique_ptr<IItemReader> val_reader )
        : m_name( name )
        , m_is_top( true )
        , m_key_reader( std::move( key_reader ) )
        , m_val_reader( std::move( val_reader ) )
        , m_offsets( { 0 } ) {}

    std::string_view name() override { return m_name; }

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
    void read( RootBinaryParser& bparser ) override {
        if ( m_is_top )
        {
            bparser.read_fNBytes();
            bparser.skip( 8 ); // I don't know what these 8 bytes are :(
        }

        auto fSize = bparser.read<uint32_t>();
        m_offsets.push_back( m_offsets.back() + fSize );
        for ( uint32_t i = 0; i < fSize; i++ ) { m_key_reader->read( bparser ); }
        for ( uint32_t i = 0; i < fSize; i++ ) { m_val_reader->read( bparser ); }
    }

    /**
     * @brief Returns the array data of the map.
     *
     * @return A tuple of offsets array, key data, and value data.
     */
    py::tuple data() override {
        auto key_data = m_key_reader->data();
        auto val_data = m_val_reader->data();

        py::array_t<uint32_t> offsets_array( m_offsets.size() );
        auto ptr_offsets = offsets_array.mutable_data();
        std::copy( m_offsets.begin(), m_offsets.end(), ptr_offsets );

        return py::make_tuple( offsets_array, key_data, val_data );
    }

    /**
     * @brief Set whether this reader is the top reader.
     *
     * @param is_top Whether this reader is the top reader.
     */
    void set_is_top( const bool is_top ) { m_is_top = is_top; }

  private:
    const std::string m_name;
    bool m_is_top;

    std::unique_ptr<IItemReader> m_key_reader;
    std::unique_ptr<IItemReader> m_val_reader;
    std::vector<uint32_t> m_offsets;
};

/**
 * @brief Reader for a simple array.
 *
 * Simple array means no extra header located at the beginning of the array.
 * To the contrary, ObjArrayReader reads an array with fNBytes(4), fVersion(2) at the
 * beginning.
 */
class SimpleArrayReader : public IItemReader {
  public:
    /**
     * @brief Constructs a SimpleArrayReader object.
     *
     * ArrayReader does not read arrays with shape. It reads arrays with a flattened size.
     *
     * @param name Reader's name.
     * @param reader The reader for the array elements.
     * @param flatten_size The flattened size of the array.
     */
    SimpleArrayReader( std::string_view name, std::unique_ptr<IItemReader> reader,
                       uint32_t flatten_size )
        : m_name( name ), m_flatten_size( flatten_size ), m_reader( std::move( reader ) ) {}

    std::string_view name() override { return m_name; }

    void read( RootBinaryParser& bparser ) override {
        for ( int i = 0; i < m_flatten_size; i++ ) { m_reader->read( bparser ); }
    }

    /**
     * @brief Returns the data of the array.
     *
     * @return A tuple with 1 element: the flattened data.
     */
    py::tuple data() override { return m_reader->data(); }

  private:
    const std::string m_name;
    const uint32_t m_flatten_size;

    std::unique_ptr<IItemReader> m_reader;
};

/**
 * @brief Reader for an object array.
 *
 * This class reads an object array from a binary parser.
 *
 * This is not TObjArray reader! It reads `TObject[n]` like data, which contains fNBytes(4),
 * fVersion(2) at the beginning.
 */
class ObjArrayReader : public IItemReader {
  public:
    /**
     * @brief Constructs an ObjArrayReader object.
     *
     * ObjArrayReader reads an array with fNBytes(4), fVersion(2) at the beginning.
     * It reads arrays with a flattened size.
     *
     * @param name Reader's name.
     * @param reader The reader for the array elements.
     * @param flatten_size The flattened size of the array.
     */
    ObjArrayReader( std::string_view name, std::unique_ptr<IItemReader> reader,
                    uint32_t flatten_size )
        : m_name( name ), m_flatten_size( flatten_size ), m_reader( std::move( reader ) ) {}

    std::string_view name() override { return m_name; }

    void read( RootBinaryParser& bparser ) override {
        bparser.read_fNBytes();
        bparser.read_fVersion();
        for ( int i = 0; i < m_flatten_size; i++ ) { m_reader->read( bparser ); }
    }

    /**
     * @brief Returns the data of the array.
     *
     * @return A tuple with 1 element: the flattened data.
     */
    py::tuple data() override { return m_reader->data(); }

  private:
    const std::string m_name;
    const uint32_t m_flatten_size;

    std::unique_ptr<IItemReader> m_reader;
};

/**
 * @brief Reader for a base object.
 *
 * Base object is what a custom object inherits from. It has fNBytes(4), fVersion(2) at the
 * beginning.
 *
 */
class BaseObjectReader : public IItemReader {
  public:
    /**
     * @brief Constructs a BaseObjectReader object.
     *
     * BaseObjectReader reads an object with fNBytes(4), fVersion(2) at the beginning.
     *
     * @param name Reader's name.
     * @param sub_readers The readers for the object's members.
     */
    BaseObjectReader( std::string_view name,
                      std::vector<std::unique_ptr<IItemReader>> sub_readers )
        : m_name( name ), m_sub_readers( std::move( sub_readers ) ) {}

    std::string_view name() override { return m_name; }

    void read( RootBinaryParser& bparser ) override {
#ifdef PRINT_DEBUG_INFO
        std::cout << "BaseObjectReader " << m_name << "::read(): " << std::endl;
        for ( int i = 0; i < 40; i++ ) std::cout << (int)bparser.get_cursor()[i] << " ";
        std::cout << std::endl << std::endl;
#endif
        bparser.skip_fNBytes();
        bparser.skip_fVersion();
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
    py::tuple data() override {
        py::list res;
        for ( auto& parser : m_sub_readers ) res.append( parser->data() );
        return py::tuple( res );
    }

  private:
    const std::string m_name;
    std::vector<std::unique_ptr<IItemReader>> m_sub_readers;
};

/**
 * @brief Reader for an object.
 *
 * This class reads an object from a binary parser.
 * An object start with an object header.
 */
class ObjectReader : public IItemReader {
  public:
    ObjectReader( std::string_view name,
                  std::vector<std::unique_ptr<IItemReader>> sub_readers )
        : m_name( name ), m_sub_readers( std::move( sub_readers ) ) {}

    std::string_view name() override { return m_name; }

    void read( RootBinaryParser& bparser ) override {
#ifdef PRINT_DEBUG_INFO
        std::cout << "ObjectReader(" + m_name + ")" << m_name << "::read(): " << std::endl;
        for ( int i = 0; i < 40; i++ ) std::cout << (int)bparser.get_cursor()[i] << " ";
        std::cout << std::endl << std::endl;
#endif
        bparser.read_ObjHeader();
        bparser.skip_fNBytes();
        bparser.skip_fVersion();
        for ( auto& reader : m_sub_readers )
        {
#ifdef PRINT_DEBUG_INFO
            std::cout << "ObjectReader(" + m_name + ")" << m_name << ": " << reader->name()
                      << ":" << std::endl;
            for ( int i = 0; i < 40; i++ ) std::cout << (int)bparser.get_cursor()[i] << " ";
            std::cout << std::endl << std::endl;
#endif
            reader->read( bparser );
        }
    }

    /**
     * @brief Returns the data of the TClass object.
     *
     * @return A tuple with the data of sub-readers.
     */
    py::tuple data() override {
        py::list res;
        for ( auto& parser : m_sub_readers ) res.append( parser->data() );
        return py::tuple( res );
    }

  private:
    const std::string m_name;
    std::vector<std::unique_ptr<IItemReader>> m_sub_readers;
};

const std::string kBool   = "bool";
const std::string kChar   = "char";
const std::string kShort  = "short";
const std::string kInt    = "int";
const std::string kLong   = "long";
const std::string kFloat  = "float";
const std::string kDouble = "double";
const std::string kUChar  = "unsigned char";
const std::string kUShort = "unsigned short";
const std::string kUInt   = "unsigned int";
const std::string kULong  = "unsigned long";
const std::string kInt8   = "int8_t";
const std::string kUInt8  = "uint8_t";
const std::string kInt16  = "int16_t";
const std::string kUInt16 = "uint16_t";
const std::string kInt32  = "int32_t";
const std::string kUInt32 = "uint32_t";
const std::string kInt64  = "int64_t";
const std::string kUInt64 = "uint64_t";

const std::string kBASE     = "BASE";
const std::string kTString  = "TString";
const std::string kTObject  = "TObject";
const std::string kVector   = "vector";
const std::string kMap      = "map";
const std::string kSet      = "set";
const std::string kList     = "list";
const std::string kDeque    = "deque";
const std::string kMultimap = "multimap";
const std::string kMultiset = "multiset";

const std::string kTArrayC = "TArrayC";
const std::string kTArrayS = "TArrayS";
const std::string kTArrayI = "TArrayI";
const std::string kTArrayL = "TArrayL";
const std::string kTArrayF = "TArrayF";
const std::string kTArrayD = "TArrayD";

const std::set<std::string> CTYPE_NAMES = {
    kBool,  kChar, kShort, kInt,   kLong,   kFloat, kDouble, kUChar, kUShort, kUInt,
    kULong, kInt8, kUInt8, kInt16, kUInt16, kInt32, kUInt32, kInt64, kUInt64 };

const std::set<std::string> STL_NAMES = { kVector, kMap,      kSet,     kList,
                                          kDeque,  kMultimap, kMultiset };

const std::set<std::string> TARRAY_NAMES = { kTArrayC, kTArrayS, kTArrayI,
                                             kTArrayL, kTArrayF, kTArrayD };

/**
 * @brief Check if a type name is a C type.
 *
 * @param type_name The type name to check.
 * @return True if the type name is a C type, false otherwise.
 */
const bool is_ctype( const std::string& type_name );

/**
 * @brief Check if a type name is an STL type.
 *
 * @param type_name The type name to check.
 * @return True if the type name is an STL type, false otherwise.
 */
const bool is_stl( std::string& type_name );

/**
 * @brief Check if a type name is a TArray type.
 *
 * @param type_name The type name to check.
 * @return True if the type name is a TArray type, false otherwise.
 */
const bool is_tarray( const std::string& type_name );

/**
 * @brief Check if a string starts with a prefix.
 *
 * @param str The string to check.
 * @param prefix The prefix to check.
 * @return True if the string starts with the prefix, false otherwise.
 */
const bool starts_with( const std::string& str, const std::string& prefix );
/**
 * @brief Check if a string ends with a suffix.
 *
 * @param str The string to check.
 * @param suffix The suffix to check.
 * @return True if the string ends with the suffix, false otherwise.
 */
const bool ends_with( const std::string& str, const std::string& suffix );

/**
 * @brief Strip leading and trailing whitespaces from a string.
 *
 * @param str The string to strip.
 *
 * @return The stripped string.
 */
const std::string strip( const std::string& str );

/**
 * @brief Get the top type name of a type name.
 *
 * The top type name is the type name without template arguments.
 *
 * @param type_name The type name to get the top type name.
 * @return The top type name.
 */
const std::string get_top_type_name( const std::string& type_name );

/**
 * @brief Get the element type of a vector type name.
 *
 * @param type_name The type name of the vector.
 * @return The element type of the vector.
 */
const std::string get_vector_element_type( const std::string& type_name );

/**
 * @brief Get the key and value types of a map type name.
 *
 * @param type_name The type name of the map.
 * @return A tuple of key and value types of the map.
 */
const std::tuple<const std::string, const std::string>
get_map_key_val_types( const std::string& type_name );

/**
 * @brief Create a reader for C types.
 *
 * @param fName The name of the reader.
 * @param type_name The type name of the C type.
 * @return A unique pointer to the created reader.
 */
std::unique_ptr<IItemReader> create_ctype_reader( const std::string& fName,
                                                  const std::string& type_name );

/**
 * @brief Create a reader for TArray.
 *
 * @param fName The name of the reader.
 * @param type_name The type name of the TArray.
 * @return A unique pointer to the created reader.
 */
std::unique_ptr<IItemReader> create_tarray_reader( const std::string& fName,
                                                   const std::string& type_name );

/**
 * @brief Create a reader for a ROOT item.
 *
 * @param streamer_info The streamer information of the item.
 * @param all_streamer_info The streamer information of all items.
 * @return A unique pointer to the created reader.
 */
std::unique_ptr<IItemReader> create_reader( py::dict streamer_info,
                                            py::dict all_streamer_info );

py::list py_read_bes_stl( py::array_t<uint8_t> data, py::array_t<uint32_t> offsets,
                          std::string type_name, py::dict all_streamer_info );

py::list py_read_bes_tobject( py::array_t<uint8_t> data, py::array_t<uint32_t> offsets,
                              std::string type_name, py::dict all_streamer_info );

py::dict py_read_bes_tobjarray( py::array_t<uint8_t> data, py::array_t<uint32_t> offsets,
                                std::string type_name, py::dict all_streamer_info );