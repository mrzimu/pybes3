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
#include <vector>

#include "root_io.hh"

namespace py = pybind11;
using namespace std;

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
        MDC     = 0xA1,
        TOF     = 0xA2,
        EMC     = 0xA3,
        MUC     = 0xA4,
        TrigGTD = 0xA5,
        MRPC    = 0xA7,
        CGEM    = 0xA8,
    };

    const set<uint32_t> sub_det_ids = {
        SubDetID::MDC,     SubDetID::TOF,  SubDetID::EMC,  SubDetID::MUC,
        SubDetID::TrigGTD, SubDetID::MRPC, SubDetID::CGEM,
    };

    map<string, const uint32_t> sub_det_names_to_ids = {
        { "mdc", SubDetID::MDC }, { "tof", SubDetID::TOF },         { "emc", SubDetID::EMC },
        { "muc", SubDetID::MUC }, { "trigGTD", SubDetID::TrigGTD }, { "cgem", SubDetID::CGEM },
    };

    // (21 x 8 + 4) x 64 for 21 fully used gemrocs, 8 tigers per gemroc, 64 channels per tiger,
    // plus 4 extra tigers for partial used gemroc.
    static constexpr size_t CGEM_N_ELEC_STRIPS = 11008;

  public:
    RawBinaryParser( py::array_t<uint32_t> data, vector<string> sub_detectors,
                     map<string, py::array> info_tables )
        : m_data_start( static_cast<uint32_t*>( data.request().ptr ) )
        , m_data_end( static_cast<uint32_t*>( data.request().ptr ) + data.size() )
        , m_cursor( static_cast<uint32_t*>( data.request().ptr ) ) {

        /* Initialize CGEM table */
        auto np_layer      = info_tables["cgem_layer"].cast<py::array_t<uint8_t>>();
        auto np_sheet      = info_tables["cgem_sheet"].cast<py::array_t<uint8_t>>();
        auto np_strip_type = info_tables["cgem_strip_type"].cast<py::array_t<uint8_t>>();
        auto np_strip      = info_tables["cgem_strip"].cast<py::array_t<uint16_t>>();
        auto np_const      = info_tables["cgem_constant"].cast<py::array_t<double>>();
        auto np_slope      = info_tables["cgem_slope"].cast<py::array_t<double>>();
        auto np_digi_id    = info_tables["cgem_digi_id"].cast<py::array_t<uint32_t>>();

        // check shape
        bool check_shape = true;

        check_shape = check_shape && np_layer.size() == CGEM_N_ELEC_STRIPS;
        check_shape = check_shape && np_sheet.size() == CGEM_N_ELEC_STRIPS;
        check_shape = check_shape && np_strip_type.size() == CGEM_N_ELEC_STRIPS;
        check_shape = check_shape && np_strip.size() == CGEM_N_ELEC_STRIPS;
        check_shape = check_shape && np_const.size() == CGEM_N_ELEC_STRIPS;
        check_shape = check_shape && np_slope.size() == CGEM_N_ELEC_STRIPS;
        check_shape = check_shape && np_digi_id.size() == CGEM_N_ELEC_STRIPS;
        if ( !check_shape )
        {
            throw runtime_error(
                "Invalid CGEM table: expecting arrays of size " +
                to_string( CGEM_N_ELEC_STRIPS ) + ", get: " + to_string( np_layer.size() ) +
                ", " + to_string( np_sheet.size() ) + ", " +
                to_string( np_strip_type.size() ) + ", " + to_string( np_strip.size() ) +
                ", " + to_string( np_const.size() ) + ", " + to_string( np_slope.size() ) +
                ", " + to_string( np_digi_id.size() ) );
        }

        // assign to table
        m_cgem_table.idx_to_layer      = static_cast<uint8_t*>( np_layer.request().ptr );
        m_cgem_table.idx_to_sheet      = static_cast<uint8_t*>( np_sheet.request().ptr );
        m_cgem_table.idx_to_strip_type = static_cast<uint8_t*>( np_strip_type.request().ptr );
        m_cgem_table.idx_to_strip      = static_cast<uint16_t*>( np_strip.request().ptr );
        m_cgem_table.idx_to_const      = static_cast<double*>( np_const.request().ptr );
        m_cgem_table.idx_to_slope      = static_cast<double*>( np_slope.request().ptr );
        m_cgem_table.idx_to_digi_id    = static_cast<uint32_t*>( np_digi_id.request().ptr );

        /* Initialize REID to TEID tables */
        auto np_mdc_reid_to_teid = info_tables["mdc_re2te"].cast<py::array_t<uint32_t>>();
        auto np_tof_reid_to_teid = info_tables["tof_re2te"].cast<py::array_t<uint32_t>>();
        auto np_emc_reid_to_teid = info_tables["emc_re2te"].cast<py::array_t<uint32_t>>();
        auto np_muc_reid_to_teid = info_tables["muc_re2te"].cast<py::array_t<uint32_t>>();
        auto np_muc_strsqc       = info_tables["muc_strsqc"].cast<py::array_t<uint32_t>>();

        // check shape
        check_shape = true;
        check_shape = check_shape && np_mdc_reid_to_teid.size() == 16384;
        check_shape = check_shape && np_tof_reid_to_teid.size() == 16384;
        check_shape = check_shape && np_emc_reid_to_teid.size() == 8192;
        check_shape = check_shape && np_muc_reid_to_teid.size() == 1024;
        check_shape = check_shape && np_muc_strsqc.size() == 1024;
        if ( !check_shape )
        {
            throw runtime_error(
                "Invalid REID to TEID table: expecting arrays of size 16384, get: " +
                to_string( np_mdc_reid_to_teid.size() ) );
        }

        // assign to table
        m_re2te.mdc  = static_cast<uint32_t*>( np_mdc_reid_to_teid.request().ptr );
        m_re2te.tof  = static_cast<uint32_t*>( np_tof_reid_to_teid.request().ptr );
        m_re2te.emc  = static_cast<uint32_t*>( np_emc_reid_to_teid.request().ptr );
        m_re2te.muc  = static_cast<uint32_t*>( np_muc_reid_to_teid.request().ptr );
        m_muc_strsqc = static_cast<uint32_t*>( np_muc_strsqc.request().ptr );

        /* set target sub_detectors */
        for ( auto& sub_det_name : sub_detectors )
        {
            if ( sub_det_names_to_ids.find( sub_det_name ) == sub_det_names_to_ids.end() )
                throw runtime_error( "Invalid sub-detector name: " + sub_det_name );

            auto sub_det_id = sub_det_names_to_ids[sub_det_name];
            m_activated_sub_det_ids.insert( sub_det_id );

            if ( sub_det_id == SubDetID::TOF )
                m_activated_sub_det_ids.insert( SubDetID::MRPC );
        }
    }

    py::dict arrays();

  private:
    uint32_t read();
    vector<uint32_t> read( size_t n );
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
    vector<uint32_t>& get_sub_detector_data( const uint32_t sub_det_id );

    uint32_t read_ROS( const uint32_t sub_det_id );
    uint32_t read_ROB( const uint32_t sub_det_id );

    void read_data_from_buffers();
    void read_mdc_buffer();
    void read_tof_buffer();
    void read_emc_buffer();
    void read_muc_buffer();
    void read_trg_buffer();
    void read_cgem_buffer();

    // binary data
    const uint32_t* m_data_start;
    const uint32_t* m_data_end;
    uint32_t* m_cursor;

    // parsed data
    set<uint32_t> m_activated_sub_det_ids;

    // reid to teid tables
    struct {
        uint32_t* mdc{ nullptr };
        uint32_t* tof{ nullptr };
        uint32_t* emc{ nullptr };
        uint32_t* muc{ nullptr };
    } m_re2te;

    // buffers for current event
    struct {
        vector<uint32_t> mdc{};
        vector<uint32_t> tof{};
        vector<uint32_t> emc{};
        vector<uint32_t> muc{};
        vector<vector<uint32_t>> trg{};
        vector<uint32_t> mrpc{};
        vector<uint32_t> cgem{};

        void clear() {
            mdc.clear();
            tof.clear();
            emc.clear();
            muc.clear();
            trg.clear();
            mrpc.clear();
            cgem.clear();
        }
    } m_buffers;

    /* Event Header*/
    struct {
        SharedVector<uint32_t> evt_time{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> evt_no{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> run_no{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> l1_id{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> evt_tag1{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> evt_tag2{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> evt_tag3{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> evt_tag4{ make_shared_vector<uint32_t>() };
    } m_evt_header_data;

    /* MDC */
    SharedVector<uint32_t> m_mdc_offsets{ make_shared_vector<uint32_t>() };
    array<array<uint32_t, 4>, 16384> m_mdc_tags{};

    struct {
        SharedVector<uint32_t> id{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> tdc{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> adc{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> overflow{ make_shared_vector<uint32_t>() };
        size_t size() const { return id->size(); }
    } m_mdc_data;

    inline void mdc_reverse_id( uint32_t& teid, array<uint32_t, 4>& tag, const uint32_t val1,
                                const uint32_t val2 ) {
        const uint32_t mask = 65528;
        if ( ( teid & mask ) == val1 )
        {
            teid = ( teid & ~mask ) | val2;
            tag[3] |= 0x10;
        }
        else if ( ( teid & mask ) == val2 )
        {
            teid = ( teid & ~mask ) | val1;
            tag[3] |= 0x10;
        }
    }

    /* TOF */
    SharedVector<uint32_t> m_tof_offsets{ make_shared_vector<uint32_t>() };
    struct {
        SharedVector<uint32_t> id{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> tdc{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> adc{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> overflow{ make_shared_vector<uint32_t>() };
        size_t size() const { return id->size(); }
    } m_tof_data;

    /* EMC */
    SharedVector<uint32_t> m_emc_offsets{ make_shared_vector<uint32_t>() };
    struct {
        SharedVector<uint32_t> id{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> tdc{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> adc{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> measure{ make_shared_vector<uint32_t>() };
        size_t size() const { return id->size(); }
    } m_emc_data;

    /* MUC */
    uint32_t* m_muc_strsqc{ nullptr };
    SharedVector<uint32_t> m_muc_offsets{ make_shared_vector<uint32_t>() };
    struct {
        SharedVector<uint32_t> id{ make_shared_vector<uint32_t>() };
        size_t size() const { return id->size(); }
    } m_muc_data;

    /* TrigGTD */
    SharedVector<uint32_t> m_trg_offsets{ make_shared_vector<uint32_t>() };
    struct {
        SharedVector<uint32_t> id{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> data_size{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> time_window{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> data_type{ make_shared_vector<uint32_t>() };
        size_t size() const { return id->size(); }
    } m_trg_data;

    /* LUMI */
    SharedVector<uint32_t> m_lumi_offsets{ make_shared_vector<uint32_t>() };
    struct {
        SharedVector<uint32_t> id{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> tdc{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> adc{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> overflow{ make_shared_vector<uint32_t>() };
        size_t size() const { return id->size(); }
    } m_lumi_data;

    /* CGEM */
    struct {
        uint8_t* idx_to_layer{ nullptr };
        uint8_t* idx_to_sheet{ nullptr };
        uint8_t* idx_to_strip_type{ nullptr };
        uint16_t* idx_to_strip{ nullptr };
        double* idx_to_const{ nullptr };
        double* idx_to_slope{ nullptr };
        uint32_t* idx_to_digi_id{ nullptr };
    } m_cgem_table;

    SharedVector<uint32_t> m_cgem_offsets{ make_shared_vector<uint32_t>() };

    struct {
        SharedVector<uint32_t> id{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> adc{ make_shared_vector<uint32_t>() };
        SharedVector<uint32_t> tdc{ make_shared_vector<uint32_t>() };
        SharedVector<double> charge{ make_shared_vector<double>() };
        SharedVector<double> time{ make_shared_vector<double>() };
        size_t size() const { return id->size(); }
    } m_cgem_data;

    /* reading status */
    int64_t m_current_entry = -1;
};

py::dict py_read_bes_raw( py::array_t<uint32_t> data, vector<string> sub_detectors,
                          map<string, py::array> into_tables );
