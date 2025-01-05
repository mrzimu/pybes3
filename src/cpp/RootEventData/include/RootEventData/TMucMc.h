#ifndef RootEventData_TMucMc_H
#define RootEventData_TMucMc_H 1

#include "TObject.h"
// #include <vector>
// using namespace std;

class TMucMc : public TObject {

  public:
    TMucMc();
    ~TMucMc();
    // Get
    //  Get associated id
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

    // Set
    void setId( UInt_t id ) { m_id = id; }
    void setTrackIndex( UInt_t trackIndex ) { m_trackIndex = trackIndex; }
    void setPositionX( Double_t positionX ) { m_xPosition = positionX; }
    void setPositionY( Double_t positionY ) { m_yPosition = positionY; }
    void setPositionZ( Double_t positionZ ) { m_zPosition = positionZ; }
    void setPx( Double_t px ) { m_px = px; }
    void setPy( Double_t py ) { m_py = py; }
    void setPz( Double_t pz ) { m_pz = pz; }

  private:
    UInt_t m_id;

    UInt_t m_trackIndex;

    Double_t m_xPosition;

    Double_t m_yPosition;

    Double_t m_zPosition;

    Double_t m_px;

    Double_t m_py;

    Double_t m_pz;

    Double_t m_depositEnergy;

    ClassDef( TMucMc, 1 )
};

#endif // TrackRootData_TMucMc_H
