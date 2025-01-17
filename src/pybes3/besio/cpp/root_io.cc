#include "root_io.hh"
#include <pybind11/pybind11.h>

const bool is_ctype( const std::string& type_name ) {
    return CTYPE_NAMES.find( type_name ) != CTYPE_NAMES.end();
}

const bool is_stl( std::string& type_name ) {
    return STL_NAMES.find( type_name ) != STL_NAMES.end();
}

const bool is_tarray( const std::string& type_name ) {
    return TARRAY_NAMES.find( type_name ) != TARRAY_NAMES.end();
}

const bool starts_with( const std::string& str, const std::string& prefix ) {
    return str.substr( 0, prefix.size() ) == prefix;
}

const bool ends_with( const std::string& str, const std::string& suffix ) {
    return str.substr( str.size() - suffix.size(), suffix.size() ) == suffix;
}

const std::string strip( const std::string& str ) {
    auto res = std::string( str );
    res.erase( 0, res.find_first_not_of( " \t\n" ) );
    res.erase( res.find_last_not_of( " \t\n" ) + 1 );
    if ( res.back() == '*' ) res.pop_back();

    // remove first "std::"
    if ( starts_with( res, "std::" ) ) res = res.substr( 5, res.size() - 5 );
    return res;
}

const std::string get_top_type_name( const std::string& type_name ) {
    if ( is_ctype( type_name ) ) return type_name;
    else if ( type_name.find( "<" ) != std::string::npos )
    {
        auto pos           = type_name.find( "<" );
        auto top_type_name = strip( type_name.substr( 0, pos ) );
        if ( is_stl( top_type_name ) ) return top_type_name;
        else throw py::type_error( "Unsupported STL type: " + top_type_name );
    }
    else if ( type_name == kTString ) return kTString;
    else if ( type_name == kBASE ) return kBASE;
    else return strip( type_name );
}

const std::string get_vector_element_type( const std::string& type_name ) {
    if ( !starts_with( type_name, "vector<" ) || !ends_with( type_name, ">" ) )
        throw std::runtime_error( "Unsupported type_name: " + type_name );
    return strip( type_name.substr( 7, type_name.size() - 7 - 1 ) );
}

const std::tuple<const std::string, const std::string>
get_map_key_val_types( const std::string& type_name ) {
    if ( !starts_with( type_name, "map<" ) || !ends_with( type_name, ">" ) )
        throw std::runtime_error( "Unsupported type_name: " + type_name );

    int pos_split = 0;
    int n_level   = 0;

    for ( int i = 0; i < type_name.size(); i++ )
    {
        if ( type_name[i] == '<' ) n_level++;
        if ( type_name[i] == '>' ) n_level--;

        if ( n_level == 1 && type_name[i] == ',' )
        {
            pos_split = i;
            break;
        }
    }

    if ( pos_split == 0 ) throw std::runtime_error( "Unsupported type_name: " + type_name );

    auto key_type_name = type_name.substr( 4, pos_split - 4 );
    auto val_type_name =
        type_name.substr( pos_split + 1, type_name.size() - pos_split - 1 - 1 );

    return std::make_tuple( strip( key_type_name ), strip( val_type_name ) );
}

std::unique_ptr<IItemReader> create_ctype_reader( const std::string& fName,
                                                  const std::string& type_name ) {
    if ( type_name == kBool ) return std::make_unique<CTypeReader<bool>>( fName );
    else if ( type_name == kChar ) return std::make_unique<CTypeReader<int8_t>>( fName );
    else if ( type_name == kShort ) return std::make_unique<CTypeReader<int16_t>>( fName );
    else if ( type_name == kInt ) return std::make_unique<CTypeReader<int32_t>>( fName );
    else if ( type_name == kLong ) return std::make_unique<CTypeReader<int64_t>>( fName );
    else if ( type_name == kFloat ) return std::make_unique<CTypeReader<float>>( fName );
    else if ( type_name == kDouble ) return std::make_unique<CTypeReader<double>>( fName );
    else if ( type_name == kUChar ) return std::make_unique<CTypeReader<uint8_t>>( fName );
    else if ( type_name == kUShort ) return std::make_unique<CTypeReader<uint16_t>>( fName );
    else if ( type_name == kUInt ) return std::make_unique<CTypeReader<uint32_t>>( fName );
    else if ( type_name == kULong ) return std::make_unique<CTypeReader<uint64_t>>( fName );

    else if ( type_name == kUInt8 ) return std::make_unique<CTypeReader<uint8_t>>( fName );
    else if ( type_name == kInt16 ) return std::make_unique<CTypeReader<int16_t>>( fName );
    else if ( type_name == kUInt16 ) return std::make_unique<CTypeReader<uint16_t>>( fName );
    else if ( type_name == kInt32 ) return std::make_unique<CTypeReader<int32_t>>( fName );
    else if ( type_name == kUInt32 ) return std::make_unique<CTypeReader<uint32_t>>( fName );
    else if ( type_name == kInt64 ) return std::make_unique<CTypeReader<int64_t>>( fName );
    else if ( type_name == kUInt64 ) return std::make_unique<CTypeReader<uint64_t>>( fName );
    else throw py::type_error( "Unsupported type: " + std::string( type_name ) );
}

std::unique_ptr<IItemReader> create_tarray_reader( const std::string& fName,
                                                   const std::string& type_name ) {
    if ( type_name == kTArrayC ) return std::make_unique<TArrayReader<int8_t>>( fName );
    else if ( type_name == kTArrayS ) return std::make_unique<TArrayReader<int16_t>>( fName );
    else if ( type_name == kTArrayI ) return std::make_unique<TArrayReader<int32_t>>( fName );
    else if ( type_name == kTArrayL ) return std::make_unique<TArrayReader<int64_t>>( fName );
    else if ( type_name == kTArrayF ) return std::make_unique<TArrayReader<float>>( fName );
    else if ( type_name == kTArrayD ) return std::make_unique<TArrayReader<double>>( fName );
    else throw py::type_error( "Unsupported type: " + std::string( type_name ) );
}

std::unique_ptr<IItemReader> create_reader( py::dict streamer_info,
                                            py::dict all_streamer_info ) {
    auto fTypeName     = streamer_info["fTypeName"].cast<std::string>();
    auto fName         = streamer_info["fName"].cast<std::string>();
    auto top_type_name = get_top_type_name( fTypeName );

    // first check if it is an array
    if ( streamer_info.contains( "fArrayDim" ) )
    {
        auto fArrayDim = streamer_info["fArrayDim"].cast<uint32_t>();
        if ( fArrayDim > 0 )
        {
            py::dict new_info;
            for ( auto [key, value] : streamer_info ) { new_info[key] = value; }
            new_info["fArrayDim"] = 0;
            auto base_reader      = create_reader( new_info, all_streamer_info );

            auto fMaxIndex        = streamer_info["fMaxIndex"].cast<py::array_t<uint32_t>>();
            uint32_t flatten_size = 1;
            for ( int i = 0; i < 5; i++ )
            {
                if ( fMaxIndex.data()[i] == 0 ) break;
                flatten_size *= fMaxIndex.data()[i];
            }
            if ( flatten_size <= 1 )
                throw std::runtime_error( "Invalid flatten_size: " +
                                          std::to_string( flatten_size ) );

            if ( is_ctype( top_type_name ) || is_tarray( top_type_name ) )
            {
                return std::make_unique<SimpleArrayReader>(
                    fName + "_array", std::move( base_reader ), flatten_size );
            }
            else if ( top_type_name == kTString )
            {
                return std::make_unique<ObjArrayReader>(
                    fName + "_array", std::move( base_reader ), flatten_size );
            }
            else if ( is_stl( top_type_name ) )
            {
                if ( top_type_name == kVector )
                    dynamic_cast<VectorReader*>( base_reader.get() )->set_is_top( false );
                else if ( top_type_name == kMap || top_type_name == kMultimap )
                    dynamic_cast<MapReader*>( base_reader.get() )->set_is_top( false );
                else throw py::type_error( "Unsupported STL type: " + top_type_name );

                return std::make_unique<ObjArrayReader>(
                    fName + "_array", std::move( base_reader ), flatten_size );
            }
            else
                throw py::type_error( "Unsupported type for array reading: " + top_type_name );
        }
    }

    // if it is not an array, then create the reader

    // ctype
    if ( is_ctype( top_type_name ) ) return create_ctype_reader( fName, fTypeName );

    // TString
    else if ( top_type_name == kTString ) return std::make_unique<TStringReader>( fName );

    // STL
    else if ( is_stl( top_type_name ) )
    {
        // vector
        if ( top_type_name == kVector )
        {
            auto element_type = get_vector_element_type( fTypeName );
            py::dict element_info;
            element_info["fName"]     = fName + "_element";
            element_info["fTypeName"] = element_type;
            element_info["fType"]     = -1;
            auto element_reader       = create_reader( element_info, all_streamer_info );
            return std::make_unique<VectorReader>( fName, std::move( element_reader ) );
        }

        // map
        else if ( top_type_name == kMap || top_type_name == kMultimap )
        {
            auto [key_type_name, val_type_name] = get_map_key_val_types( fTypeName );
            py::dict key_info, val_info;
            key_info["fName"]     = fName + "_key";
            key_info["fTypeName"] = key_type_name;
            key_info["fType"]     = -1;

            val_info["fName"]     = fName + "_val";
            val_info["fTypeName"] = val_type_name;
            val_info["fType"]     = -1;
            auto key_reader       = create_reader( key_info, all_streamer_info );
            auto val_reader       = create_reader( val_info, all_streamer_info );
            return std::make_unique<MapReader>( fName, std::move( key_reader ),
                                                std::move( val_reader ) );
        }
        else throw py::type_error( "Unsupported STL type: " + top_type_name );
    }

    // BASE, may be TObject or some other class. By so far only fType==0 is supported
    else if ( top_type_name == kBASE )
    {
        auto fType = streamer_info["fType"].cast<int32_t>();
        if ( fType == 66 ) return std::make_unique<TObjectReader>( fName );
        else if ( fType == 0 ) // Other ROOT class, obtain its streamer information and create
                               // BaseObjectReader
        {
            auto sub_streamers = all_streamer_info[fName.c_str()].cast<py::list>();
            std::vector<std::unique_ptr<IItemReader>> sub_readers;
            for ( auto s : sub_streamers )
            {
                auto s_dict = s.cast<py::dict>();
                auto reader = create_reader( s_dict, all_streamer_info );
                sub_readers.push_back( std::move( reader ) );
            }
            return std::make_unique<BaseObjectReader>( fName, std::move( sub_readers ) );
        }
        else throw py::type_error( "Unsupported fType: " + std::to_string( fType ) );
    }

    // TArray
    else if ( is_tarray( top_type_name ) ) return create_tarray_reader( fName, top_type_name );

    // Other classes, read its streamer information and create ObjectReader
    else
    {
        auto sub_streamers = all_streamer_info[top_type_name.c_str()].cast<py::list>();
        std::vector<std::unique_ptr<IItemReader>> sub_readers;
        for ( auto s : sub_streamers )
        {
            auto s_dict = s.cast<py::dict>();
            auto reader = create_reader( s_dict, all_streamer_info );
            sub_readers.push_back( std::move( reader ) );
        }
        return std::make_unique<ObjectReader>( fName, std::move( sub_readers ) );
    }
}

py::list py_read_bes_stl( py::array_t<uint8_t> data, py::array_t<uint32_t> offsets,
                          std::string type_name, py::dict all_streamer_info ) {
    RootBinaryParser bparser( data, offsets );

    py::dict tmp_info;
    tmp_info["fName"]     = "tmp";
    tmp_info["fTypeName"] = type_name;
    tmp_info["fType"]     = -1;

    auto reader = create_reader( tmp_info, all_streamer_info );

    py::gil_scoped_release release;
    for ( uint64_t i_evt = 0; i_evt < bparser.m_entries; i_evt++ ) { reader->read( bparser ); }
    py::gil_scoped_acquire acquire;

    return reader->data();
}

py::list py_read_bes_tobject( py::array_t<uint8_t> data, py::array_t<uint32_t> offsets,
                              std::string type_name, py::dict all_streamer_info ) {
    RootBinaryParser bparser( data, offsets );
    std::vector<std::unique_ptr<IItemReader>> sub_readers;
    auto streamer_members = all_streamer_info[type_name.c_str()].cast<py::list>();

    for ( auto s : streamer_members )
    {
        auto reader = create_reader( s.cast<py::dict>(), all_streamer_info );
        sub_readers.push_back( std::move( reader ) );
    }
    auto reader = std::make_unique<BaseObjectReader>( type_name, std::move( sub_readers ) );

    py::gil_scoped_release release;
    for ( uint64_t i_evt = 0; i_evt < bparser.m_entries; i_evt++ )
    {
        reader->read( bparser );

#ifdef SAFETY_PARSE
        auto cur_offset = bparser.get_cursor() - bparser.get_data();
        if ( cur_offset != offsets.data()[i_evt + 1] )
        {
            throw std::runtime_error( "Event " + std::to_string( i_evt ) +
                                      " parsing error: " + std::to_string( cur_offset ) +
                                      " != " + std::to_string( offsets.data()[i_evt + 1] ) );
        }
#endif
    }
    py::gil_scoped_acquire acquire;

    return reader->data();
}

py::dict py_read_bes_tobjarray( py::array_t<uint8_t> data, py::array_t<uint32_t> offsets,
                                std::string type_name, py::dict all_streamer_info ) {
    RootBinaryParser bparser( data, offsets );

    std::vector<std::unique_ptr<IItemReader>> sub_readers;
    auto streamer_info_list      = all_streamer_info[type_name.c_str()].cast<py::list>();
    bool is_derived_from_tobject = false;
    for ( auto s : streamer_info_list )
    {
        auto reader = create_reader( s.cast<py::dict>(), all_streamer_info );
        if ( reader->name() == kTObject ) is_derived_from_tobject = true;
        sub_readers.push_back( std::move( reader ) );
    }

    auto obj_reader = std::make_unique<ObjectReader>( type_name, std::move( sub_readers ) );

    std::vector<uint32_t> obj_offsets = { 0 };

    py::gil_scoped_release release;
    for ( uint64_t i_evt = 0; i_evt < bparser.m_entries; i_evt++ )
    {
#ifdef PRINT_DEBUG_INFO
        std::cout << "Event " << i_evt << ":" << std::endl;
        for ( int i = 0; i < 40; i++ ) std::cout << (int)bparser.get_cursor()[i] << " ";
        std::cout << std::endl << std::endl;
#endif
        auto n_objs = std::get<1>( bparser.read_TObjArray() );
        obj_offsets.push_back( obj_offsets.back() + n_objs );

        for ( int i_obj = 0; i_obj < n_objs; i_obj++ )
        {
#ifdef PRINT_DEBUG_INFO
            std::cout << "obj_start (" << i_obj << "):" << std::endl;
            for ( int i = 0; i < 40; i++ ) std::cout << (int)bparser.get_cursor()[i] << " ";
            std::cout << std::endl << std::endl;
#endif
            obj_reader->read( bparser );
        }

#ifdef SAFETY_PARSE
        auto cur_offset = bparser.get_cursor() - bparser.get_data();
        if ( cur_offset != offsets.data()[i_evt + 1] )
        {
            throw std::runtime_error( "Event " + std::to_string( i_evt ) +
                                      " parsing error: " + std::to_string( cur_offset ) +
                                      " != " + std::to_string( offsets.data()[i_evt + 1] ) );
        }
#endif
    }
    py::gil_scoped_acquire acquire;

    py::dict results;

    // obj_offsets
    py::array_t<uint32_t> py_obj_offsets( obj_offsets.size() );
    std::copy( obj_offsets.begin(), obj_offsets.end(), py_obj_offsets.mutable_data() );
    results["obj_offsets"] = py_obj_offsets;

    results["data"] = obj_reader->data();
    return results;
}
