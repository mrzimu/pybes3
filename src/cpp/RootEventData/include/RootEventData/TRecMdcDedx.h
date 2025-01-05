#ifndef RootEventData_TRecMdcDedx_H
#define RootEventData_TRecMdcDedx_H 1

#include "TObject.h"

class TRecMdcDedx : public TObject {

  public:
    TRecMdcDedx();

    ~TRecMdcDedx();

    //   void Clear(Option_t *option ="");

    //   void PrInt_t(Option_t *option="") const;
    // get
    Int_t mdcTrackId() const { return m_mdcTrackId; }
    Int_t mdcKalTrackId() const { return m_mdcKalTrackId; }
    Int_t trackId() const { return m_trackId; }
    Int_t particleId() const { return m_particleId; }
    Int_t status() const { return m_status; }
    Int_t truncAlg() const { return m_trunc_alg; }
    // Double_t prob(Int_t i)  const { return m_prob[i]; }
    Double_t chi( int i ) const { return m_chi[i]; }
    Double_t chiE() const { return m_chiE; }
    Double_t chiMu() const { return m_chiMu; }
    Double_t chiPi() const { return m_chiPi; }
    Double_t chiK() const { return m_chiK; }
    Double_t chiP() const { return m_chiP; }

    Int_t numGoodHits() const { return m_numGoodHits; }
    Int_t numTotalHits() const { return m_numTotalHits; }

    Double_t probPH() const { return m_probPH; }
    Double_t normPH() const { return m_normPH; }
    Double_t errorPH() const { return m_errorPH; }
    Double_t twentyPH() const { return m_twentyPH; }

    Double_t dedxExpect( int pid ) const { return m_dedx_exp[pid]; }
    Double_t sigmaDedx( int pid ) const { return m_sigma_dedx[pid]; }
    Double_t pidProb( int pid ) const { return m_pid_prob[pid]; }

    Double_t dedxHit() const { return m_dedx_hit; }
    Double_t dedxEsat() const { return m_dedx_esat; }
    Double_t dedxNoRun() const { return m_dedx_norun; }
    Double_t dedxMoment() const { return m_dedx_momentum; }

    // set
    void setDedxHit( const Double_t dedx_hit ) { m_dedx_hit = dedx_hit; }
    void setDedxEsat( const Double_t dedx_esat ) { m_dedx_esat = dedx_esat; }
    void setDedxNoRun( const Double_t dedx_norun ) { m_dedx_norun = dedx_norun; }
    void setDedxMoment( const Double_t dedx_momentum ) { m_dedx_momentum = dedx_momentum; }

    void setMdcTrackId( const int mdcTrackId ) { m_mdcTrackId = mdcTrackId; }
    void setMdcKalTrackId( const int mdcKalTrackId ) { m_mdcKalTrackId = mdcKalTrackId; }
    void setTrackId( const Int_t trackId ) { m_trackId = trackId; }
    void setParticleId( const Int_t particleId ) { m_particleId = particleId; }
    void setStatus( const Int_t status ) { m_status = status; }
    void setTruncAlg( const Int_t trunc_alg ) { m_trunc_alg = trunc_alg; }

    void setChiE( const Double_t chiE ) { m_chiE = chiE; }
    void setChiMu( const Double_t chiMu ) { m_chiMu = chiMu; }
    void setChiPi( const Double_t chiPi ) { m_chiPi = chiPi; }
    void setChiK( const Double_t chiK ) { m_chiK = chiK; }
    void setChiP( const Double_t chiP ) { m_chiP = chiP; }

    void setNumGoodHits( const Int_t numGoodHits ) { m_numGoodHits = numGoodHits; }
    void setNumTotalHits( const Int_t numTotalHits ) { m_numTotalHits = numTotalHits; }

    void setProbPH( const Double_t probPH ) { m_probPH = probPH; }
    void setNormPH( const Double_t normPH ) { m_normPH = normPH; }
    void setErrorPH( const Double_t errorPH ) { m_errorPH = errorPH; }
    void setTwentyPH( const Double_t twentyPH ) { m_twentyPH = twentyPH; }

    void setChi( double* chi ) {
        for ( int i = 0; i < 5; i++ ) m_chi[i] = chi[i];
    }

    void setDedxExpect( double* dedx_exp ) {
        for ( int i = 0; i < 5; i++ ) m_dedx_exp[i] = dedx_exp[i];
    }
    void setSigmaDedx( double* sigma_dedx ) {
        for ( int i = 0; i < 5; i++ ) m_sigma_dedx[i] = sigma_dedx[i];
    }
    void setPidProb( double* pid_prob ) {
        for ( int i = 0; i < 5; i++ ) m_pid_prob[i] = pid_prob[i];
    }

  private:
    Double_t m_dedx_hit;      // double trucation mean of hit-level calib
    Double_t m_dedx_esat;     // double trucation mean of hit-level+electron saturation calib
    Double_t m_dedx_norun;    // double trucation mean of no run gain calib
    Double_t m_dedx_momentum; // dE/dx calib used momentum

    Int_t m_trackId; // Track Id wensp Add 2005-10-19
    Int_t m_mdcTrackId;
    Int_t m_mdcKalTrackId;
    Int_t m_particleId; // Particle ID from De/Dx fit
    Int_t m_status;     // Status
    Int_t m_trunc_alg;  // truncate method

    // Double_t m_prob[5];       //Probility // Changed on Oct. 10 following by Wangdy
    Double_t m_chiE;        // Number of sigama from e
    Double_t m_chiMu;       // Number of sigama from muon
    Double_t m_chiPi;       // Number of sigama from pion
    Double_t m_chiK;        // Number of sigama from k
    Double_t m_chiP;        // Number of sigama from p
    Int_t m_numGoodHits;    // No. of good de/dx hits(exclude overflow)
    Int_t m_numTotalHits;   // No. of good de/dx hits(include overflow)
    Double_t m_probPH;      // Most probable pulse height from truncated mean
    Double_t m_normPH;      // normalizd pulse height // Changed on Oct. 10 following by Wangdy
    Double_t m_errorPH;     // resolution of truncated mean
    Double_t m_twentyPH;    // de/dx value of bitrunction rate equal to 20%
    Double_t m_chi[5];      // Number of Chi_dEdx for different particles
                            // 0: e  1: mu   2: pi  3: K  4:P
    Double_t m_dedx_exp[5]; // expected value of dE/dx for 5 particle hypotheses
    Double_t m_sigma_dedx[5]; // sigma value of dE/dx for 5 particle hypotheses
    Double_t m_pid_prob[5];   // probability for each of  the 5 particle hypotheses

    ClassDef( TRecMdcDedx, 5 )
};

#endif
