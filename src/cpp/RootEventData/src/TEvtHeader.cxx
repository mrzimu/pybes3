#include "RootEventData/TEvtHeader.h"
#include "TCollection.h" // Declares TIter
#include <iostream>

ClassImp( TEvtHeader );

// Allocate the TObjArray just once

//***************************************************************
TEvtHeader::TEvtHeader()
    : m_eventId( -1 )
    , m_runId( -1 )
    , m_time( 0 )
    , m_eventTag( 0 )
    , m_flag1( 0 )
    , m_flag2( 0 )
    , m_etsT1( 0 )
    , m_etsT2( 0 ) {}

//*****************************************************************
TEvtHeader::~TEvtHeader() {}

//*****************************************************************
void TEvtHeader::initialize( Int_t event, Int_t runId, UInt_t eventTag ) {
    m_eventId  = event;
    m_runId    = runId;
    m_eventTag = eventTag;
}

//*****************************************************************
void TEvtHeader::Clear( Option_t* option ) {

    m_eventId  = 0;
    m_runId    = 0;
    m_eventTag = 0;
    m_time     = 0;
    m_flag1    = 0;
    m_flag2    = 0;
}

//*****************************************************************************
void TEvtHeader::Print( Option_t* option ) const {
    TObject::Print( option );
    std::cout.precision( 2 );
    std::cout << "Run, Event, TotEvtNum, EventTag: " << m_runId << ", " << m_eventId << ", "
              << std::hex << m_eventTag << std::dec << std::endl;
}
