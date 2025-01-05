#ifndef RootEventData_TExtTrack_H
#define RootEventData_TExtTrack_H 1

#include "SimMatr.h"
#include "TObject.h"
#include "TString.h"
// using namespace std;

class TExtTrack : public TObject {

  public:
    TExtTrack();

    ~TExtTrack();

    // modifiers
    void SetTrackId( const Int_t trackId ) { m_trackId = trackId; }
    // Tof layer1:
    void SetTof1PositionX( const Double_t Tof1PositionX ) { myTof1PositionX = Tof1PositionX; }
    void SetTof1PositionY( const Double_t Tof1PositionY ) { myTof1PositionY = Tof1PositionY; }
    void SetTof1PositionZ( const Double_t Tof1PositionZ ) { myTof1PositionZ = Tof1PositionZ; }
    void SetTof1MomentumX( const Double_t Tof1MomentumX ) { myTof1MomentumX = Tof1MomentumX; }
    void SetTof1MomentumY( const Double_t Tof1MomentumY ) { myTof1MomentumY = Tof1MomentumY; }
    void SetTof1MomentumZ( const Double_t Tof1MomentumZ ) { myTof1MomentumZ = Tof1MomentumZ; }

    void SetTof1VolumeName( const TString Tof1VolumeName ) {
        myTof1VolumeName = Tof1VolumeName;
    }
    void SetTof1VolumeNumber( const Int_t Tof1VolumeNumber ) {
        myTof1VolumeNumber = Tof1VolumeNumber;
    }
    void SetTof1( const Double_t Tof1 ) { myTof1 = Tof1; }
    void SetTof1Path( const Double_t Tof1Path ) { myTof1Path = Tof1Path; }
    void SetTof1PosSigmaAlongZ( const Double_t Tof1PosSigmaAlongZ ) {
        myTof1PosSigmaAlongZ = Tof1PosSigmaAlongZ;
    }
    void SetTof1PosSigmaAlongT( const Double_t Tof1PosSigmaAlongT ) {
        myTof1PosSigmaAlongT = Tof1PosSigmaAlongT;
    }
    void SetTof1PosSigmaAlongX( const Double_t Tof1PosSigmaAlongX ) {
        myTof1PosSigmaAlongX = Tof1PosSigmaAlongX;
    }
    void SetTof1PosSigmaAlongY( const Double_t Tof1PosSigmaAlongY ) {
        myTof1PosSigmaAlongY = Tof1PosSigmaAlongY;
    }
    void SetTof1ErrorMatrix( const Double_t Tof1ErrorMatrix[6][6] ) {
        SimMat::pack2d( 6, &Tof1ErrorMatrix[0][0], myTof1ErrorMatrix );
    }

    // Tof layer2:
    void SetTof2PositionX( const Double_t Tof2PositionX ) { myTof2PositionX = Tof2PositionX; }
    void SetTof2PositionY( const Double_t Tof2PositionY ) { myTof2PositionY = Tof2PositionY; }
    void SetTof2PositionZ( const Double_t Tof2PositionZ ) { myTof2PositionZ = Tof2PositionZ; }
    void SetTof2MomentumX( const Double_t Tof2MomentumX ) { myTof2MomentumX = Tof2MomentumX; }
    void SetTof2MomentumY( const Double_t Tof2MomentumY ) { myTof2MomentumY = Tof2MomentumY; }
    void SetTof2MomentumZ( const Double_t Tof2MomentumZ ) { myTof2MomentumZ = Tof2MomentumZ; }

    void SetTof2VolumeName( const TString Tof2VolumeName ) {
        myTof2VolumeName = Tof2VolumeName;
    }
    void SetTof2VolumeNumber( const Int_t Tof2VolumeNumber ) {
        myTof2VolumeNumber = Tof2VolumeNumber;
    }
    void SetTof2( const Double_t Tof2 ) { myTof2 = Tof2; }
    void SetTof2Path( const Double_t Tof2Path ) { myTof2Path = Tof2Path; }
    void SetTof2PosSigmaAlongZ( const Double_t Tof2PosSigmaAlongZ ) {
        myTof2PosSigmaAlongZ = Tof2PosSigmaAlongZ;
    }
    void SetTof2PosSigmaAlongT( const Double_t Tof2PosSigmaAlongT ) {
        myTof2PosSigmaAlongT = Tof2PosSigmaAlongT;
    }
    void SetTof2PosSigmaAlongX( const Double_t Tof2PosSigmaAlongX ) {
        myTof2PosSigmaAlongX = Tof2PosSigmaAlongX;
    }
    void SetTof2PosSigmaAlongY( const Double_t Tof2PosSigmaAlongY ) {
        myTof2PosSigmaAlongY = Tof2PosSigmaAlongY;
    }
    void SetTof2ErrorMatrix( const Double_t Tof2ErrorMatrix[6][6] ) {
        SimMat::pack2d( 6, &Tof2ErrorMatrix[0][0], myTof2ErrorMatrix );
    }

    // Emc:
    void SetEmcPositionX( const Double_t EmcPositionX ) { myEmcPositionX = EmcPositionX; }
    void SetEmcPositionY( const Double_t EmcPositionY ) { myEmcPositionY = EmcPositionY; }
    void SetEmcPositionZ( const Double_t EmcPositionZ ) { myEmcPositionZ = EmcPositionZ; }
    void SetEmcMomentumX( const Double_t EmcMomentumX ) { myEmcMomentumX = EmcMomentumX; }
    void SetEmcMomentumY( const Double_t EmcMomentumY ) { myEmcMomentumY = EmcMomentumY; }
    void SetEmcMomentumZ( const Double_t EmcMomentumZ ) { myEmcMomentumZ = EmcMomentumZ; }

    void SetEmcVolumeName( const TString EmcVolumeName ) { myEmcVolumeName = EmcVolumeName; }
    void SetEmcVolumeNumber( const Int_t EmcVolumeNumber ) {
        myEmcVolumeNumber = EmcVolumeNumber;
    }

    void SetEmcPosSigmaAlongTheta( const Double_t EmcPosSigmaAlongTheta ) {
        myEmcPosSigmaAlongTheta = EmcPosSigmaAlongTheta;
    }
    void SetEmcPosSigmaAlongPhi( const Double_t EmcPosSigmaAlongPhi ) {
        myEmcPosSigmaAlongPhi = EmcPosSigmaAlongPhi;
    }

    void SetEmcErrorMatrix( const Double_t EmcErrorMatrix[6][6] ) {
        SimMat::pack2d( 6, &EmcErrorMatrix[0][0], myEmcErrorMatrix );
    }

    void SetEmcPath( Double_t path ) { myEmcPath = path; }

    // Muc:
    void SetMucPositionX( const Double_t MucPositionX ) { myMucPositionX = MucPositionX; }
    void SetMucPositionY( const Double_t MucPositionY ) { myMucPositionY = MucPositionY; }
    void SetMucPositionZ( const Double_t MucPositionZ ) { myMucPositionZ = MucPositionZ; }
    void SetMucMomentumX( const Double_t MucMomentumX ) { myMucMomentumX = MucMomentumX; }
    void SetMucMomentumY( const Double_t MucMomentumY ) { myMucMomentumY = MucMomentumY; }
    void SetMucMomentumZ( const Double_t MucMomentumZ ) { myMucMomentumZ = MucMomentumZ; }

    void SetMucVolumeName( const TString MucVolumeName ) { myMucVolumeName = MucVolumeName; }
    void SetMucVolumeNumber( const Int_t MucVolumeNumber ) {
        myMucVolumeNumber = MucVolumeNumber;
    }

    void SetMucPosSigmaAlongZ( const Double_t MucPosSigmaAlongZ ) {
        myMucPosSigmaAlongZ = MucPosSigmaAlongZ;
    }
    void SetMucPosSigmaAlongT( const Double_t MucPosSigmaAlongT ) {
        myMucPosSigmaAlongT = MucPosSigmaAlongT;
    }
    void SetMucPosSigmaAlongX( const Double_t MucPosSigmaAlongX ) {
        myMucPosSigmaAlongX = MucPosSigmaAlongX;
    }
    void SetMucPosSigmaAlongY( const Double_t MucPosSigmaAlongY ) {
        myMucPosSigmaAlongY = MucPosSigmaAlongY;
    }

    void SetMucErrorMatrix( const Double_t MucErrorMatrix[6][6] ) {
        SimMat::pack2d( 6, &MucErrorMatrix[0][0], myMucErrorMatrix );
    }

    // extractors
    Int_t GetTrackId() const { return m_trackId; }
    // Tof layer1:
    Double_t GetTof1PositionX() const { return myTof1PositionX; }
    Double_t GetTof1PositionY() const { return myTof1PositionY; }
    Double_t GetTof1PositionZ() const { return myTof1PositionZ; }
    Double_t GetTof1MomentumX() const { return myTof1MomentumX; }
    Double_t GetTof1MomentumY() const { return myTof1MomentumY; }
    Double_t GetTof1MomentumZ() const { return myTof1MomentumZ; }

    TString GetTof1VolumeName() const { return myTof1VolumeName; }
    Int_t GetTof1VolumeNumber() const { return myTof1VolumeNumber; }
    Double_t GetTof1() const { return myTof1; }
    Double_t GetTof1Path() const { return myTof1Path; }
    Double_t GetTof1PosSigmaAlongZ() const { return myTof1PosSigmaAlongZ; }
    Double_t GetTof1PosSigmaAlongT() const { return myTof1PosSigmaAlongT; }
    Double_t GetTof1PosSigmaAlongX() const { return myTof1PosSigmaAlongX; }
    Double_t GetTof1PosSigmaAlongY() const { return myTof1PosSigmaAlongY; }
    Double_t GetTof1ErrorMatrix( Int_t i, Int_t j ) const {
        return SimMat::get_element( myTof1ErrorMatrix, i, j );
    }

    // Tof layer2:
    Double_t GetTof2PositionX() const { return myTof2PositionX; }
    Double_t GetTof2PositionY() const { return myTof2PositionY; }
    Double_t GetTof2PositionZ() const { return myTof2PositionZ; }
    Double_t GetTof2MomentumX() const { return myTof2MomentumX; }
    Double_t GetTof2MomentumY() const { return myTof2MomentumY; }
    Double_t GetTof2MomentumZ() const { return myTof2MomentumZ; }

    TString GetTof2VolumeName() const { return myTof2VolumeName; }
    Int_t GetTof2VolumeNumber() const { return myTof2VolumeNumber; }
    Double_t GetTof2() const { return myTof2; }
    Double_t GetTof2Path() const { return myTof2Path; }
    Double_t GetTof2PosSigmaAlongZ() const { return myTof2PosSigmaAlongZ; }
    Double_t GetTof2PosSigmaAlongT() const { return myTof2PosSigmaAlongT; }
    Double_t GetTof2PosSigmaAlongX() const { return myTof2PosSigmaAlongX; }
    Double_t GetTof2PosSigmaAlongY() const { return myTof2PosSigmaAlongY; }
    Double_t GetTof2ErrorMatrix( Int_t i, Int_t j ) const {
        return SimMat::get_element( myTof2ErrorMatrix, i, j );
    }

    // Emc
    Double_t GetEmcPositionX() const { return myEmcPositionX; }
    Double_t GetEmcPositionY() const { return myEmcPositionY; }
    Double_t GetEmcPositionZ() const { return myEmcPositionZ; }
    Double_t GetEmcMomentumX() const { return myEmcMomentumX; }
    Double_t GetEmcMomentumY() const { return myEmcMomentumY; }
    Double_t GetEmcMomentumZ() const { return myEmcMomentumZ; }

    TString GetEmcVolumeName() const { return myEmcVolumeName; }
    Int_t GetEmcVolumeNumber() const { return myEmcVolumeNumber; }
    Double_t GetEmcPosSigmaAlongTheta() const { return myEmcPosSigmaAlongTheta; }
    Double_t GetEmcPosSigmaAlongPhi() const { return myEmcPosSigmaAlongPhi; }
    Double_t GetEmcErrorMatrix( Int_t i, Int_t j ) const {
        return SimMat::get_element( myEmcErrorMatrix, i, j );
    }
    Double_t emcPath() const { return myEmcPath; }

    // Muc
    Double_t GetMucPositionX() const { return myMucPositionX; }
    Double_t GetMucPositionY() const { return myMucPositionY; }
    Double_t GetMucPositionZ() const { return myMucPositionZ; }
    Double_t GetMucMomentumX() const { return myMucMomentumX; }
    Double_t GetMucMomentumY() const { return myMucMomentumY; }
    Double_t GetMucMomentumZ() const { return myMucMomentumZ; }

    TString GetMucVolumeName() const { return myMucVolumeName; }
    Int_t GetMucVolumeNumber() const { return myMucVolumeNumber; }
    Double_t GetMucPosSigmaAlongZ() const { return myMucPosSigmaAlongZ; }
    Double_t GetMucPosSigmaAlongT() const { return myMucPosSigmaAlongT; }
    Double_t GetMucPosSigmaAlongX() const { return myMucPosSigmaAlongX; }
    Double_t GetMucPosSigmaAlongY() const { return myMucPosSigmaAlongY; }
    Double_t GetMucErrorMatrix( Int_t i, Int_t j ) const {
        return SimMat::get_element( myMucErrorMatrix, i, j );
    }

  private:
    // Tof TrkExt data.
    Int_t m_trackId; // Track Id wensp Add 2005-10-19
    //
    // Tof layer1:
    Double_t myTof1PositionX; // Position when the particle enters the TOF layer1.
    Double_t myTof1PositionY; // Position when the particle enters the TOF layer1
    Double_t myTof1PositionZ; // Position when the particle enters the TOF layer1
    Double_t myTof1MomentumX; // Momentum when the particle enters the TOF layer1.
    Double_t myTof1MomentumY; // Momentum when the particle enters the TOF layer1.
    Double_t myTof1MomentumZ; // Momentum when the particle enters the TOF layer1.

    TString myTof1VolumeName;      // Scintillator volume name
    Int_t myTof1VolumeNumber;      // Scintillator volume number
    Double_t myTof1;               // Time of flight
    Double_t myTof1Path;           // Path of flight
    Double_t myTof1PosSigmaAlongZ; // Sigma Z
    Double_t myTof1PosSigmaAlongT; // Sigma along Z x R
    Double_t myTof1PosSigmaAlongX; // Sigma X
    Double_t myTof1PosSigmaAlongY; // Sigma Y
    // o Double_t myTof1ErrorMatrix[6][6]; //Error matrix 6x6 (x,p)
    Double_t myTof1ErrorMatrix[21]; // Error matrix 6x6 (x,p)

    // Tof layer2:
    Double_t myTof2PositionX; // Position when the particle enters the TOF layer2.
    Double_t myTof2PositionY; // Position when the particle enters the TOF layer2
    Double_t myTof2PositionZ; // Position when the particle enters the TOF layer2
    Double_t myTof2MomentumX; // Momentum when the particle enters the TOF layer2
    Double_t myTof2MomentumY; // Momentum when the particle enters the TOF layer2
    Double_t myTof2MomentumZ; // Momentum when the particle enters the TOF layer2

    TString myTof2VolumeName;      // Scintillator volume name
    Int_t myTof2VolumeNumber;      // Scintillator volume number
    Double_t myTof2;               // Time of flight
    Double_t myTof2Path;           // Path of flight
    Double_t myTof2PosSigmaAlongZ; // Sigma Z
    Double_t myTof2PosSigmaAlongT; // Sigma along Z x R
    Double_t myTof2PosSigmaAlongX; // Sigma X
    Double_t myTof2PosSigmaAlongY; // Sigma Y
    // o Double_t myTof2ErrorMatrix[6][6]; //Error matrix 6x6 (x,p)
    Double_t myTof2ErrorMatrix[21]; // Error matrix 6x6 (x,p)

    // Emc TrkExt data,which is similar to TOF data.
    Double_t myEmcPositionX; // Position 2.
    Double_t myEmcPositionY; // Position 2
    Double_t myEmcPositionZ; // Position 2
    Double_t myEmcMomentumX; // Momentum
    Double_t myEmcMomentumY; // Momentum
    Double_t myEmcMomentumZ; // Momentum

    TString myEmcVolumeName; // Scintillator volume name
    Int_t myEmcVolumeNumber; // Scintillator volume number
    Double_t myEmcPosSigmaAlongTheta;
    Double_t myEmcPosSigmaAlongPhi;
    // o Double_t myEmcErrorMatrix[6][6]; //Error matrix 6x6 (x,p)
    Double_t myEmcErrorMatrix[21]; // Error matrix 6x6 (x,p)

    Double_t myEmcPath;

    // Muc TrkExt data,which is similar to TOF data.
    Double_t myMucPositionX; // Position 2.
    Double_t myMucPositionY; // Position 2
    Double_t myMucPositionZ; // Position 2
    Double_t myMucMomentumX; // Momentum
    Double_t myMucMomentumY; // Momentum
    Double_t myMucMomentumZ; // Momentum

    TString myMucVolumeName; // Scintillator volume name
    Int_t myMucVolumeNumber; // Scintillator volume number

    Double_t myMucPosSigmaAlongZ;
    Double_t myMucPosSigmaAlongT;
    Double_t myMucPosSigmaAlongX;
    Double_t myMucPosSigmaAlongY;
    // o Double_t myMucErrorMatrix[6][6];
    Double_t myMucErrorMatrix[21];

    ClassDef( TExtTrack, 4 )
};

#endif
