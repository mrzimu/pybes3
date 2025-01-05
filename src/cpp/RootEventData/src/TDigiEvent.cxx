#include "RootEventData/TDigiEvent.h"
#include <iostream>

ClassImp( TDigiEvent );

//***************************************************************
TDigiEvent::TDigiEvent() {
    m_mdcDigiCol  = new TObjArray();
    m_emcDigiCol  = new TObjArray();
    m_tofDigiCol  = new TObjArray();
    m_mucDigiCol  = new TObjArray();
    m_lumiDigiCol = new TObjArray();
    Clear();
}

//*****************************************************************
TDigiEvent::~TDigiEvent() {
    m_mdcDigiCol->Delete();
    delete m_mdcDigiCol;
    m_mdcDigiCol = nullptr;

    m_emcDigiCol->Delete();
    delete m_emcDigiCol;
    m_emcDigiCol = nullptr;

    m_tofDigiCol->Delete();
    delete m_tofDigiCol;
    m_tofDigiCol = nullptr;

    m_mucDigiCol->Delete();
    delete m_mucDigiCol;
    m_mucDigiCol = nullptr;

    m_lumiDigiCol->Delete();
    delete m_lumiDigiCol;
    m_lumiDigiCol = nullptr;
}

//*****************************************************************
void TDigiEvent::initialize( Bool_t fromMc ) { m_fromMc = fromMc; }

//*****************************************************************
void TDigiEvent::Clear( Option_t* option ) {}

//*****************************************************************************
void TDigiEvent::Print( Option_t* option ) const {
    TObject::Print( option );
    std::cout.precision( 2 );
    if ( m_mdcDigiCol )
        std::cout << "Number of TMdcDigis " << m_mdcDigiCol->GetEntries() << std::endl;
    else std::cout << "Number of TMdcDigis 0" << std::endl;
}

/// Mdc
void TDigiEvent::addMdcDigi( TMdcDigi* digi ) { m_mdcDigiCol->Add( digi ); }

const TMdcDigi* TDigiEvent::getMdcDigi( Int_t i ) const {
    if ( Int_t( i ) >= m_mdcDigiCol->GetEntries() ) return 0;
    return (TMdcDigi*)m_mdcDigiCol->At( i );
}
/// Emc
void TDigiEvent::addEmcDigi( TEmcDigi* digi ) { m_emcDigiCol->Add( digi ); }

const TEmcDigi* TDigiEvent::getEmcDigi( Int_t i ) const {
    if ( Int_t( i ) >= m_emcDigiCol->GetEntries() ) return 0;
    return (TEmcDigi*)m_emcDigiCol->At( i );
}

/// Tof
void TDigiEvent::addTofDigi( TTofDigi* digi ) { m_tofDigiCol->Add( digi ); }

const TTofDigi* TDigiEvent::getTofDigi( Int_t i ) const {
    if ( Int_t( i ) >= m_tofDigiCol->GetEntries() ) return 0;
    return (TTofDigi*)m_tofDigiCol->At( i );
}

/// Muc
void TDigiEvent::addMucDigi( TMucDigi* digi ) { m_mucDigiCol->Add( digi ); }

const TMucDigi* TDigiEvent::getMucDigi( Int_t i ) const {
    if ( Int_t( i ) >= m_mucDigiCol->GetEntries() ) return 0;
    return (TMucDigi*)m_mucDigiCol->At( i );
}

/// Lumi
void TDigiEvent::addLumiDigi( TLumiDigi* digi ) { m_lumiDigiCol->Add( digi ); }

const TLumiDigi* TDigiEvent::getLumiDigi( Int_t i ) const {
    if ( i >= m_lumiDigiCol->GetEntries() ) return 0;
    return (TLumiDigi*)m_lumiDigiCol->At( i );
}
