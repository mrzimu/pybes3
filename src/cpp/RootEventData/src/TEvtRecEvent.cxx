#include "RootEventData/TEvtRecEvent.h"

ClassImp( TEvtRecEvent );

// Allocate the TObjArray just once

TEvtRecEvent::TEvtRecEvent()
    : m_tottks( 0 ), m_nchrg( 0 ), m_nneu( 0 ), m_nvee( 0 ), m_npi0( 0 ), m_ndtag( 0 ) {
    Clear();
}

TEvtRecEvent::~TEvtRecEvent() {}

void TEvtRecEvent::initialize() {}

void TEvtRecEvent::Clear( Option_t* option ) {}

void TEvtRecEvent::Print( Option_t* option ) const { TObject::Print( option ); }
