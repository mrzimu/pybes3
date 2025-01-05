#include "RootEventData/THltEvent.h"

ClassImp( THltEvent );

//***************************************************************
THltEvent::THltEvent() {
    m_hltRawCol = new TObjArray();
    m_hltInf    = new THltInf();
    m_dstHltInf = new TDstHltInf();
    Clear();
}

//*****************************************************************
THltEvent::~THltEvent() {

    m_hltRawCol->Delete();
    delete m_hltRawCol;
    m_hltRawCol = nullptr;

    delete m_hltInf;
    m_hltInf = nullptr;

    delete m_dstHltInf;
    m_dstHltInf = nullptr;
}

//*****************************************************************
// o void THltEvent::initialize(Bool_t fromMc){
// o     m_fromMc = fromMc;
// o }

//*****************************************************************
void THltEvent::Clear( Option_t* option ) {}

//*****************************************************************************
void THltEvent::Print( Option_t* option ) const { TObject::Print( option ); }

/// HltRaw
void THltEvent::addHltRaw( THltRaw* hltRaw ) { m_hltRawCol->Add( hltRaw ); }
const THltRaw* THltEvent::getHltRaw( Int_t i ) const {
    if ( Int_t( i ) >= m_hltRawCol->GetEntries() ) return 0;
    return (THltRaw*)m_hltRawCol->At( i );
}
const TObjArray* THltEvent::getHltRawCol() const { return (TObjArray*)m_hltRawCol; }
void THltEvent::addHltInf( THltInf* hltInf ) { m_hltInf = hltInf; }
const THltInf* THltEvent::getHltInf() const { return (THltInf*)m_hltInf; }
void THltEvent::addDstHltInf( TDstHltInf* hltInf ) { m_dstHltInf = hltInf; }
const TDstHltInf* THltEvent::getDstHltInf() const { return (TDstHltInf*)m_dstHltInf; }
