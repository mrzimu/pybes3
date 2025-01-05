#include "RootEventData/TTrigEvent.h"

ClassImp( TTrigEvent );

//***************************************************************
TTrigEvent::TTrigEvent() : m_trigData( 0 ) {
    m_trigData = new TTrigData();
    Clear();
}

//*****************************************************************
TTrigEvent::~TTrigEvent() {
    delete m_trigData;
    m_trigData = 0;
}

//*****************************************************************
// o void TTrigEvent::initialize(Bool_t fromMc){
// o    m_fromMc = fromMc;
// o }

//*****************************************************************
void TTrigEvent::Clear( Option_t* option ) {}

//*****************************************************************************
void TTrigEvent::Print( Option_t* option ) const { TObject::Print( option ); }

/// TrigData
void TTrigEvent::addTrigData( TTrigData* trigData ) { m_trigData = trigData; }

const TTrigData* TTrigEvent::getTrigData() const { return (TTrigData*)m_trigData; }
