#include <pybind11/cast.h>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <pyerrors.h>

#include <array>
#include <cstddef>
#include <cstdint>
#include <string>
#include <vector>

#ifdef PRINT_DEBUG_INFO
#    include <iostream>
#endif

#include "raw_io.hh"

uint32_t RawBinaryParser::read() { return *( m_cursor++ ); }

std::vector<uint32_t> RawBinaryParser::read( size_t n ) {
    std::vector<uint32_t> data( m_cursor, m_cursor + n );
    m_cursor += n;
    return data;
}

void RawBinaryParser::read( size_t n, uint32_t* data ) {
    for ( size_t i = 0; i < n; i++ ) { data[i] = read(); }
}

void RawBinaryParser::skip() { m_cursor++; }

void RawBinaryParser::skip( size_t n ) { m_cursor += n; }

void RawBinaryParser::skip_event() {
    auto flag = read();

    if ( flag == RawFlag::DATA_SEPERATOR )
    {
        skip( 3 ); // header_size, data_block_number, data_block_size
        flag = read();
    }

    if ( flag != RawFlag::FULL_EVENT )
    { throw std::runtime_error( "Invalid event header flag" ); }

    auto total_size = read();
    skip( total_size - 2 );

    m_current_entry++;
}

void RawBinaryParser::skip_to_entry( long entry ) {
    while ( m_current_entry < entry ) { skip_event(); }
}

void RawBinaryParser::read_event() {
    auto flag = read();

    if ( flag == RawFlag::DATA_SEPERATOR )
    {
        skip( 3 ); // header_size, data_block_number, data_block_size
        flag = read();
    }

    if ( flag != RawFlag::FULL_EVENT )
    { throw std::runtime_error( "Invalid event header flag" ); }

    // - event header
    auto total_size  = read();
    auto header_size = read();

    auto format_version = read();
#ifdef SAFETY_PARSE
    if ( format_version != 0x3000000 )
    {
        throw std::runtime_error(
            "Invalid event format version: expecting 0x3000000 but get " +
            std::to_string( format_version ) );
    }
#endif

    skip(); // source_id

    auto n_status = read();
    skip( n_status );

    auto n_spec_units = read();
    if ( n_spec_units != 10 )
    {
        throw std::runtime_error( "Invalid number of special units: expecting 10 but get " +
                                  std::to_string( n_spec_units ) );
    }

    // read event header
    m_evt_header_data[0].push_back( read() ); // evt_time
    m_evt_header_data[1].push_back( read() ); // evt_no
    m_evt_header_data[2].push_back( read() ); // run_no
    m_evt_header_data[3].push_back( read() ); // ls_id
    skip( 2 );                                // save space
    m_evt_header_data[4].push_back( read() ); // evt_tag1
    m_evt_header_data[5].push_back( read() ); // evt_tag2
    m_evt_header_data[6].push_back( read() ); // evt_tag3
    m_evt_header_data[7].push_back( read() ); // evt_tag4

    // - read sub-detector
    auto n_left = total_size - header_size;
    while ( n_left > 0 ) { n_left -= read_sub_detector(); }
    if ( n_left != 0 ) throw std::runtime_error( "Invalid event size" );

    fill_offsets();
    m_current_entry++;
}

void RawBinaryParser::fill_offsets() {
    for ( auto sub_det_id : m_activated_sub_det_ids )
    {
        switch ( sub_det_id )
        {
        case SubDetID::MDC: m_mdc_offsets.push_back( std::get<0>( m_mdc_data ).size() ); break;
        case SubDetID::TOF: m_tof_offsets.push_back( std::get<0>( m_tof_data ).size() ); break;
        case SubDetID::EMC: m_emc_offsets.push_back( std::get<0>( m_emc_data ).size() ); break;
        case SubDetID::MUC: m_muc_offsets.push_back( std::get<0>( m_muc_data ).size() ); break;
        case SubDetID::TRG: m_trg_offsets.push_back( m_trg_data.size() ); break;
        case SubDetID::EF: m_ef_offsets.push_back( m_ef_data.size() ); break;
        default:
            throw std::runtime_error( "Invalid sub-detector id: " +
                                      std::to_string( sub_det_id ) );
        }
    }
}

uint32_t RawBinaryParser::read_sub_detector() {
    auto flag = read();
    if ( flag != RawFlag::SUB_DETECTOR )
    { throw std::runtime_error( "Invalid sub-detector flag" ); }

    auto total_size        = read();
    auto header_size       = read();
    auto format_version    = read();
    auto source_idenfitier = read();

    auto sub_det_id = ( source_idenfitier >> 16 ) & 0xFFFF;

    auto n_status = read();
    skip( n_status );

    auto n_spec_units = read();
    skip( n_spec_units );

    // get data according by sub_det_id, if not found, skip this subdetector
    if ( m_activated_sub_det_ids.find( sub_det_id ) == m_activated_sub_det_ids.end() )
    {
        skip( total_size - header_size );
        return total_size;
    }

    auto n_left = total_size - header_size;
    while ( n_left > 0 )
    {
        auto n_read = read_ROS( sub_det_id );
        n_left -= n_read;
#ifdef PRINT_DEBUG_INFO
        std::cout << "read_sub_detector(src: " << sub_det_id << ") n_left: " << n_left
                  << ", n_read: " << n_read << std::endl;
#endif
    }

    return total_size;
}

uint32_t RawBinaryParser::read_ROS( const uint32_t sub_det_id ) {
    auto flag = read();
    if ( flag != RawFlag::ROS ) { throw std::runtime_error( "Invalid ROS flag" ); }

    auto total_size        = read();
    auto header_size       = read();
    auto format_version    = read();
    auto source_idenfitier = read();

    auto n_status = read();
    skip( n_status );

    auto n_spec_units = read();
    if ( n_spec_units != 3 )
    {
        throw std::runtime_error( "Invalid number of special units: expecting 3 but get " +
                                  std::to_string( n_spec_units ) );
    }
    skip( 3 ); // run_no, space1, trigger_no

    auto n_left = total_size - header_size;
    while ( n_left > 0 )
    {
        auto n_read = read_ROB( sub_det_id );
        n_left -= n_read;
#ifdef PRINT_DEBUG_INFO
        std::cout << "read_ROS(src: " << src_id << ") n_left: " << n_left
                  << ", n_read: " << n_read << std::endl;
#endif
    }

    return total_size;
}

uint32_t RawBinaryParser::read_ROB( const uint32_t sub_det_id ) {
    // ROB header
    auto flag = read();
    if ( flag != RawFlag::ROB ) { throw std::runtime_error( "Invalid ROB flag" ); }

    auto rob_total_size        = read();
    auto rob_header_size       = read();
    auto rob_format_version    = read();
    auto rob_source_idenfitier = read();

    auto rob_n_status = read();
    skip( rob_n_status );

    auto rob_n_spec_units = read();
    skip( rob_n_spec_units );

    // ROD header
    flag = read();
    if ( flag != RawFlag::ROD ) { throw std::runtime_error( "Invalid ROD flag" ); }

    auto rod_header_size = read();
    skip( 7 );

    auto date_length = rob_total_size - rob_header_size - rod_header_size - 3;

    auto status_and_data = read( date_length );

    auto rod_n_status   = read();
    auto rod_n_data     = read();
    auto rod_status_pos = read();

    if ( rod_status_pos == 0 )
        status_and_data.erase( status_and_data.begin(),
                               status_and_data.begin() + rod_n_status );
    else status_and_data.erase( status_and_data.begin() + rod_n_data, status_and_data.end() );

    fill_digi( status_and_data, sub_det_id );

    return rob_total_size;
}

void RawBinaryParser::fill_digi( const std::vector<uint32_t>& tmp_data,
                                 const uint32_t sub_det_id ) {

    if ( sub_det_id == SubDetID::MDC )
    {
        // merge digis
        std::map<uint16_t, std::array<uint16_t, 3>> digi_data; // t, q, overflow
        for ( auto digi : tmp_data )
        {
            uint16_t signal_value = digi & 0xFFFF;
            uint16_t overflow     = ( digi >> 16 ) & 0x1;
            uint16_t t_or_q       = ( digi >> 17 ) & 0x1;
            uint16_t id           = digi >> 18;

            digi_data[id][t_or_q] = signal_value;
            digi_data[id][2] |= overflow;
        }

        // fill data
        auto& [data_id, data_t, data_q, data_overflow] = m_mdc_data;
        for ( auto& [id, cur_data] : digi_data )
        {
            data_id.push_back( id );
            data_t.push_back( cur_data[0] );
            data_q.push_back( cur_data[1] );
            data_overflow.push_back( cur_data[2] );
        }

        return;
    }

    if ( sub_det_id == SubDetID::TOF )
    {
        // merge digis
        std::map<uint16_t, std::array<uint16_t, 3>> digi_data; // t, q, overflow
        for ( auto digi : tmp_data )
        {
            uint16_t signal_value = digi & 0xFFFF;
            uint16_t overflow     = ( digi >> 16 ) & 0x1;
            uint16_t t_or_q       = ( digi >> 17 ) & 0x1;
            uint16_t id           = ( digi >> 18 ) & 0x3FF;

            digi_data[id][t_or_q] = signal_value;
            digi_data[id][2] |= overflow;
        }

        // fill data
        auto& [data_id, data_t, data_q, data_overflow] = m_tof_data;
        for ( auto& [id, cur_data] : digi_data )
        {
            data_id.push_back( id );
            data_t.push_back( cur_data[0] );
            data_q.push_back( cur_data[1] );
            data_overflow.push_back( cur_data[2] );
        }

        return;
    }

    if ( sub_det_id == SubDetID::EMC )
    {
        // fill data
        auto& [data_id, data_t, data_q, data_measure] = m_emc_data;
        for ( auto digi : tmp_data )
        {
            uint16_t adc     = digi & 0x7FF;
            uint16_t measure = ( digi >> 11 ) & 0x3;
            uint16_t tdc     = ( digi >> 13 ) & 0x7F;
            uint16_t id      = digi >> 19;

            data_id.push_back( id );
            data_t.push_back( tdc );
            data_q.push_back( adc );
            data_measure.push_back( measure );
        }

        return;
    }

    if ( sub_det_id == SubDetID::MUC )
    {
        // fill data
        auto& [data_id, data_fec] = m_muc_data;

        for ( auto digi : tmp_data )
        {
            uint16_t fec = digi & 0xFFFF;
            uint16_t id  = ( digi >> 16 ) & 0x7FF;

            data_fec.push_back( fec );
            data_id.push_back( id );
        }

        return;
    }

    if ( sub_det_id == SubDetID::TRG )
    {
        m_trg_data.insert( m_trg_data.end(), tmp_data.begin(), tmp_data.end() );
        return;
    }

    if ( sub_det_id == SubDetID::EF )
    {
        m_ef_data.insert( m_ef_data.end(), tmp_data.begin(), tmp_data.end() );
        return;
    }
}

py::dict RawBinaryParser::arrays( std::vector<std::string> sub_detectors ) {

    // set target sub_detectors
    for ( auto& sub_det_name : sub_detectors )
    {
        if ( sub_det_names_to_ids.find( sub_det_name ) == sub_det_names_to_ids.end() )
        { throw std::runtime_error( "Invalid sub-detector name: " + sub_det_name ); }

        auto sub_det_id = sub_det_names_to_ids[sub_det_name];
        m_activated_sub_det_ids.insert( sub_det_id );
    }

    // - read data
    py::gil_scoped_release release;
    fill_offsets(); // fill the first offset
    while ( m_cursor < m_data_end ) { read_event(); }
    py::gil_scoped_acquire acquire;

    // - convert data to numpy array
    py::dict res;

    // event header
    py::dict evt_header;
    for ( size_t i = 0; i < m_evt_header_data.size(); i++ )
    {
        auto np_data =
            py::array_t<uint32_t>( m_evt_header_data[i].size(), m_evt_header_data[i].data() );

        // use i as key
        evt_header[evt_header_item_names[i].c_str()] = np_data;
    }
    res["evt_header"] = evt_header;

    // sub-detectors
    for ( auto& sub_det_id : m_activated_sub_det_ids )
    {
        switch ( sub_det_id )
        {
        case SubDetID::MDC: {
            auto& [data_id, data_t, data_q, data_overflow] = m_mdc_data;

            py::dict mdc_data;
            mdc_data["id"]  = py::array_t<uint16_t>( data_id.size(), data_id.data() );
            mdc_data["adc"] = py::array_t<uint16_t>( data_q.size(), data_q.data() );
            mdc_data["tdc"] = py::array_t<uint16_t>( data_t.size(), data_t.data() );
            mdc_data["overflow"] =
                py::array_t<uint8_t>( data_overflow.size(), data_overflow.data() );

            py::array_t<uint32_t> offsets( m_mdc_offsets.size(), m_mdc_offsets.data() );

            res["mdc"] = py::make_tuple( offsets, mdc_data );
            break;
        }

        case SubDetID::TOF: {
            auto& [data_id, data_t, data_q, data_overflow] = m_tof_data;

            py::dict tof_data;
            tof_data["id"]  = py::array_t<uint16_t>( data_id.size(), data_id.data() );
            tof_data["adc"] = py::array_t<uint16_t>( data_q.size(), data_q.data() );
            tof_data["tdc"] = py::array_t<uint16_t>( data_t.size(), data_t.data() );
            tof_data["overflow"] =
                py::array_t<uint8_t>( data_overflow.size(), data_overflow.data() );

            py::array_t<uint32_t> offsets( m_tof_offsets.size(), m_tof_offsets.data() );

            res["tof"] = py::make_tuple( offsets, tof_data );
            break;
        }

        case SubDetID::EMC: {
            auto& [data_id, data_t, data_q, data_measure] = m_emc_data;

            py::dict emc_data;
            emc_data["id"]  = py::array_t<uint16_t>( data_id.size(), data_id.data() );
            emc_data["adc"] = py::array_t<uint16_t>( data_q.size(), data_q.data() );
            emc_data["tdc"] = py::array_t<uint16_t>( data_t.size(), data_t.data() );
            emc_data["measure"] =
                py::array_t<uint8_t>( data_measure.size(), data_measure.data() );

            py::array_t<uint32_t> offsets( m_emc_offsets.size(), m_emc_offsets.data() );

            res["emc"] = py::make_tuple( offsets, emc_data );
            break;
        }

        case SubDetID::MUC: {
            auto& [data_id, data_fec] = m_muc_data;

            py::dict muc_data;
            muc_data["id"]  = py::array_t<uint16_t>( data_id.size(), data_id.data() );
            muc_data["fec"] = py::array_t<uint16_t>( data_fec.size(), data_fec.data() );

            py::array_t<uint32_t> offsets( m_muc_offsets.size(), m_muc_offsets.data() );

            res["muc"] = py::make_tuple( offsets, muc_data );
            break;
        }

        case SubDetID::EF: {
            py::array_t<uint32_t> ef_data( m_ef_data.size(), m_ef_data.data() );
            py::array_t<uint32_t> ef_offsets( m_ef_offsets.size(), m_ef_offsets.data() );
            res["ef"] = py::make_tuple( ef_offsets, ef_data );
            break;
        }

        case SubDetID::TRG: {
            py::array_t<uint32_t> trg_data( m_trg_data.size(), m_trg_data.data() );
            py::array_t<uint32_t> trg_offsets( m_trg_offsets.size(), m_trg_offsets.data() );
            res["trg"] = py::make_tuple( trg_offsets, trg_data );
            break;
        }
        }
    }

    return res;
}

py::dict py_read_bes_raw( py::array_t<uint32_t> data,
                          std::vector<std::string> sub_detectors ) {

    if ( sub_detectors.size() == 0 ) sub_detectors = { "mdc", "tof", "emc", "muc" };

    RawBinaryParser parser( data );
    return parser.arrays( sub_detectors );
}
