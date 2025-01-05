#include "RootEventData/TRecTrackEvent.h"

ClassImp( TRecTrackEvent );

// Allocate the TObjArray just once

//***************************************************************
TRecTrackEvent::TRecTrackEvent() {
    m_recMdcTrackCol       = new TObjArray();
    m_recMdcHitCol         = new TObjArray();
    m_recTofTrackCol       = new TObjArray();
    m_recEmcHitCol         = new TObjArray();
    m_recEmcClusterCol     = new TObjArray();
    m_recEmcShowerCol      = new TObjArray();
    m_recMucTrackCol       = new TObjArray();
    m_recMdcDedxCol        = new TObjArray();
    m_recMdcDedxHitCol     = new TObjArray();
    m_recExtTrackCol       = new TObjArray();
    m_recMdcKalTrackCol    = new TObjArray();
    m_recMdcKalHelixSegCol = new TObjArray();
    m_recEvTimeCol         = new TObjArray();
    m_recZddChannelCol     = new TObjArray();
    Clear();
}

//*****************************************************************
TRecTrackEvent::~TRecTrackEvent() {
    m_recMdcTrackCol->Delete();
    delete m_recMdcTrackCol;
    m_recMdcTrackCol = nullptr;

    m_recMdcHitCol->Delete();
    delete m_recMdcHitCol;
    m_recMdcHitCol = nullptr;

    m_recTofTrackCol->Delete();
    delete m_recTofTrackCol;
    m_recTofTrackCol = nullptr;

    m_recEmcHitCol->Delete();
    delete m_recEmcHitCol;
    m_recEmcHitCol = nullptr;

    m_recEmcClusterCol->Delete();
    delete m_recEmcClusterCol;
    m_recEmcClusterCol = nullptr;

    m_recEmcShowerCol->Delete();
    delete m_recEmcShowerCol;
    m_recEmcShowerCol = nullptr;

    m_recMucTrackCol->Delete();
    delete m_recMucTrackCol;
    m_recMucTrackCol = nullptr;

    m_recMdcDedxCol->Delete();
    delete m_recMdcDedxCol;
    m_recMdcDedxCol = nullptr;

    m_recMdcDedxHitCol->Delete();
    delete m_recMdcDedxHitCol;
    m_recMdcDedxHitCol = nullptr;

    m_recExtTrackCol->Delete();
    delete m_recExtTrackCol;
    m_recExtTrackCol = nullptr;

    m_recMdcKalTrackCol->Delete();
    delete m_recMdcKalTrackCol;
    m_recMdcKalTrackCol = nullptr;

    m_recMdcKalHelixSegCol->Delete();
    delete m_recMdcKalHelixSegCol;
    m_recMdcKalHelixSegCol = nullptr;

    m_recEvTimeCol->Delete();
    delete m_recEvTimeCol;
    m_recEvTimeCol = nullptr;

    m_recZddChannelCol->Delete();
    delete m_recZddChannelCol;
    m_recZddChannelCol = nullptr;
}

//*****************************************************************
void TRecTrackEvent::initialize() {}

//*****************************************************************
void TRecTrackEvent::Clear( Option_t* option ) {}

//*****************************************************************************
void TRecTrackEvent::Print( Option_t* option ) const { TObject::Print( option ); }

/****************     Dst Track     ************************/
/// Mdc
void TRecTrackEvent::addRecMdcTrack( TRecMdcTrack* Track ) { m_recMdcTrackCol->Add( Track ); }

const TRecMdcTrack* TRecTrackEvent::getRecMdcTrack( Int_t i ) const {
    if ( Int_t( i ) >= m_recMdcTrackCol->GetEntries() ) return 0;
    return (TRecMdcTrack*)m_recMdcTrackCol->At( i );
}

void TRecTrackEvent::addRecMdcHit( TRecMdcHit* Hit ) { m_recMdcHitCol->Add( Hit ); }

const TRecMdcHit* TRecTrackEvent::getRecMdcHit( Int_t i ) const {
    if ( Int_t( i ) >= m_recMdcHitCol->GetEntries() ) return 0;
    return (TRecMdcHit*)m_recMdcHitCol->At( i );
}

/// Tof
void TRecTrackEvent::addTofTrack( TRecTofTrack* Track ) { m_recTofTrackCol->Add( Track ); }

const TRecTofTrack* TRecTrackEvent::getTofTrack( Int_t i ) const {
    if ( Int_t( i ) >= m_recTofTrackCol->GetEntries() ) return 0;
    return (TRecTofTrack*)m_recTofTrackCol->At( i );
}

/// Emc
void TRecTrackEvent::addEmcHit( TRecEmcHit* Track ) { m_recEmcHitCol->Add( Track ); }

const TRecEmcHit* TRecTrackEvent::getEmcHit( Int_t i ) const {
    if ( Int_t( i ) >= m_recEmcHitCol->GetEntries() ) return 0;
    return (TRecEmcHit*)m_recEmcHitCol->At( i );
}

void TRecTrackEvent::addEmcCluster( TRecEmcCluster* Track ) {
    m_recEmcClusterCol->Add( Track );
}

const TRecEmcCluster* TRecTrackEvent::getEmcCluster( Int_t i ) const {
    if ( Int_t( i ) >= m_recEmcClusterCol->GetEntries() ) return 0;
    return (TRecEmcCluster*)m_recEmcClusterCol->At( i );
}

void TRecTrackEvent::addEmcShower( TRecEmcShower* Track ) { m_recEmcShowerCol->Add( Track ); }

const TRecEmcShower* TRecTrackEvent::getEmcShower( Int_t i ) const {
    if ( Int_t( i ) >= m_recEmcShowerCol->GetEntries() ) return 0;
    return (TRecEmcShower*)m_recEmcShowerCol->At( i );
}

/// Muc
void TRecTrackEvent::addMucTrack( TRecMucTrack* Track ) { m_recMucTrackCol->Add( Track ); }

const TRecMucTrack* TRecTrackEvent::getMucTrack( Int_t i ) const {
    if ( Int_t( i ) >= m_recMucTrackCol->GetEntries() ) return 0;
    return (TRecMucTrack*)m_recMucTrackCol->At( i );
}

/// Dedx
void TRecTrackEvent::addRecMdcDedx( TRecMdcDedx* Track ) { m_recMdcDedxCol->Add( Track ); }

const TRecMdcDedx* TRecTrackEvent::getRecMdcDedx( Int_t i ) const {
    if ( Int_t( i ) >= m_recMdcDedxCol->GetEntries() ) return 0;
    return (TRecMdcDedx*)m_recMdcDedxCol->At( i );
}

void TRecTrackEvent::addRecMdcDedxHit( TRecMdcDedxHit* Track ) {
    m_recMdcDedxHitCol->Add( Track );
}

const TRecMdcDedxHit* TRecTrackEvent::getRecMdcDedxHit( Int_t i ) const {
    if ( Int_t( i ) >= m_recMdcDedxHitCol->GetEntries() ) return 0;
    return (TRecMdcDedxHit*)m_recMdcDedxHitCol->At( i );
}

// // Ext
void TRecTrackEvent::addExtTrack( TRecExtTrack* Track ) { m_recExtTrackCol->Add( Track ); }

const TRecExtTrack* TRecTrackEvent::getExtTrack( Int_t i ) const {
    if ( Int_t( i ) >= m_recExtTrackCol->GetEntries() ) return 0;
    return (TRecExtTrack*)m_recExtTrackCol->At( i );
}

// RecMdcKal
void TRecTrackEvent::addRecMdcKalTrack( TRecMdcKalTrack* Track ) {
    m_recMdcKalTrackCol->Add( Track );
}

const TRecMdcKalTrack* TRecTrackEvent::getRecMdcKalTrack( Int_t i ) const {
    if ( Int_t( i ) >= m_recMdcKalTrackCol->GetEntries() ) return 0;
    return (TRecMdcKalTrack*)m_recMdcKalTrackCol->At( i );
}

void TRecTrackEvent::addRecMdcKalHelixSeg( TRecMdcKalHelixSeg* Track ) {
    m_recMdcKalHelixSegCol->Add( Track );
}

const TRecMdcKalHelixSeg* TRecTrackEvent::getRecMdcKalHelixSeg( Int_t i ) const {
    if ( Int_t( i ) >= m_recMdcKalHelixSegCol->GetEntries() ) return 0;
    return (TRecMdcKalHelixSeg*)m_recMdcKalHelixSegCol->At( i );
}

// EsTime
void TRecTrackEvent::addEvTime( TRecEvTime* Track ) { m_recEvTimeCol->Add( Track ); }

const TRecEvTime* TRecTrackEvent::getEvTime( Int_t i ) const {
    if ( Int_t( i ) >= m_recEvTimeCol->GetEntries() ) return 0;
    return (TRecEvTime*)m_recEvTimeCol->At( i );
}

// ZDD
void TRecTrackEvent::addRecZddChannel( TRecZddChannel* zdd ) {
    m_recZddChannelCol->Add( zdd );
}

const TRecZddChannel* TRecTrackEvent::getRecZddChannel( Int_t i ) const {
    if ( i >= m_recZddChannelCol->GetEntries() || i < 0 ) return 0;
    return (TRecZddChannel*)m_recZddChannelCol->At( i );
}
