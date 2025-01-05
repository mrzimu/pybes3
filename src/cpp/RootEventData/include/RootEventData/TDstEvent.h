#ifndef ROOT_TDstEvent_H
#define ROOT_TDstEvent_H 1

#include "TClonesArray.h"
#include "TObjArray.h"
#include "TObject.h"

#include "TEmcTrack.h"
#include "TExtTrack.h"
#include "TMdcDedx.h"
#include "TMdcKalTrack.h"
#include "TMdcTrack.h"
#include "TMucTrack.h"
#include "TTofTrack.h"

class TDstEvent : public TObject {

  public:
    TDstEvent();
    virtual ~TDstEvent();

    void initialize();

    void Clear( Option_t* option = "" );

    void Print( Option_t* option = "" ) const;

    //  inline Bool_t getFromMc() { return m_fromMc; };

    // ********************* Dst Track ******************************/

    /// retrieve the whole TObjArray of MdcTrack Data
    const TObjArray* getMdcTrackCol() const { return m_mdcTrackCol; };

    /// Add a TkrTrack into the Mdc data collection
    void addMdcTrack( TMdcTrack* Track );

    /// retrieve a MdcTrack from the collection, using the index into the array
    const TMdcTrack* getMdcTrack( Int_t i ) const;

    /// clear the whole array (necessary because of the consts-s)
    void clearMdcTrackCol() { m_mdcTrackCol->Clear(); }

    /// retrieve the whole TObjArray of EmcTrack Data
    const TObjArray* getEmcTrackCol() const { return m_emcTrackCol; };

    /// Add a TkrTrack into the Emc data collection
    void addEmcTrack( TEmcTrack* Track );

    /// retrieve a EmcTrack from the collection, using the index into the array
    const TEmcTrack* getEmcTrack( Int_t i ) const;

    /// clear the whole array (necessary because of the consts-s)
    void clearEmcTrackCol() { m_emcTrackCol->Clear(); }

    /// retrieve the whole TObjArray  of TofTrack Data
    const TObjArray* getTofTrackCol() const { return m_tofTrackCol; };

    /// Add a TofTrack into the TOF Data collection
    void addTofTrack( TTofTrack* Track );

    /// retrieve a TofTrack From the collection, using the index into the array
    const TTofTrack* getTofTrack( Int_t i ) const;

    /// clear the whole  array
    void clearTofTrackCol() { m_tofTrackCol->Clear(); }

    /// retrieve the whole TObjArray  of MucTrack Data
    const TObjArray* getMucTrackCol() const { return m_mucTrackCol; };

    /// Add a MucTrack into the TOF Data collection
    void addMucTrack( TMucTrack* Track );

    /// retrieve a MucTrack From the collection, using the index into the array
    const TMucTrack* getMucTrack( Int_t i ) const;

    /// clear the whole  array
    void clearMucTrackCol() { m_mucTrackCol->Clear(); }

    /// retrieve the whole TObjArray  of Dedx Data
    const TObjArray* getMdcDedxCol() const { return m_mdcDedxCol; };

    /// Add a Dedx into the TOF Data collection
    void addMdcDedx( TMdcDedx* Track );

    /// retrieve a TofTrack From the collection, using the index into the array
    const TMdcDedx* getMdcDedx( Int_t i ) const;

    /// clear the whole  array
    void clearMdcDedxCol() { m_mdcDedxCol->Clear(); }

    /// retrieve the whole TObjArray  of Ext Data
    const TObjArray* getExtTrackCol() const { return m_extTrackCol; };

    /// Add a ExtTrack into the Ext Data collection
    void addExtTrack( TExtTrack* Track );

    /// retrieve a MucTrack From the collection, using the index into the array
    const TExtTrack* getExtTrack( Int_t i ) const;

    /// clear the whole  array
    void clearExtTrackCol() { m_extTrackCol->Clear(); }

    //  TObjArray  of MdcKal Data
    const TObjArray* getMdcKalTrackCol() const { return m_mdcKalTrackCol; };
    void addMdcKalTrack( TMdcKalTrack* Track );
    const TMdcKalTrack* getMdcKalTrack( Int_t i ) const;
    void clearMdcKalTrackCol() { m_mdcKalTrackCol->Clear(); }

  private:
    /// data members to store Emc track data
    TObjArray* m_emcTrackCol; //->

    /// data members to store Mdc data
    TObjArray* m_mdcTrackCol; //->

    /// data members to store Tof data
    TObjArray* m_tofTrackCol; //->

    /// data members to store Muc data
    TObjArray* m_mucTrackCol; //->

    /// data members to store Dedx data
    TObjArray* m_mdcDedxCol; //->

    /// data members to store Ext data
    TObjArray* m_extTrackCol; //->

    /// data members to store MdcKal data
    TObjArray* m_mdcKalTrackCol; //->

    ClassDef( TDstEvent, 6 )
};

#endif
