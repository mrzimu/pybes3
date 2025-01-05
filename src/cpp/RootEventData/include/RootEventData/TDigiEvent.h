#ifndef ROOT_TDigiEvent_H
#define ROOT_TDigiEvent_H

#include "TObjArray.h"
#include "TObject.h"

#include "TEmcDigi.h"
#include "TLumiDigi.h"
#include "TMdcDigi.h"
#include "TMucDigi.h"
#include "TTofDigi.h"

class TDigiEvent : public TObject {
  public:
    TDigiEvent();
    ~TDigiEvent();

    void initialize( Bool_t fromMc = true );

    void Clear( Option_t* option = "" );

    void Print( Option_t* option = "" ) const;

    inline Bool_t getFromMc() { return m_fromMc; };

    /// retrieve the whole TObjArray of TkrDigi Data
    const TObjArray* getMdcDigiCol() const { return m_mdcDigiCol; };

    /// Add a TkrDigi into the TKR data collection
    void addMdcDigi( TMdcDigi* digi );

    /// retrieve a TkrDigi from the collection, using the index into the array
    const TMdcDigi* getMdcDigi( Int_t i ) const;

    /// clear the whole array (necessary because of the consts-s)
    void clearMdcDigiCol() { m_mdcDigiCol->Clear(); }

    /// retrieve the whole TObjArray of TkrDigi Data
    const TObjArray* getEmcDigiCol() const { return m_emcDigiCol; };

    /// Add a TkrDigi into the TKR data collection
    void addEmcDigi( TEmcDigi* digi );

    /// retrieve a EmcDigi from the collection, using the index into the array
    const TEmcDigi* getEmcDigi( Int_t i ) const;

    /// clear the whole array (necessary because of the consts-s)
    void clearEmcDigiCol() { m_emcDigiCol->Clear(); }

    /// retrieve the whole TObjArray  of TofDigi Data
    const TObjArray* getTofDigiCol() const { return m_tofDigiCol; };

    /// Add a TofDigi into the TOF Data collection
    void addTofDigi( TTofDigi* digi );

    /// retrieve a TofDigi From the collection, using the index into the array
    const TTofDigi* getTofDigi( Int_t i ) const;

    /// clear the whole  array
    void clearTofDigiCol() { m_tofDigiCol->Clear(); }

    /// retrieve the whole TObjArray  of MucDigi Data
    const TObjArray* getMucDigiCol() const { return m_mucDigiCol; };

    /// Add a MucDigi into the MUC Data collection
    void addMucDigi( TMucDigi* digi );

    /// retrieve a MucDigi From the collection, using the index into the array
    const TMucDigi* getMucDigi( Int_t i ) const;

    /// clear the whole  array
    void clearMucDigiCol() { m_mucDigiCol->Clear(); }

    /// retrieve the whole TObjArray  of LumiDigi Data
    const TObjArray* getLumiDigiCol() const { return m_lumiDigiCol; };

    /// Add a LumiDigi into the MUC Data collection
    void addLumiDigi( TLumiDigi* digi );

    /// retrieve a LumiDigi From the collection, using the index into the array
    const TLumiDigi* getLumiDigi( Int_t i ) const;

    /// clear the whole  array
    void clearLumiDigiCol() { m_lumiDigiCol->Clear(); }

  private:
    /// Denote whether or not this data was simulated
    Bool_t m_fromMc;

    /// data members to store Mdc data
    TObjArray* m_mdcDigiCol; //->

    /// data members to store Emc data
    TObjArray* m_emcDigiCol; //->

    /// data members to store Tof data
    TObjArray* m_tofDigiCol; //->

    /// data members to store Muc data
    TObjArray* m_mucDigiCol; //->

    /// data members to store Lumi data
    TObjArray* m_lumiDigiCol; //->

    ClassDef( TDigiEvent, 5 ) // Storage for Raw(Digi) event and subsystem data
};

#endif
