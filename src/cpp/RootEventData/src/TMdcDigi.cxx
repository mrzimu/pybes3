#include "RootEventData/TMdcDigi.h"

ClassImp( TMdcDigi );

//************************************************
//
TMdcDigi::TMdcDigi() { Clear(); }
//************************************************
//
TMdcDigi::~TMdcDigi() { Clear(); }
/************************************************
 void TMdcDigi::Clear(Option_t *option) {
     m_intId =0;
     m_timeChannel =0;
     m_chargeChannel =0;
 }
 ***********************************************
 void TMdcDigi::Print(Option_t *option) const {
    TObject::Print(option);
    std::cout.precision(2);
    std::cout << "Idetifier:    " << m_intId         << std::endl;
    std::cout << "TimeChannel:  " << m_timeChannel    <<std::endl;
    std::cout << "ChargeChannel:" << m_chargeChannel <<std::endl;
 }
 void TMdcDigi::initialize(UInt_t id, UInt_t time, UInt_t charge){
      m_intId = id ;
      m_timeChannel =time;
      m_chargeChannel = charge;
 }
***********************************************/

void TMdcDigi::setOverflow( const UInt_t overflow ) { m_overflow = overflow; }

// Get
UInt_t TMdcDigi::getOverflow() const { return m_overflow; }
