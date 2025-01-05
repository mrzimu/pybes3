#ifndef RootEventData_TEvtRecEvent_H
#define RootEventData_TEvtRecEvent_H

#include "TObject.h"

class TEvtRecEvent : public TObject {

  public:
    TEvtRecEvent();
    virtual ~TEvtRecEvent();

    void initialize();

    void Clear( Option_t* option = "" );

    void Print( Option_t* option = "" ) const;

    Int_t totalTracks() const { return m_tottks; }
    Int_t totalCharged() const { return m_nchrg; }
    Int_t totalNeutral() const { return m_nneu; }
    Int_t numberOfVee() const { return m_nvee; }
    Int_t numberOfPi0() const { return m_npi0; }
    Int_t numberOfEtaToGG() const { return m_neta; }
    Int_t numberOfDTag() const { return m_ndtag; }

    void setTotalTracks( const int tottks ) { m_tottks = tottks; }
    void setTotalCharged( const int nchrg ) { m_nchrg = nchrg; }
    void setTotalNeutral( const int nneu ) { m_nneu = nneu; }
    void setNumberOfVee( const int nvee ) { m_nvee = nvee; }
    void setNumberOfPi0( const int npi0 ) { m_npi0 = npi0; }
    void setNumberOfEtaToGG( const int neta ) { m_neta = neta; }
    void setNumberOfDTag( const int ndtag ) { m_ndtag = ndtag; }

  private:
    // Global event info: number of track, vertex in events
    Int_t m_tottks; // total tracks
    Int_t m_nchrg;  // total charged tracks
    Int_t m_nneu;   // total neutral tracks
    Int_t m_nvee;   // number of VEEs: Ks, Lambda, gamma conversion
    Int_t m_npi0;   // number of pi0'
    Int_t m_neta;   // number of eta'
    Int_t m_ndtag;  // number of dtags'

    ClassDef( TEvtRecEvent, 4 )
};

#endif
