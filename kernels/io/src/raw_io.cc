#include <map>
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

using uproot::make_array;

uint32_t RawBinaryParser::read() { return *( m_cursor++ ); }

vector<uint32_t> RawBinaryParser::read( size_t n ) {
    vector<uint32_t> data( m_cursor, m_cursor + n );
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

    if ( flag != RawFlag::FULL_EVENT ) { throw runtime_error( "Invalid event header flag" ); }

    auto total_size = read();
    skip( total_size - 2 );

    m_current_entry++;
}

void RawBinaryParser::skip_to_entry( long entry ) {
    while ( m_current_entry < entry ) { skip_event(); }
}

void RawBinaryParser::read_event() {
    m_buffers.clear();

    auto flag = read();

    if ( flag == RawFlag::DATA_SEPERATOR )
    {
        skip( 3 ); // header_size, data_block_number, data_block_size
        flag = read();
    }

    if ( flag != RawFlag::FULL_EVENT ) { throw runtime_error( "Invalid event header flag" ); }

    // - event header
    auto total_size  = read();
    auto header_size = read();

    auto format_version = read();
    if ( format_version != 0x3000000 )
    {
        throw runtime_error( "Invalid event format version: expecting 0x3000000 but get " +
                             to_string( format_version ) );
    }

    skip(); // source_id

    auto n_status = read();
    skip( n_status );

    auto n_spec_units = read();
    if ( n_spec_units != 10 )
    {
        throw runtime_error( "Invalid number of special units: expecting 10 but get " +
                             to_string( n_spec_units ) );
    }

    // read event header
    m_evt_header_data.evt_time->push_back( read() );
    m_evt_header_data.evt_no->push_back( read() );
    m_evt_header_data.run_no->push_back( read() );
    m_evt_header_data.l1_id->push_back( read() );
    skip( 2 );
    m_evt_header_data.evt_tag1->push_back( read() );
    m_evt_header_data.evt_tag2->push_back( read() );
    m_evt_header_data.evt_tag3->push_back( read() );
    m_evt_header_data.evt_tag4->push_back( read() );

    // - read field
    auto n_left = total_size - header_size;
    while ( n_left > 0 ) { n_left -= read_field(); }
    if ( n_left != 0 ) throw runtime_error( "Invalid event size" );

    read_data_from_buffers();

    fill_offsets();
    m_current_entry++;
}

void RawBinaryParser::read_data_from_buffers() {
    if ( m_active_field_ids.find( FieldID::MDC ) != m_active_field_ids.end() )
        read_mdc_buffer();
    if ( m_active_field_ids.find( FieldID::TOF ) != m_active_field_ids.end() )
        read_tof_buffer();
    if ( m_active_field_ids.find( FieldID::EMC ) != m_active_field_ids.end() )
        read_emc_buffer();
    if ( m_active_field_ids.find( FieldID::MUC ) != m_active_field_ids.end() )
        read_muc_buffer();
    if ( m_active_field_ids.find( FieldID::TrigGTD ) != m_active_field_ids.end() )
        read_trg_buffer();
    if ( m_active_field_ids.find( FieldID::CGEM ) != m_active_field_ids.end() )
        read_cgem_buffer();
}

void RawBinaryParser::fill_offsets() {
    for ( auto field_id : m_active_field_ids )
    {
        switch ( field_id )
        {
        case FieldID::MDC: m_mdc_offsets->push_back( m_mdc_data.size() ); break;
        case FieldID::TOF: m_tof_offsets->push_back( m_tof_data.size() ); break;
        case FieldID::EMC: m_emc_offsets->push_back( m_emc_data.size() ); break;
        case FieldID::MUC: m_muc_offsets->push_back( m_muc_data.size() ); break;
        case FieldID::TrigGTD: m_trg_offsets->push_back( m_trg_data.size() ); break;
        case FieldID::CGEM: m_cgem_offsets->push_back( m_cgem_data.size() ); break;
        case FieldID::MRPC: break; // filled in TOF
        default: throw runtime_error( "Invalid field id: " + to_string( field_id ) );
        }
    }
}

uint32_t RawBinaryParser::read_field() {
    auto flag = read();
    if ( flag != RawFlag::SUB_DETECTOR ) { throw runtime_error( "Invalid field flag" ); }

    auto total_size  = read();
    auto header_size = read();
    skip(); // format-version
    auto source_identifier = read();

    auto field_id = ( source_identifier >> 16 ) & 0xFFFF;

    auto n_status = read();
    skip( n_status );

    auto n_spec_units = read();
    skip( n_spec_units );

    // get data according to field_id; if not found, skip this field
    if ( m_active_field_ids.find( field_id ) == m_active_field_ids.end() )
    {
        skip( total_size - header_size );
        return total_size;
    }

    auto n_left = total_size - header_size;
    while ( n_left > 0 )
    {
        auto n_read = read_ROS( field_id );
        n_left -= n_read;
#ifdef PRINT_DEBUG_INFO
        cout << "read_field(src: " << field_id << ") n_left: " << n_left
             << ", n_read: " << n_read << endl;
#endif
    }

    return total_size;
}

uint32_t RawBinaryParser::read_ROS( const uint32_t field_id ) {
    auto flag = read();
    if ( flag != RawFlag::ROS ) { throw runtime_error( "Invalid ROS flag" ); }

    auto total_size  = read();
    auto header_size = read();
    skip(); // format-version
    skip(); // source_idenfitier

    auto n_status = read();
    skip( n_status );

    auto n_spec_units = read();
    if ( n_spec_units != 3 )
    {
        throw runtime_error( "Invalid number of special units: expecting 3 but get " +
                             to_string( n_spec_units ) );
    }
    skip( 3 ); // run_no, space1, trigger_no

    auto n_left = total_size - header_size;
    while ( n_left > 0 )
    {
        auto n_read = read_ROB( field_id );
        n_left -= n_read;
#ifdef PRINT_DEBUG_INFO
        cout << "read_ROS(src: " << src_id << ") n_left: " << n_left << ", n_read: " << n_read
             << endl;
#endif
    }

    return total_size;
}

uint32_t RawBinaryParser::read_ROB( const uint32_t field_id ) {
    // ROB header
    auto flag = read();
    if ( flag != RawFlag::ROB ) { throw runtime_error( "Invalid ROB flag" ); }

    auto rob_total_size  = read();
    auto rob_header_size = read();
    skip(); // rob_format_version
    skip(); // rob_source_idenfitier

    auto rob_n_status = read();
    skip( rob_n_status );

    auto rob_n_spec_units = read();
    skip( rob_n_spec_units );

    // ROD header
    flag = read();
    if ( flag != RawFlag::ROD ) { throw runtime_error( "Invalid ROD flag" ); }

    auto rod_header_size = read();
    skip( 7 );

    auto data_length = rob_total_size - rob_header_size - rod_header_size - 3;

    auto status_and_data = m_cursor;
    m_cursor += data_length;

    auto rod_n_status   = read();
    auto rod_n_data     = read();
    auto rod_status_pos = read();

    uint32_t* data_begin{ nullptr };
    uint32_t* data_end{ nullptr };

    if ( rod_status_pos == 0 )
    {
        data_begin = status_and_data + rod_n_status;
        data_end   = status_and_data + data_length;
    }
    else
    {
        data_begin = status_and_data;
        data_end   = status_and_data + rod_n_data;
    }

    vector<uint32_t>* target_buffer{ nullptr };
    if ( field_id == FieldID::MDC ) target_buffer = &m_buffers.mdc;
    else if ( field_id == FieldID::TOF ) target_buffer = &m_buffers.tof;
    else if ( field_id == FieldID::EMC ) target_buffer = &m_buffers.emc;
    else if ( field_id == FieldID::MUC ) target_buffer = &m_buffers.muc;
    else if ( field_id == FieldID::CGEM ) target_buffer = &m_buffers.cgem;
    else if ( field_id == FieldID::MRPC ) target_buffer = &m_buffers.mrpc;
    else if ( field_id == FieldID::TrigGTD )
        m_buffers.trg.emplace_back( data_begin, data_end );

    if ( target_buffer ) target_buffer->insert( target_buffer->end(), data_begin, data_end );
    return rob_total_size;
}

void RawBinaryParser::read_mdc_buffer() {
    if ( m_buffers.mdc.empty() ) return;

    /* Refer to BOSS_Source/Event/RawDataCnv/MdcConverter */
    vector<uint32_t> hits;
    vector<pair<uint32_t, uint32_t>> vm_tdc;

    for ( auto digi : m_buffers.mdc )
    {
        uint32_t reid = ( digi & 0xFFFC0000 ) >> 18;
        if ( reid == 0 ) continue;

        auto teid = m_re2te.mdc[reid];
        if ( teid == 0xFFFFFFFF ) continue;

        uint32_t signal_value = digi & 0xFFFF;
        uint32_t overflow     = ( digi & 0x10000 ) >> 16;
        uint32_t t_or_q       = ( digi & 0x20000 ) >> 17;

        auto& tag = m_mdc_tags[reid];
        if ( tag[0] == 0 )
        {
            tag[1] = 0x7FFFFFFF;
            tag[2] = 0x7FFFFFFF;
            tag[3] = 0;

            /* Do fixing, refer to
             * BOSS_Source/Event/RawDataCnv/share/Config4Reverse.json */

            // Fix 1: exchange layer[20]wire[0-7] <=> layer[42]wire[0-7]
            mdc_reverse_id( teid, tag, 21504, 43008 );

            // Fix 2: exchange layer[40]wire[200-207] <=> layer[40]wire[208-215]
            mdc_reverse_id( teid, tag, 20680, 20688 );

            auto cur_run_no = m_evt_header_data.run_no->back();
            if ( cur_run_no >= 66719 && cur_run_no <= 69292 )
            {
                // Fix 3: exchange layer[26]wire[8-15] <=> layer[28]wire[40-47]
                mdc_reverse_id( teid, tag, 46088, 47144 );

                // Fix 4: exchange layer[26]wire[16-23] <=> layer[30]wire[24-31]
                mdc_reverse_id( teid, tag, 46096, 48152 );
            }

            tag[0] = teid << 2;
            hits.push_back( reid );
        }

        if ( t_or_q == 0 )
        {
            if ( ( tag[0] & 1 ) == 0 )
            {
                tag[0] |= 1;
                tag[1] = signal_value;
                tag[3] |= overflow;
            }
            else
            {
                tag[3] |= 0xC;
                if ( signal_value >= tag[1] )
                {
                    if ( overflow ) signal_value |= ( 1 << 31 );
                    vm_tdc.push_back( { reid, signal_value } );
                }
                else
                {
                    if ( tag[3] & 1 ) tag[1] |= ( 1 << 31 );
                    vm_tdc.push_back( { reid, tag[1] } );
                    tag[1] = signal_value;
                    tag[3] &= ( 0xFFFFFFFF - 1 );
                    tag[3] |= overflow;
                }
            }
        }
        else
        {
            tag[0] |= 2;
            tag[2] = signal_value;
            if ( overflow ) tag[3] |= 2;
        }
    }

    // fill data
    for ( auto& [reid, data] : vm_tdc )
    {
        auto& tag = m_mdc_tags[reid];
        m_mdc_data.id->push_back( tag[0] >> 2 );
        m_mdc_data.tdc->push_back( data & 0x7FFFFFFF );
        m_mdc_data.adc->push_back( tag[2] );
        m_mdc_data.overflow->push_back( ( tag[3] & 0x16 ) | ( data >> 31 ) );
    }

    for ( auto& reid : hits )
    {
        auto& tag = m_mdc_tags[reid];
        m_mdc_data.id->push_back( tag[0] >> 2 );
        m_mdc_data.tdc->push_back( tag[1] );
        m_mdc_data.adc->push_back( tag[2] );
        m_mdc_data.overflow->push_back( tag[3] );
        tag[0] = 0;
    }
}

void RawBinaryParser::read_tof_buffer() {
    if ( m_buffers.tof.empty() && m_buffers.mrpc.empty() ) return;

    /* Refer to BOSS_Source/Event/RawDataCnv/TofConverter */
    auto n1buf = m_buffers.tof.size();
    auto n2buf = m_buffers.mrpc.size();
    auto nbuf  = n1buf + n2buf;

    struct TofDigi {
        uint32_t id;
        uint32_t adc;
        uint32_t tdc;
        uint32_t overflow;
    };

    multimap<uint32_t, TofDigi*> teid_to_digi;

    for ( uint32_t i = 0; i < nbuf; i++ )
    {
        bool is_tof      = i < n1buf;
        uint32_t buf_val = is_tof ? m_buffers.tof[i] : m_buffers.mrpc[i - n1buf];

        uint32_t teid, signal_value, overflow, t_or_q;

        if ( is_tof )
        {
            auto reid    = ( buf_val & 0x7FE00000 ) >> 21;
            signal_value = buf_val & 0x7FFFF;
            overflow     = ( buf_val & 0x80000 ) >> 19;
            t_or_q       = ( buf_val & 0x100000 ) >> 20;
            teid         = m_re2te.tof[reid];
        }
        else
        {
            if ( ( buf_val >> 25 ) == 0x7F ) teid = 0xFFFFFFFF;
            else
            {
                auto endcap = buf_val >> 31;
                auto module = ( buf_val >> 25 ) & 0x3F;
                auto strip  = ( buf_val >> 21 ) & 0xF;
                auto end    = ( buf_val >> 20 ) & 1;

                // refer to TofID::getIntID( int barrel_ec, int endcap, int module, int strip,
                // int end )
                teid = ( 0x20 << 24 ) | ( 3 << 14 ) | ( endcap << 11 ) | ( module << 5 ) |
                       ( strip << 1 ) | end;
                signal_value = buf_val & 0x7FFFF;
                overflow     = 0;
                t_or_q       = ( buf_val >> 19 ) & 1;
            }
        }

        if ( teid == 0xFFFFFFFF )
        {
            if ( ( buf_val >> 25 ) == 0x7F )
            {
                m_tof_data.id->push_back( 0xFFFFFFFF );
                m_tof_data.tdc->push_back( 0x7FFFFFFF );
                m_tof_data.adc->push_back( 0x7FFFFFFF );
                m_tof_data.overflow->push_back( buf_val );
            }
            continue;
        }

        auto count = teid_to_digi.count( teid );

        if ( count == 0 )
        {
            TofDigi* digi = new TofDigi{ .id       = teid,                               //
                                         .adc      = t_or_q ? signal_value : 0x7FFFFFFF, //
                                         .tdc      = t_or_q ? 0x7FFFFFFF : signal_value, //
                                         .overflow = t_or_q ? ( 0x10 | ( overflow << 1 ) )
                                                            : ( 0x20 | overflow ) };

            teid_to_digi.insert( { teid, digi } );
        }
        else
        {
            auto range = teid_to_digi.equal_range( teid );
            auto it    = range.first;
            auto digi  = it->second;
            if ( t_or_q ) // Q
            {
                if ( digi->adc == 0x7FFFFFFF ) // matched Q and T, first Q
                {
                    digi->adc      = signal_value;
                    digi->overflow = ( digi->overflow | ( overflow << 1 ) ) & 0xF;

                    while ( ++it != range.second ) // multiT
                    {
                        digi = it->second;
                        digi->overflow &= 0xF;
                    }
                }
                else // multiQ
                {
                    uint32_t flag = ( digi->overflow & 0x3C ) | 8;
                    while ( it != range.second )
                    {
                        digi           = ( it++ )->second;
                        digi->overflow = ( digi->overflow & 0x3 ) | flag;
                    }

                    digi = new TofDigi{ .id       = teid,
                                        .adc      = signal_value,
                                        .tdc      = 0x7FFFFFFF,
                                        .overflow = flag | ( overflow << 1 ) };

                    teid_to_digi.insert( { teid, digi } );
                }
            }
            else // T
            {
                if ( digi->tdc == 0x7FFFFFFF ) // matched T and Q, firstT
                {
                    digi->tdc      = signal_value;
                    digi->overflow = ( digi->overflow | overflow ) & 0xF;

                    while ( ++it != range.second ) // multiQ
                    {
                        digi = it->second;
                        digi->overflow &= 0xF;
                    }
                }
                else // multi T
                {
                    uint32_t flag = ( digi->overflow & 0x3C ) | 4;
                    while ( it != range.second )
                    {
                        digi           = ( it++ )->second;
                        digi->overflow = ( digi->overflow & 0x3 ) | flag;
                    }

                    digi = new TofDigi{ .id       = teid,
                                        .adc      = 0x7FFFFFFF,
                                        .tdc      = signal_value,
                                        .overflow = flag | overflow };

                    teid_to_digi.insert( { teid, digi } );
                }
            }
        }
    }

    // fill data
    for ( auto& [teid, digi] : teid_to_digi )
    {
        if ( ( teid & 0xFFFF7FFF ) != 0x20000060 )
        {
            m_tof_data.id->push_back( digi->id );
            m_tof_data.tdc->push_back( digi->tdc );
            m_tof_data.adc->push_back( digi->adc );
            m_tof_data.overflow->push_back( digi->overflow );
        }
        else
        {
            m_lumi_data.id->push_back( digi->id );
            m_lumi_data.tdc->push_back( digi->tdc );
            m_lumi_data.adc->push_back( digi->adc );
            m_lumi_data.overflow->push_back( digi->overflow );
        }

        delete digi;
    }
}

void RawBinaryParser::read_emc_buffer() {
    if ( m_buffers.emc.empty() ) return;

    /* Refer to BOSS_Source/Event/RawDataCnv/EmcConverter */
    for ( const auto& digi : m_buffers.emc )
    {
        auto reid = ( digi & 0xFFF80000 ) >> 19;
        auto teid = m_re2te.emc[reid];
        if ( teid == 0xFFFFFFFF ) continue;

        uint32_t adc     = digi & 0x7FF;
        uint32_t measure = ( digi & 0x1800 ) >> 11;
        uint32_t tdc     = ( digi & 0x7E000 ) >> 13;

        m_emc_data.id->push_back( teid );
        m_emc_data.adc->push_back( adc );
        m_emc_data.tdc->push_back( tdc );
        m_emc_data.measure->push_back( measure );
    }
}

void RawBinaryParser::read_muc_buffer() {
    if ( m_buffers.muc.empty() ) return;

    for ( const auto& digi : m_buffers.muc )
    {
        auto fec_addr = ( digi & 0xFFFF0000 ) >> 16;
        auto module   = ( fec_addr & 0xF800 ) >> 5;
        auto reid     = ( fec_addr & 0x07FF ) | module;
        auto fec_data = digi & 0xFFFF;

        auto strsqc = m_muc_strsqc[reid];
        auto teid   = m_re2te.muc[reid];
        if ( teid == 0xFFFFFFFF ) continue;

        auto teid_base = teid & 0xFF0FFFFF;
        uint32_t new_teid;
        for ( uint32_t k = 0; fec_data != 0 && k < 16; fec_data >>= 1, ++k )
        {
            if ( ( fec_data & 1 ) == 0 ) continue;
            if ( strsqc == 0 ) new_teid = teid_base + 15 - k;
            else new_teid = teid_base + k;
            m_muc_data.id->push_back( new_teid );
        }
    }
}

void RawBinaryParser::read_trg_buffer() {
    if ( m_buffers.trg.empty() ) return;

    /* Refer to BOSS_Source/Event/RawDataCnvSvc/RawDataTrigGTDCnv */
    for ( const auto& buf : m_buffers.trg )
    {
        uint32_t cursor = 0;
        while ( cursor < buf.size() - 1 )
        {
            auto word       = buf[cursor];
            auto block_size = ( word >> 14 ) & 0x3FF;
            auto id         = word >> 24;
            if ( block_size == 0 || ( cursor + block_size > buf.size() ) ) break;

            if ( ( id > 0xD1 && id < 0xD8 && id != 0xD5 ) || id == 0xDA ||
                 ( id > 0xE1 && id < 0xED ) )
            {
                m_trg_data.id->push_back( id );
                m_trg_data.data_size->push_back( block_size - 1 );
                m_trg_data.time_window->push_back( ( word >> 8 ) & 0x3F );
                m_trg_data.data_type->push_back( ( word >> 3 ) & 0x1F );
            }

            cursor += block_size;
        }
    }
}

void RawBinaryParser::read_cgem_buffer() {
    if ( m_buffers.cgem.empty() ) return;

    auto cursor = m_buffers.cgem.data();

    auto evt_size = *cursor;
    if ( evt_size != m_buffers.cgem.size() * 4 )
    {
        throw runtime_error( "Invalid CGEM data size: expecting " + to_string( evt_size ) +
                             " but get " + to_string( m_buffers.cgem.size() * 4 ) );
    }

    auto evt_start = cursor[1];
    if ( evt_start != 0xFFFFFFFF )
    {
        throw runtime_error( "Invalid CGEM event start: expecting 0xFFFFFFFF but get " +
                             to_string( evt_start ) );
    }

    cursor += 2;

    struct CgemDigi {
        uint32_t tiger;
        uint32_t last_trigger_frame;
        uint32_t tac;
        uint32_t channel;
        uint32_t t_coarse;
        uint32_t e_coarse;
        uint32_t t_fine;
        uint32_t e_fine;
    };

    vector<CgemDigi> digi_buffer;

    auto cursor_end = m_buffers.cgem.data() + m_buffers.cgem.size();
    while ( cursor < cursor_end )
    {
        auto pack_header = cursor[0] & 0xE0000000;
        if ( pack_header != 0xC0000000 )
        {
            throw runtime_error( "Invalid CGEM pack header: expecting 0xC0000000 but get " +
                                 to_string( pack_header ) );
        }

        auto local_l1_timestamp = cursor[1] & 0xFFFF;

        // hits
        cursor += 2;
        while ( true )
        {
            if ( ( cursor[0] & 0xC0000000 ) != 0 ) break;

            auto hit0 = cursor[0];
            auto hit1 = cursor[1];

            digi_buffer.emplace_back( CgemDigi{
                .tiger              = hit0 >> 27,
                .last_trigger_frame = ( hit0 >> 24 ) & 0x7,
                .tac                = ( hit0 >> 16 ) & 0x3,
                .channel            = ( hit0 >> 18 ) & 0x3F,
                .t_coarse           = hit0 & 0xFFFF,
                .e_coarse           = hit1 >> 20,
                .t_fine             = ( hit1 >> 10 ) & 0x3FF,
                .e_fine             = hit1 & 0x3FF,
            } );

            cursor += 2;
        }

        auto trailer0 = cursor[0];
        // auto trailer1 = cursor[1];
        auto trailer2 = cursor[2];
        auto trailer3 = cursor[3];
        cursor += 4;

        auto gemroc = trailer0 & 0x1F;
        // auto tiger  = trailer1 >> 27; // no need to read this

        if ( ( trailer2 & 0xF0000000 ) != 0x40000000 )
        {
            throw runtime_error(
                "Invalid CGEM UDPSeqCounter[0]: expecting 0x40000000 but get " +
                to_string( trailer2 & 0xF0000000 ) );
        }

        if ( ( trailer3 & 0xF0000000 ) != 0xA0000000 )
        {
            throw runtime_error(
                "Invalid CGEM UDPSeqCounter[1]: expecting 0xA0000000 but get " +
                to_string( trailer3 & 0xF0000000 ) );
        }

        if ( ( ( trailer2 >> 20 ) & 0x1F ) != gemroc )
        {
            throw runtime_error( "Invalid CGEM trailer gemroc: expecting " +
                                 to_string( gemroc ) + " but get " +
                                 to_string( ( trailer2 >> 20 ) & 0x1F ) );
        }

        // fill data
        for ( auto& digi : digi_buffer )
        {
            auto idx     = ( gemroc * 8 + digi.tiger ) * 64 + digi.channel;
            auto digi_id = m_cgem_table.idx_to_digi_id[idx];
            if ( digi_id == 0xFFFFFFFF ) continue; // invalid digi id, skip this hit

            auto constant = m_cgem_table.idx_to_const[idx];
            auto slope    = m_cgem_table.idx_to_slope[idx];

            m_cgem_data.id->push_back( digi_id );
            m_cgem_data.adc->push_back( digi.e_fine );
            m_cgem_data.tdc->push_back( digi.t_fine );

            // calculate time
            double t_l1 = local_l1_timestamp;
            if ( local_l1_timestamp < digi.t_coarse ) t_l1 += 65536;
            double time = ( t_l1 - digi.t_coarse ) * ( -1000. ) / 4. / 41.65;
            m_cgem_data.time->push_back( time );

            // calculate charge
            double e_fine_new = digi.e_fine;

            if ( ( ( constant == 0.0 ) && ( slope == 0.0 ) ) ||
                 ( ( constant == 1.0 ) && ( slope == 1.0 ) ) )
                m_cgem_data.charge->push_back( 9999. ); // invalid charge
            else
            {
                if ( digi.e_fine > 1007 ) e_fine_new -= 1024.;
                m_cgem_data.charge->push_back( ( e_fine_new - constant ) / slope );
            }
        }

        digi_buffer.clear();
    }
}

py::dict RawBinaryParser::arrays() {
    // - read data
    py::gil_scoped_release release;
    fill_offsets(); // fill the first offset
    while ( m_cursor < m_data_end ) { read_event(); }
    py::gil_scoped_acquire acquire;

    // - convert data to numpy array
    py::dict res;

    // event header
    py::dict evt_header;
    evt_header["evt_time"] = make_array( m_evt_header_data.evt_time );
    evt_header["evt_no"]   = make_array( m_evt_header_data.evt_no );
    evt_header["run_no"]   = make_array( m_evt_header_data.run_no );
    evt_header["l1_id"]    = make_array( m_evt_header_data.l1_id );
    evt_header["evt_tag1"] = make_array( m_evt_header_data.evt_tag1 );
    evt_header["evt_tag2"] = make_array( m_evt_header_data.evt_tag2 );
    evt_header["evt_tag3"] = make_array( m_evt_header_data.evt_tag3 );
    evt_header["evt_tag4"] = make_array( m_evt_header_data.evt_tag4 );

    res["evt_header"] = evt_header;

    // fields
    for ( auto& field_id : m_active_field_ids )
    {
        switch ( field_id )
        {
        case FieldID::MDC: {
            auto& [data_id, data_t, data_q, data_overflow] = m_mdc_data;

            py::dict mdc_data;
            mdc_data["m_intId"]         = make_array( data_id );
            mdc_data["m_chargeChannel"] = make_array( data_q );
            mdc_data["m_timeChannel"]   = make_array( data_t );
            mdc_data["m_overflow"]      = make_array( data_overflow );

            auto offsets = make_array( m_mdc_offsets );

            res["mdc"] = py::make_tuple( offsets, mdc_data );
            break;
        }

        case FieldID::TOF: {
            auto& [data_id, data_t, data_q, data_overflow] = m_tof_data;

            py::dict tof_data;
            tof_data["m_intId"]         = make_array( data_id );
            tof_data["m_chargeChannel"] = make_array( data_q );
            tof_data["m_timeChannel"]   = make_array( data_t );
            tof_data["m_overflow"]      = make_array( data_overflow );

            auto offsets = make_array( m_tof_offsets );

            res["tof"] = py::make_tuple( offsets, tof_data );
            break;
        }

        case FieldID::EMC: {
            auto& [data_id, data_t, data_q, data_measure] = m_emc_data;

            py::dict emc_data;
            emc_data["m_intId"]         = make_array( data_id );
            emc_data["m_chargeChannel"] = make_array( data_q );
            emc_data["m_timeChannel"]   = make_array( data_t );
            emc_data["m_measure"]       = make_array( data_measure );

            auto offsets = make_array( m_emc_offsets );

            res["emc"] = py::make_tuple( offsets, emc_data );
            break;
        }

        case FieldID::MUC: {
            auto& [data_id] = m_muc_data;

            py::dict muc_data;
            muc_data["m_intId"] = make_array( data_id );

            auto offsets = make_array( m_muc_offsets );

            res["muc"] = py::make_tuple( offsets, muc_data );
            break;
        }

        case FieldID::TrigGTD: {
            auto& [id, data_size, time_window, data_type] = m_trg_data;

            py::dict trg_data;
            trg_data["m_id"]         = make_array( id );
            trg_data["m_dataSize"]   = make_array( data_size );
            trg_data["m_timeWindow"] = make_array( time_window );
            trg_data["m_dataType"]   = make_array( data_type );

            auto trg_offsets = make_array( m_trg_offsets );
            res["trigGTD"]   = py::make_tuple( trg_offsets, trg_data );
            break;
        }

        case FieldID::CGEM: {
            py::dict cgem_data;
            cgem_data["m_intId"]         = make_array( m_cgem_data.id );
            cgem_data["m_chargeChannel"] = make_array( m_cgem_data.adc );
            cgem_data["m_timeChannel"]   = make_array( m_cgem_data.tdc );
            cgem_data["m_time_ns"]       = make_array( m_cgem_data.time );
            cgem_data["m_charge_fc"]     = make_array( m_cgem_data.charge );

            auto cgem_offsets = make_array( m_cgem_offsets );
            res["cgem"]       = py::make_tuple( cgem_offsets, cgem_data );
            break;
        }
        }
    }

    return res;
}

py::dict py_read_bes_raw( py::array_t<uint32_t> data, vector<string> fields,
                          map<string, py::array> info_tables ) {
    return RawBinaryParser( data, fields, info_tables ).arrays();
}
