#include "RootEventData/TMcEvent.h"

ClassImp( TMcEvent );

// TObject *TMcEvent::s_staticDecayMode = 0;

//***************************************************************
TMcEvent::TMcEvent() {
    m_mdcMcHitCol   = new TObjArray();
    m_emcMcHitCol   = new TObjArray();
    m_tofMcHitCol   = new TObjArray();
    m_mucMcHitCol   = new TObjArray();
    m_mcParticleCol = new TObjArray();

    Clear();
}

//*****************************************************************
TMcEvent::~TMcEvent() {
    m_mdcMcHitCol->Delete();
    delete m_mdcMcHitCol;
    m_mdcMcHitCol = nullptr;

    m_emcMcHitCol->Delete();
    delete m_emcMcHitCol;
    m_emcMcHitCol = nullptr;

    m_tofMcHitCol->Delete();
    delete m_tofMcHitCol;
    m_tofMcHitCol = nullptr;

    m_mucMcHitCol->Delete();
    delete m_mucMcHitCol;
    m_mucMcHitCol = nullptr;

    m_mcParticleCol->Delete();
    delete m_mcParticleCol;
    m_mcParticleCol = nullptr;
}

//*****************************************************************
void TMcEvent::initialize() {}

//*****************************************************************
void TMcEvent::Clear( Option_t* option ) {}

//*****************************************************************************
void TMcEvent::Print( Option_t* option ) const { TObject::Print( option ); }

/// Mdc
void TMcEvent::addMdcMc( TMdcMc* mcHit ) { m_mdcMcHitCol->Add( mcHit ); }

const TMdcMc* TMcEvent::getMdcMc( Int_t i ) const {
    if ( Int_t( i ) >= m_mdcMcHitCol->GetEntries() ) return 0;
    return (TMdcMc*)m_mdcMcHitCol->At( i );
}
/// Emc
void TMcEvent::addEmcMc( TEmcMc* mcHit ) { m_emcMcHitCol->Add( mcHit ); }

const TEmcMc* TMcEvent::getEmcMc( Int_t i ) const {
    if ( Int_t( i ) >= m_emcMcHitCol->GetEntries() ) return 0;
    return (TEmcMc*)m_emcMcHitCol->At( i );
}

/// Tof
void TMcEvent::addTofMc( TTofMc* mcHit ) { m_tofMcHitCol->Add( mcHit ); }

const TTofMc* TMcEvent::getTofMc( Int_t i ) const {
    if ( Int_t( i ) >= m_tofMcHitCol->GetEntries() ) return 0;
    return (TTofMc*)m_tofMcHitCol->At( i );
}

/// Muc
void TMcEvent::addMucMc( TMucMc* mcHit ) { m_mucMcHitCol->Add( mcHit ); }

const TMucMc* TMcEvent::getMucMc( Int_t i ) const {
    if ( Int_t( i ) >= m_mucMcHitCol->GetEntries() ) return 0;
    return (TMucMc*)m_mucMcHitCol->At( i );
}

/// McParticle
void TMcEvent::addMcParticle( TMcParticle* mcHit ) { m_mcParticleCol->Add( mcHit ); }

const TMcParticle* TMcEvent::getMcParticle( Int_t i ) const {
    if ( Int_t( i ) >= m_mcParticleCol->GetEntries() ) return 0;
    return (TMcParticle*)m_mcParticleCol->At( i );
}