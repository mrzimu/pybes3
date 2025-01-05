#include "RootEventData/TRecMdcTrack.h"
#include <cmath>

ClassImp( TRecMdcTrack );

//************************************************
//
TRecMdcTrack::TRecMdcTrack() { Clear(); }
//************************************************
//
TRecMdcTrack::~TRecMdcTrack() { Clear(); }

Int_t TRecMdcTrack::charge() const {
    Int_t charge;
    Double_t temp = m_helix[2];
    if ( temp > 0.0000000001 ) charge = 1;
    else if ( temp < -0.0000000001 ) charge = -1;
    else charge = 0;
    return charge;
}

Double_t TRecMdcTrack::x() const { return m_helix[0] * cos( m_helix[1] ); }

Double_t TRecMdcTrack::y() const { return m_helix[0] * sin( m_helix[1] ); }

Double_t TRecMdcTrack::z() const { return m_helix[3]; }

Double_t TRecMdcTrack::r() const { return sqrt( x() * x() + y() * y() ); }

Double_t TRecMdcTrack::pxy() const {
    if ( m_helix[2] != 0 ) return 1. / fabs( m_helix[2] );
    else return 0.;
}

Double_t TRecMdcTrack::px() const { return pxy() * ( -sin( m_helix[1] ) ); }

Double_t TRecMdcTrack::py() const { return pxy() * cos( m_helix[1] ); }

Double_t TRecMdcTrack::pz() const { return pxy() * m_helix[4]; }

Double_t TRecMdcTrack::p() const { return sqrt( px() * px() + py() * py() + pz() * pz() ); }

Double_t TRecMdcTrack::theta() const { return acos( pz() / p() ); }

Double_t TRecMdcTrack::phi() const { return atan2( py(), px() ); }
