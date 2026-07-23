#include "mod.hh"
#include "ufunc.hh"

constexpr size_t N_CRYSTALS = 6240;

constexpr size_t ENDCAP_PHI_01   = 64;
constexpr size_t ENDCAP_PHI_23   = 80;
constexpr size_t ENDCAP_PHI_45   = 96;
constexpr size_t ENDCAP_CRYSTALS = 480;
constexpr size_t BARREL_PHI      = 120;
constexpr size_t BARREL_CRYSTALS = 5280;

consteval auto _init_index() {
    std::array<uint8_t, N_CRYSTALS> _part{};
    std::array<uint8_t, N_CRYSTALS> _theta{};
    std::array<uint8_t, N_CRYSTALS> _phi{};

    size_t gid = 0;
    // part 0
    for ( size_t theta = 0; theta < 6; ++theta )
    {
        size_t n_phi = 0;
        switch ( theta )
        {
        case 0: n_phi = ENDCAP_PHI_01; break;
        case 1: n_phi = ENDCAP_PHI_01; break;
        case 2: n_phi = ENDCAP_PHI_23; break;
        case 3: n_phi = ENDCAP_PHI_23; break;
        case 4: n_phi = ENDCAP_PHI_45; break;
        case 5: n_phi = ENDCAP_PHI_45; break;
        default: break;
        }
        for ( size_t phi = 0; phi < n_phi; ++phi )
        {
            _part[gid]  = 0;
            _theta[gid] = static_cast<uint8_t>( theta );
            _phi[gid]   = static_cast<uint8_t>( phi );
            gid++;
        }
    }

    // part 1
    for ( size_t theta = 0; theta < 44; ++theta )
    {
        for ( size_t phi = 0; phi < BARREL_PHI; ++phi )
        {
            _part[gid]  = 1;
            _theta[gid] = static_cast<uint8_t>( theta );
            _phi[gid]   = static_cast<uint8_t>( phi );
            gid++;
        }
    }

    // part 2
    for ( int theta = 5; theta >= 0; --theta )
    {
        size_t n_phi = 0;
        switch ( theta )
        {
        case 5: n_phi = ENDCAP_PHI_45; break;
        case 4: n_phi = ENDCAP_PHI_45; break;
        case 3: n_phi = ENDCAP_PHI_23; break;
        case 2: n_phi = ENDCAP_PHI_23; break;
        case 1: n_phi = ENDCAP_PHI_01; break;
        case 0: n_phi = ENDCAP_PHI_01; break;
        default: break;
        }
        for ( size_t phi = 0; phi < n_phi; ++phi )
        {
            _part[gid]  = 2;
            _theta[gid] = static_cast<uint8_t>( theta );
            _phi[gid]   = static_cast<uint8_t>( phi );
            gid++;
        }
    }

    return std::make_tuple( _part, _theta, _phi );
}

constexpr auto _init_index_tuple = _init_index();
constexpr auto _part             = std::get<0>( _init_index_tuple );
constexpr auto _theta            = std::get<1>( _init_index_tuple );
constexpr auto _phi              = std::get<2>( _init_index_tuple );

/* Geometry arrays */
std::array<double, N_CRYSTALS * 8> _points_x{};
std::array<double, N_CRYSTALS * 8> _points_y{};
std::array<double, N_CRYSTALS * 8> _points_z{};
std::array<double, N_CRYSTALS> _center_x{};
std::array<double, N_CRYSTALS> _center_y{};
std::array<double, N_CRYSTALS> _center_z{};
std::array<double, N_CRYSTALS> _front_center_x{};
std::array<double, N_CRYSTALS> _front_center_y{};
std::array<double, N_CRYSTALS> _front_center_z{};

PyObject* _init_emc_geom( PyObject* self, PyObject* args ) {
    PyArrayObject *points_x = nullptr, *points_y = nullptr, *points_z = nullptr;
    PyArrayObject *center_x = nullptr, *center_y = nullptr, *center_z = nullptr;
    PyArrayObject *front_center_x = nullptr, *front_center_y = nullptr,
                  *front_center_z = nullptr;

    if ( !PyArg_ParseTuple( args, "O!O!O!O!O!O!O!O!O!",     //
                            &PyArray_Type, &points_x,       //
                            &PyArray_Type, &points_y,       //
                            &PyArray_Type, &points_z,       //
                            &PyArray_Type, &center_x,       //
                            &PyArray_Type, &center_y,       //
                            &PyArray_Type, &center_z,       //
                            &PyArray_Type, &front_center_x, //
                            &PyArray_Type, &front_center_y, //
                            &PyArray_Type, &front_center_z  //
                            ) )                             //
        return nullptr;

    memcpy( _points_x.data(), PyArray_DATA( points_x ), _points_x.size() * sizeof( double ) );
    memcpy( _points_y.data(), PyArray_DATA( points_y ), _points_y.size() * sizeof( double ) );
    memcpy( _points_z.data(), PyArray_DATA( points_z ), _points_z.size() * sizeof( double ) );
    memcpy( _center_x.data(), PyArray_DATA( center_x ), _center_x.size() * sizeof( double ) );
    memcpy( _center_y.data(), PyArray_DATA( center_y ), _center_y.size() * sizeof( double ) );
    memcpy( _center_z.data(), PyArray_DATA( center_z ), _center_z.size() * sizeof( double ) );
    memcpy( _front_center_x.data(), PyArray_DATA( front_center_x ),
            _front_center_x.size() * sizeof( double ) );
    memcpy( _front_center_y.data(), PyArray_DATA( front_center_y ),
            _front_center_y.size() * sizeof( double ) );
    memcpy( _front_center_z.data(), PyArray_DATA( front_center_z ),
            _front_center_z.size() * sizeof( double ) );

    Py_RETURN_NONE;
}

template <typename T>
inline void get_emc_gid( T* part, T* theta, T* phi, T* out ) noexcept {
    if ( *part == 0 )
    {
        switch ( *theta )
        {
        case 0: *out = *phi; break;
        case 1: *out = ENDCAP_PHI_01 + *phi; break;
        case 2: *out = 2 * ENDCAP_PHI_01 + *phi; break;
        case 3: *out = 2 * ENDCAP_PHI_01 + ENDCAP_PHI_23 + *phi; break;
        case 4: *out = 2 * ( ENDCAP_PHI_01 + ENDCAP_PHI_23 ) + *phi; break;
        case 5: *out = 2 * ( ENDCAP_PHI_01 + ENDCAP_PHI_23 ) + ENDCAP_PHI_45 + *phi; break;
        default: *out = -1; break;
        }
        return;
    }
    else if ( *part == 1 )
    {
        *out = ENDCAP_CRYSTALS + *theta * BARREL_PHI + *phi;
        return;
    }
    else if ( *part == 2 )
    {
        *out = ENDCAP_CRYSTALS + BARREL_CRYSTALS;
        switch ( *theta )
        {
        case 5: *out += *phi; break;
        case 4: *out += ENDCAP_PHI_45 + *phi; break;
        case 3: *out += 2 * ENDCAP_PHI_45 + *phi; break;
        case 2: *out += 2 * ENDCAP_PHI_45 + ENDCAP_PHI_23 + *phi; break;
        case 1: *out += 2 * ( ENDCAP_PHI_45 + ENDCAP_PHI_23 ) + *phi; break;
        case 0: *out += 2 * ( ENDCAP_PHI_45 + ENDCAP_PHI_23 ) + ENDCAP_PHI_01 + *phi; break;
        default: *out = -1; break;
        }
        return;
    }
    else
    {
        *out = -1;
        return;
    }
}

template <typename T>
inline void emc_gid_to_part( T* gid, T* part ) noexcept {
    *part = _part[*gid];
}

template <typename T>
inline void emc_gid_to_theta( T* gid, T* theta ) noexcept {
    *theta = _theta[*gid];
}

template <typename T>
inline void emc_gid_to_phi( T* gid, T* phi ) noexcept {
    *phi = _phi[*gid];
}

template <typename T>
inline void emc_gid_to_center_x( T* gid, double* out ) noexcept {
    *out = _center_x[*gid];
}

template <typename T>
inline void emc_gid_to_center_y( T* gid, double* out ) noexcept {
    *out = _center_y[*gid];
}

template <typename T>
inline void emc_gid_to_center_z( T* gid, double* out ) noexcept {
    *out = _center_z[*gid];
}

template <typename T>
inline void emc_gid_to_front_center_x( T* gid, double* out ) noexcept {
    *out = _front_center_x[*gid];
}

template <typename T>
inline void emc_gid_to_front_center_y( T* gid, double* out ) noexcept {
    *out = _front_center_y[*gid];
}

template <typename T>
inline void emc_gid_to_front_center_z( T* gid, double* out ) noexcept {
    *out = _front_center_z[*gid];
}

template <typename T>
inline void emc_gid_to_point_x( T* gid, T* point, double* out ) noexcept {
    *out = _points_x[*gid * 8 + *point];
}

template <typename T>
inline void emc_gid_to_point_y( T* gid, T* point, double* out ) noexcept {
    *out = _points_y[*gid * 8 + *point];
}

template <typename T>
inline void emc_gid_to_point_z( T* gid, T* point, double* out ) noexcept {
    *out = _points_z[*gid * 8 + *point];
}

constexpr double MEASURE_EMAX[4] = { 0.078, 0.625, 2.500, 2.500 };

template <typename T>
inline void emc_adc_to_charge( T* measure, T* adc, double* out ) noexcept {
    *out = static_cast<double>( *adc ) / 1024. * MEASURE_EMAX[*measure];
}

void declare_emc( PyObject* d ) {
    if ( _import_array() < 0 ) return;
    if ( _import_umath() < 0 ) return;

    decl_ufunc_31<             //
        get_emc_gid<uint16_t>, //
        get_emc_gid<int16_t>,  //
        get_emc_gid<uint32_t>, //
        get_emc_gid<int32_t>,  //
        get_emc_gid<uint64_t>, //
        get_emc_gid<int64_t>>  //
        ( d, "get_emc_gid" );

    decl_ufunc_11<                 //
        emc_gid_to_part<uint16_t>, //
        emc_gid_to_part<int16_t>,  //
        emc_gid_to_part<uint32_t>, //
        emc_gid_to_part<int32_t>,  //
        emc_gid_to_part<uint64_t>, //
        emc_gid_to_part<int64_t>>  //
        ( d, "emc_gid_to_part" );

    decl_ufunc_11<                  //
        emc_gid_to_theta<uint16_t>, //
        emc_gid_to_theta<int16_t>,  //
        emc_gid_to_theta<uint32_t>, //
        emc_gid_to_theta<int32_t>,  //
        emc_gid_to_theta<uint64_t>, //
        emc_gid_to_theta<int64_t>>  //
        ( d, "emc_gid_to_theta" );

    decl_ufunc_11<                //
        emc_gid_to_phi<uint16_t>, //
        emc_gid_to_phi<int16_t>,  //
        emc_gid_to_phi<uint32_t>, //
        emc_gid_to_phi<int32_t>,  //
        emc_gid_to_phi<uint64_t>, //
        emc_gid_to_phi<int64_t>>  //
        ( d, "emc_gid_to_phi" );

    decl_ufunc_11<                     //
        emc_gid_to_center_x<uint16_t>, //
        emc_gid_to_center_x<int16_t>,  //
        emc_gid_to_center_x<uint32_t>, //
        emc_gid_to_center_x<int32_t>,  //
        emc_gid_to_center_x<uint64_t>, //
        emc_gid_to_center_x<int64_t>>  //
        ( d, "emc_gid_to_center_x" );

    decl_ufunc_11<                     //
        emc_gid_to_center_y<uint16_t>, //
        emc_gid_to_center_y<int16_t>,  //
        emc_gid_to_center_y<uint32_t>, //
        emc_gid_to_center_y<int32_t>,  //
        emc_gid_to_center_y<uint64_t>, //
        emc_gid_to_center_y<int64_t>>  //
        ( d, "emc_gid_to_center_y" );

    decl_ufunc_11<                     //
        emc_gid_to_center_z<uint16_t>, //
        emc_gid_to_center_z<int16_t>,  //
        emc_gid_to_center_z<uint32_t>, //
        emc_gid_to_center_z<int32_t>,  //
        emc_gid_to_center_z<uint64_t>, //
        emc_gid_to_center_z<int64_t>>  //
        ( d, "emc_gid_to_center_z" );

    decl_ufunc_11<                           //
        emc_gid_to_front_center_x<uint16_t>, //
        emc_gid_to_front_center_x<int16_t>,  //
        emc_gid_to_front_center_x<uint32_t>, //
        emc_gid_to_front_center_x<int32_t>,  //
        emc_gid_to_front_center_x<uint64_t>, //
        emc_gid_to_front_center_x<int64_t>>  //
        ( d, "emc_gid_to_front_center_x" );

    decl_ufunc_11<                           //
        emc_gid_to_front_center_y<uint16_t>, //
        emc_gid_to_front_center_y<int16_t>,  //
        emc_gid_to_front_center_y<uint32_t>, //
        emc_gid_to_front_center_y<int32_t>,  //
        emc_gid_to_front_center_y<uint64_t>, //
        emc_gid_to_front_center_y<int64_t>>  //
        ( d, "emc_gid_to_front_center_y" );

    decl_ufunc_11<                           //
        emc_gid_to_front_center_z<uint16_t>, //
        emc_gid_to_front_center_z<int16_t>,  //
        emc_gid_to_front_center_z<uint32_t>, //
        emc_gid_to_front_center_z<int32_t>,  //
        emc_gid_to_front_center_z<uint64_t>, //
        emc_gid_to_front_center_z<int64_t>>  //
        ( d, "emc_gid_to_front_center_z" );

    decl_ufunc_21<                    //
        emc_gid_to_point_x<uint16_t>, //
        emc_gid_to_point_x<int16_t>,  //
        emc_gid_to_point_x<uint32_t>, //
        emc_gid_to_point_x<int32_t>,  //
        emc_gid_to_point_x<uint64_t>, //
        emc_gid_to_point_x<int64_t>>  //
        ( d, "emc_gid_to_point_x" );

    decl_ufunc_21<                    //
        emc_gid_to_point_y<uint16_t>, //
        emc_gid_to_point_y<int16_t>,  //
        emc_gid_to_point_y<uint32_t>, //
        emc_gid_to_point_y<int32_t>,  //
        emc_gid_to_point_y<uint64_t>, //
        emc_gid_to_point_y<int64_t>>  //
        ( d, "emc_gid_to_point_y" );

    decl_ufunc_21<                    //
        emc_gid_to_point_z<uint16_t>, //
        emc_gid_to_point_z<int16_t>,  //
        emc_gid_to_point_z<uint32_t>, //
        emc_gid_to_point_z<int32_t>,  //
        emc_gid_to_point_z<uint64_t>, //
        emc_gid_to_point_z<int64_t>>  //
        ( d, "emc_gid_to_point_z" );

    decl_ufunc_21<                   //
        emc_adc_to_charge<uint16_t>, //
        emc_adc_to_charge<int16_t>,  //
        emc_adc_to_charge<uint32_t>, //
        emc_adc_to_charge<int32_t>,  //
        emc_adc_to_charge<uint64_t>, //
        emc_adc_to_charge<int64_t>>  //
        ( d, "emc_adc_to_charge" );
}
