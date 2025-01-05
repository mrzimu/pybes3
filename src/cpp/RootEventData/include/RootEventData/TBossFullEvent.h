#ifndef ROOT_TBossFullEvent_H
#define ROOT_TBossFullEvent_H

#include "TDigiEvent.h"
#include "TDstEvent.h"
#include "TEvtHeader.h"
#include "TEvtRecObject.h"
#include "THltEvent.h"
#include "TMcEvent.h"
#include "TObject.h"
#include "TRecTrackEvent.h"
#include "TTrigEvent.h"

class TBossFullEvent : public TObject {
  public:
    TBossFullEvent();
    virtual ~TBossFullEvent();

    void Print( Option_t* option = "" ) const;

    void copy( TBossFullEvent* obj );

    void reset() { m_mask = 0; }

    void setEvtHeader( TEvtHeader* obj ) {
        if ( obj != 0 )
        {
            m_mask |= hasEvtHeader;
            m_EvtHeader = obj;
        }
    }

    void setDigiEvent( TDigiEvent* obj ) {
        if ( obj != 0 )
        {
            m_mask |= hasDigiEvent;
            m_digiEvt = obj;
        }
    }

    void setDstEvent( TDstEvent* obj ) {
        if ( obj != 0 )
        {
            m_mask |= hasDstEvent;
            m_dstEvt = obj;
        }
    }

    void setMcEvent( TMcEvent* obj ) {
        if ( obj != 0 )
        {
            m_mask |= hasMcEvent;
            m_mcEvt = obj;
        }
    }

    void setTrigEvent( TTrigEvent* obj ) {
        if ( obj != 0 )
        {
            m_mask |= hasTrigEvent;
            m_trigEvt = obj;
        }
    }

    void setHltEvent( THltEvent* obj ) {
        if ( obj != 0 )
        {
            m_mask |= hasHltEvent;
            m_hltEvt = obj;
        }
    }

    void setRecTrackEvent( TRecTrackEvent* obj ) {
        if ( obj != 0 )
        {
            m_mask |= hasRecTrackEvent;
            m_rectrackEvt = obj;
        }
    }

    void setEvtRecObject( TEvtRecObject* obj ) {
        if ( obj != 0 )
        {
            m_mask |= hasEvtRecObject;
            m_evtRecObject = obj;
        }
    }

    TEvtHeader* getEvtHeader() { return m_EvtHeader; }
    TDigiEvent* getDigiEvent() { return m_digiEvt; }
    TDstEvent* getDstEvent() { return m_dstEvt; }
    TMcEvent* getMcEvent() { return m_mcEvt; }
    TTrigEvent* getTrigEvent() { return m_trigEvt; }
    THltEvent* getHltEvent() { return m_hltEvt; }
    TRecTrackEvent* getRecTrackEvent() { return m_rectrackEvt; }
    TEvtRecObject* getEvtRecObject() { return m_evtRecObject; }

  private:
    enum {
        hasEvtHeader     = 1 << 0,
        hasDigiEvent     = 1 << 1,
        hasDstEvent      = 1 << 2,
        hasMcEvent       = 1 << 3,
        hasTrigEvent     = 1 << 4,
        hasHltEvent      = 1 << 5,
        hasRecTrackEvent = 1 << 6,
        hasEvtRecObject  = 1 << 7
    };

    UInt_t m_mask;

  public:
    TEvtHeader* m_EvtHeader;       //->
    TDigiEvent* m_digiEvt;         //->
    TDstEvent* m_dstEvt;           //->
    TMcEvent* m_mcEvt;             //->
    TTrigEvent* m_trigEvt;         //->
    THltEvent* m_hltEvt;           //->
    TRecTrackEvent* m_rectrackEvt; //->
    TEvtRecObject* m_evtRecObject; //->

  private:
    ClassDef( TBossFullEvent, 1 )
};

#endif
