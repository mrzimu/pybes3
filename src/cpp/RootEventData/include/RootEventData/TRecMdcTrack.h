#ifndef RootEventData_TRecMdcTrack_H
#define RootEventData_TRecMdcTrack_H 1

#include "TObject.h"
#include <vector>

using namespace std;

class TRecMdcTrack : public TObject {

  public:
    TRecMdcTrack();

    ~TRecMdcTrack();
    // Get
    Int_t trackId() const { return m_trackId; }
    Double_t helix( Int_t i ) const { return m_helix[i]; }
    Int_t charge() const;
    Double_t pxy() const;
    Double_t px() const;
    Double_t py() const;
    Double_t pz() const;
    Double_t p() const;
    Double_t theta() const;
    Double_t phi() const;
    Double_t x() const;
    Double_t y() const;
    Double_t z() const;
    Double_t r() const;
    Int_t stat() const { return m_stat; }
    Double_t chi2() const { return m_chi2; }
    Int_t ndof() const { return m_ndof; }
    Double_t err( Int_t i ) const { return m_err[i]; }
    Int_t nhits() const { return m_nhits; }
    Int_t nster() const { return m_nster; }
    Int_t nlayer() const { return m_nlayer; }
    // vector<Int_t> vecHits() const { return  m_vecHits ; }
    // Get rec
    Double_t vx0( void ) const { return m_vx0; }
    Double_t vy0( void ) const { return m_vy0; }
    Double_t vz0( void ) const { return m_vz0; }
    Double_t fiTerm( void ) const { return m_fiTerm; }

    // Set
    void setTrackId( const Int_t trackId ) { m_trackId = trackId; }
    void setHelix( const Double_t helix[5] ) {
        for ( Int_t i = 0; i < 5; i++ ) m_helix[i] = helix[i];
    }
    void setStat( const Int_t stat ) { m_stat = stat; }
    void setChi2( const Double_t chi ) { m_chi2 = chi; }
    void setNdof( const Int_t ndof ) { m_ndof = ndof; }

    void setErr( const Double_t er[15] ) {
        for ( Int_t i = 0; i < 15; i++ ) m_err[i] = er[i];
    }

    void setNhits( const Int_t nh ) { m_nhits = nh; }
    void setNster( const Int_t ns ) { m_nster = ns; }
    void setNlayer( const Int_t nlayer ) { m_nlayer = nlayer; }
    // void    setVecHits(vector<Int_t>& vecHits) { m_vecHits = vecHits; }
    // Set rec
    void setVX0( Double_t vx0 ) { m_vx0 = vx0; }
    void setVY0( Double_t vy0 ) { m_vy0 = vy0; }
    void setVZ0( Double_t vz0 ) { m_vz0 = vz0; }
    void setFiTerm( Double_t fiterm ) { m_fiTerm = fiterm; }
    void setTRecMdcTrack( const TRecMdcTrack* mdcTrk ) {
        for ( int i = 0; i < 5; i++ ) { m_helix[i] = mdcTrk->helix( i ); }
        for ( int i = 0; i < 15; i++ ) { m_err[i] = mdcTrk->err( i ); }
        m_trackId = mdcTrk->trackId();
        m_stat    = mdcTrk->stat();
        m_chi2    = mdcTrk->chi2();
        m_ndof    = mdcTrk->ndof();
        m_nster   = mdcTrk->nster();
        m_nlayer  = mdcTrk->nlayer();
        m_vx0     = mdcTrk->vx0();
        m_vy0     = mdcTrk->vy0();
        m_vz0     = mdcTrk->vz0();
        m_fiTerm  = mdcTrk->fiTerm();
    }

  private:
    Int_t m_trackId;     // Track Id Wensp add 2005-10-19
    Double_t m_helix[5]; // 5 track parameters
    Int_t m_stat;        // Track Fit Quality
    Double_t m_chi2;
    Int_t m_ndof;
    Double_t m_err[15]; // Error  Matrix
    Int_t m_nhits;      // number of  total hits contained
    Int_t m_nster;      // number of  stereo hits contained
    Int_t m_nlayer;     // number of  layer hits contained
    // vector<Int_t> m_vecHits; // Hit list of the track wensp Add 2005-10-20

    // Rec
    Double_t m_vx0;    // The coordinate of pivot(cm)
    Double_t m_vy0;    //
    Double_t m_vz0;    //
    Double_t m_fiTerm; // phi angle value at track terminated point

    ClassDef( TRecMdcTrack, 3 )
};

#endif
