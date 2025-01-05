#ifndef ROOT_THltEvent_H
#define ROOT_THltEvent_H

#include "TClonesArray.h"
#include "TObjArray.h"
#include "TObject.h"

#include "TDstHltInf.h"
#include "THltInf.h"
#include "THltRaw.h"

class THltEvent : public TObject {
  public:
    THltEvent();
    virtual ~THltEvent();

    // o void initialize( Bool_t fromMc=true);
    void initialize() {};

    void Clear( Option_t* option = "" );

    void Print( Option_t* option = "" ) const;

    // o inline Bool_t getFromMc() { return m_fromMc; };

    // HltData
    void addHltRaw( THltRaw* hltRaw );
    const THltRaw* getHltRaw( int i ) const;
    const TObjArray* getHltRawCol() const;
    void clearHltRawCol() { m_hltRawCol->Clear(); }

    void addHltInf( THltInf* hltInf );
    const THltInf* getHltInf() const;
    void clearHltInf() { m_hltInf->Clear(); }

    void addDstHltInf( TDstHltInf* dstHltInf );
    const TDstHltInf* getDstHltInf() const;
    void clearDstHltInf() { m_dstHltInf->Clear(); }

  private:
    /// Denote whether or not this data was simulated
    // o Bool_t m_fromMc;

    /// data members to store trigger data
    TObjArray* m_hltRawCol; //->

    THltInf* m_hltInf; //->

    TDstHltInf* m_dstHltInf; //->

    ClassDef( THltEvent, 3 ) // Storage for event filter and subsystem data
};

#endif
