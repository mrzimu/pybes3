#include "RootEventData/TEvtRecObject.h"

ClassImp( TEvtRecObject );

TEvtRecObject::TEvtRecObject() {
    m_evtRecEvent         = new TEvtRecEvent;
    m_evtRecTrackCol      = new TObjArray();
    m_evtRecPrimaryVertex = new TEvtRecPrimaryVertex();
    m_evtRecVeeVertexCol  = new TObjArray();
    m_evtRecPi0Col        = new TObjArray();
    m_evtRecEtaToGGCol    = new TObjArray();
    m_evtRecDTagCol       = new TObjArray();
    Clear();
}

TEvtRecObject::~TEvtRecObject() {
    delete m_evtRecEvent;
    m_evtRecEvent = nullptr;

    m_evtRecTrackCol->Delete();
    delete m_evtRecTrackCol;
    m_evtRecTrackCol = nullptr;

    delete m_evtRecPrimaryVertex;
    m_evtRecPrimaryVertex = nullptr;

    m_evtRecVeeVertexCol->Delete();
    delete m_evtRecVeeVertexCol;
    m_evtRecVeeVertexCol = nullptr;

    m_evtRecPi0Col->Delete();
    delete m_evtRecPi0Col;
    m_evtRecPi0Col = nullptr;

    m_evtRecEtaToGGCol->Delete();
    delete m_evtRecEtaToGGCol;
    m_evtRecEtaToGGCol = nullptr;

    m_evtRecDTagCol->Delete();
    delete m_evtRecDTagCol;
    m_evtRecDTagCol = nullptr;
}

void TEvtRecObject::initialize() {}

void TEvtRecObject::Clear( Option_t* option ) {}

void TEvtRecObject::Print( Option_t* option ) const { TObject::Print( option ); }

void TEvtRecObject::setEvtRecEvent( TEvtRecEvent* evtRecEvent ) {
    m_evtRecEvent->setTotalTracks( evtRecEvent->totalTracks() );
    m_evtRecEvent->setTotalCharged( evtRecEvent->totalCharged() );
    m_evtRecEvent->setTotalNeutral( evtRecEvent->totalNeutral() );
    m_evtRecEvent->setNumberOfVee( evtRecEvent->numberOfVee() );
    m_evtRecEvent->setNumberOfPi0( evtRecEvent->numberOfPi0() );
    m_evtRecEvent->setNumberOfEtaToGG( evtRecEvent->numberOfEtaToGG() );
    m_evtRecEvent->setNumberOfDTag( evtRecEvent->numberOfDTag() );
}

void TEvtRecObject::addEvtRecTrack( TEvtRecTrack* track ) { m_evtRecTrackCol->Add( track ); }

const TEvtRecTrack* TEvtRecObject::getEvtRecTrack( Int_t i ) const {
    if ( i >= m_evtRecTrackCol->GetEntries() || i < 0 ) return 0;
    return (TEvtRecTrack*)m_evtRecTrackCol->At( i );
}

void TEvtRecObject::setEvtRecPrimaryVertex( TEvtRecPrimaryVertex* evtRecPrimaryVertex ) {
    m_evtRecPrimaryVertex->setIsValid( evtRecPrimaryVertex->isValid() );
    m_evtRecPrimaryVertex->setNTracks( evtRecPrimaryVertex->nTracks() );
    m_evtRecPrimaryVertex->setTrackIdList( evtRecPrimaryVertex->trackIdList() );
    m_evtRecPrimaryVertex->setChi2( evtRecPrimaryVertex->chi2() );
    m_evtRecPrimaryVertex->setNdof( evtRecPrimaryVertex->ndof() );
    m_evtRecPrimaryVertex->setFitMethod( evtRecPrimaryVertex->fitMethod() );
    Double_t vtx[3];
    for ( Int_t i = 0; i < 3; i++ ) { vtx[i] = evtRecPrimaryVertex->vertex( i ); }
    Double_t Evtx[6];
    for ( Int_t i = 0; i < 6; i++ ) { Evtx[i] = evtRecPrimaryVertex->errorVertex( i ); }
    m_evtRecPrimaryVertex->setVertex( vtx );
    m_evtRecPrimaryVertex->setErrorVertex( Evtx );
}

void TEvtRecObject::addEvtRecVeeVertex( TEvtRecVeeVertex* veeVertex ) {
    m_evtRecVeeVertexCol->Add( veeVertex );
}

void TEvtRecObject::addEvtRecPi0( TEvtRecPi0* pi0 ) { m_evtRecPi0Col->Add( pi0 ); }

void TEvtRecObject::addEvtRecEtaToGG( TEvtRecEtaToGG* eta ) { m_evtRecEtaToGGCol->Add( eta ); }

void TEvtRecObject::addEvtRecDTag( TEvtRecDTag* dtag ) { m_evtRecDTagCol->Add( dtag ); }

const TEvtRecVeeVertex* TEvtRecObject::getEvtRecVeeVertex( Int_t i ) const {
    if ( i >= m_evtRecVeeVertexCol->GetEntries() || i < 0 ) return 0;
    return (TEvtRecVeeVertex*)m_evtRecVeeVertexCol->At( i );
}

const TEvtRecPi0* TEvtRecObject::getEvtRecPi0( Int_t i ) const {
    if ( i >= m_evtRecPi0Col->GetEntries() || i < 0 ) return 0;
    return (TEvtRecPi0*)m_evtRecPi0Col->At( i );
}

const TEvtRecEtaToGG* TEvtRecObject::getEvtRecEtaToGG( Int_t i ) const {
    if ( i >= m_evtRecEtaToGGCol->GetEntries() || i < 0 ) return 0;
    return (TEvtRecEtaToGG*)m_evtRecEtaToGGCol->At( i );
}

const TEvtRecDTag* TEvtRecObject::getEvtRecDTag( Int_t i ) const {
    if ( i >= m_evtRecDTagCol->GetEntries() || i < 0 ) return 0;
    return (TEvtRecDTag*)m_evtRecDTagCol->At( i );
}
