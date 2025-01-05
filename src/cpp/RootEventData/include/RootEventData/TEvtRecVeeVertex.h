#ifndef RootEventData_TEvtRecVeeVertex_H
#define RootEventData_TEvtRecVeeVertex_H

#include "TObject.h"

class TEvtRecVeeVertex : public TObject {

  public:
    TEvtRecVeeVertex();
    ~TEvtRecVeeVertex();

    Int_t vertexId() const { return m_vertexId; }
    Int_t vertexType() const { return m_vertexType; }
    Double_t chi2() const { return m_chi2; }
    Int_t ndof() const { return m_ndof; }
    Double_t mass() const { return m_mass; }
    Double_t w( Int_t i ) const { return m_w[i]; }
    Double_t Ew( Int_t i ) const { return m_Ew[i]; }
    Int_t pair( Int_t i ) const { return m_pair[i]; }
    Int_t nCharge() const { return m_nCharge; }
    Int_t nTracks() const { return m_nTracks; }
    Int_t daughter( Int_t i ) const { return m_daughter[i]; }

    void setVertexId( Int_t vtxId ) { m_vertexId = vtxId; }
    void setVertexType( Int_t vtxType ) { m_vertexType = vtxType; }
    void setChi2( Double_t chi2 ) { m_chi2 = chi2; }
    void setNdof( Int_t ndof ) { m_ndof = ndof; }
    void setMass( Double_t mass ) { m_mass = mass; }
    void setW( Double_t w[7] ) {
        for ( Int_t i = 0; i < 7; i++ ) m_w[i] = w[i];
    }
    void setEw( Double_t Ew[28] ) {
        for ( Int_t i = 0; i < 28; i++ ) m_Ew[i] = Ew[i];
    }
    void setPair( Int_t pair[2] ) {
        for ( Int_t i = 0; i < 2; i++ ) m_pair[i] = pair[i];
    }
    void setNCharge( Int_t nCharge ) { m_nCharge = nCharge; }
    void setNTracks( Int_t nTracks ) { m_nTracks = nTracks; }
    void setDaughter( Int_t daughter[2] ) {
        for ( Int_t i = 0; i < 2; i++ ) m_daughter[i] = daughter[i];
    }

  private:
    Int_t m_vertexId;
    Int_t m_vertexType; // 0 : Ks;  1 : Lambda; 2 : gamma conversion
    Double_t m_chi2;    // chi square of vertex fitting
    Int_t m_ndof;       // degree of freedom
    Double_t m_mass;    // mass of "V" type decay particle
    Double_t m_w[7];    // (px, py, pz, E, x, y, z) of "V" type decay particle
    Double_t m_Ew[28];  // error matrix
    Int_t m_pair[2];    // identification of daughter particles
                        // 1:e   2:mu   3:pion  4:kaon  5:proton
    Int_t m_nCharge;    // total charges of daughter particles
    Int_t m_nTracks;    // total tracks of daughter particles
    Int_t m_daughter[2];

    ClassDef( TEvtRecVeeVertex, 1 )
};
#endif
