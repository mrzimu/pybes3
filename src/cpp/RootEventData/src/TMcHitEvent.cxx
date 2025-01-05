#include "RootEventData/TMcHitEvent.h"
#include "TCollection.h" // Declares TIter

ClassImp( TMcHitEvent );

//***************************************************************
TMcHitEvent::TMcHitEvent() {
    m_beamTime      = -1.;
    m_tTofMcHitCol  = new TObjArray();
    m_tMdcMcHitCol  = new TObjArray();
    m_tEmcMcDigiCol = new TObjArray();
    Clear();
}

//*****************************************************************
TMcHitEvent::~TMcHitEvent() {
    m_tTofMcHitCol->Delete();
    delete m_tTofMcHitCol;
    m_tTofMcHitCol = 0;

    m_tMdcMcHitCol->Delete();
    delete m_tMdcMcHitCol;
    m_tMdcMcHitCol = 0;

    m_tEmcMcDigiCol->Delete();
    delete m_tEmcMcDigiCol;
    m_tEmcMcDigiCol = 0;
}

//*****************************************************************
void TMcHitEvent::Clear( Option_t* option ) {
    int i = 0;

    for ( i = 0; i < m_tTofMcHitCol->GetEntries(); i++ ) delete m_tTofMcHitCol->At( i );
    m_tTofMcHitCol->Clear();

    for ( i = 0; i < m_tMdcMcHitCol->GetEntries(); i++ ) delete m_tMdcMcHitCol->At( i );
    m_tMdcMcHitCol->Clear();

    for ( i = 0; i < m_tEmcMcDigiCol->GetEntries(); i++ ) delete m_tEmcMcDigiCol->At( i );
    m_tEmcMcDigiCol->Clear();
}

//*****************************************************************************
void TMcHitEvent::Print( Option_t* option ) const { TObject::Print( option ); }

/// Emc
void TMcHitEvent::addMcDigiEmc( TMcDigiEmc* mcDigi ) { m_tEmcMcDigiCol->Add( mcDigi ); }

const TMcDigiEmc* TMcHitEvent::getMcDigiEmc( Int_t i ) const {
    if ( Int_t( i ) >= m_tEmcMcDigiCol->GetEntries() ) return 0;
    else return (TMcDigiEmc*)m_tEmcMcDigiCol->At( i );
}

/// Tof
void TMcHitEvent::addMcHitTof( TMcHitTof* mcHit ) { m_tTofMcHitCol->Add( mcHit ); }

const TMcHitTof* TMcHitEvent::getMcHitTof( Int_t i ) const {
    if ( Int_t( i ) >= m_tTofMcHitCol->GetEntries() ) return 0;
    else return (TMcHitTof*)m_tTofMcHitCol->At( i );
}

/// Mdc
void TMcHitEvent::addMcHitMdc( TMcHitMdc* mcHit ) { m_tMdcMcHitCol->Add( mcHit ); }

const TMcHitMdc* TMcHitEvent::getMcHitMdc( Int_t i ) const {
    if ( Int_t( i ) >= m_tMdcMcHitCol->GetEntries() ) return 0;
    else return (TMcHitMdc*)m_tMdcMcHitCol->At( i );
}
