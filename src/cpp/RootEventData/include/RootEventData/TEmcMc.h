#ifndef RootEventData_TEmcMc_H
#define RootEventData_TEmcMc_H 1

#include "TObject.h"
#include <map>

// #include <vector>
// using namespace std;

class TEmcMc : public TObject {

  public:
    TEmcMc();
    ~TEmcMc();
    // Get

    // Get Hit_Map
    std::map<Int_t, Double_t> getHitMap() const { return m_hitMap; }

    // Get whether or not hit on EMC
    int getHitEmc() const { return m_hitEmc; }

    // Get pdg id
    int getPDGCode() const { return m_PDGCode; }

    // Get pdg charge
    double getPDGCharge() const { return m_PDGCharge; }

    // Get crystal or dead time
    double getTime() const { return m_time; }

    // Get associated id
    UInt_t getId() const { return m_id; }

    // Get the associated track id
    UInt_t getTrackIndex() const { return m_trackIndex; }

    // Get the position x
    Double_t getPositionX() const { return m_xPosition; }

    // Get the position y
    Double_t getPositionY() const { return m_yPosition; }

    // Get the position z
    Double_t getPositionZ() const { return m_zPosition; }

    // Get momentum Px
    Double_t getPx() const { return m_px; }

    // Get momentum Py
    Double_t getPy() const { return m_py; }

    // Get momentum Pz
    Double_t getPz() const { return m_pz; }

    // Get the total deposited energy
    Double_t getDepositEnergy() const { return m_depositEnergy; }

    // Set

    void setHitMap( std::map<Int_t, Double_t> hitMap ) { m_hitMap = hitMap; }
    void setHitEmc( int hitEmc ) { m_hitEmc = hitEmc; }
    void setPDGCode( int PDGCode ) { m_PDGCode = PDGCode; }
    void setPDGCharge( double PDGCharge ) { m_PDGCharge = PDGCharge; }
    void setTime( double time ) { m_time = time; }

    void setId( UInt_t id ) { m_id = id; }
    void setTrackIndex( UInt_t trackIndex ) { m_trackIndex = trackIndex; }
    void setPositionX( Double_t positionX ) { m_xPosition = positionX; }
    void setPositionY( Double_t positionY ) { m_yPosition = positionY; }
    void setPositionZ( Double_t positionZ ) { m_zPosition = positionZ; }
    void setPx( Double_t px ) { m_px = px; }
    void setPy( Double_t py ) { m_py = py; }
    void setPz( Double_t pz ) { m_pz = pz; }
    void setDepositEnergy( Double_t depositEnergy ) { m_depositEnergy = depositEnergy; }

  private:
    // whether hit Emc
    Int_t m_hitEmc;
    // particle ID
    Int_t m_PDGCode;
    // particle charge;
    Double_t m_PDGCharge;
    // hit crystal time or dead time
    Double_t m_time;

    UInt_t m_id;

    UInt_t m_trackIndex;

    Double_t m_xPosition;

    Double_t m_yPosition;

    Double_t m_zPosition;

    Double_t m_px;

    Double_t m_py;

    Double_t m_pz;

    Double_t m_depositEnergy;

    std::map<Int_t, Double_t> m_hitMap;

    ClassDef( TEmcMc, 1 )
};

#endif // TrackRootData_TEmcMc_H
