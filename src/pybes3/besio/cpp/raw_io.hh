#pragma once

#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>

#include <array>
#include <cstddef>
#include <cstdint>
#include <map>
#include <set>
#include <string>
#include <tuple>
#include <vector>

namespace py = pybind11;

class RawBinaryParser {

    enum RawFlag : const uint32_t {
        FILE_START      = 0x1234AAAA,
        FILE_NAME       = 0x1234AABB,
        RUN_PARAMS      = 0x1234BBBB,
        DATA_SEPERATOR  = 0x1234CCCC,
        FILE_END_HEADER = 0x1234DDDD,
        FILE_END_TAIL   = 0x1234EEEE,

        FULL_EVENT   = 0xAA1234AA,
        SUB_DETECTOR = 0xBB1234BB,
        ROS          = 0xCC1234CC,
        ROB          = 0xDD1234DD,
        ROD          = 0xEE1234EE,
    };

    enum SubDetID : const uint32_t {
        MDC = 0xA1,
        TOF = 0xA2,
        EMC = 0xA3,
        MUC = 0xA4,
        TRG = 0xA5,
        EF  = 0x7C,
    };

    const std::set<uint32_t> sub_det_ids = {
        SubDetID::MDC, SubDetID::TOF, SubDetID::EMC,
        SubDetID::MUC, SubDetID::TRG, SubDetID::EF,
    };

    std::map<std::string, const uint32_t> sub_det_names_to_ids = {
        { "mdc", SubDetID::MDC }, { "tof", SubDetID::TOF }, { "emc", SubDetID::EMC },
        { "muc", SubDetID::MUC }, { "trg", SubDetID::TRG }, { "ef", SubDetID::EF },
    };

    const std::vector<std::string> evt_header_item_names = {
        "evt_time", "evt_no",   "run_no",   "l1_id",
        "evt_tag1", "evt_tag2", "evt_tag3", "evt_tag4",
    };

  public:
    RawBinaryParser( py::array_t<uint32_t> data )
        : m_data_start( static_cast<uint32_t*>( data.request().ptr ) )
        , m_data_end( static_cast<uint32_t*>( data.request().ptr ) + data.size() )
        , m_cursor( static_cast<uint32_t*>( data.request().ptr ) ) {}

    py::dict arrays( std::vector<std::string> sub_detectors );

  private:
    uint32_t read();
    std::vector<uint32_t> read( size_t n );
    void read( size_t n, uint32_t* data );

    void skip();
    void skip( size_t n );

    void reset_cursor();

    void preprocess_file();
    void skip_to_entry( long entry_start );
    void skip_event();
    void read_event();
    void fill_offsets();

    uint32_t read_sub_detector();
    std::vector<uint32_t>& get_sub_detector_data( const uint32_t sub_det_id );

    uint32_t read_ROS( const uint32_t sub_det_id );
    uint32_t read_ROB( const uint32_t sub_det_id );

    void fill_digi( const std::vector<uint32_t>& tmp_data, const uint32_t sub_det_id );

    // binary data
    const uint32_t* m_data_start;
    const uint32_t* m_data_end;
    uint32_t* m_cursor;

    // parsed data
    std::set<uint32_t> m_activated_sub_det_ids;

    std::vector<uint32_t> m_mdc_offsets;
    std::tuple<std::vector<uint16_t>, std::vector<uint16_t>, std::vector<uint16_t>,
               std::vector<uint8_t>>
        m_mdc_data; // id, t, q, overflow

    std::vector<uint32_t> m_tof_offsets;
    std::tuple<std::vector<uint16_t>, std::vector<uint16_t>, std::vector<uint16_t>,
               std::vector<uint8_t>>
        m_tof_data; // id, t, q, overflow

    std::vector<uint32_t> m_emc_offsets;
    std::tuple<std::vector<uint16_t>, std::vector<uint16_t>, std::vector<uint16_t>,
               std::vector<uint8_t>>
        m_emc_data; // id, t, q, measure

    std::vector<uint32_t> m_muc_offsets;
    std::tuple<std::vector<uint16_t>, std::vector<uint16_t>> m_muc_data; // id, FEC (?)

    std::vector<uint32_t> m_trg_offsets;
    std::vector<uint32_t> m_trg_data;

    std::vector<uint32_t> m_ef_offsets;
    std::vector<uint32_t> m_ef_data;

    std::array<std::vector<uint32_t>, 8> m_evt_header_data;

    // reading status
    int64_t m_current_entry = -1;
};

py::dict py_read_bes_raw( py::array_t<uint32_t> data, std::vector<std::string> sub_detectors );
