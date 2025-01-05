#ifndef DigiRootData_TMcHitTof_H
#define DigiRootData_TMcHitTof_H 1

#include "TObject.h"
#include "TString.h"
#include "TVector3.h"

class TMcHitTof : public TObject {

  public:
    TMcHitTof();

    ~TMcHitTof();

    void SetTrackIndex( Int_t trackIndex ) { m_trackIndex = trackIndex; };
    void SetG4Index( Int_t index ) { m_g4Index = index; }
    void SetPartId( Int_t partId ) { m_partId = partId; }
    void SetScinNb( Int_t scinNb ) { m_scinNb = scinNb; }
    void SetEdep( Double_t edep ) { m_edep = edep; }
    void SetStepL( Double_t stepL ) { m_stepL = stepL; }
    void SetTrackL( Double_t length ) { m_trackL = length; }
    void SetPos( TVector3 pos ) { m_pos = pos; }
    void SetTime( Double_t time ) { m_time = time; }
    void SetDeltaT( Double_t deltaT ) { m_deltaT = deltaT; }
    void SetPDirection( TVector3 pDirection ) { m_pDirection = pDirection; }
    void SetMomentum( TVector3 momentum ) { m_momentum = momentum; }
    void SetCharge( Int_t charge ) { m_charge = charge; }

    Int_t GetTrackIndex() const { return m_trackIndex; }
    Int_t GetG4Index() const { return m_g4Index; }
    Int_t GetPartId() const { return m_partId; }
    Int_t GetScinNb() const { return m_scinNb; }
    Double_t GetEdep() const { return m_edep; }
    Double_t GetStepL() const { return m_stepL; }
    Double_t GetTrackL() const { return m_trackL; }
    TVector3 GetPos() const { return m_pos; }
    Double_t GetTime() const { return m_time; }
    Double_t GetDeltaT() const { return m_deltaT; }
    TVector3 GetPDirection() const { return m_pDirection; }
    TVector3 GetMomentum() const { return m_momentum; }
    Int_t GetCharge() const { return m_charge; }

  private:
    // static Int_t s_count;

    Int_t m_trackIndex;
    Int_t m_g4Index;
    Int_t m_partId;
    Int_t m_scinNb;
    Double_t m_edep;
    Double_t m_stepL;
    Double_t m_trackL;
    TVector3 m_pos;
    Double_t m_time;
    Double_t m_deltaT;
    TVector3 m_pDirection;
    TVector3 m_momentum;
    Int_t m_charge;

    ClassDef( TMcHitTof, 1 )
};

#endif
