#include "RootEventData/TDisTrack.h"
#include "TCollection.h" // Declares TIter
#include <iostream>

ClassImp( TDisTrack );

// Allocate the TObjArray just once

//***************************************************************
TDisTrack::TDisTrack() {
    // Dst Track
    // Rec Track
    //  if (!m_recMdcTrackCol) {

    m_recMdcTrackCol = new TObjArray();
    //   }
    m_recMdcHitCol    = new TObjArray();
    m_recTofTrackCol  = new TObjArray();
    m_recMucTrackCol  = new TObjArray();
    m_recEmcShowerCol = new TObjArray();
    /*    m_recTofTrackCol = s_staticTofTrackCol;


        Clear();*/
}

//*****************************************************************
TDisTrack::~TDisTrack() {

    /****************************    Dst Track *************************/

    //  delete m_recMdcTrackCol;
    if ( m_recMdcTrackCol )
    { // m_recMdcTrackCol->Clear();
        m_recMdcTrackCol->Delete();
        delete m_recMdcTrackCol;
    }
    m_recMdcTrackCol = 0;

    if ( m_recMdcHitCol )
    { // m_recMdcHitCol->Clear();
        m_recMdcHitCol->Delete();
        delete m_recMdcHitCol;
    }
    m_recMdcHitCol = 0;

    if ( m_recTofTrackCol )
    { // m_recTofTrackCol->Clear();
        m_recTofTrackCol->Delete();
        delete m_recTofTrackCol;
    }
    m_recTofTrackCol = 0;

    if ( m_recMucTrackCol )
    { // m_recMucTrackCol->Clear();
        m_recMucTrackCol->Delete();
        delete m_recMucTrackCol;
    }
    m_recMucTrackCol = 0;

    if ( m_recEmcShowerCol )
    { // m_recEmcShowerCol->Clear();
        m_recEmcShowerCol->Delete();
        delete m_recEmcShowerCol;
    }
    m_recEmcShowerCol = 0;
}

//*****************************************************************
void TDisTrack::initialize() {}

//*****************************************************************
void TDisTrack::Clear( Option_t* option ) {
    if ( m_recMdcTrackCol )
    { // m_recMdcTrackCol->Clear();
        std::cout << "step1" << std::endl;
        // m_recMdcTrackCol->Delete();
        delete m_recMdcTrackCol;
    }
    m_recMdcTrackCol = 0;

    if ( m_recMdcHitCol )
    { // m_recMdcHitCol->Clear();
        std::cout << "step2" << std::endl;
        //    m_recMdcHitCol->Delete();
        delete m_recMdcHitCol;
    }
    m_recMdcHitCol = 0;

    if ( m_recTofTrackCol )
    { // m_recTofTrackCol->Clear();
        std::cout << "step3" << std::endl;
        // m_recTofTrackCol->Delete();
        delete m_recTofTrackCol;
    }
    m_recTofTrackCol = 0;

    if ( m_recMucTrackCol )
    { // m_recMucTrackCol->Clear();
        std::cout << "step4" << std::endl;
        //;  m_recMucTrackCol->Delete();
        delete m_recMucTrackCol;
    }
    m_recMucTrackCol = 0;

    if ( m_recEmcShowerCol )
    { // m_recEmcShowerCol->Clear();
        std::cout << "step5" << std::endl;
        //   m_recEmcShowerCol->Delete();
        delete m_recEmcShowerCol;
    }
    m_recEmcShowerCol = 0;
}

//*****************************************************************************
void TDisTrack::Print( Option_t* option ) const { TObject::Print( option ); }

/****************     Dst Track     ************************/
/// Mdc
void TDisTrack::addRecMdcTrack( TRecMdcTrack* Track ) { m_recMdcTrackCol->Add( Track ); }

const TRecMdcTrack* TDisTrack::getRecMdcTrack( Int_t i ) const {
    if ( Int_t( i ) >= m_recMdcTrackCol->GetEntries() ) return 0;
    return (TRecMdcTrack*)m_recMdcTrackCol->At( i );
}

// MdcHits
void TDisTrack::addRecMdcHit( TRecMdcHit* Hit ) { m_recMdcHitCol->Add( Hit ); }

const TRecMdcHit* TDisTrack::getRecMdcHit( Int_t i ) const {
    if ( Int_t( i ) >= m_recMdcHitCol->GetEntries() ) return 0;
    return (TRecMdcHit*)m_recMdcHitCol->At( i );
}

// TOF
void TDisTrack::addTofTrack( TRecTofTrack* Track ) { m_recTofTrackCol->Add( Track ); }
const TRecTofTrack* TDisTrack::getTofTrack( Int_t i ) const {
    if ( Int_t( i ) >= m_recTofTrackCol->GetEntries() ) return 0;
    return (TRecTofTrack*)m_recTofTrackCol->At( i );
}

/// Muc
void TDisTrack::addMucTrack( TRecMucTrack* Track ) { m_recMucTrackCol->Add( Track ); }

const TRecMucTrack* TDisTrack::getMucTrack( Int_t i ) const {
    if ( Int_t( i ) >= m_recMucTrackCol->GetEntries() ) return 0;
    return (TRecMucTrack*)m_recMucTrackCol->At( i );
}

// EmcShowers
void TDisTrack::addEmcShower( TRecEmcShower* Track ) { m_recEmcShowerCol->Add( Track ); }

/// retrieve a EmcShower from the collection, using the index into the array
const TRecEmcShower* TDisTrack::getEmcShower( Int_t i ) const {
    if ( Int_t( i ) >= m_recEmcShowerCol->GetEntries() ) return 0;
    return (TRecEmcShower*)m_recEmcShowerCol->At( i );
}

int TDisTrack::getMdcTrackNum() {
    std::cout << "getMdcTrackNum step1" << std::endl;
    if ( m_recMdcTrackCol )
    {
        std::cout << "getMdcTrackNum step2" << std::endl;
        return m_recMdcTrackCol->GetEntries();
    }
    std::cout << "getMdcTrackNum step3" << std::endl;
    return 0;
}

int TDisTrack::getTofTrackNum() {
    std::cout << "getTofTrackNum step1" << std::endl;
    if ( m_recTofTrackCol )
    {
        std::cout << "getTofTrackNum step2" << std::endl;
        return m_recTofTrackCol->GetEntries();
    }
    std::cout << "getTofTrackNum step3" << std::endl;
    return 0;
}

int TDisTrack::getEmcShowerNum() {
    std::cout << "getEmcShowerNum step1" << std::endl;
    if ( m_recEmcShowerCol )
    {
        std::cout << "getEmcShowerNum step2" << std::endl;
        return m_recEmcShowerCol->GetEntries();
    }
    std::cout << "getEmcShowerNum step3" << std::endl;
    return 0;
}

int TDisTrack::getMucTrackNum() {
    std::cout << "getMucTrackNum step1" << std::endl;
    if ( m_recMucTrackCol )
    {
        std::cout << "getMucTrackNum step2" << std::endl;
        return m_recMucTrackCol->GetEntries();
    }
    std::cout << "getMucTrackNum step3" << std::endl;
    return 0;
}

int TDisTrack::getMdcHitNum() {
    std::cout << "getMdcHitkNum step1" << std::endl;
    if ( m_recMdcHitCol )
    {
        std::cout << "getMdcHitkNum step2" << std::endl;
        return m_recMdcHitCol->GetEntries();
    }
    std::cout << "getMdcHitkNum step3" << std::endl;
    return 0;
}
