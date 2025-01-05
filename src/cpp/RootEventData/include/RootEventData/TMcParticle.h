#ifndef RootEventData_TMcParticle_H
#define RootEventData_TMcParticle_H 1

#include "TObject.h"
#include <vector>

using namespace std;

class TMcParticle : public TObject {

  public:
    TMcParticle();
    ~TMcParticle();
    // Get
    //  Get associated id
    Int_t getParticleID() const { return m_particleID; }

    // Get the track id
    Int_t getTrackIndex() const { return m_trackIndex; }

    // Get the index for the vertex where the particle starts
    Int_t getVertexIndex0() const { return m_vertexIndex0; }

    // Get the index for the vertex where the particle stops
    Int_t getVertexIndex1() const { return m_vertexIndex1; }

    // Get Bit-field status flag
    UInt_t getStatusFlags() const { return m_statusFlags; }

    // Get the initial position x
    Double_t getInitialPositionX() const { return m_xInitialPosition; }

    // Get the initial position y
    Double_t getInitialPositionY() const { return m_yInitialPosition; }

    // Get the initial position z
    Double_t getInitialPositionZ() const { return m_zInitialPosition; }

    // Get the initial position time
    Double_t getInitialPositionT() const { return m_tInitialPosition; }

    // Get the final position x
    Double_t getFinalPositionX() const { return m_xFinalPosition; }

    // Get the final position y
    Double_t getFinalPositionY() const { return m_yFinalPosition; }

    // Get the final position z
    Double_t getFinalPositionZ() const { return m_zFinalPosition; }

    // Get the final position time
    Double_t getFinalPositionT() const { return m_tFinalPosition; }

    // Get the initial momentum x
    Double_t getInitialMomentumX() const { return m_xInitialMomentum; }

    // Get the initial momentum y
    Double_t getInitialMomentumY() const { return m_yInitialMomentum; }

    // Get the initial momentum z
    Double_t getInitialMomentumZ() const { return m_zInitialMomentum; }

    // Get the initial momentum energy
    Double_t getInitialMomentumE() const { return m_eInitialMomentum; }

    // Get the final momentum x
    // Double_t getFinalMomentumX() const {return m_xFinalMomentum;}

    // Get the final momentum y
    // Double_t getFinalMomentumY() const {return m_yFinalMomentum;}

    // Get the final momentum z
    // Double_t getFinalMomentumZ() const {return m_zFinalMomentum;}

    // Get the final momentum energy
    // Double_t getFinalMomentumE() const {return m_eFinalMomentum;}

    //   Bool_t primaryParticle() const;

    // Get mother index
    Int_t getMother() const { return m_mother; }

    // Get daughters index
    vector<Int_t> getDaughters() const { return m_daughters; }

    // helper functions ported from McTruth
    enum StatusBits {
        DECAYED  = 1,      //! Decayed by generator
        DECAYFLT = 1 << 1, //! Decayed in flight
        PRIMARY  = 1 << 2, //! primary particle
        LEAF     = 1 << 3, //! this particle is a leaf in the particle tree
        ERROR    = 1 << 4  //! error
                           // MISSED=  1<<2,  //! Does not hit detector
                           // NOINTER =1<<3,  //! Traverses detector w/o interacting
                           // STOPPED =1<<4,  //! Energy below cut; other bits may say why
                           // INTERACT=1<<5,  //! Interacted, no further decision to be made
        // INTSHDEP=1<<6,  //! Interacted, further decision depends on ! selection of shower
        // deposition PRIMARY =1<<7,  //! primary particle SWERROR =1<<8,  //! Error occurred
        // in swimming the track BCKSPL=1<<9,    //! The particle is backsplashed from the CAL
        // back in the TKR region POSHIT =1<<10,     //! The particle released a hit a
        // PositionHit detector NOTTRACK=1<<11, //! Not tracked by user request Swum =   1<<12,
        // //! this particle was produced by the swimmer LEAF = 1<<13     //! this particle is
        // a leaf in the particle tree
    };

    // Retrieve whether this is a primary particle
    bool primaryParticle() const { return ( m_statusFlags & PRIMARY ) == PRIMARY; }
    // Retrieve whether this is a leave particle
    bool leafParticle() const { return ( m_statusFlags & LEAF ) == LEAF; }
    // Retrieve whether decayed from generator
    bool decayFromGenerator() const { return ( m_statusFlags & DECAYED ) == DECAYED; }
    // Retrieve wheter decayed in flight
    bool decayInFlight() const { return ( m_statusFlags & DECAYFLT ) == DECAYFLT; }

    // Set
    void setParticleID( Int_t particleID ) { m_particleID = particleID; }
    void setTrackIndex( Int_t trackIndex ) { m_trackIndex = trackIndex; }

    void setVertexIndex0( Int_t vertexIndex0 ) { m_vertexIndex0 = vertexIndex0; }
    void setVertexIndex1( Int_t vertexIndex1 ) { m_vertexIndex1 = vertexIndex1; }
    void setStatusFlags( UInt_t statusFlags ) { m_statusFlags = statusFlags; }

    void setInitialPositionX( Double_t positionX ) { m_xInitialPosition = positionX; }
    void setInitialPositionY( Double_t positionY ) { m_yInitialPosition = positionY; }
    void setInitialPositionZ( Double_t positionZ ) { m_zInitialPosition = positionZ; }
    void setInitialPositionT( Double_t positionT ) { m_tInitialPosition = positionT; }

    void setFinalPositionX( Double_t positionX ) { m_xFinalPosition = positionX; }
    void setFinalPositionY( Double_t positionY ) { m_yFinalPosition = positionY; }
    void setFinalPositionZ( Double_t positionZ ) { m_zFinalPosition = positionZ; }
    void setFinalPositionT( Double_t positionT ) { m_tFinalPosition = positionT; }

    void setInitialMomentumX( Double_t momentumX ) { m_xInitialMomentum = momentumX; }
    void setInitialMomentumY( Double_t momentumY ) { m_yInitialMomentum = momentumY; }
    void setInitialMomentumZ( Double_t momentumZ ) { m_zInitialMomentum = momentumZ; }
    void setInitialMomentumE( Double_t momentumE ) { m_eInitialMomentum = momentumE; }

    // void setFinalMomentumX(Double_t momentumX) {m_xFinalMomentum = momentumX;}
    // void setFinalMomentumY(Double_t momentumY) {m_yFinalMomentum = momentumY;}
    // void setFinalMomentumZ(Double_t momentumZ) {m_zFinalMomentum = momentumZ;}
    // void setFinalMomentumE(Double_t momentumE) {m_eFinalMomentum = momentumE;}

    void setMother( Int_t mother ) { m_mother = mother; }
    void setDaughters( vector<Int_t>& daughters ) { m_daughters = daughters; }

  private:
    Int_t m_particleID;

    Int_t m_trackIndex;

    Int_t m_vertexIndex0;

    Int_t m_vertexIndex1;

    UInt_t m_statusFlags;

    Double_t m_xInitialPosition;
    Double_t m_yInitialPosition;
    Double_t m_zInitialPosition;
    Double_t m_tInitialPosition;

    Double_t m_xFinalPosition;
    Double_t m_yFinalPosition;
    Double_t m_zFinalPosition;
    Double_t m_tFinalPosition;

    Double_t m_xInitialMomentum;
    Double_t m_yInitialMomentum;
    Double_t m_zInitialMomentum;
    Double_t m_eInitialMomentum;

    // Double_t m_xFinalMomentum;
    // Double_t m_yFinalMomentum;
    // Double_t m_zFinalMomentum;
    // Double_t m_eFinalMomentum;

    Int_t m_mother;
    vector<Int_t> m_daughters;

    ClassDef( TMcParticle, 1 )
};

#endif // TrackRootData_TMcParticle_H
