#include <numeric>
#include <tuple>

#include "mod.hh"
#include "ufunc.hh"

constexpr size_t N_PARTS = 5;

constexpr std::array<size_t, N_PARTS> N_LAYER_OR_MODULE = { 1, 2, 1, 36, 36 };
constexpr std::array<size_t, N_PARTS> N_PHI_OR_STRIP    = { 48, 88, 48, 12, 12 };

constexpr size_t N_STRIPS = std::inner_product(
    N_LAYER_OR_MODULE.begin(), N_LAYER_OR_MODULE.end(), N_PHI_OR_STRIP.begin(), 0 );

consteval auto _init() {
    std::array<uint8_t, N_STRIPS> _part{};
    std::array<uint8_t, N_STRIPS> _layer_or_module{};
    std::array<uint8_t, N_STRIPS> _phi_or_strip{};
    std::array<uint16_t, N_PARTS> _part_offset{};

    size_t idx = 0;
    for ( size_t part = 0; part < N_PARTS; ++part )
    {
        auto n_layer_or_module = N_LAYER_OR_MODULE[part];
        auto n_phi_or_strip    = N_PHI_OR_STRIP[part];

        _part_offset[part] = idx;
        for ( size_t i = 0; i < n_layer_or_module; ++i )
        {
            for ( size_t j = 0; j < n_phi_or_strip; ++j )
            {
                _part[idx]            = part;
                _layer_or_module[idx] = i;
                _phi_or_strip[idx]    = j;
                idx++;
            }
        }
    }
    return std::make_tuple( _part, _layer_or_module, _phi_or_strip, _part_offset );
}

constexpr auto _init_tuple      = _init();
constexpr auto _part            = std::get<0>( _init_tuple );
constexpr auto _layer_or_module = std::get<1>( _init_tuple );
constexpr auto _phi_or_strip    = std::get<2>( _init_tuple );
constexpr auto _part_offset     = std::get<3>( _init_tuple );

template <typename T>
inline void get_tof_idx( T* part, T* layer_or_module, T* phi_or_strip, T* out ) noexcept {
    *out = _part_offset[*part];
    *out += *layer_or_module * N_PHI_OR_STRIP[*part];
    *out += *phi_or_strip;
}

template <typename T>
inline void tof_idx_to_part( T* idx, T* part ) noexcept {
    *part = _part[*idx];
}

template <typename T>
inline void tof_idx_to_layer_or_module( T* idx, T* layer_or_module ) noexcept {
    *layer_or_module = _layer_or_module[*idx];
}

template <typename T>
inline void tof_idx_to_phi_or_strip( T* idx, T* phi_or_strip ) noexcept {
    *phi_or_strip = _phi_or_strip[*idx];
}

/* ------ Hit Status ------*/

template <typename T>
inline void tof_hit_status_to_is_raw( T* status, bool* out ) noexcept {
    *out = ( ( *status & 0x00000001 ) >> 0 ) > 0;
}

template <typename T>
inline void tof_hit_status_to_is_readout( T* status, bool* out ) noexcept {
    *out = ( ( *status & 0x00000002 ) >> 1 ) > 0;
}

template <typename T>
inline void tof_hit_status_to_is_counter( T* status, bool* out ) noexcept {
    *out = ( ( *status & 0x00000004 ) >> 2 ) > 0;
}

template <typename T>
inline void tof_hit_status_to_is_cluster( T* status, bool* out ) noexcept {
    *out = ( ( *status & 0x00000008 ) >> 3 ) > 0;
}

template <typename T>
inline void tof_hit_status_to_is_barrel( T* status, bool* out ) noexcept {
    *out = ( ( *status & 0x00000010 ) >> 4 ) > 0;
}

template <typename T>
inline void tof_hit_status_to_is_east( T* status, bool* out ) noexcept {
    *out = ( ( *status & 0x00000020 ) >> 5 ) > 0;
}

template <typename T>
inline void tof_hit_status_to_layer( T* status, T* out ) noexcept {
    *out = ( *status & 0x000000C0 ) >> 6;
}

template <typename T>
inline void tof_hit_status_to_is_overflow( T* status, bool* out ) noexcept {
    *out = ( ( *status & 0x00000100 ) >> 8 ) > 0;
}

template <typename T>
inline void tof_hit_status_to_is_multihit( T* status, bool* out ) noexcept {
    *out = ( ( *status & 0x00000200 ) >> 9 ) > 0;
}

template <typename T>
inline void tof_hit_status_to_n_counter( T* status, T* out ) noexcept {
    *out = ( *status >> 12 ) & 0x0000000F;
}

template <typename T>
inline void tof_hit_status_to_n_east( T* status, T* out ) noexcept {
    *out = ( *status >> 16 ) & 0x0000000F;
}

template <typename T>
inline void tof_hit_status_to_n_west( T* status, T* out ) noexcept {
    *out = ( *status >> 20 ) & 0x0000000F;
}

template <typename T>
inline void tof_hit_status_to_is_mrpc( T* status, bool* out ) noexcept {
    *out = ( ( *status & 0x01000000 ) >> 24 ) > 0;
}

void declare_tof( PyObject* d ) {
    if ( _import_array() < 0 ) return;
    if ( _import_umath() < 0 ) return;

    decl_ufunc_31<             //
        get_tof_idx<uint16_t>, //
        get_tof_idx<int16_t>,  //
        get_tof_idx<uint32_t>, //
        get_tof_idx<int32_t>,  //
        get_tof_idx<uint64_t>, //
        get_tof_idx<int64_t>>( d, "get_tof_idx" );

    decl_ufunc_11<                 //
        tof_idx_to_part<uint16_t>, //
        tof_idx_to_part<int16_t>,  //
        tof_idx_to_part<uint32_t>, //
        tof_idx_to_part<int32_t>,  //
        tof_idx_to_part<uint64_t>, //
        tof_idx_to_part<int64_t>>( d, "tof_idx_to_part" );

    decl_ufunc_11<                            //
        tof_idx_to_layer_or_module<uint16_t>, //
        tof_idx_to_layer_or_module<int16_t>,  //
        tof_idx_to_layer_or_module<uint32_t>, //
        tof_idx_to_layer_or_module<int32_t>,  //
        tof_idx_to_layer_or_module<uint64_t>, //
        tof_idx_to_layer_or_module<int64_t>>( d, "tof_idx_to_layer_or_module" );

    decl_ufunc_11<                         //
        tof_idx_to_phi_or_strip<uint16_t>, //
        tof_idx_to_phi_or_strip<int16_t>,  //
        tof_idx_to_phi_or_strip<uint32_t>, //
        tof_idx_to_phi_or_strip<int32_t>,  //
        tof_idx_to_phi_or_strip<uint64_t>, //
        tof_idx_to_phi_or_strip<int64_t>>( d, "tof_idx_to_phi_or_strip" );

    /* ------ Hit Status ------ */

    decl_ufunc_11<                          //
        tof_hit_status_to_is_raw<uint16_t>, //
        tof_hit_status_to_is_raw<int16_t>,  //
        tof_hit_status_to_is_raw<uint32_t>, //
        tof_hit_status_to_is_raw<int32_t>,  //
        tof_hit_status_to_is_raw<uint64_t>, //
        tof_hit_status_to_is_raw<int64_t>>( d, "tof_hit_status_to_is_raw" );

    decl_ufunc_11<                              //
        tof_hit_status_to_is_readout<uint16_t>, //
        tof_hit_status_to_is_readout<int16_t>,  //
        tof_hit_status_to_is_readout<uint32_t>, //
        tof_hit_status_to_is_readout<int32_t>,  //
        tof_hit_status_to_is_readout<uint64_t>, //
        tof_hit_status_to_is_readout<int64_t>>( d, "tof_hit_status_to_is_readout" );

    decl_ufunc_11<                              //
        tof_hit_status_to_is_counter<uint16_t>, //
        tof_hit_status_to_is_counter<int16_t>,  //
        tof_hit_status_to_is_counter<uint32_t>, //
        tof_hit_status_to_is_counter<int32_t>,  //
        tof_hit_status_to_is_counter<uint64_t>, //
        tof_hit_status_to_is_counter<int64_t>>( d, "tof_hit_status_to_is_counter" );

    decl_ufunc_11<                              //
        tof_hit_status_to_is_cluster<uint16_t>, //
        tof_hit_status_to_is_cluster<int16_t>,  //
        tof_hit_status_to_is_cluster<uint32_t>, //
        tof_hit_status_to_is_cluster<int32_t>,  //
        tof_hit_status_to_is_cluster<uint64_t>, //
        tof_hit_status_to_is_cluster<int64_t>>( d, "tof_hit_status_to_is_cluster" );

    decl_ufunc_11<                             //
        tof_hit_status_to_is_barrel<uint16_t>, //
        tof_hit_status_to_is_barrel<int16_t>,  //
        tof_hit_status_to_is_barrel<uint32_t>, //
        tof_hit_status_to_is_barrel<int32_t>,  //
        tof_hit_status_to_is_barrel<uint64_t>, //
        tof_hit_status_to_is_barrel<int64_t>>( d, "tof_hit_status_to_is_barrel" );

    decl_ufunc_11<                           //
        tof_hit_status_to_is_east<uint16_t>, //
        tof_hit_status_to_is_east<int16_t>,  //
        tof_hit_status_to_is_east<uint32_t>, //
        tof_hit_status_to_is_east<int32_t>,  //
        tof_hit_status_to_is_east<uint64_t>, //
        tof_hit_status_to_is_east<int64_t>>( d, "tof_hit_status_to_is_east" );

    decl_ufunc_11<                         //
        tof_hit_status_to_layer<uint16_t>, //
        tof_hit_status_to_layer<int16_t>,  //
        tof_hit_status_to_layer<uint32_t>, //
        tof_hit_status_to_layer<int32_t>,  //
        tof_hit_status_to_layer<uint64_t>, //
        tof_hit_status_to_layer<int64_t>>( d, "tof_hit_status_to_layer" );

    decl_ufunc_11<                               //
        tof_hit_status_to_is_overflow<uint16_t>, //
        tof_hit_status_to_is_overflow<int16_t>,  //
        tof_hit_status_to_is_overflow<uint32_t>, //
        tof_hit_status_to_is_overflow<int32_t>,  //
        tof_hit_status_to_is_overflow<uint64_t>, //
        tof_hit_status_to_is_overflow<int64_t>>( d, "tof_hit_status_to_is_overflow" );

    decl_ufunc_11<                               //
        tof_hit_status_to_is_multihit<uint16_t>, //
        tof_hit_status_to_is_multihit<int16_t>,  //
        tof_hit_status_to_is_multihit<uint32_t>, //
        tof_hit_status_to_is_multihit<int32_t>,  //
        tof_hit_status_to_is_multihit<uint64_t>, //
        tof_hit_status_to_is_multihit<int64_t>>( d, "tof_hit_status_to_is_multihit" );

    decl_ufunc_11<                             //
        tof_hit_status_to_n_counter<uint16_t>, //
        tof_hit_status_to_n_counter<int16_t>,  //
        tof_hit_status_to_n_counter<uint32_t>, //
        tof_hit_status_to_n_counter<int32_t>,  //
        tof_hit_status_to_n_counter<uint64_t>, //
        tof_hit_status_to_n_counter<int64_t>>( d, "tof_hit_status_to_n_counter" );

    decl_ufunc_11<                          //
        tof_hit_status_to_n_east<uint16_t>, //
        tof_hit_status_to_n_east<int16_t>,  //
        tof_hit_status_to_n_east<uint32_t>, //
        tof_hit_status_to_n_east<int32_t>,  //
        tof_hit_status_to_n_east<uint64_t>, //
        tof_hit_status_to_n_east<int64_t>>( d, "tof_hit_status_to_n_east" );

    decl_ufunc_11<                          //
        tof_hit_status_to_n_west<uint16_t>, //
        tof_hit_status_to_n_west<int16_t>,  //
        tof_hit_status_to_n_west<uint32_t>, //
        tof_hit_status_to_n_west<int32_t>,  //
        tof_hit_status_to_n_west<uint64_t>, //
        tof_hit_status_to_n_west<int64_t>>( d, "tof_hit_status_to_n_west" );

    decl_ufunc_11<                           //
        tof_hit_status_to_is_mrpc<uint16_t>, //
        tof_hit_status_to_is_mrpc<int16_t>,  //
        tof_hit_status_to_is_mrpc<uint32_t>, //
        tof_hit_status_to_is_mrpc<int32_t>,  //
        tof_hit_status_to_is_mrpc<uint64_t>, //
        tof_hit_status_to_is_mrpc<int64_t>>( d, "tof_hit_status_to_is_mrpc" );
}
