#ifndef RootEventData_TMdcKalTrack_H
#define RootEventData_TMdcKalTrack_H 1

#include "SimMatr.h"
#include "TObject.h"
#include "TString.h"

class TMdcKalTrack : public TObject {

  public:
    TMdcKalTrack();

    ~TMdcKalTrack();

    // extractors
    Int_t getTrackId() const { return m_trackId; }
    Int_t getStat( const Int_t pid ) const { return m_stat[pid]; }
    Int_t getStat2( const Int_t pid ) const { return m_stat2[pid]; }
    Double_t getChisq( const Int_t pid ) const { return m_chisq[pid]; }
    Int_t getNdf( const Int_t pid ) const { return m_ndf[pid]; }
    Int_t getNlayer( const Int_t pid ) const { return m_nlayer[pid]; }
    // o Int_t    getNster(const Int_t pid) const {return m_nster[pid];}
    // o Int_t    getFirstLayer(const Int_t pid) const { return m_firstLayer[pid]; }
    // o Int_t    getLastLayer(const Int_t pid) const {return m_lastLayer[pid];}

    Double_t getZHelix( Int_t i ) const { return m_zhelix[i]; }
    Double_t getZError( Int_t i, Int_t j ) const {
        return SimMat::get_element( m_zerror, i, j );
    }
    // Double_t getPoca(Int_t i) const {return m_poca[i];}
    Double_t getZHelixE( Int_t i ) const { return m_zhelix_e[i]; }
    Double_t getZErrorE( Int_t i, Int_t j ) const {
        return SimMat::get_element( m_zerror_e, i, j );
    }
    // Double_t getPocaE(Int_t i) const {return m_poca_e[i];}
    Double_t getZHelixMu( Int_t i ) const { return m_zhelix_mu[i]; }
    Double_t getZErrorMu( Int_t i, Int_t j ) const {
        return SimMat::get_element( m_zerror_mu, i, j );
    }
    // Double_t getPocaMu(Int_t i) const {return m_poca_mu[i];}
    Double_t getZHelixK( Int_t i ) const { return m_zhelix_k[i]; }
    Double_t getZErrorK( Int_t i, Int_t j ) const {
        return SimMat::get_element( m_zerror_k, i, j );
    }
    // Double_t getPocaK(Int_t i) const {return m_poca_k[i];}
    Double_t getZHelixP( Int_t i ) const { return m_zhelix_p[i]; }
    Double_t getZErrorP( Int_t i, Int_t j ) const {
        return SimMat::get_element( m_zerror_p, i, j );
    }
    // Double_t getPocaP(Int_t i) const {return m_poca_p[i];}

    Double_t getFHelix( Int_t i ) const { return m_fhelix[i]; }
    Double_t getFError( Int_t i, Int_t j ) const {
        return SimMat::get_element( m_ferror, i, j );
    }
    Double_t getFHelixE( Int_t i ) const { return m_fhelix_e[i]; }
    Double_t getFErrorE( Int_t i, Int_t j ) const {
        return SimMat::get_element( m_ferror_e, i, j );
    }
    Double_t getFHelixMu( Int_t i ) const { return m_fhelix_mu[i]; }
    Double_t getFErrorMu( Int_t i, Int_t j ) const {
        return SimMat::get_element( m_ferror_mu, i, j );
    }
    Double_t getFHelixK( Int_t i ) const { return m_fhelix_k[i]; }
    Double_t getFErrorK( Int_t i, Int_t j ) const {
        return SimMat::get_element( m_ferror_k, i, j );
    }
    Double_t getFHelixP( Int_t i ) const { return m_fhelix_p[i]; }
    Double_t getFErrorP( Int_t i, Int_t j ) const {
        return SimMat::get_element( m_ferror_p, i, j );
    }
    // modifiers
    void setTrackId( const Int_t trackId ) { m_trackId = trackId; }
    void setStat( const Int_t stat, const Int_t pid ) { m_stat[pid] = stat; }
    void setStat2( const Int_t stat, const Int_t pid ) { m_stat2[pid] = stat; }
    void setChisq( const Double_t chisq, const Int_t pid ) { m_chisq[pid] = chisq; }
    void setNdf( const Int_t ndf, const Int_t pid ) { m_ndf[pid] = ndf; }
    void setNlayer( const Int_t nlayer, const Int_t pid ) { m_nlayer[pid] = nlayer; }
    // o void setNster(const Int_t nster, const Int_t pid) {m_nster[pid] = nster;}
    // o void setFirstLayer(const Int_t fL, const Int_t pid) { m_firstLayer[pid] = fL; }
    // o void setLastLayer(const Int_t lL, const Int_t pid){ m_lastLayer[pid] = lL;}

    void setZHelix( const Double_t zhelix[5] ) {
        for ( int i = 0; i < 5; i++ ) m_zhelix[i] = zhelix[i];
    }
    void setZError( const Double_t zerror[5][5] ) {
        SimMat::pack2d( 5, &zerror[0][0], m_zerror );
    }

    // void setPoca(const Double_t poca[3]){
    //   for(int i=0; i<3; i++) m_poca[i] = poca[i];
    // }

    void setZHelixE( const Double_t zhelix_e[5] ) {
        for ( int i = 0; i < 5; i++ ) m_zhelix_e[i] = zhelix_e[i];
    }
    void setZErrorE( const Double_t zerror_e[5][5] ) {
        SimMat::pack2d( 5, &zerror_e[0][0], m_zerror_e );
    }
    // void setPocaE(const Double_t poca_e[3]){
    //   for(int i=0; i<3; i++) m_poca_e[i] = poca_e[i];
    // }

    void setZHelixMu( const Double_t zhelix_mu[5] ) {
        for ( int i = 0; i < 5; i++ ) m_zhelix_mu[i] = zhelix_mu[i];
    }
    void setZErrorMu( const Double_t zerror_mu[5][5] ) {
        SimMat::pack2d( 5, &zerror_mu[0][0], m_zerror_mu );
    }
    // void setPocaMu(const Double_t poca_mu[3]){
    //   for(int i=0; i<3; i++) m_poca_mu[i] = poca_mu[i];
    // }

    void setZHelixK( const Double_t zhelix_k[5] ) {
        for ( int i = 0; i < 5; i++ ) m_zhelix_k[i] = zhelix_k[i];
    }
    void setZErrorK( const Double_t zerror_k[5][5] ) {
        SimMat::pack2d( 5, &zerror_k[0][0], m_zerror_k );
    }
    // void setPocaK(const Double_t poca_k[3]){
    //   for(int i=0; i<3; i++) m_poca_k[i] = poca_k[i];
    // }

    void setZHelixP( const Double_t zhelix_p[5] ) {
        for ( int i = 0; i < 5; i++ ) m_zhelix_p[i] = zhelix_p[i];
    }
    void setZErrorP( const Double_t zerror_p[5][5] ) {
        SimMat::pack2d( 5, &zerror_p[0][0], m_zerror_p );
    }
    // void setPocaP(const Double_t poca_p[3]){
    //   for(int i=0; i<3; i++) m_poca_p[i] = poca_p[i];
    // }

    void setFHelix( const Double_t fhelix[5] ) {
        for ( int i = 0; i < 5; i++ ) m_fhelix[i] = fhelix[i];
    }
    void setFError( const Double_t ferror[5][5] ) {
        SimMat::pack2d( 5, &ferror[0][0], m_ferror );
    }

    void setFHelixE( const Double_t fhelix_e[5] ) {
        for ( int i = 0; i < 5; i++ ) m_fhelix_e[i] = fhelix_e[i];
    }
    void setFErrorE( const Double_t ferror_e[5][5] ) {
        SimMat::pack2d( 5, &ferror_e[0][0], m_ferror_e );
    }

    void setFHelixMu( const Double_t fhelix_mu[5] ) {
        for ( int i = 0; i < 5; i++ ) m_fhelix_mu[i] = fhelix_mu[i];
    }
    void setFErrorMu( const Double_t ferror_mu[5][5] ) {
        SimMat::pack2d( 5, &ferror_mu[0][0], m_ferror_mu );
    }

    void setFHelixK( const Double_t fhelix_k[5] ) {
        for ( int i = 0; i < 5; i++ ) m_fhelix_k[i] = fhelix_k[i];
    }
    void setFErrorK( const Double_t ferror_k[5][5] ) {
        SimMat::pack2d( 5, &ferror_k[0][0], m_ferror_k );
    }

    void setFHelixP( const Double_t fhelix_p[5] ) {
        for ( int i = 0; i < 5; i++ ) m_fhelix_p[i] = fhelix_p[i];
    }
    void setFErrorP( const Double_t ferror_p[5][5] ) {
        SimMat::pack2d( 5, &ferror_p[0][0], m_ferror_p );
    }

  private:
    Int_t m_trackId;
    Int_t m_stat[5];
    Int_t m_stat2[5];
    Double_t m_chisq[5];
    Int_t m_ndf[5];
    Int_t m_nlayer[5];
    // o Int_t    m_nster[5];
    // o Int_t    m_firstLayer[5];
    // o Int_t    m_lastLayer[5];

    // Double_t m_poca[3];
    Double_t m_zhelix[5]; // 5 track parameters at zero point for pi
    // o Double_t m_zerror[5][5];   // error matrix at zero point for pion
    Double_t m_zerror[15]; // error matrix at zero point for pion

    // Double_t m_poca_e[3];
    Double_t m_zhelix_e[5]; // 5 track parameters at zero point for el
    // o Double_t m_zerror_e[5][5]; // error matrix at zero point for electron
    Double_t m_zerror_e[15]; // error matrix at zero point for electron

    // Double_t m_poca_mu[3];
    Double_t m_zhelix_mu[5]; // 5 track parameters at zero point for mu
    // o Double_t m_zerror_mu[5][5];// error matrix at zero point  for muon   ;
    Double_t m_zerror_mu[15]; // error matrix at zero point  for muon   ;

    // Double_t m_poca_k[3];
    Double_t m_zhelix_k[5]; // 5 track parameters at zero point for ka
    // o Double_t m_zerror_k[5][5]; // error matrix at zero point for kaon
    Double_t m_zerror_k[15]; // error matrix at zero point for kaon

    // Double_t m_poca_p[3];
    Double_t m_zhelix_p[5]; // 5 track parameters at zero point for pr
    // o Double_t m_zerror_p[5][5]; // error matrix at zero point for proton
    Double_t m_zerror_p[15]; // error matrix at zero point for proton

    Double_t m_fhelix[5]; // 5 track parameters at first Mdchit  for pi
    // o Double_t m_ferror[5][5];   // error matrix at first Mdc hit for pion
    Double_t m_ferror[15]; // error matrix at first Mdc hit for pion
    Double_t m_fhelix_e[5];
    // o Double_t m_ferror_e[5][5];
    Double_t m_ferror_e[15];
    Double_t m_fhelix_mu[5];
    // o Double_t m_ferror_mu[5][5];
    Double_t m_ferror_mu[15];
    Double_t m_fhelix_k[5];
    // o Double_t m_ferror_k[5][5];
    Double_t m_ferror_k[15];
    Double_t m_fhelix_p[5];
    // o Double_t m_ferror_p[5][5];
    Double_t m_ferror_p[15];

    ClassDef( TMdcKalTrack, 3 )
};

#endif
