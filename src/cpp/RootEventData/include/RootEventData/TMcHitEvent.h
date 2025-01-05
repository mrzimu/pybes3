#ifndef TMcHitEvent_H
#define TMcHitEvent_H

#include "TClonesArray.h"
#include "TObjArray.h"
#include "TObject.h"

#include "TMcDigiEmc.h"
#include "TMcHitMdc.h"
#include "TMcHitTof.h"

class TMcHitEvent : public TObject {
  public:
    TMcHitEvent();
    virtual ~TMcHitEvent();

    void Clear( Option_t* option = "" );

    void Print( Option_t* option = "" ) const;

    /// retrieve the whole TObjArray  of McHitTof Data
    const TObjArray* getMcHitTofCol() const { return m_tTofMcHitCol; };

    /// Add a McHitTof into the TOF Data collection
    void addMcHitTof( TMcHitTof* hit );

    /// retrieve a McHitTof From the collection, using the index into the array
    const TMcHitTof* getMcHitTof( Int_t i ) const;

    /// retrieve the whole TObjArray  of McHitMdc Data
    const TObjArray* getMcHitMdcCol() const { return m_tMdcMcHitCol; };

    /// Add a McHitMdc into the Mdc Data collection
    void addMcHitMdc( TMcHitMdc* hit );

    /// retrieve a McHitMdc From the collection, using the index into the array
    const TMcHitMdc* getMcHitMdc( Int_t i ) const;

    /// retrieve the whole TObjArray  of McHitMdc Data
    const TObjArray* getMcDigiEmcCol() const { return m_tEmcMcDigiCol; };

    /// Add a McHitMdc into the Mdc Data collection
    void addMcDigiEmc( TMcDigiEmc* digi );

    /// retrieve a McHitMdc From the collection, using the index into the array
    const TMcDigiEmc* getMcDigiEmc( Int_t i ) const;

    void setBeamTime( Double_t time ) { m_beamTime = time; }
    Double_t getBeamTime() const { return m_beamTime; }

  private:
    /// data members to store Tof data
    TObjArray* m_tTofMcHitCol; //->
    /// data members to store Mdc data
    TObjArray* m_tMdcMcHitCol; //->
    /// data members to store Mdc data
    TObjArray* m_tEmcMcDigiCol; //->

    Double_t m_beamTime;

    ClassDef( TMcHitEvent, 4 ) // Storage for Raw(Digi) event and subsystem data
};

#endif
