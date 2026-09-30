#include <cmath>
#include <limits>
#include <numbers>
#include <tuple>

#include "mod.hh"
#include "ufunc.hh"

namespace cgem {
    constexpr double TWO_PI = 2.0 * std::numbers::pi_v<double>;

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

        size_t gid = 0;
        for ( size_t layer = 0; layer < N_LAYER; ++layer )
        {
            auto n_sheets  = N_SHEETS[layer];
            auto n_xstrips = N_XSTRIPS[layer];
            auto n_vstrips = N_VSTRIPS[layer];

            _layer_offset[layer] = gid;
            for ( size_t sheet = 0; sheet < n_sheets; ++sheet )
            {
                for ( size_t strip = 0; strip < n_xstrips; ++strip )
                {
                    _layer[gid]      = layer;
                    _sheet[gid]      = sheet;
                    _strip_type[gid] = X_STRIP_TYPE;
                    _strip[gid]      = strip;
                    gid++;
                }
                for ( size_t strip = 0; strip < n_vstrips; ++strip )
                {
                    _layer[gid]      = layer;
                    _sheet[gid]      = sheet;
                    _strip_type[gid] = V_STRIP_TYPE;
                    _strip[gid]      = strip;
                    gid++;
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

    /* Geometry */
    constexpr std::array<double, 2> STRIP_WIDTH                 = { 0.058, 0.013 }; // X, V
    constexpr std::array<std::array<double, 2>, 3> STRIP_RADIUS = {
        std::array<double, 2>{ 9.0195, 9.0140 },   // layer 0 -> X, V
        std::array<double, 2>{ 13.2555, 13.2500 }, // layer 1 -> X, V
        std::array<double, 2>{ 17.5250, 17.5195 }  // layer 2 -> X, V
    };

    std::array<double, N_STRIPS> _phi0{};
    std::array<double, N_STRIPS> _dphi{};
    std::array<double, N_STRIPS> _z0{};
    std::array<double, N_STRIPS> _dz{};

    PyObject* _init_cgem_geom( PyObject* self, PyObject* args ) {
        PyArrayObject *phi0 = nullptr, *dphi = nullptr, *z0 = nullptr, *dz = nullptr;

        if ( !PyArg_ParseTuple( args, "O!O!O!O!",     //
                                &PyArray_Type, &phi0, //
                                &PyArray_Type, &dphi, //
                                &PyArray_Type, &z0,   //
                                &PyArray_Type, &dz    //
                                ) )                   //
            return nullptr;

        memcpy( _phi0.data(), PyArray_DATA( phi0 ), _phi0.size() * sizeof( double ) );
        memcpy( _dphi.data(), PyArray_DATA( dphi ), _dphi.size() * sizeof( double ) );
        memcpy( _z0.data(), PyArray_DATA( z0 ), _z0.size() * sizeof( double ) );
        memcpy( _dz.data(), PyArray_DATA( dz ), _dz.size() * sizeof( double ) );

        Py_RETURN_NONE;
    }

    template <typename T>
    inline void get_cgem_gid( T* layer, T* sheet, T* strip_type, T* strip, T* gid ) noexcept {
        *gid = _layer_offset[*layer];
        *gid += *sheet * ( N_XSTRIPS[*layer] + N_VSTRIPS[*layer] );
        *gid += ( *strip_type ) * N_XSTRIPS[*layer];
        *gid += *strip;
    }

    template <typename T>
    inline void cgem_gid_to_layer( T* gid, T* layer ) noexcept {
        *layer = _layer[*gid];
    }

    template <typename T>
    inline void cgem_gid_to_sheet( T* gid, T* sheet ) noexcept {
        *sheet = _sheet[*gid];
    }

    template <typename T>
    inline void cgem_gid_to_strip_type( T* gid, T* strip_type ) noexcept {
        *strip_type = _strip_type[*gid];
    }

    template <typename T>
    inline void cgem_gid_to_strip( T* gid, T* strip ) noexcept {
        *strip = _strip[*gid];
    }

    template <typename T>
    inline void cgem_gid_to_is_xstrip( T* gid, bool* is_xstrip ) noexcept {
        *is_xstrip = _strip_type[*gid] == X_STRIP_TYPE;
    }

    template <typename T>
    inline void cgem_gid_to_is_vstrip( T* gid, bool* is_vstrip ) noexcept {
        *is_vstrip = _strip_type[*gid] == V_STRIP_TYPE;
    }

    template <typename T>
    inline void cgem_gid_to_width( T* gid, double* out ) noexcept {
        auto strip_type = _strip_type[*gid];
        *out            = STRIP_WIDTH[strip_type];
    }

    template <typename T>
    inline void cgem_gid_to_radius( T* gid, double* out ) noexcept {
        auto layer      = _layer[*gid];
        auto strip_type = _strip_type[*gid];
        *out            = STRIP_RADIUS[layer][strip_type];
    }

    template <typename T>
    inline void cgem_gid_to_phi0( T* gid, double* out ) noexcept {
        *out = _phi0[*gid];
    }

    template <typename T>
    inline void cgem_gid_to_dphi( T* gid, double* out ) noexcept {
        *out = _dphi[*gid];
    }

    template <typename T>
    inline void cgem_gid_to_z0( T* gid, double* out ) noexcept {
        *out = _z0[*gid];
    }

    template <typename T>
    inline void cgem_gid_to_dz( T* gid, double* out ) noexcept {
        *out = _dz[*gid];
    }

    template <typename T>
    inline void cgem_gid_phi_to_z( T* gid, double* phi, double* out ) noexcept {
        auto phi0 = _phi0[*gid];
        auto dphi = _dphi[*gid];
        auto z0   = _z0[*gid];
        auto dz   = _dz[*gid];

        // An x-strip (dphi == 0) runs along the z axis, so its phi does not give any z.
        if ( dphi == 0.0 )
        {
            *out = std::numeric_limits<double>::quiet_NaN();
            return;
        }

        // Offset from the start point. It is measured from the middle of the strip, which
        // is less than half a turn away from every point of it, so that the offset of a
        // point on the strip is exact whatever the period of `phi` is, and a `phi` outside
        // the strip is extrapolated instead of being folded to its other end.
        auto d = std::remainder( *phi - ( phi0 + 0.5 * dphi ), TWO_PI ) + 0.5 * dphi;

        *out = z0 + d / dphi * dz;
    }

    template <typename T>
    inline void cgem_gid_z_to_phi( T* gid, double* z, double* out ) noexcept {
        auto phi0 = _phi0[*gid];
        auto dphi = _dphi[*gid];
        auto z0   = _z0[*gid];
        auto dz   = _dz[*gid];

        // An x-strip (dphi == 0) runs along the z axis, so it always gives phi0 here.
        *out = phi0 + ( *z - z0 ) / dz * dphi;
    }

    void declare_cgem( PyObject* d ) {
        if ( _import_array() < 0 ) return;
        if ( _import_umath() < 0 ) return;

        decl_ufunc_41<              //
            get_cgem_gid<uint16_t>, //
            get_cgem_gid<int16_t>,  //
            get_cgem_gid<uint32_t>, //
            get_cgem_gid<int32_t>,  //
            get_cgem_gid<uint64_t>, //
            get_cgem_gid<int64_t>>  //
            ( d, "get_cgem_gid" );

        decl_ufunc_11<                   //
            cgem_gid_to_layer<uint16_t>, //
            cgem_gid_to_layer<int16_t>,  //
            cgem_gid_to_layer<uint32_t>, //
            cgem_gid_to_layer<int32_t>,  //
            cgem_gid_to_layer<uint64_t>, //
            cgem_gid_to_layer<int64_t>>  //
            ( d, "cgem_gid_to_layer" );

        decl_ufunc_11<                   //
            cgem_gid_to_sheet<uint16_t>, //
            cgem_gid_to_sheet<int16_t>,  //
            cgem_gid_to_sheet<uint32_t>, //
            cgem_gid_to_sheet<int32_t>,  //
            cgem_gid_to_sheet<uint64_t>, //
            cgem_gid_to_sheet<int64_t>>  //
            ( d, "cgem_gid_to_sheet" );

        decl_ufunc_11<                        //
            cgem_gid_to_strip_type<uint16_t>, //
            cgem_gid_to_strip_type<int16_t>,  //
            cgem_gid_to_strip_type<uint32_t>, //
            cgem_gid_to_strip_type<int32_t>,  //
            cgem_gid_to_strip_type<uint64_t>, //
            cgem_gid_to_strip_type<int64_t>>  //
            ( d, "cgem_gid_to_strip_type" );

        decl_ufunc_11<                   //
            cgem_gid_to_strip<uint16_t>, //
            cgem_gid_to_strip<int16_t>,  //
            cgem_gid_to_strip<uint32_t>, //
            cgem_gid_to_strip<int32_t>,  //
            cgem_gid_to_strip<uint64_t>, //
            cgem_gid_to_strip<int64_t>>  //
            ( d, "cgem_gid_to_strip" );

        decl_ufunc_11<                       //
            cgem_gid_to_is_xstrip<uint16_t>, //
            cgem_gid_to_is_xstrip<int16_t>,  //
            cgem_gid_to_is_xstrip<uint32_t>, //
            cgem_gid_to_is_xstrip<int32_t>,  //
            cgem_gid_to_is_xstrip<uint64_t>, //
            cgem_gid_to_is_xstrip<int64_t>>  //
            ( d, "cgem_gid_to_is_xstrip" );

        decl_ufunc_11<                       //
            cgem_gid_to_is_vstrip<uint16_t>, //
            cgem_gid_to_is_vstrip<int16_t>,  //
            cgem_gid_to_is_vstrip<uint32_t>, //
            cgem_gid_to_is_vstrip<int32_t>,  //
            cgem_gid_to_is_vstrip<uint64_t>, //
            cgem_gid_to_is_vstrip<int64_t>>  //
            ( d, "cgem_gid_to_is_vstrip" );

        decl_ufunc_11<                   //
            cgem_gid_to_width<uint16_t>, //
            cgem_gid_to_width<int16_t>,  //
            cgem_gid_to_width<uint32_t>, //
            cgem_gid_to_width<int32_t>,  //
            cgem_gid_to_width<uint64_t>, //
            cgem_gid_to_width<int64_t>>  //
            ( d, "cgem_gid_to_width" );

        decl_ufunc_11<                    //
            cgem_gid_to_radius<uint16_t>, //
            cgem_gid_to_radius<int16_t>,  //
            cgem_gid_to_radius<uint32_t>, //
            cgem_gid_to_radius<int32_t>,  //
            cgem_gid_to_radius<uint64_t>, //
            cgem_gid_to_radius<int64_t>>  //
            ( d, "cgem_gid_to_radius" );

        decl_ufunc_11<                  //
            cgem_gid_to_phi0<uint16_t>, //
            cgem_gid_to_phi0<int16_t>,  //
            cgem_gid_to_phi0<uint32_t>, //
            cgem_gid_to_phi0<int32_t>,  //
            cgem_gid_to_phi0<uint64_t>, //
            cgem_gid_to_phi0<int64_t>>  //
            ( d, "cgem_gid_to_phi0" );

        decl_ufunc_11<                  //
            cgem_gid_to_dphi<uint16_t>, //
            cgem_gid_to_dphi<int16_t>,  //
            cgem_gid_to_dphi<uint32_t>, //
            cgem_gid_to_dphi<int32_t>,  //
            cgem_gid_to_dphi<uint64_t>, //
            cgem_gid_to_dphi<int64_t>>  //
            ( d, "cgem_gid_to_dphi" );

        decl_ufunc_11<                //
            cgem_gid_to_z0<uint16_t>, //
            cgem_gid_to_z0<int16_t>,  //
            cgem_gid_to_z0<uint32_t>, //
            cgem_gid_to_z0<int32_t>,  //
            cgem_gid_to_z0<uint64_t>, //
            cgem_gid_to_z0<int64_t>>  //
            ( d, "cgem_gid_to_z0" );

        decl_ufunc_11<                //
            cgem_gid_to_dz<uint16_t>, //
            cgem_gid_to_dz<int16_t>,  //
            cgem_gid_to_dz<uint32_t>, //
            cgem_gid_to_dz<int32_t>,  //
            cgem_gid_to_dz<uint64_t>, //
            cgem_gid_to_dz<int64_t>>  //
            ( d, "cgem_gid_to_dz" );

        decl_ufunc_21<                   //
            cgem_gid_phi_to_z<uint16_t>, //
            cgem_gid_phi_to_z<int16_t>,  //
            cgem_gid_phi_to_z<uint32_t>, //
            cgem_gid_phi_to_z<int32_t>,  //
            cgem_gid_phi_to_z<uint64_t>, //
            cgem_gid_phi_to_z<int64_t>>  //
            ( d, "cgem_gid_phi_to_z" );

        decl_ufunc_21<                   //
            cgem_gid_z_to_phi<uint16_t>, //
            cgem_gid_z_to_phi<int16_t>,  //
            cgem_gid_z_to_phi<uint32_t>, //
            cgem_gid_z_to_phi<int32_t>,  //
            cgem_gid_z_to_phi<uint64_t>, //
            cgem_gid_z_to_phi<int64_t>>  //
            ( d, "cgem_gid_z_to_phi" );
    }
} // namespace cgem
