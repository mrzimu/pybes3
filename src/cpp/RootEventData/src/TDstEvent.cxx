#include "RootEventData/TDstEvent.h"

ClassImp( TDstEvent );

//***************************************************************
TDstEvent::TDstEvent() {
    m_mdcTrackCol    = new TObjArray();
    m_emcTrackCol    = new TObjArray();
    m_tofTrackCol    = new TObjArray();
    m_mucTrackCol    = new TObjArray();
    m_mdcDedxCol     = new TObjArray();
    m_extTrackCol    = new TObjArray();
    m_mdcKalTrackCol = new TObjArray();
    Clear();
}

//*****************************************************************
TDstEvent::~TDstEvent() {
    m_mdcTrackCol->Delete();
    delete m_mdcTrackCol;
    m_mdcTrackCol = nullptr;

    m_emcTrackCol->Delete();
    delete m_emcTrackCol;
    m_emcTrackCol = nullptr;

    m_tofTrackCol->Delete();
    delete m_tofTrackCol;
    m_tofTrackCol = nullptr;

    m_mucTrackCol->Delete();
    delete m_mucTrackCol;
    m_mucTrackCol = nullptr;

    m_mdcDedxCol->Delete();
    delete m_mdcDedxCol;
    m_mdcDedxCol = nullptr;

    m_extTrackCol->Delete();
    delete m_extTrackCol;
    m_extTrackCol = nullptr;

    m_mdcKalTrackCol->Delete();
    delete m_mdcKalTrackCol;
    m_mdcKalTrackCol = nullptr;
}

//*****************************************************************
void TDstEvent::initialize() {}

//*****************************************************************
void TDstEvent::Clear( Option_t* option ) {}

//*****************************************************************************
void TDstEvent::Print( Option_t* option ) const { TObject::Print( option ); }

/****************     Dst Track     ************************/
/// Mdc
void TDstEvent::addMdcTrack( TMdcTrack* Track ) { m_mdcTrackCol->Add( Track ); }

const TMdcTrack* TDstEvent::getMdcTrack( Int_t i ) const {
    if ( Int_t( i ) >= m_mdcTrackCol->GetEntries() ) return 0;
    return (TMdcTrack*)m_mdcTrackCol->At( i );
}
/// Emc
void TDstEvent::addEmcTrack( TEmcTrack* Track ) { m_emcTrackCol->Add( Track ); }

const TEmcTrack* TDstEvent::getEmcTrack( Int_t i ) const {
    if ( Int_t( i ) >= m_emcTrackCol->GetEntries() ) return 0;
    return (TEmcTrack*)m_emcTrackCol->At( i );
}

/// Tof
void TDstEvent::addTofTrack( TTofTrack* Track ) { m_tofTrackCol->Add( Track ); }

const TTofTrack* TDstEvent::getTofTrack( Int_t i ) const {
    if ( Int_t( i ) >= m_tofTrackCol->GetEntries() ) return 0;
    return (TTofTrack*)m_tofTrackCol->At( i );
}
/// Muc
void TDstEvent::addMucTrack( TMucTrack* Track ) { m_mucTrackCol->Add( Track ); }

const TMucTrack* TDstEvent::getMucTrack( Int_t i ) const {
    if ( Int_t( i ) >= m_mucTrackCol->GetEntries() ) return 0;
    return (TMucTrack*)m_mucTrackCol->At( i );
}
/// Dedx
void TDstEvent::addMdcDedx( TMdcDedx* Track ) { m_mdcDedxCol->Add( Track ); }

const TMdcDedx* TDstEvent::getMdcDedx( Int_t i ) const {
    if ( Int_t( i ) >= m_mdcDedxCol->GetEntries() ) return 0;
    return (TMdcDedx*)m_mdcDedxCol->At( i );
}

// Ext
void TDstEvent::addExtTrack( TExtTrack* Track ) { m_extTrackCol->Add( Track ); }

const TExtTrack* TDstEvent::getExtTrack( Int_t i ) const {
    if ( Int_t( i ) >= m_extTrackCol->GetEntries() ) return 0;
    return (TExtTrack*)m_extTrackCol->At( i );
}

// MdcKal
void TDstEvent::addMdcKalTrack( TMdcKalTrack* Track ) { m_mdcKalTrackCol->Add( Track ); }

const TMdcKalTrack* TDstEvent::getMdcKalTrack( Int_t i ) const {
    if ( Int_t( i ) >= m_mdcKalTrackCol->GetEntries() ) return 0;
    return (TMdcKalTrack*)m_mdcKalTrackCol->At( i );
}
