#ifndef RootEventData_TEvtRecPrimaryVertex_H
#define RootEventData_TEvtRecPrimaryVertex_H

#include "TObject.h"
#include <vector>

class TEvtRecPrimaryVertex : public TObject {
  public:
    TEvtRecPrimaryVertex();
    ~TEvtRecPrimaryVertex();

    Bool_t isValid() const { return m_isValid; }
    Int_t nTracks() const { return m_nTracks; }
    const std::vector<Int_t>& trackIdList() const { return m_trackIdList; }
    Double_t chi2() const { return m_chi2; }
    Int_t ndof() const { return m_ndof; }
    Int_t fitMethod() const { return m_fitMethod; }
    Double_t vertex( Int_t i ) const { return m_vtx[i]; }
    Double_t errorVertex( Int_t i ) const { return m_Evtx[i]; }

    void setIsValid( Bool_t isValid ) { m_isValid = isValid; }
    void setNTracks( Int_t nTracks ) { m_nTracks = nTracks; }
    void setTrackIdList( const std::vector<Int_t>& trackIdList ) {
        m_trackIdList = trackIdList;
    }
    void setChi2( Double_t chi2 ) { m_chi2 = chi2; }
    void setNdof( Int_t ndof ) { m_ndof = ndof; }
    void setFitMethod( Int_t fitMethod ) { m_fitMethod = fitMethod; }
    void setVertex( Double_t vtx[3] ) {
        for ( Int_t i = 0; i < 3; i++ ) m_vtx[i] = vtx[i];
    }
    void setErrorVertex( Double_t Evtx[6] ) {
        for ( Int_t i = 0; i < 6; i++ ) m_Evtx[i] = Evtx[i];
    }

  private:
    Bool_t m_isValid;
    Int_t m_nTracks;                  // number of tracks contributing to vertex fitting
    std::vector<Int_t> m_trackIdList; // id list of tracks contributing to vertex fitting
    Double_t m_chi2;                  // chi square of vertex fitting
    Int_t m_ndof;                     // degree of freedom
                  // for a fixed position => 2n; for unknown position => 2n-3;
    Int_t m_fitMethod;  // vertex fitting algorithm
                        // 0 => global method; 1 => kalman filter method;
    Double_t m_vtx[3];  // primary vertex position : (Vx, Vy, Vz)
    Double_t m_Evtx[6]; // error matrix of primary vertex

    ClassDef( TEvtRecPrimaryVertex, 1 )
};

#endif
