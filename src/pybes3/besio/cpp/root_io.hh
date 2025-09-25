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
  private:
    SharedReader m_element_reader;
    SharedVector<uint32_t> m_offsets;

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

class Bes3CgemClusterColReader : public IElementReader {
  private:
    int m_version{ -1 }; // -1: unknown, 0: with recpositiony, 1: without recpositiony

    SharedVector<uint32_t> m_offsets;
    SharedVector<int32_t> m_clusterid;
    SharedVector<int32_t> m_trkid;
    SharedVector<int32_t> m_layerid;
    SharedVector<int32_t> m_sheetid;
    SharedVector<int32_t> m_flag;
    SharedVector<double> m_energydeposit;
    SharedVector<double> m_recphi;
    SharedVector<double> m_recpositiony;
    SharedVector<double> m_recv;
    SharedVector<double> m_recZ;
    SharedVector<int32_t> m_clusterflag;
    SharedVector<int32_t> m_stripid;

  public:
    Bes3CgemClusterColReader( std::string name )
        : IElementReader( name )
        , m_offsets( make_shared_vector<uint32_t>( 1, 0 ) )
        , m_clusterid( make_shared_vector<int32_t>() )
        , m_trkid( make_shared_vector<int32_t>() )
        , m_layerid( make_shared_vector<int32_t>() )
        , m_sheetid( make_shared_vector<int32_t>() )
        , m_flag( make_shared_vector<int32_t>() )
        , m_energydeposit( make_shared_vector<double>() )
        , m_recphi( make_shared_vector<double>() )
        , m_recpositiony( make_shared_vector<double>() )
        , m_recv( make_shared_vector<double>() )
        , m_recZ( make_shared_vector<double>() )
        , m_clusterflag( make_shared_vector<int32_t>() )
        , m_stripid( make_shared_vector<int32_t>() ) {}

    void read( BinaryBuffer& bparser ) override final {
        bparser.skip_obj_header();

        // TObjArray
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

            auto fNBytes = bparser.read_fNBytes();
            bparser.skip_fVersion();

            // Determine class version
            if ( m_version == -1 )
            {
                switch ( fNBytes )
                {
                case 96: m_version = 0; break;
                case 88: m_version = 1; break;
                default:
                    throw std::runtime_error( "Unknown TCgemCluster version with fNBytes=" +
                                              std::to_string( fNBytes ) );
                }
            }

            // TObject
            bparser.skip_TObject();

            // TRecCgemCluster
            m_clusterid->push_back( bparser.read<int32_t>() );
            m_trkid->push_back( bparser.read<int32_t>() );
            m_layerid->push_back( bparser.read<int32_t>() );
            m_sheetid->push_back( bparser.read<int32_t>() );
            m_flag->push_back( bparser.read<int32_t>() );
            m_energydeposit->push_back( bparser.read<double>() );
            m_recphi->push_back( bparser.read<double>() );
            if ( m_version == 0 ) m_recpositiony->push_back( bparser.read<double>() );
            m_recv->push_back( bparser.read<double>() );
            m_recZ->push_back( bparser.read<double>() );

            // m_clusterflag is int[2]
            for ( int i = 0; i < 2; i++ ) m_clusterflag->push_back( bparser.read<int32_t>() );

            // m_stripid is int[2][2]
            for ( int i = 0; i < 4; i++ ) m_stripid->push_back( bparser.read<int32_t>() );
        }
    }

    py::object data() const override final {
        py::dict result;
        result["offsets"]         = make_array( m_offsets );
        result["m_clusterID"]     = make_array( m_clusterid );
        result["m_trkID"]         = make_array( m_trkid );
        result["m_layerID"]       = make_array( m_layerid );
        result["m_sheetID"]       = make_array( m_sheetid );
        result["m_flag"]          = make_array( m_flag );
        result["m_energyDeposit"] = make_array( m_energydeposit );
        result["m_recPhi"]        = make_array( m_recphi );
        if ( m_version == 0 ) result["m_recPositionY"] = make_array( m_recpositiony );
        result["m_recV"]        = make_array( m_recv );
        result["m_recZ"]        = make_array( m_recZ );
        result["m_clusterFlag"] = make_array( m_clusterflag );
        result["m_stripID"]     = make_array( m_stripid );
        return result;
    }
};
