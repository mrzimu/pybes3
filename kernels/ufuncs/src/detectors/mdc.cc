#include "mod.hh"
#include "ufunc.hh"

constexpr size_t N_WIRES  = 6796;
constexpr size_t N_LAYERS = 43;

constexpr std::array<uint16_t, N_LAYERS> _layer_nwires = {
    40,  44,  48,  56,  64,  72,  80,  80,  76,  76,  88,  88,  100, 100, 112,
    112, 128, 128, 140, 140, 160, 160, 160, 160, 176, 176, 176, 176, 208, 208,
    208, 208, 240, 240, 240, 240, 256, 256, 256, 256, 288, 288, 288 };

constexpr std::array<int8_t, N_LAYERS> _layer_stereo = {
    -1, -1, -1, -1, 1, 1, 1,  1,  0,  0,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1,
    -1, -1, 1,  1,  1, 1, -1, -1, -1, -1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0 };

constexpr std::array<uint8_t, 12> _superlayer_splits = { 0,  4,  8,  12, 16, 20,
                                                         24, 28, 32, 36, 40, 43 };

consteval auto _init_index() {
    std::array<uint8_t, N_WIRES> _layer{};
    std::array<uint16_t, N_WIRES> _wire{};
    std::array<int8_t, N_WIRES> _stereo{};
    std::array<bool, N_WIRES> _is_stereo{};
    std::array<uint8_t, N_WIRES> _superlayer{};

    std::array<uint16_t, N_LAYERS> _layer_start_idx{};
    std::array<bool, N_LAYERS> _is_layer_stereo{};

    size_t idx         = 0;
    uint8_t superlayer = 0;
    for ( uint16_t layer = 0; layer < N_LAYERS; ++layer )
    {
        _layer_start_idx[layer] = idx;
        _is_layer_stereo[layer] = _layer_stereo[layer] != 0;

        if ( superlayer < _superlayer_splits.size() - 1 &&
             layer >= _superlayer_splits[superlayer + 1] )
        { superlayer++; }

        auto n_wires = _layer_nwires[layer];
        for ( uint16_t wire = 0; wire < n_wires; ++wire )
        {
            _superlayer[idx] = superlayer;
            _layer[idx]      = layer;
            _wire[idx]       = wire;
            _stereo[idx]     = _layer_stereo[layer];
            _is_stereo[idx]  = _stereo[idx] != 0;
            idx++;
        }
    }
    return std::make_tuple( _layer, _wire, _stereo, _is_stereo, _superlayer, _layer_start_idx,
                            _is_layer_stereo );
}

constexpr auto _init_index_tuple = _init_index();
constexpr auto _layer            = std::get<0>( _init_index_tuple );
constexpr auto _wire             = std::get<1>( _init_index_tuple );
constexpr auto _stereo           = std::get<2>( _init_index_tuple );
constexpr auto _is_stereo        = std::get<3>( _init_index_tuple );
constexpr auto _superlayer       = std::get<4>( _init_index_tuple );

constexpr auto _layer_start_idx = std::get<5>( _init_index_tuple );
constexpr auto _is_layer_stereo = std::get<6>( _init_index_tuple );

/* Geometry arrays */
std::array<double, N_WIRES> _east_x{};
std::array<double, N_WIRES> _east_y{};
std::array<double, N_WIRES> _east_z{};
std::array<double, N_WIRES> _west_x{};
std::array<double, N_WIRES> _west_y{};
std::array<double, N_WIRES> _west_z{};
std::array<double, N_WIRES> _dx_dz{};
std::array<double, N_WIRES> _dy_dz{};

PyObject* _init_mdc_geom( PyObject* self, PyObject* args ) {
    PyArrayObject *east_x = nullptr, *east_y = nullptr, *east_z = nullptr;
    PyArrayObject *west_x = nullptr, *west_y = nullptr, *west_z = nullptr;

    if ( !PyArg_ParseTuple( args, "O!O!O!O!O!O!",   //
                            &PyArray_Type, &east_x, //
                            &PyArray_Type, &east_y, //
                            &PyArray_Type, &east_z, //
                            &PyArray_Type, &west_x, //
                            &PyArray_Type, &west_y, //
                            &PyArray_Type, &west_z  //
                            ) )
        return nullptr;

    memcpy( _east_x.data(), PyArray_DATA( east_x ), _east_x.size() * sizeof( double ) );
    memcpy( _east_y.data(), PyArray_DATA( east_y ), _east_y.size() * sizeof( double ) );
    memcpy( _east_z.data(), PyArray_DATA( east_z ), _east_z.size() * sizeof( double ) );
    memcpy( _west_x.data(), PyArray_DATA( west_x ), _west_x.size() * sizeof( double ) );
    memcpy( _west_y.data(), PyArray_DATA( west_y ), _west_y.size() * sizeof( double ) );
    memcpy( _west_z.data(), PyArray_DATA( west_z ), _west_z.size() * sizeof( double ) );

    for ( size_t i = 0; i < N_WIRES; i++ )
    {
        _dx_dz[i] = ( _east_x[i] - _west_x[i] ) / ( _east_z[i] - _west_z[i] );
        _dy_dz[i] = ( _east_y[i] - _west_y[i] ) / ( _east_z[i] - _west_z[i] );
    }

    Py_RETURN_NONE;
}

template <typename T>
inline void get_mdc_idx( T* layer, T* wire, T* out ) noexcept {
    *out = _layer_start_idx[*layer] + *wire;
}

template <typename T>
inline void mdc_idx_to_superlayer( T* idx, T* out ) noexcept {
    *out = _superlayer[*idx];
}

template <typename T>
inline void mdc_layer_to_superlayer( T* layer, T* out ) noexcept {
    int32_t result = 0;
    for ( size_t i = 1; i < _superlayer_splits.size(); ++i )
    {
        if ( *layer >= _superlayer_splits[i] ) result = static_cast<int32_t>( i );
        else break;
    }
    *out = result;
}

template <typename T>
inline void mdc_idx_to_layer( T* idx, T* out ) noexcept {
    *out = _layer[*idx];
}

template <typename T>
inline void mdc_idx_to_wire( T* idx, T* out ) noexcept {
    *out = _wire[*idx];
}

template <typename TIN, typename TOUT>
inline void mdc_idx_to_stereo( TIN* idx, TOUT* out ) noexcept {
    *out = _stereo[*idx];
}

template <typename TIN>
inline void mdc_layer_to_is_stereo( TIN* layer, bool* out ) noexcept {
    *out = _is_layer_stereo[*layer] != 0;
}

template <typename TIN>
inline void mdc_idx_to_is_stereo( TIN* idx, bool* out ) noexcept {
    *out = _is_stereo[*idx];
}

template <typename T>
inline void mdc_idx_to_west_x( T* idx, double* out ) noexcept {
    *out = _west_x[*idx];
}

template <typename T>
inline void mdc_idx_to_west_y( T* idx, double* out ) noexcept {
    *out = _west_y[*idx];
}

template <typename T>
inline void mdc_idx_to_west_z( T* idx, double* out ) noexcept {
    *out = _west_z[*idx];
}

template <typename T>
inline void mdc_idx_to_east_x( T* idx, double* out ) noexcept {
    *out = _east_x[*idx];
}

template <typename T>
inline void mdc_idx_to_east_y( T* idx, double* out ) noexcept {
    *out = _east_y[*idx];
}

template <typename T>
inline void mdc_idx_to_east_z( T* idx, double* out ) noexcept {
    *out = _east_z[*idx];
}

template <typename T>
inline void mdc_idx_z_to_x( T* idx, double* z, double* out ) noexcept {
    *out = _west_x[*idx] + _dx_dz[*idx] * ( *z - _west_z[*idx] );
}

template <typename T>
inline void mdc_idx_z_to_y( T* idx, double* z, double* out ) noexcept {
    *out = _west_y[*idx] + _dy_dz[*idx] * ( *z - _west_z[*idx] );
}

void declare_mdc( PyObject* d ) {
    if ( _import_array() < 0 ) return;
    if ( _import_umath() < 0 ) return;

    decl_ufunc_21<             //
        get_mdc_idx<uint16_t>, //
        get_mdc_idx<int16_t>,  //
        get_mdc_idx<uint32_t>, //
        get_mdc_idx<int32_t>,  //
        get_mdc_idx<uint64_t>, //
        get_mdc_idx<int64_t>>( d, "get_mdc_idx" );

    decl_ufunc_11<                       //
        mdc_idx_to_superlayer<uint16_t>, //
        mdc_idx_to_superlayer<int16_t>,  //
        mdc_idx_to_superlayer<uint32_t>, //
        mdc_idx_to_superlayer<int32_t>,  //
        mdc_idx_to_superlayer<uint64_t>, //
        mdc_idx_to_superlayer<int64_t>>( d, "mdc_idx_to_superlayer" );

    decl_ufunc_11<                         //
        mdc_layer_to_superlayer<uint16_t>, //
        mdc_layer_to_superlayer<int16_t>,  //
        mdc_layer_to_superlayer<uint32_t>, //
        mdc_layer_to_superlayer<int32_t>,  //
        mdc_layer_to_superlayer<uint64_t>, //
        mdc_layer_to_superlayer<int64_t>>( d, "mdc_layer_to_superlayer" );

    decl_ufunc_11<                  //
        mdc_idx_to_layer<uint16_t>, //
        mdc_idx_to_layer<int16_t>,  //
        mdc_idx_to_layer<uint32_t>, //
        mdc_idx_to_layer<int32_t>,  //
        mdc_idx_to_layer<uint64_t>, //
        mdc_idx_to_layer<int64_t>>( d, "mdc_idx_to_layer" );

    decl_ufunc_11<                 //
        mdc_idx_to_wire<uint16_t>, //
        mdc_idx_to_wire<int16_t>,  //
        mdc_idx_to_wire<uint32_t>, //
        mdc_idx_to_wire<int32_t>,  //
        mdc_idx_to_wire<uint64_t>, //
        mdc_idx_to_wire<int64_t>>( d, "mdc_idx_to_wire" );

    decl_ufunc_11<                            //
        mdc_idx_to_stereo<uint16_t, int16_t>, //
        mdc_idx_to_stereo<int16_t, int16_t>,  //
        mdc_idx_to_stereo<uint32_t, int32_t>, //
        mdc_idx_to_stereo<int32_t, int32_t>,  //
        mdc_idx_to_stereo<uint64_t, int64_t>, //
        mdc_idx_to_stereo<int64_t, int64_t>>( d, "mdc_idx_to_stereo" );

    decl_ufunc_11<                        //
        mdc_layer_to_is_stereo<uint16_t>, //
        mdc_layer_to_is_stereo<int16_t>,  //
        mdc_layer_to_is_stereo<uint32_t>, //
        mdc_layer_to_is_stereo<int32_t>,  //
        mdc_layer_to_is_stereo<uint64_t>, //
        mdc_layer_to_is_stereo<int64_t>>( d, "mdc_layer_to_is_stereo" );

    decl_ufunc_11<                      //
        mdc_idx_to_is_stereo<uint16_t>, //
        mdc_idx_to_is_stereo<int16_t>,  //
        mdc_idx_to_is_stereo<uint32_t>, //
        mdc_idx_to_is_stereo<int32_t>,  //
        mdc_idx_to_is_stereo<uint64_t>, //
        mdc_idx_to_is_stereo<int64_t>>( d, "mdc_idx_to_is_stereo" );

    decl_ufunc_11<                   //
        mdc_idx_to_west_x<uint16_t>, //
        mdc_idx_to_west_x<int16_t>,  //
        mdc_idx_to_west_x<uint32_t>, //
        mdc_idx_to_west_x<int32_t>,  //
        mdc_idx_to_west_x<uint64_t>, //
        mdc_idx_to_west_x<int64_t>>( d, "mdc_idx_to_west_x" );

    decl_ufunc_11<                   //
        mdc_idx_to_west_y<uint16_t>, //
        mdc_idx_to_west_y<int16_t>,  //
        mdc_idx_to_west_y<uint32_t>, //
        mdc_idx_to_west_y<int32_t>,  //
        mdc_idx_to_west_y<uint64_t>, //
        mdc_idx_to_west_y<int64_t>>( d, "mdc_idx_to_west_y" );

    decl_ufunc_11<                   //
        mdc_idx_to_west_z<uint16_t>, //
        mdc_idx_to_west_z<int16_t>,  //
        mdc_idx_to_west_z<uint32_t>, //
        mdc_idx_to_west_z<int32_t>,  //
        mdc_idx_to_west_z<uint64_t>, //
        mdc_idx_to_west_z<int64_t>>( d, "mdc_idx_to_west_z" );

    decl_ufunc_11<                   //
        mdc_idx_to_east_x<uint16_t>, //
        mdc_idx_to_east_x<int16_t>,  //
        mdc_idx_to_east_x<uint32_t>, //
        mdc_idx_to_east_x<int32_t>,  //
        mdc_idx_to_east_x<uint64_t>, //
        mdc_idx_to_east_x<int64_t>>( d, "mdc_idx_to_east_x" );

    decl_ufunc_11<                   //
        mdc_idx_to_east_y<uint16_t>, //
        mdc_idx_to_east_y<int16_t>,  //
        mdc_idx_to_east_y<uint32_t>, //
        mdc_idx_to_east_y<int32_t>,  //
        mdc_idx_to_east_y<uint64_t>, //
        mdc_idx_to_east_y<int64_t>>( d, "mdc_idx_to_east_y" );

    decl_ufunc_11<                   //
        mdc_idx_to_east_z<uint16_t>, //
        mdc_idx_to_east_z<int16_t>,  //
        mdc_idx_to_east_z<uint32_t>, //
        mdc_idx_to_east_z<int32_t>,  //
        mdc_idx_to_east_z<uint64_t>, //
        mdc_idx_to_east_z<int64_t>>( d, "mdc_idx_to_east_z" );

    decl_ufunc_21<                //
        mdc_idx_z_to_x<uint16_t>, //
        mdc_idx_z_to_x<int16_t>,  //
        mdc_idx_z_to_x<uint32_t>, //
        mdc_idx_z_to_x<int32_t>,  //
        mdc_idx_z_to_x<uint64_t>, //
        mdc_idx_z_to_x<int64_t>>( d, "mdc_idx_z_to_x" );

    decl_ufunc_21<                //
        mdc_idx_z_to_y<uint16_t>, //
        mdc_idx_z_to_y<int16_t>,  //
        mdc_idx_z_to_y<uint32_t>, //
        mdc_idx_z_to_y<int32_t>,  //
        mdc_idx_z_to_y<uint64_t>, //
        mdc_idx_z_to_y<int64_t>>( d, "mdc_idx_z_to_y" );
}
