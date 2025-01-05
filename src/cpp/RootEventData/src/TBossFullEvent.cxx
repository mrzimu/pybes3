#include "RootEventData/TBossFullEvent.h"
#include "TBuffer.h"
#include "TClass.h"
#include <iostream>

ClassImp( TBossFullEvent );
;

TBossFullEvent::TBossFullEvent()
    : m_mask( 0 )
    , m_EvtHeader( 0 )
    , m_digiEvt( 0 )
    , m_dstEvt( 0 )
    , m_mcEvt( 0 )
    , m_trigEvt( 0 )
    , m_hltEvt( 0 )
    , m_rectrackEvt( 0 )
    , m_evtRecObject( 0 ) {}

#define SafeDeleteObject( ObjType, var )                                                      \
    if ( m_mask & has##ObjType ) { delete var; }

TBossFullEvent::~TBossFullEvent() {
    SafeDeleteObject( EvtHeader, m_EvtHeader );
    SafeDeleteObject( DigiEvent, m_digiEvt );
    SafeDeleteObject( DstEvent, m_dstEvt );
    SafeDeleteObject( McEvent, m_mcEvt );
    SafeDeleteObject( TrigEvent, m_trigEvt );
    SafeDeleteObject( HltEvent, m_hltEvt );
    SafeDeleteObject( RecTrackEvent, m_rectrackEvt );
    SafeDeleteObject( EvtRecObject, m_evtRecObject );
}

#define SafePrintObject( ObjType, var )                                                       \
    if ( m_mask & has##ObjType ) { var->Print(); }

void TBossFullEvent::Print( Option_t* option ) const {
    std::cout << "=============================================" << std::endl
              << "TBossFullEvent mask: 0x" << std::hex << m_mask << std::dec << std::endl
              << "---------------------------------------------" << std::endl;

    SafePrintObject( EvtHeader, m_EvtHeader );
    SafePrintObject( DigiEvent, m_digiEvt );
    SafePrintObject( DstEvent, m_dstEvt );
    SafePrintObject( McEvent, m_mcEvt );
    SafePrintObject( TrigEvent, m_trigEvt );
    SafePrintObject( HltEvent, m_hltEvt );
    SafePrintObject( RecTrackEvent, m_rectrackEvt );
    SafePrintObject( EvtRecObject, m_evtRecObject );

    std::cout << "=============================================" << std::endl;
}

void TBossFullEvent::copy( TBossFullEvent* obj ) {
    m_mask         = obj->m_mask;
    m_EvtHeader    = obj->m_EvtHeader;
    m_digiEvt      = obj->m_digiEvt;
    m_dstEvt       = obj->m_dstEvt;
    m_mcEvt        = obj->m_mcEvt;
    m_trigEvt      = obj->m_trigEvt;
    m_hltEvt       = obj->m_hltEvt;
    m_rectrackEvt  = obj->m_rectrackEvt;
    m_evtRecObject = obj->m_evtRecObject;
}

#define SafeReadObject( ObjType, var )                                                        \
    if ( m_mask & has##ObjType ) { var = (T##ObjType*)R__b.ReadObject( T##ObjType::Class() ); }

#define SafeWriteObject( ObjType, var )                                                       \
    if ( m_mask & has##ObjType ) { R__b.WriteObject( var ); }

void TBossFullEvent::Streamer( TBuffer& R__b ) {
    if ( R__b.IsReading() )
    {
        R__b >> m_mask;
        SafeReadObject( EvtHeader, m_EvtHeader );
        SafeReadObject( DigiEvent, m_digiEvt );
        SafeReadObject( DstEvent, m_dstEvt );
        SafeReadObject( McEvent, m_mcEvt );
        SafeReadObject( TrigEvent, m_trigEvt );
        SafeReadObject( HltEvent, m_hltEvt );
        SafeReadObject( RecTrackEvent, m_rectrackEvt );
        SafeReadObject( EvtRecObject, m_evtRecObject );
    }
    else
    {
        R__b << m_mask;
        SafeWriteObject( EvtHeader, m_EvtHeader );
        SafeWriteObject( DigiEvent, m_digiEvt );
        SafeWriteObject( DstEvent, m_dstEvt );
        SafeWriteObject( McEvent, m_mcEvt );
        SafeWriteObject( TrigEvent, m_trigEvt );
        SafeWriteObject( HltEvent, m_hltEvt );
        SafeWriteObject( RecTrackEvent, m_rectrackEvt );
        SafeWriteObject( EvtRecObject, m_evtRecObject );
    }
}
