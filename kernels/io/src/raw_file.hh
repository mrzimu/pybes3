#pragma once

#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

#include <cstddef>
#include <cstdint>
#include <fstream>
#include <string>
#include <vector>

namespace py = pybind11;

/**
 * Sequential and random-access reader for a BES3 raw file.
 *
 * The class owns one file handle. The entry scan uses a small window and the
 * parse path streams the file through a reusable buffer, so a full read never
 * materialises the whole data section.
 */
class RawFileReader {
  public:
    explicit RawFileReader( const std::string& path );
    ~RawFileReader();

    void close();

    // file metadata
    int64_t file_version() const { return m_file_version; }
    int64_t file_number() const { return m_file_number; }
    int64_t file_date() const { return m_file_date; }
    int64_t file_time() const { return m_file_time; }
    const std::string& file_name() const { return m_file_name; }
    const std::string& file_tag() const { return m_file_tag; }
    int64_t run_number() const { return m_run_number; }
    int64_t max_events() const { return m_max_events; }
    int64_t rec_enable() const { return m_rec_enable; }
    int64_t trigger_type() const { return m_trigger_type; }
    int64_t detector_mask() const { return m_detector_mask; }
    int64_t beam_type() const { return m_beam_type; }
    int64_t beam_energy() const { return m_beam_energy; }
    int64_t entries() const { return m_entries; }
    int64_t data_start() const { return m_data_start; }
    int64_t data_end() const { return m_data_end; }
    int64_t size() const { return m_size; }
    bool closed() const { return !m_file.is_open(); }

    py::dict read( int64_t entry_start, int64_t n_events,
                   const std::vector<std::string>& fields, const py::dict& info_tables );

    // Entry index. The byte range of an entry is discovered by a forward scan, either
    // on demand while reading or all at once through build_entry_index().
    void build_entry_index();

    // Number of leading entries whose byte range is already known.
    int64_t index_valid() const { return m_max_looped_entry + 1; }

    // Byte offset of the FULL_EVENT flag of every entry. Entries that have not been
    // scanned yet are reported as -1, so call build_entry_index() first when the whole
    // index is needed.
    py::array_t<int64_t> entry_starts();
    py::array_t<int64_t> entry_stops();

    // Raw words of the data section. A negative n_blocks reads the whole section.
    py::array_t<uint32_t> read_block( int64_t n_blocks );

  private:
    static constexpr size_t SCAN_CHUNK      = 4u << 20;
    static constexpr size_t MAX_PARSE_BYTES = 64u << 20;
    static constexpr size_t MIN_PARSE_BYTES = 1u << 20;

    // The smallest possible event: the FULL_EVENT flag plus its size word.
    static constexpr int64_t MIN_EVENT_BYTES = 2 * 4;

    uint32_t read_word();
    void skip_words( size_t n );
    std::string read_string( size_t n_bytes );
    size_t read_at( int64_t pos, void* dst, size_t n_bytes );
    void preprocess_file();

    const uint32_t* scan_ptr( int64_t pos, size_t n_words );
    size_t peek_event_words( int64_t pos, size_t& prefix_words );
    void scan_to( int64_t entry );

    void seek_entry( int64_t entry );
    void ensure( size_t n_words );
    size_t ensure_event();

    std::ifstream m_file;
    std::string m_path;

    int64_t m_size             = 0;
    int64_t m_data_start       = 0;
    int64_t m_data_end         = 0;
    int64_t m_entries          = 0;
    int64_t m_mean_event_bytes = 0;

    int64_t m_file_version  = -1;
    int64_t m_file_number   = -1;
    int64_t m_file_date     = -1;
    int64_t m_file_time     = -1;
    int64_t m_run_number    = -1;
    int64_t m_max_events    = -1;
    int64_t m_rec_enable    = -1;
    int64_t m_trigger_type  = -1;
    int64_t m_detector_mask = -1;
    int64_t m_beam_type     = -1;
    int64_t m_beam_energy   = -1;

    std::string m_file_name;
    std::string m_file_tag;

    // entry boundaries, byte offsets; -1 means "not scanned yet"
    std::vector<int64_t> m_starts;
    std::vector<int64_t> m_stops;
    int64_t m_max_looped_entry = -1;

    // scan window
    std::vector<uint32_t> m_scan_buf;
    int64_t m_scan_base = 0;
    size_t m_scan_len   = 0;

    // parse stream buffer
    std::vector<uint32_t> m_buf;
    int64_t m_buf_byte   = 0;
    size_t m_buf_words   = 0;
    size_t m_pos         = 0;
    size_t m_chunk_words = 0;
    size_t m_event_words = 0;
    int64_t m_next_entry = -1;
};
