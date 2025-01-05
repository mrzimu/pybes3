#include "RootEventData/TRecEmcShower.h"

ClassImp( TRecEmcShower );

//**************************************
TRecEmcShower::TRecEmcShower() { Clear(); }

//*************************************

TRecEmcShower::~TRecEmcShower() { Clear(); }

void TRecEmcShower::setErr( const Double_t err[6] ) {
    for ( int i = 0; i < 6; i++ ) { m_err[i] = err[i]; }
}
/************************************

  void TRecEmcShower::Clear(Option_t *option) {
  }


  void TRecEmcShower::Print(Option_t *option) const {
  TObject::Print(option);
  std::cout.precision(2);
  std::cout << "Idetifier:    " << m_intId         << std::endl;
  std::cout << "TimeChannel:  " << m_timeChannel    <<std::endl;
  std::cout << "ChargeChannel:" << m_chargeChannel <<std::endl;
  }
 ******************************/
