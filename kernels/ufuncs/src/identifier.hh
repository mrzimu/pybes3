#pragma once

#include <cstdint>

namespace identifier {
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
            *out =
                ( ( *part << DIGI_TOF_PART_OFFSET ) & DIGI_TOF_PART_MASK ) |
                ( ( *layer_or_module << DIGI_TOF_SCINT_LAYER_OFFSET ) &
                  DIGI_TOF_SCINT_LAYER_MASK ) |
                ( ( *phi_or_strip << DIGI_TOF_SCINT_PHI_OFFSET ) & DIGI_TOF_SCINT_PHI_MASK ) |
                ( ( *end << DIGI_TOF_END_OFFSET ) & DIGI_TOF_END_MASK ) |
                ( DIGI_TOF_FLAG << DIGI_FLAG_OFFSET );
        }
        else
        {
            *out = ( ( 3 << DIGI_TOF_PART_OFFSET ) & DIGI_TOF_PART_MASK ) |
                   ( ( ( *part - 3 ) << DIGI_TOF_MRPC_ENDCAP_OFFSET ) &
                     DIGI_TOF_MRPC_ENDCAP_MASK ) |
                   ( ( *layer_or_module << DIGI_TOF_MRPC_MODULE_OFFSET ) &
                     DIGI_TOF_MRPC_MODULE_MASK ) |
                   ( ( *phi_or_strip << DIGI_TOF_MRPC_STRIP_OFFSET ) &
                     DIGI_TOF_MRPC_STRIP_MASK ) |
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
    inline void get_muc_id( T* part, T* segment, T* layer, T* channel,
                            uint32_t* out ) noexcept {
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
        *out = static_cast<uint16_t>( ( *cgem_id & DIGI_CGEM_STRIP_MASK ) >>
                                      DIGI_CGEM_STRIP_OFFSET );
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
} // namespace identifier
