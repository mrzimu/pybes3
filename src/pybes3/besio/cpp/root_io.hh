#pragma once

#include <uproot-custom/uproot-custom.hh>

using namespace uproot;

template <typename T>
using SharedVector = std::shared_ptr<std::vector<T>>;

template <typename T, typename... Args>
SharedVector<T> make_shared_vector( Args&&... args ) {
    return std::make_shared<std::vector<T>>( std::forward<Args>( args )... );
}

class Bes3TObjArrayReader : public IElementReader {

  public:
    Bes3TObjArrayReader( std::string name, SharedReader element_reader )
        : IElementReader( name )
        , m_element_reader( element_reader )
        , m_offsets( make_shared_vector<uint32_t>( 1, 0 ) ) {}

    void read( BinaryBuffer& bparser ) override final {
        bparser.skip_fNBytes();
        bparser.skip_fVersion();
        bparser.skip_fVersion();
        bparser.skip( 4 ); // fUniqueID
        bparser.skip( 4 ); // fBits

        bparser.skip( 1 ); // fName
        auto fSize = bparser.read<uint32_t>();
        bparser.skip( 4 ); // fLowerBound

        m_offsets->push_back( m_offsets->back() + fSize );
        for ( uint32_t i = 0; i < fSize; i++ )
        {
            bparser.skip_obj_header();
            m_element_reader->read( bparser );
        }
    }

    py::object data() const override final {
        auto offsets_array      = make_array( m_offsets );
        py::object element_data = m_element_reader->data();
        return py::make_tuple( offsets_array, element_data );
    }

  private:
    SharedReader m_element_reader;
    SharedVector<uint32_t> m_offsets;
};

template <typename T>
class Bes3SymMatrixArrayReader : public IElementReader {
  private:
    SharedVector<T> m_data;
    const uint32_t m_flat_size;
    const uint32_t m_full_dim;

  public:
    Bes3SymMatrixArrayReader( std::string name, uint32_t flat_size, uint32_t full_dim )
        : IElementReader( name )
        , m_data( make_shared_vector<T>() )
        , m_flat_size( flat_size )
        , m_full_dim( full_dim ) {
        for ( auto i = 0; i < full_dim; i++ )
        {
            for ( auto j = 0; j < full_dim; j++ )
            {
                auto idx = get_symmetric_matrix_index( i, j );
                if ( idx >= flat_size )
                {
                    throw std::runtime_error(
                        "Invalid flat size: " + std::to_string( flat_size ) + ", full dim: " +
                        std::to_string( full_dim ) + ", i: " + std::to_string( i ) +
                        ", j: " + std::to_string( j ) + ", idx: " + std::to_string( idx ) );
                }
            }
        }
    }

    const int get_symmetric_matrix_index( int i, int j ) const {
        return i < j ? j * ( j + 1 ) / 2 + i : i * ( i + 1 ) / 2 + j;
    }

    void read( BinaryBuffer& bparser ) override final {
        // temporary flat array to hold the data
        std::vector<T> flat_array( m_flat_size );
        for ( int i = 0; i < m_flat_size; i++ ) flat_array[i] = bparser.read<T>();

        // fill the m_data with the symmetric matrix data
        for ( int i = 0; i < m_full_dim; i++ )
        {
            for ( int j = 0; j < m_full_dim; j++ )
            {
                auto idx = get_symmetric_matrix_index( i, j );
                m_data->push_back( flat_array[idx] );
            }
        }
    }

    py::object data() const override final {
        auto data_array = make_array( m_data );
        return data_array;
    }
};
