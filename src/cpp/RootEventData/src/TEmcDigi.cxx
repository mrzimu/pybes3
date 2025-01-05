#include "RootEventData/TEmcDigi.h"

ClassImp( TEmcDigi );

//**************************************
TEmcDigi::TEmcDigi() { Clear(); }

//*************************************

TEmcDigi::~TEmcDigi() { Clear(); }

/************************************

void TEmcDigi::Clear(Option_t *option) {
}


void TEmcDigi::Print(Option_t *option) const {
     TObject::Print(option);
     std::cout.precision(2);
     std::cout << "Idetifier:    " << m_intId         << std::endl;
     std::cout << "TimeChannel:  " << m_timeChannel    <<std::endl;
     std::cout << "ChargeChannel:" << m_chargeChannel <<std::endl;
}
 ******************************/

void TEmcDigi::setMeasure( const UInt_t measure ) { m_measure = measure; }

UInt_t TEmcDigi::getMeasure() const { return m_measure; }
