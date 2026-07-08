#include "mod.hh"
#include "ufunc.hh"

constexpr uint32_t DIGI_MDC_FLAG    = 0x10;
constexpr uint32_t DIGI_TOF_FLAG    = 0x20;
constexpr uint32_t DIGI_EMC_FLAG    = 0x30;
constexpr uint32_t DIGI_MUC_FLAG    = 0x40;
constexpr uint32_t DIGI_CGEM_FLAG   = 0x60;
constexpr uint32_t DIGI_FLAG_OFFSET = 24;
constexpr uint32_t DIGI_FLAG_MASK   = 0xFF000000;

constexpr uint32_t DIGI_MDC_WIRETYPE_OFFSET = 15;
constexpr uint32_t DIGI_MDC_WIRETYPE_MASK   = 0x00008000;
constexpr uint32_t DIGI_MDC_LAYER_OFFSET    = 9;
constexpr uint32_t DIGI_MDC_LAYER_MASK      = 0x00007E00;
constexpr uint32_t DIGI_MDC_WIRE_OFFSET     = 0;
constexpr uint32_t DIGI_MDC_WIRE_MASK       = 0x000001FF;
constexpr uint32_t DIGI_MDC_STEREO_WIRE     = 1;

constexpr uint32_t DIGI_TOF_PART_OFFSET = 14;
constexpr uint32_t DIGI_TOF_PART_MASK   = 0x0000C000;
constexpr uint32_t DIGI_TOF_END_OFFSET  = 0;
constexpr uint32_t DIGI_TOF_END_MASK    = 0x00000001;

constexpr uint32_t DIGI_TOF_SCINT_LAYER_OFFSET = 8;
constexpr uint32_t DIGI_TOF_SCINT_LAYER_MASK   = 0x00000100;
constexpr uint32_t DIGI_TOF_SCINT_PHI_OFFSET   = 1;
constexpr uint32_t DIGI_TOF_SCINT_PHI_MASK     = 0x000000FE;

constexpr uint32_t DIGI_TOF_MRPC_ENDCAP_OFFSET = 11;
constexpr uint32_t DIGI_TOF_MRPC_ENDCAP_MASK   = 0x00000800;
constexpr uint32_t DIGI_TOF_MRPC_MODULE_OFFSET = 5;
constexpr uint32_t DIGI_TOF_MRPC_MODULE_MASK   = 0x000007E0;
constexpr uint32_t DIGI_TOF_MRPC_STRIP_OFFSET  = 1;
constexpr uint32_t DIGI_TOF_MRPC_STRIP_MASK    = 0x0000001E;

constexpr uint32_t DIGI_EMC_MODULE_OFFSET = 16;
constexpr uint32_t DIGI_EMC_MODULE_MASK   = 0x000F0000;
constexpr uint32_t DIGI_EMC_THETA_OFFSET  = 8;
constexpr uint32_t DIGI_EMC_THETA_MASK    = 0x00003F00;
constexpr uint32_t DIGI_EMC_PHI_OFFSET    = 0;
constexpr uint32_t DIGI_EMC_PHI_MASK      = 0x000000FF;

constexpr uint32_t DIGI_MUC_PART_OFFSET    = 16;
constexpr uint32_t DIGI_MUC_PART_MASK      = 0x000F0000;
constexpr uint32_t DIGI_MUC_SEGMENT_OFFSET = 12;
constexpr uint32_t DIGI_MUC_SEGMENT_MASK   = 0x0000F000;
constexpr uint32_t DIGI_MUC_LAYER_OFFSET   = 8;
constexpr uint32_t DIGI_MUC_LAYER_MASK     = 0x00000F00;
constexpr uint32_t DIGI_MUC_CHANNEL_OFFSET = 0;
constexpr uint32_t DIGI_MUC_CHANNEL_MASK   = 0x000000FF;

constexpr uint32_t DIGI_CGEM_STRIP_OFFSET     = 7;
constexpr uint32_t DIGI_CGEM_STRIP_MASK       = 0x0007FF80;
constexpr uint32_t DIGI_CGEM_STRIPTYPE_OFFSET = 6;
constexpr uint32_t DIGI_CGEM_STRIPTYPE_MASK   = 0x00000040;
constexpr uint32_t DIGI_CGEM_SHEET_OFFSET     = 3;
constexpr uint32_t DIGI_CGEM_SHEET_MASK       = 0x00000038;
constexpr uint32_t DIGI_CGEM_LAYER_OFFSET     = 0;
constexpr uint32_t DIGI_CGEM_LAYER_MASK       = 0x00000007;

// ===========================================================================
// MDC
// ===========================================================================
template <typename T>
inline void check_mdc_id( T* mdc_id, bool* out ) noexcept {
    *out = ( ( *mdc_id & DIGI_FLAG_MASK ) >> DIGI_FLAG_OFFSET ) == DIGI_MDC_FLAG;
}

template <typename T>
inline void mdc_id_to_wire( T* mdc_id, T* out ) noexcept {
    *out = ( *mdc_id & DIGI_MDC_WIRE_MASK ) >> DIGI_MDC_WIRE_OFFSET;
}

template <typename T>
inline void mdc_id_to_layer( T* mdc_id, T* out ) noexcept {
    *out = ( *mdc_id & DIGI_MDC_LAYER_MASK ) >> DIGI_MDC_LAYER_OFFSET;
}

template <typename T>
inline void mdc_id_to_is_stereo( T* mdc_id, bool* out ) noexcept {
    *out = ( ( *mdc_id & DIGI_MDC_WIRETYPE_MASK ) >> DIGI_MDC_WIRETYPE_OFFSET ) ==
           DIGI_MDC_STEREO_WIRE;
}

template <typename T>
inline void get_mdc_id( T* wire, T* layer, T* wire_type, uint32_t* out ) noexcept {
    *out = ( ( *wire << DIGI_MDC_WIRE_OFFSET ) & DIGI_MDC_WIRE_MASK ) |
           ( ( *layer << DIGI_MDC_LAYER_OFFSET ) & DIGI_MDC_LAYER_MASK ) |
           ( ( *wire_type << DIGI_MDC_WIRETYPE_OFFSET ) & DIGI_MDC_WIRETYPE_MASK ) |
           ( DIGI_MDC_FLAG << DIGI_FLAG_OFFSET );
}

// ===========================================================================
// TOF
// ===========================================================================
template <typename T>
inline void check_tof_id( T* tof_id, bool* out ) noexcept {
    *out = ( ( *tof_id & DIGI_FLAG_MASK ) >> DIGI_FLAG_OFFSET ) == DIGI_TOF_FLAG;
}

template <typename T>
inline void tof_id_to_part( T* tof_id, T* out ) noexcept {
    T part = ( *tof_id & DIGI_TOF_PART_MASK ) >> DIGI_TOF_PART_OFFSET;
    if ( part == 3 )
    { part += ( *tof_id & DIGI_TOF_MRPC_ENDCAP_MASK ) >> DIGI_TOF_MRPC_ENDCAP_OFFSET; }
    *out = part;
}

template <typename T>
inline void tof_id_to_end( T* tof_id, T* out ) noexcept {
    *out = ( *tof_id & DIGI_TOF_END_MASK ) >> DIGI_TOF_END_OFFSET;
}

template <typename T>
inline void _tof_id_to_layer_or_module_1( T* tof_id, T* out ) noexcept {
    T part = ( *tof_id & DIGI_TOF_PART_MASK ) >> DIGI_TOF_PART_OFFSET;
    if ( part == 3 )
    { part += ( *tof_id & DIGI_TOF_MRPC_ENDCAP_MASK ) >> DIGI_TOF_MRPC_ENDCAP_OFFSET; }
    if ( part < 3 )
    { *out = ( *tof_id & DIGI_TOF_SCINT_LAYER_MASK ) >> DIGI_TOF_SCINT_LAYER_OFFSET; }
    else { *out = ( *tof_id & DIGI_TOF_MRPC_MODULE_MASK ) >> DIGI_TOF_MRPC_MODULE_OFFSET; }
}

template <typename T>
inline void _tof_id_to_layer_or_module_2( T* tof_id, T* part, T* out ) noexcept {
    if ( *part < 3 )
    { *out = ( *tof_id & DIGI_TOF_SCINT_LAYER_MASK ) >> DIGI_TOF_SCINT_LAYER_OFFSET; }
    else { *out = ( *tof_id & DIGI_TOF_MRPC_MODULE_MASK ) >> DIGI_TOF_MRPC_MODULE_OFFSET; }
}

template <typename T>
inline void _tof_id_to_phi_or_strip_1( T* tof_id, T* out ) noexcept {
    T part = ( *tof_id & DIGI_TOF_PART_MASK ) >> DIGI_TOF_PART_OFFSET;
    if ( part == 3 )
    { part += ( *tof_id & DIGI_TOF_MRPC_ENDCAP_MASK ) >> DIGI_TOF_MRPC_ENDCAP_OFFSET; }
    if ( part < 3 )
    { *out = ( *tof_id & DIGI_TOF_SCINT_PHI_MASK ) >> DIGI_TOF_SCINT_PHI_OFFSET; }
    else { *out = ( *tof_id & DIGI_TOF_MRPC_STRIP_MASK ) >> DIGI_TOF_MRPC_STRIP_OFFSET; }
}

template <typename T>
inline void _tof_id_to_phi_or_strip_2( T* tof_id, T* part, T* out ) noexcept {
    if ( *part < 3 )
    { *out = ( *tof_id & DIGI_TOF_SCINT_PHI_MASK ) >> DIGI_TOF_SCINT_PHI_OFFSET; }
    else { *out = ( *tof_id & DIGI_TOF_MRPC_STRIP_MASK ) >> DIGI_TOF_MRPC_STRIP_OFFSET; }
}

template <typename T>
inline void get_tof_id( T* part, T* layer_or_module, T* phi_or_strip, T* end,
                        uint32_t* out ) noexcept {
    if ( *part < 3 )
    {
        *out = ( ( *part << DIGI_TOF_PART_OFFSET ) & DIGI_TOF_PART_MASK ) |
               ( ( *layer_or_module << DIGI_TOF_SCINT_LAYER_OFFSET ) &
                 DIGI_TOF_SCINT_LAYER_MASK ) |
               ( ( *phi_or_strip << DIGI_TOF_SCINT_PHI_OFFSET ) & DIGI_TOF_SCINT_PHI_MASK ) |
               ( ( *end << DIGI_TOF_END_OFFSET ) & DIGI_TOF_END_MASK ) |
               ( DIGI_TOF_FLAG << DIGI_FLAG_OFFSET );
    }
    else
    {
        *out =
            ( ( 3 << DIGI_TOF_PART_OFFSET ) & DIGI_TOF_PART_MASK ) |
            ( ( ( *part - 3 ) << DIGI_TOF_MRPC_ENDCAP_OFFSET ) & DIGI_TOF_MRPC_ENDCAP_MASK ) |
            ( ( *layer_or_module << DIGI_TOF_MRPC_MODULE_OFFSET ) &
              DIGI_TOF_MRPC_MODULE_MASK ) |
            ( ( *phi_or_strip << DIGI_TOF_MRPC_STRIP_OFFSET ) & DIGI_TOF_MRPC_STRIP_MASK ) |
            ( ( *end << DIGI_TOF_END_OFFSET ) & DIGI_TOF_END_MASK ) |
            ( DIGI_TOF_FLAG << DIGI_FLAG_OFFSET );
    }
}

// ===========================================================================
// EMC
// ===========================================================================
template <typename T>
inline void check_emc_id( T* emc_id, bool* out ) noexcept {
    *out = ( ( *emc_id & DIGI_FLAG_MASK ) >> DIGI_FLAG_OFFSET ) == DIGI_EMC_FLAG;
}

template <typename T>
inline void emc_id_to_module( T* emc_id, T* out ) noexcept {
    *out = ( *emc_id & DIGI_EMC_MODULE_MASK ) >> DIGI_EMC_MODULE_OFFSET;
}

template <typename T>
inline void emc_id_to_theta( T* emc_id, T* out ) noexcept {
    *out = ( *emc_id & DIGI_EMC_THETA_MASK ) >> DIGI_EMC_THETA_OFFSET;
}

template <typename T>
inline void emc_id_to_phi( T* emc_id, T* out ) noexcept {
    *out = ( *emc_id & DIGI_EMC_PHI_MASK ) >> DIGI_EMC_PHI_OFFSET;
}

template <typename T>
inline void get_emc_id( T* module, T* theta, T* phi, uint32_t* out ) noexcept {
    *out = ( ( *module << DIGI_EMC_MODULE_OFFSET ) & DIGI_EMC_MODULE_MASK ) |
           ( ( *theta << DIGI_EMC_THETA_OFFSET ) & DIGI_EMC_THETA_MASK ) |
           ( ( *phi << DIGI_EMC_PHI_OFFSET ) & DIGI_EMC_PHI_MASK ) |
           ( DIGI_EMC_FLAG << DIGI_FLAG_OFFSET );
}

// ===========================================================================
// MUC
// ===========================================================================
template <typename T>
inline void check_muc_id( T* muc_id, bool* out ) noexcept {
    *out = ( ( *muc_id & DIGI_FLAG_MASK ) >> DIGI_FLAG_OFFSET ) == DIGI_MUC_FLAG;
}

template <typename T>
inline void muc_id_to_part( T* muc_id, T* out ) noexcept {
    *out = ( *muc_id & DIGI_MUC_PART_MASK ) >> DIGI_MUC_PART_OFFSET;
}

template <typename T>
inline void muc_id_to_segment( T* muc_id, T* out ) noexcept {
    *out = ( *muc_id & DIGI_MUC_SEGMENT_MASK ) >> DIGI_MUC_SEGMENT_OFFSET;
}

template <typename T>
inline void muc_id_to_layer( T* muc_id, T* out ) noexcept {
    *out = ( *muc_id & DIGI_MUC_LAYER_MASK ) >> DIGI_MUC_LAYER_OFFSET;
}

template <typename T>
inline void muc_id_to_channel( T* muc_id, T* out ) noexcept {
    *out = ( *muc_id & DIGI_MUC_CHANNEL_MASK ) >> DIGI_MUC_CHANNEL_OFFSET;
}

template <typename T>
inline void get_muc_id( T* part, T* segment, T* layer, T* channel, uint32_t* out ) noexcept {
    *out = ( ( *part << DIGI_MUC_PART_OFFSET ) & DIGI_MUC_PART_MASK ) |
           ( ( *segment << DIGI_MUC_SEGMENT_OFFSET ) & DIGI_MUC_SEGMENT_MASK ) |
           ( ( *layer << DIGI_MUC_LAYER_OFFSET ) & DIGI_MUC_LAYER_MASK ) |
           ( ( *channel << DIGI_MUC_CHANNEL_OFFSET ) & DIGI_MUC_CHANNEL_MASK ) |
           ( DIGI_MUC_FLAG << DIGI_FLAG_OFFSET );
}

// ===========================================================================
// CGEM
// ===========================================================================
template <typename T>
inline void check_cgem_id( T* cgem_id, bool* out ) noexcept {
    *out = ( ( *cgem_id & DIGI_FLAG_MASK ) >> DIGI_FLAG_OFFSET ) == DIGI_CGEM_FLAG;
}

template <typename T>
inline void cgem_id_to_layer( T* cgem_id, T* out ) noexcept {
    *out = ( *cgem_id & DIGI_CGEM_LAYER_MASK ) >> DIGI_CGEM_LAYER_OFFSET;
}

template <typename T>
inline void cgem_id_to_sheet( T* cgem_id, T* out ) noexcept {
    *out = ( *cgem_id & DIGI_CGEM_SHEET_MASK ) >> DIGI_CGEM_SHEET_OFFSET;
}

template <typename T>
inline void cgem_id_to_strip_type( T* cgem_id, T* out ) noexcept {
    *out = ( *cgem_id & DIGI_CGEM_STRIPTYPE_MASK ) >> DIGI_CGEM_STRIPTYPE_OFFSET;
}

template <typename T>
inline void cgem_id_to_strip( T* cgem_id, uint16_t* out ) noexcept {
    *out =
        static_cast<uint16_t>( ( *cgem_id & DIGI_CGEM_STRIP_MASK ) >> DIGI_CGEM_STRIP_OFFSET );
}

template <typename T>
inline void get_cgem_id( T* layer, T* sheet, T* strip_type, T* strip,
                         uint32_t* out ) noexcept {
    *out = ( ( *strip << DIGI_CGEM_STRIP_OFFSET ) & DIGI_CGEM_STRIP_MASK ) |
           ( ( *strip_type << DIGI_CGEM_STRIPTYPE_OFFSET ) & DIGI_CGEM_STRIPTYPE_MASK ) |
           ( ( *sheet << DIGI_CGEM_SHEET_OFFSET ) & DIGI_CGEM_SHEET_MASK ) |
           ( ( *layer << DIGI_CGEM_LAYER_OFFSET ) & DIGI_CGEM_LAYER_MASK ) |
           ( DIGI_CGEM_FLAG << DIGI_FLAG_OFFSET );
}

// ===========================================================================
// declare_identifier – register all ufuncs into the module dict
// ===========================================================================
void declare_identifier( PyObject* d ) {
    if ( _import_array() < 0 ) return;
    if ( _import_umath() < 0 ) return;

    // ---- MDC ----
    decl_ufunc_11<              //
        check_mdc_id<uint32_t>, //
        check_mdc_id<uint64_t>, //
        check_mdc_id<int64_t>>  //
        ( d, "check_mdc_id" );

    decl_ufunc_11<                //
        mdc_id_to_wire<uint32_t>, //
        mdc_id_to_wire<uint64_t>, //
        mdc_id_to_wire<int64_t>>  //
        ( d, "mdc_id_to_wire" );

    decl_ufunc_11<                 //
        mdc_id_to_layer<uint32_t>, //
        mdc_id_to_layer<uint64_t>, //
        mdc_id_to_layer<int64_t>>  //
        ( d, "mdc_id_to_layer" );

    decl_ufunc_11<                     //
        mdc_id_to_is_stereo<uint32_t>, //
        mdc_id_to_is_stereo<uint64_t>, //
        mdc_id_to_is_stereo<int64_t>>  //
        ( d, "mdc_id_to_is_stereo" );

    decl_ufunc_31<            //
        get_mdc_id<uint32_t>, //
        get_mdc_id<uint64_t>, //
        get_mdc_id<int64_t>>  //
        ( d, "get_mdc_id" );

    // ---- TOF ----
    decl_ufunc_11<              //
        check_tof_id<uint32_t>, //
        check_tof_id<uint64_t>, //
        check_tof_id<int64_t>>  //
        ( d, "check_tof_id" );

    decl_ufunc_11<                //
        tof_id_to_part<uint32_t>, //
        tof_id_to_part<uint64_t>, //
        tof_id_to_part<int64_t>>  //
        ( d, "tof_id_to_part" );

    decl_ufunc_11<               //
        tof_id_to_end<uint32_t>, //
        tof_id_to_end<uint64_t>, //
        tof_id_to_end<int64_t>>  //
        ( d, "tof_id_to_end" );

    decl_ufunc_11<                              //
        _tof_id_to_layer_or_module_1<uint32_t>, //
        _tof_id_to_layer_or_module_1<uint64_t>, //
        _tof_id_to_layer_or_module_1<int64_t>>  //
        ( d, "_tof_id_to_layer_or_module_1" );

    decl_ufunc_21<                              //
        _tof_id_to_layer_or_module_2<uint32_t>, //
        _tof_id_to_layer_or_module_2<uint64_t>, //
        _tof_id_to_layer_or_module_2<int64_t>>  //
        ( d, "_tof_id_to_layer_or_module_2" );

    decl_ufunc_11<                           //
        _tof_id_to_phi_or_strip_1<uint32_t>, //
        _tof_id_to_phi_or_strip_1<uint64_t>, //
        _tof_id_to_phi_or_strip_1<int64_t>>  //
        ( d, "_tof_id_to_phi_or_strip_1" );

    decl_ufunc_21<                           //
        _tof_id_to_phi_or_strip_2<uint32_t>, //
        _tof_id_to_phi_or_strip_2<uint64_t>, //
        _tof_id_to_phi_or_strip_2<int64_t>>  //
        ( d, "_tof_id_to_phi_or_strip_2" );

    decl_ufunc_41<            //
        get_tof_id<uint32_t>, //
        get_tof_id<uint64_t>, //
        get_tof_id<int64_t>>  //
        ( d, "get_tof_id" );

    // ---- EMC ----
    decl_ufunc_11<              //
        check_emc_id<uint32_t>, //
        check_emc_id<uint64_t>, //
        check_emc_id<int64_t>>  //
        ( d, "check_emc_id" );

    decl_ufunc_11<                  //
        emc_id_to_module<uint32_t>, //
        emc_id_to_module<uint64_t>, //
        emc_id_to_module<int64_t>>  //
        ( d, "emc_id_to_module" );

    decl_ufunc_11<                 //
        emc_id_to_theta<uint32_t>, //
        emc_id_to_theta<uint64_t>, //
        emc_id_to_theta<int64_t>>  //
        ( d, "emc_id_to_theta" );

    decl_ufunc_11<               //
        emc_id_to_phi<uint32_t>, //
        emc_id_to_phi<uint64_t>, //
        emc_id_to_phi<int64_t>>  //
        ( d, "emc_id_to_phi" );

    decl_ufunc_31<            //
        get_emc_id<uint32_t>, //
        get_emc_id<uint64_t>, //
        get_emc_id<int64_t>>  //
        ( d, "get_emc_id" );

    // ---- MUC ----
    decl_ufunc_11<              //
        check_muc_id<uint32_t>, //
        check_muc_id<uint64_t>, //
        check_muc_id<int64_t>>  //
        ( d, "check_muc_id" );

    decl_ufunc_11<                //
        muc_id_to_part<uint32_t>, //
        muc_id_to_part<uint64_t>, //
        muc_id_to_part<int64_t>>  //
        ( d, "muc_id_to_part" );

    decl_ufunc_11<                   //
        muc_id_to_segment<uint32_t>, //
        muc_id_to_segment<uint64_t>, //
        muc_id_to_segment<int64_t>>  //
        ( d, "muc_id_to_segment" );

    decl_ufunc_11<                 //
        muc_id_to_layer<uint32_t>, //
        muc_id_to_layer<uint64_t>, //
        muc_id_to_layer<int64_t>>  //
        ( d, "muc_id_to_layer" );

    decl_ufunc_11<                   //
        muc_id_to_channel<uint32_t>, //
        muc_id_to_channel<uint64_t>, //
        muc_id_to_channel<int64_t>>  //
        ( d, "muc_id_to_channel" );

    decl_ufunc_41<            //
        get_muc_id<uint32_t>, //
        get_muc_id<uint64_t>, //
        get_muc_id<int64_t>>  //
        ( d, "get_muc_id" );

    // ---- CGEM ----
    decl_ufunc_11<               //
        check_cgem_id<uint32_t>, //
        check_cgem_id<uint64_t>, //
        check_cgem_id<int64_t>>  //
        ( d, "check_cgem_id" );

    decl_ufunc_11<                  //
        cgem_id_to_layer<uint32_t>, //
        cgem_id_to_layer<uint64_t>, //
        cgem_id_to_layer<int64_t>>  //
        ( d, "cgem_id_to_layer" );

    decl_ufunc_11<                  //
        cgem_id_to_sheet<uint32_t>, //
        cgem_id_to_sheet<uint64_t>, //
        cgem_id_to_sheet<int64_t>>  //
        ( d, "cgem_id_to_sheet" );

    decl_ufunc_11<                       //
        cgem_id_to_strip_type<uint32_t>, //
        cgem_id_to_strip_type<uint64_t>, //
        cgem_id_to_strip_type<int64_t>>  //
        ( d, "cgem_id_to_strip_type" );

    decl_ufunc_11<                  //
        cgem_id_to_strip<uint32_t>, //
        cgem_id_to_strip<uint64_t>, //
        cgem_id_to_strip<int64_t>>  //
        ( d, "cgem_id_to_strip" );

    decl_ufunc_41<             //
        get_cgem_id<uint32_t>, //
        get_cgem_id<uint64_t>, //
        get_cgem_id<int64_t>>  //
        ( d, "get_cgem_id" );
}
