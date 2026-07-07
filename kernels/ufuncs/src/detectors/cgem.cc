#include <tuple>

#include "mod.hh"
#include "ufunc.hh"

constexpr size_t N_LAYER       = 3;
constexpr size_t N_STRIPS      = 9897;
constexpr uint8_t X_STRIP_TYPE = 0;
constexpr uint8_t V_STRIP_TYPE = 1;

constexpr std::array<size_t, 3> N_SHEETS  = { 1, 2, 2 };
constexpr std::array<size_t, 3> N_XSTRIPS = { 856, 630, 832 };
constexpr std::array<size_t, 3> N_VSTRIPS = { 1173, 1077, 1395 };

consteval auto _init() {
    std::array<uint8_t, N_STRIPS> _layer{};
    std::array<uint8_t, N_STRIPS> _sheet{};
    std::array<uint8_t, N_STRIPS> _strip_type{};
    std::array<uint16_t, N_STRIPS> _strip{};
    std::array<uint16_t, N_LAYER> _layer_offset{};

    size_t idx = 0;
    for ( size_t layer = 0; layer < N_LAYER; ++layer )
    {
        auto n_sheets  = N_SHEETS[layer];
        auto n_xstrips = N_XSTRIPS[layer];
        auto n_vstrips = N_VSTRIPS[layer];

        _layer_offset[layer] = idx;
        for ( size_t sheet = 0; sheet < n_sheets; ++sheet )
        {
            for ( size_t strip = 0; strip < n_xstrips; ++strip )
            {
                _layer[idx]      = layer;
                _sheet[idx]      = sheet;
                _strip_type[idx] = X_STRIP_TYPE;
                _strip[idx]      = strip;
                idx++;
            }
            for ( size_t strip = 0; strip < n_vstrips; ++strip )
            {
                _layer[idx]      = layer;
                _sheet[idx]      = sheet;
                _strip_type[idx] = V_STRIP_TYPE;
                _strip[idx]      = strip;
                idx++;
            }
        }
    }
    return std::make_tuple( _layer, _sheet, _strip_type, _strip, _layer_offset );
}

constexpr auto _init_tuple   = _init();
constexpr auto _layer        = std::get<0>( _init_tuple );
constexpr auto _sheet        = std::get<1>( _init_tuple );
constexpr auto _strip_type   = std::get<2>( _init_tuple );
constexpr auto _strip        = std::get<3>( _init_tuple );
constexpr auto _layer_offset = std::get<4>( _init_tuple );

template <typename T>
inline void get_cgem_idx( T* layer, T* sheet, T* strip_type, T* strip, T* idx ) noexcept {
    *idx = _layer_offset[*layer];
    *idx += *sheet * ( N_XSTRIPS[*layer] + N_VSTRIPS[*layer] );
    *idx += ( *strip_type ) * N_XSTRIPS[*layer];
    *idx += *strip;
}

template <typename T>
inline void cgem_idx_to_layer( T* idx, T* layer ) noexcept {
    *layer = _layer[*idx];
}

template <typename T>
inline void cgem_idx_to_sheet( T* idx, T* sheet ) noexcept {
    *sheet = _sheet[*idx];
}

template <typename T>
inline void cgem_idx_to_strip_type( T* idx, T* strip_type ) noexcept {
    *strip_type = _strip_type[*idx];
}

template <typename T>
inline void cgem_idx_to_strip( T* idx, T* strip ) noexcept {
    *strip = _strip[*idx];
}

template <typename T>
inline void cgem_idx_to_is_xstrip( T* idx, bool* is_xstrip ) noexcept {
    *is_xstrip = _strip_type[*idx] == X_STRIP_TYPE;
}

template <typename T>
inline void cgem_idx_to_is_vstrip( T* idx, bool* is_vstrip ) noexcept {
    *is_vstrip = _strip_type[*idx] == V_STRIP_TYPE;
}

void declare_cgem( PyObject* d ) {
    if ( _import_array() < 0 ) return;
    if ( _import_umath() < 0 ) return;

    decl_ufunc_41<              //
        get_cgem_idx<uint16_t>, //
        get_cgem_idx<int16_t>,  //
        get_cgem_idx<uint32_t>, //
        get_cgem_idx<int32_t>,  //
        get_cgem_idx<uint64_t>, //
        get_cgem_idx<int64_t>>  //
        ( d, "get_cgem_idx" );

    decl_ufunc_11<                   //
        cgem_idx_to_layer<uint16_t>, //
        cgem_idx_to_layer<int16_t>,  //
        cgem_idx_to_layer<uint32_t>, //
        cgem_idx_to_layer<int32_t>,  //
        cgem_idx_to_layer<uint64_t>, //
        cgem_idx_to_layer<int64_t>>  //
        ( d, "cgem_idx_to_layer" );

    decl_ufunc_11<                   //
        cgem_idx_to_sheet<uint16_t>, //
        cgem_idx_to_sheet<int16_t>,  //
        cgem_idx_to_sheet<uint32_t>, //
        cgem_idx_to_sheet<int32_t>,  //
        cgem_idx_to_sheet<uint64_t>, //
        cgem_idx_to_sheet<int64_t>>  //
        ( d, "cgem_idx_to_sheet" );

    decl_ufunc_11<                        //
        cgem_idx_to_strip_type<uint16_t>, //
        cgem_idx_to_strip_type<int16_t>,  //
        cgem_idx_to_strip_type<uint32_t>, //
        cgem_idx_to_strip_type<int32_t>,  //
        cgem_idx_to_strip_type<uint64_t>, //
        cgem_idx_to_strip_type<int64_t>>  //
        ( d, "cgem_idx_to_strip_type" );

    decl_ufunc_11<                   //
        cgem_idx_to_strip<uint16_t>, //
        cgem_idx_to_strip<int16_t>,  //
        cgem_idx_to_strip<uint32_t>, //
        cgem_idx_to_strip<int32_t>,  //
        cgem_idx_to_strip<uint64_t>, //
        cgem_idx_to_strip<int64_t>>  //
        ( d, "cgem_idx_to_strip" );

    decl_ufunc_11<                        //
        cgem_idx_to_is_xstrip<uint16_t>, //
        cgem_idx_to_is_xstrip<int16_t>,  //
        cgem_idx_to_is_xstrip<uint32_t>, //
        cgem_idx_to_is_xstrip<int32_t>,  //
        cgem_idx_to_is_xstrip<uint64_t>, //
        cgem_idx_to_is_xstrip<int64_t>>  //
        ( d, "cgem_idx_to_is_xstrip" );

    decl_ufunc_11<                        //
        cgem_idx_to_is_vstrip<uint16_t>, //
        cgem_idx_to_is_vstrip<int16_t>,  //
        cgem_idx_to_is_vstrip<uint32_t>, //
        cgem_idx_to_is_vstrip<int32_t>,  //
        cgem_idx_to_is_vstrip<uint64_t>, //
        cgem_idx_to_is_vstrip<int64_t>>  //
        ( d, "cgem_idx_to_is_vstrip" );
}
