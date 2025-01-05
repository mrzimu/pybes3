#ifndef DigiRootData_TMcDigiEmc_H
#define DigiRootData_TMcDigiEmc_H 1

#include "TObject.h"
#include "TString.h"
#include "TVector3.h"

class TMcDigiEmc : public TObject {

  public:
    TMcDigiEmc();

    ~TMcDigiEmc();

    void SetPartId( Int_t id ) { m_partId = id; };
    void SetThetaNb( Int_t nTheta ) { m_nTheta = nTheta; };
    void SetPhiNb( Int_t nPhi ) { m_nPhi = nPhi; };
    void SetEnergy( Double_t energy ) { m_energy = energy; };
    void SetTime( Double_t time ) { m_time = time; };
    void SetTrackIndex( Int_t index ) { m_trackIndex = index; };
    // void SetWaveform(BesEmcWaveform* wave) { digiWaveform = wave; };

    Int_t GetPartId() const { return m_partId; };
    Int_t GetThetaNb() const { return m_nTheta; };
    Int_t GetPhiNb() const { return m_nPhi; };
    Double_t GetEnergy() const { return m_energy; };
    Double_t GetTime() const { return m_time; };
    Int_t GetTrackIndex() const { return m_trackIndex; };
    // BesEmcWaveform* GetWaveform(){ return digiWaveform; };

  private:
    // BesEmcWaveform* digiWaveform;
    Int_t m_partId;
    Int_t m_nTheta;
    Int_t m_nPhi;
    Double_t m_energy;
    Double_t m_time;
    Int_t m_trackIndex;

    ClassDef( TMcDigiEmc, 1 )
};

#endif
