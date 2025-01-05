#include "RootEventData/TLumiDigi.h"

ClassImp( TLumiDigi );

TLumiDigi::TLumiDigi() { Clear(); }

TLumiDigi::~TLumiDigi() { Clear(); }

void TLumiDigi::setOverflow( const UInt_t overflow ) { m_overflow = overflow; }

UInt_t TLumiDigi::getOverflow() const { return m_overflow; }
