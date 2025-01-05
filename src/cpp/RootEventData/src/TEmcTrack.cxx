#include "RootEventData/TEmcTrack.h"
#include <cmath>

using namespace std;

ClassImp( TEmcTrack );

//**************************************
TEmcTrack::TEmcTrack() { Clear(); }

//*************************************

TEmcTrack::~TEmcTrack() { Clear(); }

void TEmcTrack::setErr( const Double_t err[6] ) {
    for ( int i = 0; i < 6; i++ ) { m_err[i] = err[i]; }
}
/************************************

  void TEmcTrack::Clear(Option_t *option) {
  }


  void TEmcTrack::Print(Option_t *option) const {
  TObject::Print(option);
  std::cout.precision(2);
  std::cout << "Idetifier:    " << m_intId         << std::endl;
  std::cout << "TimeChannel:  " << m_timeChannel    <<std::endl;
  std::cout << "ChargeChannel:" << m_chargeChannel <<std::endl;
  }
 ******************************/

Double_t TEmcTrack::dx() const {
    double xx = 99.;
    if ( m_err[0] > 0 ) xx = sqrt( m_err[0] );
    else if ( m_err[0] == 0 ) xx = 0.;
    return xx;
}

Double_t TEmcTrack::dy() const {
    double yy = 99.;
    if ( m_err[1] > 0 ) yy = sqrt( m_err[1] );
    else if ( m_err[1] == 0 ) yy = 0.;
    return yy;
}

Double_t TEmcTrack::dz() const {
    double zz = 99.;
    if ( m_err[2] > 0 ) zz = sqrt( m_err[2] );
    else if ( m_err[2] == 0 ) zz = 0.;
    return zz;
}
