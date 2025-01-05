#ifndef RootEventData_TMdcTrack_H
#define RootEventData_TMdcTrack_H 1

#include "TObject.h"

class TMdcTrack : public TObject {

  public:
    TMdcTrack();
    ~TMdcTrack();

    // Get
    Int_t trackId() const { return m_trackId; }
    Double_t helix( Int_t i ) const { return m_helix[i]; }
    Int_t stat() const { return m_stat; }
    Double_t chi2() const { return m_chi2; }
    Int_t ndof() const { return m_ndof; }
    Double_t err( Int_t i ) const { return m_err[i]; }
    Int_t nster() const { return m_nster; }
    Int_t nlayer() const { return m_nlayer; }
    Int_t firstLayer() const { return m_firstLayer; }
    Int_t lastLayer() const { return m_lastLayer; }

    Double_t x() const;
    Double_t y() const;
    Double_t z() const;

    Double_t r() const;
    Int_t charge() const;
    Double_t pxy() const;
    Double_t px() const;
    Double_t py() const;
    Double_t pz() const;
    Double_t p() const;
    Double_t theta() const;
    Double_t phi() const;

    // set
    void setHelix( const Double_t helix[5] );
    void setErr( const Double_t err[15] );
    void setTrackId( const Int_t trackId ) { m_trackId = trackId; }
    void setStat( const Int_t stat ) { m_stat = stat; }
    void setChi2( const Double_t chi ) { m_chi2 = chi; }
    void setNdof( const Int_t ndof ) { m_ndof = ndof; }
    void setNster( const Int_t ns ) { m_nster = ns; }
    void setNlayer( const Int_t nlayer ) { m_nlayer = nlayer; }
    void setFirstLayer( const Int_t fL ) { m_firstLayer = fL; }
    void setLastLayer( const Int_t lL ) { m_lastLayer = lL; }

  private:
    Int_t m_trackId;     // Track Id Wensp add 2005-10-19
    Double_t m_helix[5]; // 5 track parameters
    Double_t m_err[15];  // Error  Matrix
    // Double_t m_poca[3];
    Int_t m_stat; // Track Fit Quality
    Double_t m_chi2;
    Int_t m_ndof;
    Int_t m_nster;      // number of  stereo hits contained
    Int_t m_nlayer;     // number of  layer track passed
    Int_t m_firstLayer; //
    Int_t m_lastLayer;  //
    ClassDef( TMdcTrack, 3 )
};

#endif
