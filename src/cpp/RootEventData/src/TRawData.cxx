#include "RootEventData/TRawData.h"
#include <iostream>

ClassImp( TRawData );

//************************************************
//
TRawData::TRawData() { Clear(); }
//************************************************
//
TRawData::~TRawData() { Clear(); }
//************************************************
//
void TRawData::Clear( Option_t* option ) {
    m_intId         = 0;
    m_timeChannel   = 0;
    m_chargeChannel = 0;
}
//************************************************
//
void TRawData::Print( Option_t* option ) const {
    TObject::Print( option );
    std::cout.precision( 2 );
    std::cout << "Idetifier:    " << m_intId << std::endl;
    std::cout << "TimeChannel:  " << m_timeChannel << std::endl;
    std::cout << "ChargeChannel:" << m_chargeChannel << std::endl;
}
//************************************************
//
void TRawData::initialize( UInt_t id, UInt_t time, UInt_t charge ) {
    m_intId         = id;
    m_timeChannel   = time;
    m_chargeChannel = charge;
}
//************************************************

void TRawData::setTrackIndex( const int trackIndex ) { m_trackIndex = trackIndex; }

int TRawData::getTrackIndex() const { return m_trackIndex; }

// Get associated int id
UInt_t TRawData::getIntId() const { return m_intId; }

// Get time channel
UInt_t TRawData::getTimeChannel() const { return m_timeChannel; }

// Get charge channel
UInt_t TRawData::getChargeChannel() const { return m_chargeChannel; }
