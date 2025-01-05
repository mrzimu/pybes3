#ifndef RootEventData_TRecMdcKalTrack_H
#define RootEventData_TRecMdcKalTrack_H 1

#include "TObject.h"
#include "TString.h"

class TRecMdcKalTrack : public TObject {

  public:
    TRecMdcKalTrack();
    ~TRecMdcKalTrack();

    // extractors
    Int_t getTrackId() const { return m_trackId; }
    Double_t getMass( Int_t pid ) const { return m_mass[pid]; }
    Double_t getLength( Int_t pid ) const { return m_length[pid]; }
    Double_t getTof( Int_t pid ) const { return m_tof[pid]; }
    Double_t getfiTerm( Int_t pid ) const { return m_fiTerm[pid]; }
    Double_t getPathSM( Int_t pid ) const { return m_pathSM[pid]; }
    Int_t getNhits( Int_t pid ) const { return m_nhits[pid]; }
    Int_t getNlayer( Int_t pid ) const { return m_nlayer[pid]; }
    Int_t getStat( Int_t i, Int_t pid ) const { return m_stat[i][pid]; }
    Double_t getChisq( Int_t i, Int_t pid ) const { return m_chisq[i][pid]; }
    Int_t getNdf( Int_t i, Int_t pid ) const { return m_ndf[i][pid]; }
    Int_t getNseg( Int_t pid ) const { return m_nSegs[pid]; }
    Double_t getZHelix( Int_t i ) const { return m_zhelix[i]; }
    Double_t getZError( Int_t i, Int_t j ) const { return m_zerror[i][j]; }
    Double_t getZHelixE( Int_t i ) const { return m_zhelix_e[i]; }
    Double_t getZErrorE( Int_t i, Int_t j ) const { return m_zerror_e[i][j]; }
    Double_t getZHelixMu( Int_t i ) const { return m_zhelix_mu[i]; }
    Double_t getZErrorMu( Int_t i, Int_t j ) const { return m_zerror_mu[i][j]; }
    Double_t getZHelixK( Int_t i ) const { return m_zhelix_k[i]; }
    Double_t getZErrorK( Int_t i, Int_t j ) const { return m_zerror_k[i][j]; }
    Double_t getZHelixP( Int_t i ) const { return m_zhelix_p[i]; }
    Double_t getZErrorP( Int_t i, Int_t j ) const { return m_zerror_p[i][j]; }
    Double_t getFHelix( Int_t i ) const { return m_fhelix[i]; }
    Double_t getFError( Int_t i, Int_t j ) const { return m_ferror[i][j]; }
    Double_t getFHelixE( Int_t i ) const { return m_fhelix_e[i]; }
    Double_t getFErrorE( Int_t i, Int_t j ) const { return m_ferror_e[i][j]; }
    Double_t getFHelixMu( Int_t i ) const { return m_fhelix_mu[i]; }
    Double_t getFErrorMu( Int_t i, Int_t j ) const { return m_ferror_mu[i][j]; }
    Double_t getFHelixK( Int_t i ) const { return m_fhelix_k[i]; }
    Double_t getFErrorK( Int_t i, Int_t j ) const { return m_ferror_k[i][j]; }
    Double_t getFHelixP( Int_t i ) const { return m_fhelix_p[i]; }
    Double_t getFErrorP( Int_t i, Int_t j ) const { return m_ferror_p[i][j]; }
    Double_t getLHelix( Int_t i ) const { return m_lhelix[i]; }
    Double_t getLError( Int_t i, Int_t j ) const { return m_lerror[i][j]; }
    Double_t getLHelixE( Int_t i ) const { return m_lhelix_e[i]; }
    Double_t getLErrorE( Int_t i, Int_t j ) const { return m_lerror_e[i][j]; }
    Double_t getLHelixMu( Int_t i ) const { return m_lhelix_mu[i]; }
    Double_t getLErrorMu( Int_t i, Int_t j ) const { return m_lerror_mu[i][j]; }
    Double_t getLHelixK( Int_t i ) const { return m_lhelix_k[i]; }
    Double_t getLErrorK( Int_t i, Int_t j ) const { return m_lerror_k[i][j]; }
    Double_t getLHelixP( Int_t i ) const { return m_lhelix_p[i]; }
    Double_t getLErrorP( Int_t i, Int_t j ) const { return m_lerror_p[i][j]; }
    Double_t getTHelix( Int_t i ) const { return m_thelix[i]; }
    Double_t getTError( Int_t i ) const { return m_terror[i]; }

    Double_t getPocaE( Int_t i ) const { return m_poca_e[i]; }

    Double_t getPocaMu( Int_t i ) const { return m_poca_mu[i]; }

    Double_t getPoca( Int_t i ) const { return m_poca[i]; }

    Double_t getPocaK( Int_t i ) const { return m_poca_k[i]; }

    Double_t getPocaP( Int_t i ) const { return m_poca_p[i]; }

    Double_t getLPointE( Int_t i ) const { return m_lpoint_e[i]; }
    Double_t getLPointMu( Int_t i ) const { return m_lpoint_mu[i]; }
    Double_t getLPoint( Int_t i ) const { return m_lpoint[i]; }
    Double_t getLPointK( Int_t i ) const { return m_lpoint_k[i]; }
    Double_t getLPointP( Int_t i ) const { return m_lpoint_p[i]; }

    Double_t getLPivotE( Int_t i ) const { return m_lpivot_e[i]; }
    Double_t getLPivotMu( Int_t i ) const { return m_lpivot_mu[i]; }
    Double_t getLPivot( Int_t i ) const { return m_lpivot[i]; }
    Double_t getLPivotK( Int_t i ) const { return m_lpivot_k[i]; }
    Double_t getLPivotP( Int_t i ) const { return m_lpivot_p[i]; }

    // modifiers

    void setTrackId( const Int_t trackId ) { m_trackId = trackId; }
    void setMass( const Double_t mass[5] ) {
        for ( int i = 0; i < 5; i++ ) m_mass[i] = mass[i];
    }

    void setLength( const Double_t length[5] ) {
        for ( int i = 0; i < 5; i++ ) m_length[i] = length[i];
    }

    void setFiTerm( const Double_t fiTerm[5] ) {
        for ( int i = 0; i < 5; i++ ) m_fiTerm[i] = fiTerm[i];
    }

    void setPathSM( const Double_t pathSM[5] ) {
        for ( int i = 0; i < 5; i++ ) m_pathSM[i] = pathSM[i];
    }

    void setTof( const Double_t tof[5] ) {
        for ( int i = 0; i < 5; i++ ) m_tof[i] = tof[i];
    }

    void setNhits( const Int_t nhits[5] ) {
        for ( int i = 0; i < 5; i++ ) m_nhits[i] = nhits[i];
    }

    void setStat( const Int_t stat, Int_t i, Int_t pid ) { m_stat[i][pid] = stat; }
    void setChisq( const Double_t chisq, Int_t i, Int_t pid ) { m_chisq[i][pid] = chisq; }
    void setNdf( const Int_t ndf, Int_t i, Int_t pid ) { m_ndf[i][pid] = ndf; }
    void setNseg( const Int_t nSeg, Int_t pid ) { m_nSegs[pid] = nSeg; }
    void setNlayer( const Int_t nlayer, Int_t pid ) { m_nlayer[pid] = nlayer; }
    // Z
    void setZHelix( const Double_t zhelix[5] ) {
        for ( int i = 0; i < 5; i++ ) m_zhelix[i] = zhelix[i];
    }
    void setZError( const Double_t zerror[5][5] ) {
        for ( int i = 0; i < 5; i++ )
            for ( int j = 0; j <= i; j++ )
            {
                m_zerror[i][j] = zerror[i][j];
                m_zerror[j][i] = zerror[i][j];
            }
    }
    void setZHelixE( const Double_t zhelix_e[5] ) {
        for ( int i = 0; i < 5; i++ ) m_zhelix_e[i] = zhelix_e[i];
    }
    void setZErrorE( const Double_t zerror_e[5][5] ) {
        for ( int i = 0; i < 5; i++ )
            for ( int j = 0; j <= i; j++ )
            {
                m_zerror_e[i][j] = zerror_e[i][j];
                m_zerror_e[j][i] = zerror_e[i][j];
            }
    }

    void setZHelixMu( const Double_t zhelix_mu[5] ) {
        for ( int i = 0; i < 5; i++ ) m_zhelix_mu[i] = zhelix_mu[i];
    }

    void setZErrorMu( const Double_t zerror_mu[5][5] ) {
        for ( int i = 0; i < 5; i++ )
            for ( int j = 0; j <= i; j++ )
            {
                m_zerror_mu[i][j] = zerror_mu[i][j];
                m_zerror_mu[j][i] = zerror_mu[i][j];
            }
    }
    void setZHelixK( const Double_t zhelix_k[5] ) {
        for ( int i = 0; i < 5; i++ ) m_zhelix_k[i] = zhelix_k[i];
    }
    void setZErrorK( const Double_t zerror_k[5][5] ) {
        for ( int i = 0; i < 5; i++ )
            for ( int j = 0; j <= i; j++ )
            {
                m_zerror_k[i][j] = zerror_k[i][j];
                m_zerror_k[j][i] = zerror_k[i][j];
            }
    }
    void setZHelixP( const Double_t zhelix_p[5] ) {
        for ( int i = 0; i < 5; i++ ) m_zhelix_p[i] = zhelix_p[i];
    }
    void setZErrorP( const Double_t zerror_p[5][5] ) {
        for ( int i = 0; i < 5; i++ )
            for ( int j = 0; j <= i; j++ )
            {
                m_zerror_p[i][j] = zerror_p[i][j];
                m_zerror_p[j][i] = zerror_p[i][j];
            }
    }

    // F
    void setFHelix( const Double_t fhelix[5] ) {
        for ( int i = 0; i < 5; i++ ) m_fhelix[i] = fhelix[i];
    }

    void setFError( const Double_t ferror[5][5] ) {
        for ( int i = 0; i < 5; i++ )
            for ( int j = 0; j <= i; j++ )
            {
                m_ferror[i][j] = ferror[i][j];
                m_ferror[j][i] = ferror[i][j];
            }
    }
    void setFHelixE( const Double_t fhelix_e[5] ) {
        for ( int i = 0; i < 5; i++ ) m_fhelix_e[i] = fhelix_e[i];
    }
    void setFErrorE( const Double_t ferror_e[5][5] ) {
        for ( int i = 0; i < 5; i++ )
            for ( int j = 0; j <= i; j++ )
            {
                m_ferror_e[i][j] = ferror_e[i][j];
                m_ferror_e[j][i] = ferror_e[i][j];
            }
    }
    void setFHelixMu( const Double_t fhelix_mu[5] ) {
        for ( int i = 0; i < 5; i++ ) m_fhelix_mu[i] = fhelix_mu[i];
    }
    void setFErrorMu( const Double_t ferror_mu[5][5] ) {
        for ( int i = 0; i < 5; i++ )
            for ( int j = 0; j <= i; j++ )
            {
                m_ferror_mu[i][j] = ferror_mu[i][j];
                m_ferror_mu[j][i] = ferror_mu[i][j];
            }
    }
    void setFHelixK( const Double_t fhelix_k[5] ) {
        for ( int i = 0; i < 5; i++ ) m_fhelix_k[i] = fhelix_k[i];
    }
    void setFErrorK( const Double_t ferror_k[5][5] ) {
        for ( int i = 0; i < 5; i++ )
            for ( int j = 0; j <= i; j++ )
            {
                m_ferror_k[i][j] = ferror_k[i][j];
                m_ferror_k[j][i] = ferror_k[i][j];
            }
    }
    void setFHelixP( const Double_t fhelix_p[5] ) {
        for ( int i = 0; i < 5; i++ ) m_fhelix_p[i] = fhelix_p[i];
    }
    void setFErrorP( const Double_t ferror_p[5][5] ) {
        for ( int i = 0; i < 5; i++ )
            for ( int j = 0; j <= i; j++ )
            {
                m_ferror_p[i][j] = ferror_p[i][j];
                m_ferror_p[j][i] = ferror_p[i][j];
            }
    }

    // L
    void setLHelix( const Double_t lhelix[5] ) {
        for ( int i = 0; i < 5; i++ ) m_lhelix[i] = lhelix[i];
    }
    void setLError( const Double_t lerror[5][5] ) {
        for ( int i = 0; i < 5; i++ )
            for ( int j = 0; j <= i; j++ )
            {
                m_lerror[i][j] = lerror[i][j];
                m_lerror[j][i] = lerror[i][j];
            }
    }
    void setLHelixE( const Double_t lhelix_e[5] ) {
        for ( int i = 0; i < 5; i++ ) m_lhelix_e[i] = lhelix_e[i];
    }

    void setLErrorE( const Double_t lerror_e[5][5] ) {
        for ( int i = 0; i < 5; i++ )
            for ( int j = 0; j <= i; j++ )
            {
                m_lerror_e[i][j] = lerror_e[i][j];
                m_lerror_e[j][i] = lerror_e[i][j];
            }
    }

    void setLHelixMu( const Double_t lhelix_mu[5] ) {
        for ( int i = 0; i < 5; i++ ) m_lhelix_mu[i] = lhelix_mu[i];
    }

    void setLErrorMu( const Double_t lerror_mu[5][5] ) {
        for ( int i = 0; i < 5; i++ )
            for ( int j = 0; j <= i; j++ )
            {
                m_lerror_mu[i][j] = lerror_mu[i][j];
                m_lerror_mu[j][i] = lerror_mu[i][j];
            }
    }

    void setLHelixK( const Double_t lhelix_k[5] ) {
        for ( int i = 0; i < 5; i++ ) m_lhelix_k[i] = lhelix_k[i];
    }

    void setLErrorK( const Double_t lerror_k[5][5] ) {
        for ( int i = 0; i < 5; i++ )
            for ( int j = 0; j <= i; j++ )
            {
                m_lerror_k[i][j] = lerror_k[i][j];
                m_lerror_k[j][i] = lerror_k[i][j];
            }
    }

    void setLHelixP( const Double_t lhelix_p[5] ) {
        for ( int i = 0; i < 5; i++ ) m_lhelix_p[i] = lhelix_p[i];
    }

    void setLErrorP( const Double_t lerror_p[5][5] ) {
        for ( int i = 0; i < 5; i++ )
            for ( int j = 0; j <= i; j++ )
            {
                m_lerror_p[i][j] = lerror_p[i][j];
                m_lerror_p[j][i] = lerror_p[i][j];
            }
    }

    void setTHelix( const Double_t thelix[5] ) {
        for ( int i = 0; i < 5; i++ ) m_thelix[i] = thelix[i];
    }
    void setTError( const Double_t terror[15] ) {
        for ( int i = 0; i < 15; i++ ) { m_terror[i] = terror[i]; }
    }

    void setPocaE( const Double_t poca_e[3] ) {
        for ( int i = 0; i < 3; i++ ) m_poca_e[i] = poca_e[i];
    }

    void setPocaMu( const Double_t poca_mu[3] ) {
        for ( int i = 0; i < 3; i++ ) m_poca_mu[i] = poca_mu[i];
    }

    void setPoca( const Double_t poca[3] ) {
        for ( int i = 0; i < 3; i++ ) m_poca[i] = poca[i];
    }

    void setPocaK( const Double_t poca_k[3] ) {
        for ( int i = 0; i < 3; i++ ) m_poca_k[i] = poca_k[i];
    }

    void setPocaP( const Double_t poca_p[3] ) {
        for ( int i = 0; i < 3; i++ ) m_poca_p[i] = poca_p[i];
    }

    void setLPointE( const Double_t lpoint_e[3] ) {
        for ( int i = 0; i < 3; i++ ) m_lpoint_e[i] = lpoint_e[i];
    }

    void setLPointMu( const Double_t lpoint_mu[3] ) {
        for ( int i = 0; i < 3; i++ ) m_lpoint_mu[i] = lpoint_mu[i];
    }

    void setLPoint( const Double_t lpoint[3] ) {
        for ( int i = 0; i < 3; i++ ) m_lpoint[i] = lpoint[i];
    }

    void setLPointK( const Double_t lpoint_k[3] ) {
        for ( int i = 0; i < 3; i++ ) m_lpoint_k[i] = lpoint_k[i];
    }

    void setLPointP( const Double_t lpoint_p[3] ) {
        for ( int i = 0; i < 3; i++ ) m_lpoint_p[i] = lpoint_p[i];
    }

    void setLPivotE( const Double_t lpivot_e[3] ) {
        for ( int i = 0; i < 3; i++ ) m_lpivot_e[i] = lpivot_e[i];
    }

    void setLPivotMu( const Double_t lpivot_mu[3] ) {
        for ( int i = 0; i < 3; i++ ) m_lpivot_mu[i] = lpivot_mu[i];
    }

    void setLPivot( const Double_t lpivot[3] ) {
        for ( int i = 0; i < 3; i++ ) m_lpivot[i] = lpivot[i];
    }

    void setLPivotK( const Double_t lpivot_k[3] ) {
        for ( int i = 0; i < 3; i++ ) m_lpivot_k[i] = lpivot_k[i];
    }

    void setLPivotP( const Double_t lpivot_p[3] ) {
        for ( int i = 0; i < 3; i++ ) m_lpivot_p[i] = lpivot_p[i];
    }

  private:
    Int_t m_trackId;      // Track Id wensp Add 2005-10-19
    Double_t m_mass[5];   // mass assumption during the fit
    Double_t m_length[5]; // track path length from closest point to coord. origin to the last
                          // hit
    Double_t m_tof[5];    // time of flight correspond to length;
    Double_t m_fiTerm[5]; // terminal phi
    Double_t m_pathSM[5];
    Int_t m_nhits[5];       // number of total hits contained
    Int_t m_nlayer[5];      // number of layer that track passed
    Int_t m_stat[2][5];     // status flag
    Double_t m_chisq[2][5]; // chi square of fit 0:filter 1:smoother
    Int_t m_ndf[2][5];      // degree of freedom for the fit 0:filter 1:smoother
    Int_t m_nSegs[5];       // number of segments

    Double_t m_poca[3];
    Double_t m_poca_e[3];
    Double_t m_poca_mu[3];
    Double_t m_poca_k[3];
    Double_t m_poca_p[3];

    Double_t m_lpoint[3];
    Double_t m_lpoint_e[3];
    Double_t m_lpoint_mu[3];
    Double_t m_lpoint_k[3];
    Double_t m_lpoint_p[3];

    Double_t m_lpivot[3];
    Double_t m_lpivot_e[3];
    Double_t m_lpivot_mu[3];
    Double_t m_lpivot_k[3];
    Double_t m_lpivot_p[3];

    Double_t m_zhelix[5];       // 5 track parameters at zero point for pi
    Double_t m_zerror[5][5];    // error matrix at zero point for pion
    Double_t m_zhelix_e[5];     // 5 track parameters at zero point for el
    Double_t m_zerror_e[5][5];  // error matrix at zero point for electron
    Double_t m_zhelix_mu[5];    // 5 track parameters at zero point for mu
    Double_t m_zerror_mu[5][5]; // error matrix at zero point  for muon   ;
    Double_t m_zhelix_k[5];     // 5 track parameters at zero point for ka
    Double_t m_zerror_k[5][5];  // error matrix at zero point for kaon
    Double_t m_zhelix_p[5];     // 5 track parameters at zero point for pr
    Double_t m_zerror_p[5][5];  // error matrix at zero point for proton

    Double_t m_fhelix[5];       // 5 track parameters at zero point for pi
    Double_t m_ferror[5][5];    // error matrix at zero point for pion
    Double_t m_fhelix_e[5];     // 5 track parameters at zero point for el
    Double_t m_ferror_e[5][5];  // error matrix at zero point for electron
    Double_t m_fhelix_mu[5];    // 5 track parameters at zero point for mu
    Double_t m_ferror_mu[5][5]; // error matrix at zero point  for muon   ;
    Double_t m_fhelix_k[5];     // 5 track parameters at zero point for ka
    Double_t m_ferror_k[5][5];  // error matrix at zero point for kaon
    Double_t m_fhelix_p[5];     // 5 track parameters at zero point for pr
    Double_t m_ferror_p[5][5];  // error matrix at zero point for proton

    Double_t m_lhelix[5];       // 5 track parameters at zero point for pi
    Double_t m_lerror[5][5];    // error matrix at zero point for pion
    Double_t m_lhelix_e[5];     // 5 track parameters at zero point for el
    Double_t m_lerror_e[5][5];  // error matrix at zero point for electron
    Double_t m_lhelix_mu[5];    // 5 track parameters at zero point for mu
    Double_t m_lerror_mu[5][5]; // error matrix at zero point  for muon   ;
    Double_t m_lhelix_k[5];     // 5 track parameters at zero point for ka
    Double_t m_lerror_k[5][5];  // error matrix at zero point for kaon
    Double_t m_lhelix_p[5];     // 5 track parameters at zero point for pr
    Double_t m_lerror_p[5][5];  // error matrix at zero point for proton

    Double_t m_thelix[5];  // 5 track parameters of track finding
    Double_t m_terror[15]; // error matrix of track finding

    ClassDef( TRecMdcKalTrack, 4 )
};

#endif
