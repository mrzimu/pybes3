#ifndef DigiRootData_TMcHitMdc_H
#define DigiRootData_TMcHitMdc_H 1

#include "TObject.h"
#include "TString.h"
#include "TVector3.h"

class TMcHitMdc : public TObject {

  public:
    TMcHitMdc();

    ~TMcHitMdc();

    void SetTrackID( Int_t track ) { trackID = track; };
    void SetLayerNo( Int_t layer ) { layerNo = layer; };
    void SetCellNo( Int_t cell ) { cellNo = cell; };
    void SetEdep( Double_t de ) { edep = de; };
    void SetPos( TVector3 xyz ) { pos = xyz; };
    void SetDriftD( Double_t distance ) { driftD = distance; };
    void SetDriftT( Double_t time ) { driftT = time; };
    void SetGlobalT( Double_t time ) { globalT = time; };
    void SetTheta( Double_t angle ) { theta = angle; };
    void SetEnterAngle( Double_t angle ) { enterAngle = angle; };
    void SetPosFlag( Int_t flag ) { posFlag = flag; };

    Int_t GetTrackID() const { return trackID; };
    Int_t GetLayerNo() const { return layerNo; };
    Int_t GetCellNo() const { return cellNo; };
    Double_t GetEdep() const { return edep; };
    TVector3 GetPos() const { return pos; };
    Double_t GetDriftD() const { return driftD; };
    Double_t GetDriftT() const { return driftT; };
    Double_t GetGlobalT() const { return globalT; };
    Double_t GetTheta() const { return theta; };
    Double_t GetEnterAngle() const { return enterAngle; };
    Int_t GetPosFlag() const { return posFlag; };

  private:
    Int_t trackID;
    Int_t layerNo;
    Int_t cellNo;
    Double_t edep;
    TVector3 pos;
    Double_t driftD;
    Double_t driftT;
    Double_t globalT;
    Double_t theta;
    Double_t enterAngle;
    Int_t posFlag;

    ClassDef( TMcHitMdc, 1 )
};

#endif
