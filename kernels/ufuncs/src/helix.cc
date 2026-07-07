#include "mod.hh"
#include "ufunc.hh"

// ---------------------------------------------------------------------------
// Constant: 1000 / 2.99792458  (for kappa -> radius conversion)
// ---------------------------------------------------------------------------
static constexpr double kKappaToRadiusFactor = 1000.0 / 2.99792458;

template <typename T>
inline void dr_phi0_to_x( T* dr, T* phi0, T* x ) noexcept {
    *x = *dr * std::cos( *phi0 );
}

template <typename T>
inline void dr_phi0_to_y( T* dr, T* phi0, T* y ) noexcept {
    *y = *dr * std::sin( *phi0 );
}

template <typename T>
inline void phi0_to_phi( T* phi0, T* phi ) noexcept {
    T result = std::fmod( *phi0 + T( M_PI_2 ), T( 2.0 * M_PI ) );
    if ( result < T( 0.0 ) ) result += T( 2.0 * M_PI );
    *phi = result;
}

template <typename T>
inline void kappa_to_pt( T* kappa, T* pt ) noexcept {
    *pt = T( 1.0 ) / std::abs( *kappa );
}

template <typename T>
inline void kappa_to_charge( T* kappa, int64_t* charge ) noexcept {
    if ( *kappa > T( 1e-10 ) ) *charge = 1;
    else if ( *kappa < T( -1e-10 ) ) *charge = -1;
    else *charge = 0;
}

template <typename T>
inline void kappa_to_radius( T* kappa, T* radius ) noexcept {
    *radius = T( kKappaToRadiusFactor ) / std::abs( *kappa );
}

template <typename T>
inline void _fix_dr_sign( T* dr, T* phi0, T* dist_phi, T* result ) noexcept {
    T a = std::fmod( *dist_phi, T( 2.0 * M_PI ) );
    if ( a < T( 0.0 ) ) a += T( 2.0 * M_PI );
    T tol = T( 1e-8 ) + T( 1e-5 ) * std::abs( *phi0 );
    if ( std::abs( a - *phi0 ) > tol ) *result = -( *dr );
    else *result = *dr;
}

void declare_helix( PyObject* d ) {
    if ( _import_array() < 0 ) return;
    if ( _import_umath() < 0 ) return;

    decl_ufunc_21<            //
        dr_phi0_to_x<double>, //
        dr_phi0_to_x<float>>  //
        ( d, "dr_phi0_to_x" );

    decl_ufunc_21<            //
        dr_phi0_to_y<double>, //
        dr_phi0_to_y<float>>  //
        ( d, "dr_phi0_to_y" );

    decl_ufunc_11<           //
        phi0_to_phi<double>, //
        phi0_to_phi<float>>  //
        ( d, "phi0_to_phi" );

    decl_ufunc_11<           //
        kappa_to_pt<double>, //
        kappa_to_pt<float>>  //
        ( d, "kappa_to_pt" );

    decl_ufunc_11<               //
        kappa_to_charge<double>, //
        kappa_to_charge<float>>  //
        ( d, "kappa_to_charge" );

    decl_ufunc_11<               //
        kappa_to_radius<double>, //
        kappa_to_radius<float>>  //
        ( d, "kappa_to_radius" );

    decl_ufunc_31<            //
        _fix_dr_sign<double>, //
        _fix_dr_sign<float>>  //
        ( d, "_fix_dr_sign" );
}
