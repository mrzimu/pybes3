#include "RootEventData/TMdcTrack.h"
#include <cmath>

using namespace std;

ClassImp( TMdcTrack );

//************************************************
//
TMdcTrack::TMdcTrack() { Clear(); }
//************************************************
//
TMdcTrack::~TMdcTrack() { Clear(); }
Int_t TMdcTrack::charge() const {
    Int_t charge;
    Double_t temp = m_helix[2];
    if ( temp > 0.0000000001 ) charge = 1;
    else if ( temp < -0.0000000001 ) charge = -1;
    else charge = 0;
    return charge;
}

Double_t TMdcTrack::x() const { return m_helix[0] * cos( m_helix[1] ); }

Double_t TMdcTrack::y() const { return m_helix[0] * sin( m_helix[1] ); }

Double_t TMdcTrack::z() const { return m_helix[3]; }

Double_t TMdcTrack::r() const {
    //    return  sqrt(x()*x()+y()*y());
    return fabs( m_helix[0] );
}

Double_t TMdcTrack::pxy() const {
    if ( m_helix[2] != 0 ) return 1. / fabs( m_helix[2] );
    else return 0.;
}

Double_t TMdcTrack::px() const { return pxy() * ( -sin( m_helix[1] ) ); }

Double_t TMdcTrack::py() const { return pxy() * cos( m_helix[1] ); }

Double_t TMdcTrack::pz() const { return pxy() * m_helix[4]; }

Double_t TMdcTrack::p() const {
    //    return  sqrt(px()*px() + py()*py() + pz()*pz());
    return pxy() * sqrt( 1. + m_helix[4] * m_helix[4] );
}

Double_t TMdcTrack::theta() const { return acos( pz() / p() ); }

Double_t TMdcTrack::phi() const { return atan2( py(), px() ); }

void TMdcTrack::setHelix( const Double_t helix[5] ) {
    for ( Int_t i = 0; i < 5; i++ ) { m_helix[i] = helix[i]; }
}

void TMdcTrack::setErr( const Double_t er[15] ) {
    for ( Int_t i = 0; i < 15; i++ ) { m_err[i] = er[i]; }
}
