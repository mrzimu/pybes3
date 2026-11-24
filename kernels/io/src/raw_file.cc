#include <pybind11/stl.h>

#include <algorithm>
#include <cstring>
#include <stdexcept>

#include "raw_file.hh"
#include "raw_io.hh"

#ifdef _WIN32
#    include <windows.h>
#endif

namespace {

    constexpr uint32_t FLAG_FILE_START      = 0x1234AAAA;
    constexpr uint32_t FLAG_FILE_NAME       = 0x1234AABB;
    constexpr uint32_t FLAG_RUN_PARAMS      = 0x1234BBBB;
    constexpr uint32_t FLAG_DATA_SEPERATOR  = 0x1234CCCC;
    constexpr uint32_t FLAG_FILE_TAIL_START = 0x1234DDDD;
    constexpr uint32_t FLAG_FILE_END        = 0x1234EEEE;
    constexpr uint32_t FLAG_FULL_EVENT      = 0xAA1234AA;

    // Header strings are padded to a multiple of four bytes with '\0'.
    bool is_padding( unsigned char c ) {
        return c == '\0' || c == ' ' || c == '\t' || c == '\n' || c == '\r' || c == '\v' ||
               c == '\f';
    }

    std::string trim_padding( std::string s ) {
        size_t begin = 0;
        size_t end   = s.size();
        while ( begin < end && is_padding( static_cast<unsigned char>( s[begin] ) ) ) begin++;
        while ( end > begin && is_padding( static_cast<unsigned char>( s[end - 1] ) ) ) end--;
        return s.substr( begin, end - begin );
    }

#ifdef _WIN32
    std::wstring utf8_to_wide( const std::string& s ) {
        if ( s.empty() ) return {};
        int n = MultiByteToWideChar( CP_UTF8, 0, s.c_str(), int( s.size() ), nullptr, 0 );
        std::wstring w( size_t( n ), L'\0' );
        MultiByteToWideChar( CP_UTF8, 0, s.c_str(), int( s.size() ), w.data(), n );
        return w;
    }
#endif

} // namespace

RawFileReader::RawFileReader( const std::string& path ) : m_path( path ) {

#ifdef _WIN32
    m_file.open( utf8_to_wide( path ), std::ios::binary );
#else
    m_file.open( path, std::ios::binary );
#endif
    if ( !m_file.is_open() )
    {
        PyErr_SetFromErrnoWithFilename( PyExc_OSError, path.c_str() );
        throw py::error_already_set();
    }

    m_file.seekg( 0, std::ios::end );
    m_size = int64_t( m_file.tellg() );
    if ( m_size < 40 ) throw std::runtime_error( "Raw file is too small: " + path );

    preprocess_file();

    m_buf_byte = m_data_start;
}

RawFileReader::~RawFileReader() { close(); }

void RawFileReader::close() {
    if ( m_file.is_open() ) m_file.close();
}

uint32_t RawFileReader::read_word() {
    uint32_t word = 0;
    m_file.read( reinterpret_cast<char*>( &word ), 4 );
    if ( m_file.gcount() != 4 ) throw std::runtime_error( "Unexpected end of raw file" );
    return word;
}

void RawFileReader::skip_words( size_t n ) { m_file.seekg( int64_t( n ) * 4, std::ios::cur ); }

std::string RawFileReader::read_string( size_t n_bytes ) {
    std::string s( n_bytes, '\0' );
    if ( n_bytes > 0 )
    {
        m_file.read( s.data(), std::streamsize( n_bytes ) );
        if ( size_t( m_file.gcount() ) != n_bytes )
            throw std::runtime_error( "Unexpected end of raw file" );
    }
    return trim_padding( s );
}

size_t RawFileReader::read_at( int64_t pos, void* dst, size_t n_bytes ) {
    if ( n_bytes == 0 ) return 0;

    m_file.clear();
    m_file.seekg( pos, std::ios::beg );
    if ( !m_file ) return 0;

    m_file.read( static_cast<char*>( dst ), std::streamsize( n_bytes ) );
    return size_t( m_file.gcount() );
}

void RawFileReader::preprocess_file() {
    m_file.seekg( 0, std::ios::beg );

    if ( read_word() != FLAG_FILE_START ) throw std::runtime_error( "Invalid start flag" );
    skip_words( 1 );

    m_file_version = read_word();
    m_file_number  = read_word();
    m_file_date    = read_word();
    m_file_time    = read_word();
    skip_words( 2 );

    if ( read_word() != FLAG_FILE_NAME ) throw std::runtime_error( "Invalid file name flag" );

    const uint32_t nchar_name = read_word();
    if ( nchar_name > 65536 ) throw std::runtime_error( "Invalid file name length" );
    m_file_name = read_string( size_t( ( nchar_name + 3 ) / 4 ) * 4 );

    const uint32_t nchar_tag = read_word();
    if ( nchar_tag > 65536 ) throw std::runtime_error( "Invalid file tag length" );
    m_file_tag = read_string( size_t( ( nchar_tag + 3 ) / 4 ) * 4 );

    if ( read_word() != FLAG_RUN_PARAMS )
        throw std::runtime_error( "Invalid run params flag" );
    skip_words( 1 );

    m_run_number    = read_word();
    m_max_events    = read_word();
    m_rec_enable    = read_word();
    m_trigger_type  = read_word();
    m_detector_mask = read_word();
    m_beam_type     = read_word();
    m_beam_energy   = read_word();

    m_data_start = int64_t( m_file.tellg() );
    m_data_end   = m_size - 40;
    if ( m_data_end < m_data_start ) throw std::runtime_error( "Invalid raw file layout" );

    m_file.seekg( m_data_end, std::ios::beg );
    if ( read_word() != FLAG_FILE_TAIL_START )
        throw std::runtime_error( "Invalid file tail start flag" );
    skip_words( 3 );
    m_entries = read_word();
    skip_words( 4 );
    if ( read_word() != FLAG_FILE_END ) throw std::runtime_error( "Invalid file end flag" );

    // A corrupt tail must not turn into a huge index allocation.
    if ( int64_t( m_entries ) * MIN_EVENT_BYTES > m_data_end - m_data_start )
        throw std::runtime_error( "Invalid number of entries: " +
                                  std::to_string( m_entries ) );

    m_starts.assign( size_t( m_entries ), -1 );
    m_stops.assign( size_t( m_entries ), -1 );
    m_max_looped_entry = -1;

    m_mean_event_bytes = ( m_entries > 0 ) ? ( m_data_end - m_data_start ) / m_entries : 0;
}

const uint32_t* RawFileReader::scan_ptr( int64_t pos, size_t n_words ) {
    const size_t need = n_words * 4;
    const bool inside =
        pos >= m_scan_base && pos + int64_t( need ) <= m_scan_base + int64_t( m_scan_len );
    if ( !inside )
    {
        const int64_t avail = m_data_end - pos;
        if ( avail <= 0 ) throw std::runtime_error( "Raw data truncated" );

        const size_t want  = std::max<size_t>( SCAN_CHUNK, need );
        const size_t bytes = size_t( std::min<int64_t>( avail, int64_t( want ) ) );
        if ( m_scan_buf.size() * 4 < bytes ) m_scan_buf.resize( ( bytes + 3 ) / 4 );

        m_scan_base = pos;
        m_scan_len  = read_at( pos, m_scan_buf.data(), bytes );
        if ( m_scan_len < need ) throw std::runtime_error( "Raw data truncated" );
    }

    return m_scan_buf.data() + ( pos - m_scan_base ) / 4;
}

size_t RawFileReader::peek_event_words( int64_t pos, size_t& prefix_words ) {
    const uint32_t* p = scan_ptr( pos, 2 );
    prefix_words      = ( p[0] == FLAG_DATA_SEPERATOR ) ? 4 : 0;

    p = scan_ptr( pos, prefix_words + 2 );
    if ( p[prefix_words] != FLAG_FULL_EVENT )
        throw std::runtime_error( "Invalid event fragment flag" );

    const size_t total = p[prefix_words + 1];
    if ( total < 2 ) throw std::runtime_error( "Invalid event size" );
    return prefix_words + total;
}

void RawFileReader::scan_to( int64_t entry ) {
    if ( m_entries == 0 ) return;
    entry = std::min( entry, m_entries - 1 );
    if ( entry <= m_max_looped_entry ) return;

    int64_t cur = m_max_looped_entry;
    int64_t pos = ( cur < 0 ) ? m_data_start : m_stops[size_t( cur )];

    while ( cur < entry )
    {
        cur++;
        size_t prefix      = 0;
        const size_t words = peek_event_words( pos, prefix );

        m_starts[size_t( cur )] = pos + int64_t( prefix ) * 4;
        pos += int64_t( words ) * 4;
        if ( pos > m_data_end ) throw std::runtime_error( "Invalid event size" );
        m_stops[size_t( cur )] = pos;
    }

    m_max_looped_entry = cur;
}

void RawFileReader::seek_entry( int64_t entry ) {
    if ( entry == m_next_entry ) return;

    int64_t offset = 0;
    if ( entry == 0 ) { offset = m_data_start; }
    else if ( entry >= m_entries ) { offset = m_data_end; }
    else if ( m_starts[size_t( entry )] >= 0 ) { offset = m_starts[size_t( entry )]; }
    else
    {
        scan_to( entry );
        offset = m_starts[size_t( entry )];
    }

    m_buf_byte   = offset;
    m_buf_words  = 0;
    m_pos        = 0;
    m_next_entry = entry;
}

void RawFileReader::ensure( size_t n_words ) {
    if ( m_pos + n_words <= m_buf_words ) return;

    // A corrupt size word must not turn into a huge allocation.
    if ( n_words > size_t( ( m_data_end - m_buf_byte ) / 4 ) )
        throw std::runtime_error( "Invalid event size" );

    if ( m_pos > 0 )
    {
        const size_t rest = m_buf_words - m_pos;
        if ( rest > 0 ) std::memmove( m_buf.data(), m_buf.data() + m_pos, rest * 4 );
        m_buf_byte += int64_t( m_pos ) * 4;
        m_buf_words = rest;
        m_pos       = 0;
    }

    while ( m_buf_words < n_words )
    {
        const size_t want = std::max<size_t>( m_chunk_words, n_words - m_buf_words );
        if ( m_buf.size() < m_buf_words + want ) m_buf.resize( m_buf_words + want );

        const int64_t pos   = m_buf_byte + int64_t( m_buf_words ) * 4;
        const int64_t avail = m_data_end - pos;
        if ( avail <= 0 ) throw std::runtime_error( "Raw data truncated" );

        const size_t bytes = size_t( std::min<int64_t>( avail, int64_t( want ) * 4 ) );
        const size_t got   = read_at( pos, m_buf.data() + m_buf_words, bytes );
        if ( got == 0 || got % 4 != 0 ) throw std::runtime_error( "Raw data truncated" );

        m_buf_words += got / 4;
    }
}

size_t RawFileReader::ensure_event() {
    ensure( 2 );

    size_t offset = ( m_buf[m_pos] == FLAG_DATA_SEPERATOR ) ? 4 : 0;
    ensure( offset + 2 );

    if ( m_buf[m_pos + offset] != FLAG_FULL_EVENT )
        throw std::runtime_error( "Invalid event fragment flag" );

    const size_t total = m_buf[m_pos + offset + 1];
    if ( total < 2 ) throw std::runtime_error( "Invalid event size" );

    ensure( offset + total );

    m_event_words = total;
    return m_pos + offset;
}

py::dict RawFileReader::read( int64_t entry_start, int64_t n_events,
                              const std::vector<std::string>& fields,
                              const py::dict& info_tables ) {
    if ( entry_start < 0 || entry_start > m_entries )
        throw py::value_error( "entry_start is out of range" );
    if ( n_events < 0 ) throw py::value_error( "n_events must not be negative" );
    if ( !m_file.is_open() ) throw py::value_error( "I/O operation on closed raw file" );

    const int64_t n = std::min( n_events, m_entries - entry_start );

    auto tables = info_tables.cast<std::map<std::string, py::array>>();
    RawBinaryParser parser( fields, std::move( tables ) );

    const int64_t estimate   = std::max<int64_t>( 1, n ) * m_mean_event_bytes;
    const size_t chunk_bytes = size_t(
        std::max<int64_t>( int64_t( MIN_PARSE_BYTES ),
                           std::min<int64_t>( int64_t( MAX_PARSE_BYTES ), estimate ) ) );
    m_chunk_words = std::max<size_t>( 1, chunk_bytes / 4 );

    {
        py::gil_scoped_release release;

        seek_entry( entry_start );
        parser.begin();

        try
        {
            for ( int64_t i = 0; i < n; i++ )
            {
                const size_t at   = ensure_event();
                const size_t span = m_event_words;

                parser.set_range( m_buf.data() + at, m_buf.data() + at + span );
                parser.read_one();

                m_pos = at + span;
            }
        } catch ( ... )
        {
            // Drop the cached cursor position: the buffer now points into the middle of
            // the event that failed, so the next read has to seek again.
            m_next_entry = -1;
            m_buf_byte   = m_data_start;
            m_buf_words  = 0;
            m_pos        = 0;
            throw;
        }

        m_next_entry = entry_start + n;
    }

    return parser.arrays();
}

void RawFileReader::build_entry_index() {
    if ( !m_file.is_open() ) throw std::runtime_error( "I/O operation on closed raw file" );
    if ( m_entries > 0 ) scan_to( m_entries - 1 );
}

py::array_t<int64_t> RawFileReader::entry_starts() {
    const py::ssize_t n = py::ssize_t( m_entries );
    py::array_t<int64_t> arr( n );
    auto* data = arr.mutable_data();
    for ( int64_t i = 0; i < m_entries; i++ ) data[i] = m_starts[size_t( i )];
    return arr;
}

py::array_t<int64_t> RawFileReader::entry_stops() {
    const py::ssize_t n = py::ssize_t( m_entries );
    py::array_t<int64_t> arr( n );
    auto* data = arr.mutable_data();
    for ( int64_t i = 0; i < m_entries; i++ ) data[i] = m_stops[size_t( i )];
    return arr;
}

py::array_t<uint32_t> RawFileReader::read_block( int64_t n_blocks ) {
    if ( !m_file.is_open() ) throw py::value_error( "I/O operation on closed raw file" );

    std::vector<uint32_t> data;

    {
        py::gil_scoped_release release;

        int64_t pos = m_data_start;

        if ( n_blocks < 0 )
        {
            const size_t words = size_t( ( m_data_end - m_data_start ) / 4 );
            data.resize( words );
            if ( words > 0 && read_at( m_data_start, data.data(), words * 4 ) != words * 4 )
                throw std::runtime_error( "Raw data truncated" );
        }
        else
        {
            for ( int64_t i = 0; i < n_blocks; i++ )
            {
                if ( pos >= m_data_end ) break;

                uint32_t header[4] = { 0, 0, 0, 0 };
                if ( read_at( pos, header, sizeof( header ) ) != sizeof( header ) )
                    throw std::runtime_error( "Raw data truncated" );
                if ( header[0] != FLAG_DATA_SEPERATOR )
                    throw std::runtime_error( "Invalid data seperator flag" );

                pos += int64_t( sizeof( header ) ) + int64_t( header[3] ) / 4 * 4;
                if ( pos > m_data_end ) throw std::runtime_error( "Invalid block size" );
            }

            const size_t words = size_t( ( pos - m_data_start ) / 4 );
            data.resize( words );
            if ( words > 0 && read_at( m_data_start, data.data(), words * 4 ) != words * 4 )
                throw std::runtime_error( "Raw data truncated" );
        }
    }

    const py::ssize_t n = py::ssize_t( data.size() );
    py::array_t<uint32_t> arr( n );
    if ( !data.empty() ) std::memcpy( arr.mutable_data(), data.data(), data.size() * 4 );
    return arr;
}
