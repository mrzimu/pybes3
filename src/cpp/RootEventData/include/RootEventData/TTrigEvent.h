#ifndef ROOT_TTrigEvent_H
#define ROOT_TTrigEvent_H

#include "TObject.h"

#include "TTrigData.h"

class TTrigEvent : public TObject {
  public:
    TTrigEvent();
    virtual ~TTrigEvent();

    // o void initialize( Bool_t fromMc=true);
    void initialize() {};

    void Clear( Option_t* option = "" );

    void Print( Option_t* option = "" ) const;

    // o inline Bool_t getFromMc() { return m_fromMc; };

    // TrigData
    void addTrigData( TTrigData* trigData );
    const TTrigData* getTrigData() const;
    void clearTrigData() { m_trigData->Clear(); }

  private:
    /// Denote whether or not this data was simulated
    // o Bool_t m_fromMc;

    /// data members to store trigger data
    TTrigData* m_trigData; //->

    ClassDef( TTrigEvent, 1 ) // Storage for trigger event and subsystem data
};

#endif
