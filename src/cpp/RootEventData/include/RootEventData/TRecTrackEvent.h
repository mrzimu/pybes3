#ifndef ROOT_TRecTrackEvent_H
#define ROOT_TRecTrackEvent_H 1

#include "TObjArray.h"
#include "TObject.h"

#include "TRecEmcCluster.h"
#include "TRecEmcHit.h"
#include "TRecEmcShower.h"
#include "TRecEvTime.h"
#include "TRecExtTrack.h"
#include "TRecMdcDedx.h"
#include "TRecMdcDedxHit.h"
#include "TRecMdcHit.h"
#include "TRecMdcKalHelixSeg.h"
#include "TRecMdcKalTrack.h"
#include "TRecMdcTrack.h"
#include "TRecMucTrack.h"
#include "TRecTofTrack.h"
#include "TRecZddChannel.h"

class TRecTrackEvent : public TObject {

  public:
    TRecTrackEvent();
    virtual ~TRecTrackEvent();

    void initialize();

    void Clear( Option_t* option = "" );

    void Print( Option_t* option = "" ) const;

    //  inline Bool_t getFromMc() { return m_fromMc; };

    // ********************* Dst Track ******************************/
    /// retrieve the whole TObjArray of RecMdcTrack Data
    const TObjArray* getRecMdcTrackCol() const { return m_recMdcTrackCol; };

    /// Add a TkrTrack into the Mdc data collection
    void addRecMdcTrack( TRecMdcTrack* Track );

    /// retrieve a MdcTrack from the collection, using the index into the array
    const TRecMdcTrack* getRecMdcTrack( Int_t i ) const;

    /// clear the whole array (necessary because of the consts-s)
    void clearRecMdcTrackCol() { m_recMdcTrackCol->Clear(); }

    /// retrieve the whole TObjArray of RecMdcHit Data
    const TObjArray* getRecMdcHitCol() const { return m_recMdcHitCol; };

    /// Add a Rec Mdc Hit into the Mdc data collection
    void addRecMdcHit( TRecMdcHit* Hit );

    /// retrieve a RecMdcHit from the collection, using the index into the array
    const TRecMdcHit* getRecMdcHit( Int_t i ) const;
    /// clear the whole array (necessary because of the consts-s)
    void clearRecMdcHitCol() { m_recMdcHitCol->Clear(); }

    /// retrieve the whole TObjArray  of TofTrack Data
    const TObjArray* getTofTrackCol() const { return m_recTofTrackCol; };

    /// Add a TofTrack into the TOF Data collection
    void addTofTrack( TRecTofTrack* Track );

    /// retrieve a TofTrack From the collection, using the index into the array
    const TRecTofTrack* getTofTrack( Int_t i ) const;

    /// clear the whole  array
    void clearTofTrackCol() { m_recTofTrackCol->Clear(); }

    /// retrieve the whole TObjArray of EmcHit Data
    const TObjArray* getEmcHitCol() const { return m_recEmcHitCol; };

    /// Add a TkrTrack into the Emc data collection */
    void addEmcHit( TRecEmcHit* Track );

    /// retrieve a EmcHit from the collection, using the index into the array */
    const TRecEmcHit* getEmcHit( Int_t i ) const;

    /// clear the whole array (necessary because of the consts-s) */
    void clearEmcHitCol() { m_recEmcHitCol->Clear(); }

    /// retrieve the whole TObjArray of EmcCluster Data
    const TObjArray* getEmcClusterCol() const { return m_recEmcClusterCol; };

    /// Add a TkrTrack into the Emc data collection */
    void addEmcCluster( TRecEmcCluster* Track );

    /// retrieve a EmcCluster from the collection, using the index into the array */
    const TRecEmcCluster* getEmcCluster( Int_t i ) const;

    /// clear the whole array (necessary because of the consts-s) */
    void clearEmcClusterCol() { m_recEmcClusterCol->Clear(); }

    /// retrieve the whole TObjArray of EmcShower Data
    const TObjArray* getEmcShowerCol() const { return m_recEmcShowerCol; };

    /// Add a TkrTrack into the Emc data collection */
    void addEmcShower( TRecEmcShower* Track );

    /// retrieve a EmcShower from the collection, using the index into the array */
    const TRecEmcShower* getEmcShower( Int_t i ) const;

    /// clear the whole array (necessary because of the consts-s) */
    void clearEmcShowerCol() { m_recEmcShowerCol->Clear(); }

    /// retrieve the whole TObjArray  of MucTrack Data
    const TObjArray* getMucTrackCol() const { return m_recMucTrackCol; };

    /// Add a MucTrack into the TOF Data collection
    void addMucTrack( TRecMucTrack* Track );

    /// retrieve a MucTrack From the collection, using the index into the array
    const TRecMucTrack* getMucTrack( Int_t i ) const;

    /// clear the whole  array
    void clearMucTrackCol() { m_recMucTrackCol->Clear(); }

    /// retrieve the whole TObjArray  of Dedx Data
    const TObjArray* getRecMdcDedxCol() const { return m_recMdcDedxCol; };

    /// Add a Dedx into the TOF Data collection
    void addRecMdcDedx( TRecMdcDedx* Track );

    /// retrieve a TofTrack From the collection, using the index into the array
    const TRecMdcDedx* getRecMdcDedx( Int_t i ) const;

    /// clear the whole  array
    void clearRecMdcDedxCol() { m_recMdcDedxCol->Clear(); }

    /// retrieve the whole TObjArray  of Dedx Data
    const TObjArray* getRecMdcDedxHitCol() const { return m_recMdcDedxHitCol; };

    /// Add a Dedx into the TOF Data collection
    void addRecMdcDedxHit( TRecMdcDedxHit* Track );

    /// retrieve a TofTrack From the collection, using the index into the array
    const TRecMdcDedxHit* getRecMdcDedxHit( Int_t i ) const;

    /// clear the whole  array
    void clearRecMdcDedxHitCol() { m_recMdcDedxHitCol->Clear(); }

    /*    /// retrieve the whole TObjArray  of Ext Data */
    const TObjArray* getExtTrackCol() const { return m_recExtTrackCol; };

    /// Add a ExtTrack into the Ext Data collection
    void addExtTrack( TRecExtTrack* Track );

    /*       /// retrieve a MucTrack From the collection, using the index into the array */
    const TRecExtTrack* getExtTrack( Int_t i ) const;

    /*       /// clear the whole  array  */
    void clearExtTrackCol() { m_recExtTrackCol->Clear(); }

    //  TObjArray  of MdcKal Data
    const TObjArray* getRecMdcKalTrackCol() const { return m_recMdcKalTrackCol; }
    void addRecMdcKalTrack( TRecMdcKalTrack* Track );
    const TRecMdcKalTrack* getRecMdcKalTrack( Int_t i ) const;
    void clearRecMdcKalTrackCol() { m_recMdcKalTrackCol->Clear(); }

    //  TObjArray  of MdcKalHit Data
    const TObjArray* getRecMdcKalHelixSegCol() const { return m_recMdcKalHelixSegCol; }
    void addRecMdcKalHelixSeg( TRecMdcKalHelixSeg* Track );
    const TRecMdcKalHelixSeg* getRecMdcKalHelixSeg( Int_t i ) const;
    void clearRecMdcKalHelixSegCol() { m_recMdcKalHelixSegCol->Clear(); }

    //  TObjArray of EsTime Data
    const TObjArray* getEvTimeCol() const { return m_recEvTimeCol; }
    void addEvTime( TRecEvTime* Track );
    const TRecEvTime* getEvTime( Int_t i ) const;
    void clearEvTimeCol() { m_recEvTimeCol->Clear(); }

    // Interfaces of RecZddChannel
    const TObjArray* getRecZddChannelCol() const { return m_recZddChannelCol; }
    void addRecZddChannel( TRecZddChannel* dtag );
    const TRecZddChannel* getRecZddChannel( Int_t i ) const;
    void clearRecZddChannelCol() { m_recZddChannelCol->Clear(); }

  private:
    /// data members to store Mdc data
    TObjArray* m_recMdcTrackCol; //->
    TObjArray* m_recMdcHitCol;   //->

    TObjArray* m_recEmcHitCol; //->

    TObjArray* m_recEmcClusterCol; //->

    /*     /// data members to store Emc track data */
    TObjArray* m_recEmcShowerCol; //->

    /// data members to store Tof data
    TObjArray* m_recTofTrackCol; //->

    /// data members to store Muc data
    TObjArray* m_recMucTrackCol; //->

    /// data members to store Dedx data
    TObjArray* m_recMdcDedxCol; //->

    /// data members to store Dedx data
    TObjArray* m_recMdcDedxHitCol; //->

    /*     /// data members to store Ext data */
    TObjArray* m_recExtTrackCol; //->

    /*     /// data members to store MdcKal data */
    TObjArray* m_recMdcKalTrackCol; //->

    /// data members to store MdcKal data
    TObjArray* m_recMdcKalHelixSegCol; //->

    /// data members to store EvTime data
    TObjArray* m_recEvTimeCol; //->

    // data members to store RecZddChannel
    TObjArray* m_recZddChannelCol; //->

    ClassDef( TRecTrackEvent, 8 )
};

#endif
