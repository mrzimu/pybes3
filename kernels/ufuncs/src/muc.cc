#include <numeric>
#include <tuple>

#include "mod.hh"
#include "ufunc.hh"

namespace muc {
    constexpr size_t N_PARTS = 3;

    constexpr std::array<size_t, N_PARTS> N_SEGMENTS = { 4, 8, 4 };
    constexpr std::array<size_t, N_PARTS> N_LAYERS   = { 8, 9, 8 };

    constexpr size_t N_STRIP_ENDCAP = 64;

    constexpr std::array<std::array<size_t, 9>, 8> N_STRIP_BARREL = {
        { { { 48, 96, 48, 96, 48, 96, 48, 96, 48 } },
          { { 48, 96, 48, 96, 48, 96, 48, 96, 48 } },
          { { 48, 112, 48, 112, 48, 112, 48, 112, 48 } },
          { { 48, 96, 48, 96, 48, 96, 48, 96, 48 } },
          { { 48, 96, 48, 96, 48, 96, 48, 96, 48 } },
          { { 48, 96, 48, 96, 48, 96, 48, 96, 48 } },
          { { 48, 96, 48, 96, 48, 96, 48, 96, 48 } },
          { { 48, 96, 48, 96, 48, 96, 48, 96, 48 } } } };

    constexpr size_t N_STRIPS = 9152;

    consteval auto _init() {
        std::array<uint8_t, N_STRIPS> _part{};
        std::array<uint8_t, N_STRIPS> _segment{};
        std::array<uint8_t, N_STRIPS> _layer{};
        std::array<uint8_t, N_STRIPS> _strip{};

        // [segment][layer] -> gid offset
        std::array<std::array<uint16_t, 8>, 4> _endcap0_gid_offsets{};
        std::array<std::array<uint16_t, 8>, 4> _endcap1_gid_offsets{};
        std::array<std::array<uint16_t, 9>, 8> _barrel_gid_offsets{};

        size_t gid = 0;
        for ( size_t part = 0; part < N_PARTS; part++ )
        {
            for ( size_t segment = 0; segment < N_SEGMENTS[part]; segment++ )
            {
                for ( size_t layer = 0; layer < N_LAYERS[part]; layer++ )
                {
                    auto n_strips =
                        ( part == 1 ) ? N_STRIP_BARREL[segment][layer] : N_STRIP_ENDCAP;

                    switch ( part )
                    {
                    case 0: _endcap0_gid_offsets[segment][layer] = gid; break;
                    case 1: _barrel_gid_offsets[segment][layer] = gid; break;
                    case 2: _endcap1_gid_offsets[segment][layer] = gid; break;
                    }

                    for ( size_t strip = 0; strip < n_strips; strip++ )
                    {
                        _part[gid]    = part;
                        _segment[gid] = segment;
                        _layer[gid]   = layer;
                        _strip[gid]   = strip;
                        gid++;
                    }
                }
            }
        }
        return std::make_tuple( _part, _segment, _layer, _strip, _endcap0_gid_offsets,
                                _barrel_gid_offsets, _endcap1_gid_offsets );
    }

    constexpr auto _init_tuple = _init();
    constexpr auto _part       = std::get<0>( _init_tuple );
    constexpr auto _segment    = std::get<1>( _init_tuple );
    constexpr auto _layer      = std::get<2>( _init_tuple );
    constexpr auto _strip      = std::get<3>( _init_tuple );

    constexpr auto _endcap0_gid_offsets = std::get<4>( _init_tuple );
    constexpr auto _barrel_gid_offsets  = std::get<5>( _init_tuple );
    constexpr auto _endcap1_gid_offsets = std::get<6>( _init_tuple );

    /* Geometry arrays */
    std::array<double, N_STRIPS * 8> _points_x{};
    std::array<double, N_STRIPS * 8> _points_y{};
    std::array<double, N_STRIPS * 8> _points_z{};
    std::array<double, N_STRIPS> _center_x{};
    std::array<double, N_STRIPS> _center_y{};
    std::array<double, N_STRIPS> _center_z{};
    std::array<double, N_STRIPS> _dx{};
    std::array<double, N_STRIPS> _dy{};
    std::array<double, N_STRIPS> _dz{};

    PyObject* _init_muc_geom( PyObject* self, PyObject* args ) {
        PyArrayObject *points_x = nullptr, *points_y = nullptr, *points_z = nullptr;
        PyArrayObject *center_x = nullptr, *center_y = nullptr, *center_z = nullptr;
        PyArrayObject *dx = nullptr, *dy = nullptr, *dz = nullptr;

        if ( !PyArg_ParseTuple( args, "O!O!O!O!O!O!O!O!O!", //
                                &PyArray_Type, &points_x,   //
                                &PyArray_Type, &points_y,   //
                                &PyArray_Type, &points_z,   //
                                &PyArray_Type, &center_x,   //
                                &PyArray_Type, &center_y,   //
                                &PyArray_Type, &center_z,   //
                                &PyArray_Type, &dx,         //
                                &PyArray_Type, &dy,         //
                                &PyArray_Type, &dz          //
                                ) )                         //
            return nullptr;

        memcpy( _points_x.data(), PyArray_DATA( points_x ),
                _points_x.size() * sizeof( double ) );
        memcpy( _points_y.data(), PyArray_DATA( points_y ),
                _points_y.size() * sizeof( double ) );
        memcpy( _points_z.data(), PyArray_DATA( points_z ),
                _points_z.size() * sizeof( double ) );
        memcpy( _center_x.data(), PyArray_DATA( center_x ),
                _center_x.size() * sizeof( double ) );
        memcpy( _center_y.data(), PyArray_DATA( center_y ),
                _center_y.size() * sizeof( double ) );
        memcpy( _center_z.data(), PyArray_DATA( center_z ),
                _center_z.size() * sizeof( double ) );
        memcpy( _dx.data(), PyArray_DATA( dx ), _dx.size() * sizeof( double ) );
        memcpy( _dy.data(), PyArray_DATA( dy ), _dy.size() * sizeof( double ) );
        memcpy( _dz.data(), PyArray_DATA( dz ), _dz.size() * sizeof( double ) );

        Py_RETURN_NONE;
    }

    template <typename T>
    inline void get_muc_gid( T* part, T* segment, T* layer, T* strip, T* out ) noexcept {
        switch ( *part )
        {
        case 0: *out = _endcap0_gid_offsets[*segment][*layer] + *strip; break;
        case 1: *out = _barrel_gid_offsets[*segment][*layer] + *strip; break;
        case 2: *out = _endcap1_gid_offsets[*segment][*layer] + *strip; break;
        }
    }

    template <typename T>
    inline void muc_gid_to_part( T* gid, T* out ) noexcept {
        *out = _part[*gid];
    }

    template <typename T>
    inline void muc_gid_to_segment( T* gid, T* out ) noexcept {
        *out = _segment[*gid];
    }

    template <typename T>
    inline void muc_gid_to_layer( T* gid, T* out ) noexcept {
        *out = _layer[*gid];
    }

    template <typename T>
    inline void muc_gid_to_strip( T* gid, T* out ) noexcept {
        *out = _strip[*gid];
    }

    template <typename T>
    inline void muc_gid_to_center_x( T* gid, double* out ) noexcept {
        *out = _center_x[*gid];
    }

    template <typename T>
    inline void muc_gid_to_center_y( T* gid, double* out ) noexcept {
        *out = _center_y[*gid];
    }

    template <typename T>
    inline void muc_gid_to_center_z( T* gid, double* out ) noexcept {
        *out = _center_z[*gid];
    }

    template <typename T>
    inline void muc_gid_to_dx( T* gid, double* out ) noexcept {
        *out = _dx[*gid];
    }

    template <typename T>
    inline void muc_gid_to_dy( T* gid, double* out ) noexcept {
        *out = _dy[*gid];
    }

    template <typename T>
    inline void muc_gid_to_dz( T* gid, double* out ) noexcept {
        *out = _dz[*gid];
    }

    template <typename T>
    inline void muc_gid_to_point_x( T* gid, T* point, double* out ) noexcept {
        *out = _points_x[*gid * 8 + *point];
    }

    template <typename T>
    inline void muc_gid_to_point_y( T* gid, T* point, double* out ) noexcept {
        *out = _points_y[*gid * 8 + *point];
    }

    template <typename T>
    inline void muc_gid_to_point_z( T* gid, T* point, double* out ) noexcept {
        *out = _points_z[*gid * 8 + *point];
    }

    void declare_muc( PyObject* d ) {
        if ( _import_array() < 0 ) return;
        if ( _import_umath() < 0 ) return;

        decl_ufunc_41<             //
            get_muc_gid<uint16_t>, //
            get_muc_gid<int16_t>,  //
            get_muc_gid<uint32_t>, //
            get_muc_gid<int32_t>,  //
            get_muc_gid<uint64_t>, //
            get_muc_gid<int64_t>>  //
            ( d, "get_muc_gid" );

        decl_ufunc_11<                 //
            muc_gid_to_part<uint16_t>, //
            muc_gid_to_part<int16_t>,  //
            muc_gid_to_part<uint32_t>, //
            muc_gid_to_part<int32_t>,  //
            muc_gid_to_part<uint64_t>, //
            muc_gid_to_part<int64_t>>  //
            ( d, "muc_gid_to_part" );

        decl_ufunc_11<                    //
            muc_gid_to_segment<uint16_t>, //
            muc_gid_to_segment<int16_t>,  //
            muc_gid_to_segment<uint32_t>, //
            muc_gid_to_segment<int32_t>,  //
            muc_gid_to_segment<uint64_t>, //
            muc_gid_to_segment<int64_t>>  //
            ( d, "muc_gid_to_segment" );

        decl_ufunc_11<                  //
            muc_gid_to_layer<uint16_t>, //
            muc_gid_to_layer<int16_t>,  //
            muc_gid_to_layer<uint32_t>, //
            muc_gid_to_layer<int32_t>,  //
            muc_gid_to_layer<uint64_t>, //
            muc_gid_to_layer<int64_t>>  //
            ( d, "muc_gid_to_layer" );

        decl_ufunc_11<                  //
            muc_gid_to_strip<uint16_t>, //
            muc_gid_to_strip<int16_t>,  //
            muc_gid_to_strip<uint32_t>, //
            muc_gid_to_strip<int32_t>,  //
            muc_gid_to_strip<uint64_t>, //
            muc_gid_to_strip<int64_t>>  //
            ( d, "muc_gid_to_strip" );

        decl_ufunc_11<                     //
            muc_gid_to_center_x<uint16_t>, //
            muc_gid_to_center_x<int16_t>,  //
            muc_gid_to_center_x<uint32_t>, //
            muc_gid_to_center_x<int32_t>,  //
            muc_gid_to_center_x<uint64_t>, //
            muc_gid_to_center_x<int64_t>>  //
            ( d, "muc_gid_to_center_x" );

        decl_ufunc_11<                     //
            muc_gid_to_center_y<uint16_t>, //
            muc_gid_to_center_y<int16_t>,  //
            muc_gid_to_center_y<uint32_t>, //
            muc_gid_to_center_y<int32_t>,  //
            muc_gid_to_center_y<uint64_t>, //
            muc_gid_to_center_y<int64_t>>  //
            ( d, "muc_gid_to_center_y" );

        decl_ufunc_11<                     //
            muc_gid_to_center_z<uint16_t>, //
            muc_gid_to_center_z<int16_t>,  //
            muc_gid_to_center_z<uint32_t>, //
            muc_gid_to_center_z<int32_t>,  //
            muc_gid_to_center_z<uint64_t>, //
            muc_gid_to_center_z<int64_t>>  //
            ( d, "muc_gid_to_center_z" );

        decl_ufunc_11<               //
            muc_gid_to_dx<uint16_t>, //
            muc_gid_to_dx<int16_t>,  //
            muc_gid_to_dx<uint32_t>, //
            muc_gid_to_dx<int32_t>,  //
            muc_gid_to_dx<uint64_t>, //
            muc_gid_to_dx<int64_t>>  //
            ( d, "muc_gid_to_dx" );

        decl_ufunc_11<               //
            muc_gid_to_dy<uint16_t>, //
            muc_gid_to_dy<int16_t>,  //
            muc_gid_to_dy<uint32_t>, //
            muc_gid_to_dy<int32_t>,  //
            muc_gid_to_dy<uint64_t>, //
            muc_gid_to_dy<int64_t>>  //
            ( d, "muc_gid_to_dy" );

        decl_ufunc_11<               //
            muc_gid_to_dz<uint16_t>, //
            muc_gid_to_dz<int16_t>,  //
            muc_gid_to_dz<uint32_t>, //
            muc_gid_to_dz<int32_t>,  //
            muc_gid_to_dz<uint64_t>, //
            muc_gid_to_dz<int64_t>>  //
            ( d, "muc_gid_to_dz" );

        decl_ufunc_21<                    //
            muc_gid_to_point_x<uint16_t>, //
            muc_gid_to_point_x<int16_t>,  //
            muc_gid_to_point_x<uint32_t>, //
            muc_gid_to_point_x<int32_t>,  //
            muc_gid_to_point_x<uint64_t>, //
            muc_gid_to_point_x<int64_t>>  //
            ( d, "muc_gid_to_point_x" );

        decl_ufunc_21<                    //
            muc_gid_to_point_y<uint16_t>, //
            muc_gid_to_point_y<int16_t>,  //
            muc_gid_to_point_y<uint32_t>, //
            muc_gid_to_point_y<int32_t>,  //
            muc_gid_to_point_y<uint64_t>, //
            muc_gid_to_point_y<int64_t>>  //
            ( d, "muc_gid_to_point_y" );

        decl_ufunc_21<                    //
            muc_gid_to_point_z<uint16_t>, //
            muc_gid_to_point_z<int16_t>,  //
            muc_gid_to_point_z<uint32_t>, //
            muc_gid_to_point_z<int32_t>,  //
            muc_gid_to_point_z<uint64_t>, //
            muc_gid_to_point_z<int64_t>>  //
            ( d, "muc_gid_to_point_z" );
    }

} // namespace muc
