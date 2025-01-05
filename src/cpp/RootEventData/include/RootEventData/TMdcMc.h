#ifndef RootEventData_TMdcMc_H
#define RootEventData_TMdcMc_H 1

#include "TObject.h"
#include "TString.h"
// #include <vector>
// using namespace std;

class TMdcMc : public TObject {

  public:
    TMdcMc();
    ~TMdcMc();
    // Get
    //  Get associated id
    UInt_t getId() const { return m_id; }

    // Get the associated track id
    UInt_t getTrackIndex() const { return m_trackIndex; }

    // Get the associated current track PID
    Int_t getCurrentTrackPID() const { return m_currentTrackPID; }

    // Get is secondary
    Double_t getIsSecondary() const { return m_isSecondary; }

    // Get the position x
    Double_t getPositionX() const { return m_xPosition; }

    // Get the position y
    Double_t getPositionY() const { return m_yPosition; }

    // Get the position z
    Double_t getPositionZ() const { return m_zPosition; }

    // Get the momentum x
    Double_t getMomentumX() const { return m_xMomentum; }

    // Get the momentum y
    Double_t getMomentumY() const { return m_yMomentum; }

    // Get the momentum z
    Double_t getMomentumZ() const { return m_zMomentum; }

    // Get Drift Distance
    Double_t getDriftDistance() const { return m_driftDistance; }

    // Get the total deposited energy
    Double_t getDepositEnergy() const { return m_depositEnergy; }

    // Get the position flag
    Int_t getPositionFlag() const { return m_posFlag; }

    // Get the flight length
    Double_t getFlightLength() const { return m_flightLength; }

    // Get the creator process
    TString getCreatorProcess() const { return m_creatorProcess; }

    // Get the creator process
    Int_t getDigiIdx() const { return m_digiIdx; }

    // Set
    void setId( UInt_t id ) { m_id = id; }
    void setTrackIndex( UInt_t trackIndex ) { m_trackIndex = trackIndex; }
    void setCurrentTrackPID( Int_t currentTrackPID ) { m_currentTrackPID = currentTrackPID; }
    void setIsSecondary( Int_t isSecondary ) { m_isSecondary = isSecondary; }
    void setPositionX( Double_t positionX ) { m_xPosition = positionX; }
    void setPositionY( Double_t positionY ) { m_yPosition = positionY; }
    void setPositionZ( Double_t positionZ ) { m_zPosition = positionZ; }
    void setMomentumX( Double_t momentumX ) { m_xMomentum = momentumX; }
    void setMomentumY( Double_t momentumY ) { m_yMomentum = momentumY; }
    void setMomentumZ( Double_t momentumZ ) { m_zMomentum = momentumZ; }
    void setDriftDistance( Double_t driftDistance ) { m_driftDistance = driftDistance; }
    void setDepositEnergy( Double_t depositEnergy ) { m_depositEnergy = depositEnergy; }
    void setPositionFlag( Int_t posFlag ) { m_posFlag = posFlag; }
    void setFlightLength( Double_t flightLength ) { m_flightLength = flightLength; }
    void setCreatorProcess( TString creatorProcess ) { m_creatorProcess = creatorProcess; }

    void setDigiIdx( int digiIdx ) { m_digiIdx = digiIdx; }

  private:
    UInt_t m_id;

    UInt_t m_trackIndex;

    Int_t m_currentTrackPID;

    Int_t m_isSecondary;

    Double_t m_xPosition;

    Double_t m_yPosition;

    Double_t m_zPosition;

    Double_t m_xMomentum;

    Double_t m_yMomentum;

    Double_t m_zMomentum;

    Double_t m_driftDistance;

    Double_t m_depositEnergy;

    Int_t m_posFlag;

    Double_t m_flightLength;

    TString m_creatorProcess;

    Int_t m_digiIdx;

    ClassDef( TMdcMc, 2 )
};

#endif // TrackRootData_TMdcMc_H
