#ifndef RootEventData_TMdcDedx_H
#define RootEventData_TMdcDedx_H 1

#include "TObject.h"

class TMdcDedx : public TObject {

  public:
    TMdcDedx();

    ~TMdcDedx();

    //   void Clear(Option_t *option ="");

    //   void PrInt_t(Option_t *option="") const;
    // get
    Int_t trackId() const { return m_trackId; }
    Int_t particleId() const { return m_particleId; }
    Int_t status() const { return m_status; }
    Int_t truncAlg() const { return m_trunc_alg; }
    // Double_t prob(Int_t i)  const { return m_prob[i]; }
    // Double_t chi(int i)        const { return m_chi[i]; } -> wrong, use chiE,...
    Double_t chi( int i ) const;
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

    // Double_t fracErrPH()        const { return m_fracErrPH; }

    //  Double_t minIronPH()       const { return m_minIronPH; }
    //  Double_t corrPH()          const { return m_corrPH; }

    // set
    void setTrackId( const Int_t trackId ) { m_trackId = trackId; }
    void setParticleId( const Int_t particleId ) { m_particleId = particleId; }
    void setStatus( const Int_t status ) { m_status = status; }
    void setTruncAlg( const Int_t trunc_alg ) { m_trunc_alg = trunc_alg; }
    /*
     void    setProb(const Double_t pb[5])  {
               for(Int_t i =0; i<5 ; i++) m_prob[i]= pb[i]; }
   */
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

    // o void   setChi( double* chi)  {
    // o   for(int i =0; i<5 ; i++) m_chi[i]= chi[i];
    // o }

    // void   setFracErrPH(const Double_t fracErrPH)        { m_fracErrPH = fracErrPH; }
    // void   setMinIronPH(const Double_t minIronPH)        { m_minIronPH = minIronPH; }
    // void   setCorrPH(const Double_t corrPH)              { m_corrPH = corrPH; }

  private:
    Int_t m_trackId;    // Track Id wensp Add 2005-10-19
    Int_t m_particleId; // Particle ID from De/Dx fit
    Int_t m_status;     // Status
    Int_t m_trunc_alg;  // truncate method
    // Double_t m_prob[5];       //Probility // Changed on Oct. 10 following by Wangdy
    Double_t m_chiE;      // Number of sigama from e
    Double_t m_chiMu;     // Number of sigama from muon
    Double_t m_chiPi;     // Number of sigama from pion
    Double_t m_chiK;      // Number of sigama from k
    Double_t m_chiP;      // Number of sigama from p
    Int_t m_numGoodHits;  // No. of good de/dx hits(exclude overflow)
    Int_t m_numTotalHits; // No. of good de/dx hits(include overflow)
    Double_t m_probPH;    // Most probable pulse height from truncated mean
    Double_t m_normPH;    // normalizd pulse height // Changed on Oct. 10 following by Wangdy
    Double_t m_errorPH;   // resolution of truncated mean
    Double_t m_twentyPH;  // de/dx value of bitrunction rate equal to 20%
    // o Double_t m_chi[5]; //Number of Chi_dEdx for different particles

    // Double_t m_fracErrPH;     //Fractional uncertaInt_ty on measured pulse height // Changed
    // on Oct. 10 following by Wangdy
    //  Double_t m_minIronPH;     //Average pulse height for min-I
    //  Double_t m_corrPH;        //Corrected pulse heights

    ClassDef( TMdcDedx, 5 )
};

#endif
