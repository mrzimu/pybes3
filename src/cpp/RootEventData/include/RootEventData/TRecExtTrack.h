#ifndef RootEventData_TRecExtTrack_H
#define RootEventData_TRecExtTrack_H 1

#include "TObject.h"
#include "TString.h"
using namespace std;

class TRecExtTrack : public TObject {

  public:
    TRecExtTrack();

    ~TRecExtTrack();

    // modifiers
    void SetTrackId( const Int_t trackId ) { m_trackId = trackId; }
    // Tof layer1:
    void SetTof1PositionX( const Double_t Tof1PositionX, const Int_t i = 2 ) {
        myTof1PositionX[i] = Tof1PositionX;
    }
    void SetTof1PositionY( const Double_t Tof1PositionY, const Int_t i = 2 ) {
        myTof1PositionY[i] = Tof1PositionY;
    }
    void SetTof1PositionZ( const Double_t Tof1PositionZ, const Int_t i = 2 ) {
        myTof1PositionZ[i] = Tof1PositionZ;
    }
    void SetTof1MomentumX( const Double_t Tof1MomentumX, const Int_t i = 2 ) {
        myTof1MomentumX[i] = Tof1MomentumX;
    }
    void SetTof1MomentumY( const Double_t Tof1MomentumY, const Int_t i = 2 ) {
        myTof1MomentumY[i] = Tof1MomentumY;
    }
    void SetTof1MomentumZ( const Double_t Tof1MomentumZ, const Int_t i = 2 ) {
        myTof1MomentumZ[i] = Tof1MomentumZ;
    }

    void SetTof1VolumeName( const TString Tof1VolumeName, const Int_t i = 2 ) {
        myTof1VolumeName[i] = Tof1VolumeName;
    }
    void SetTof1VolumeNumber( const Int_t Tof1VolumeNumber, const Int_t i = 2 ) {
        myTof1VolumeNumber[i] = Tof1VolumeNumber;
    }
    void SetTof1( const Double_t Tof1, const Int_t i = 2 ) { myTof1[i] = Tof1; }
    void SetTof1Path( const Double_t Tof1Path, const Int_t i = 2 ) {
        myTof1Path[i] = Tof1Path;
    }
    void SetTof1PosSigmaAlongZ( const Double_t Tof1PosSigmaAlongZ, const Int_t i = 2 ) {
        myTof1PosSigmaAlongZ[i] = Tof1PosSigmaAlongZ;
    }
    void SetTof1PosSigmaAlongT( const Double_t Tof1PosSigmaAlongT, const Int_t i = 2 ) {
        myTof1PosSigmaAlongT[i] = Tof1PosSigmaAlongT;
    }
    void SetTof1PosSigmaAlongX( const Double_t Tof1PosSigmaAlongX, const Int_t i = 2 ) {
        myTof1PosSigmaAlongX[i] = Tof1PosSigmaAlongX;
    }
    void SetTof1PosSigmaAlongY( const Double_t Tof1PosSigmaAlongY, const Int_t i = 2 ) {
        myTof1PosSigmaAlongY[i] = Tof1PosSigmaAlongY;
    }
    void SetTof1ErrorMatrix( const Double_t Tof1ErrorMatrix[6][6], const Int_t k = 2 ) {
        for ( Int_t i = 0; i < 6; i++ )
            for ( Int_t j = 0; j < 6; j++ ) myTof1ErrorMatrix[k][i][j] = Tof1ErrorMatrix[i][j];
    }

    // Tof layer2:
    void SetTof2PositionX( const Double_t Tof2PositionX, const Int_t i = 2 ) {
        myTof2PositionX[i] = Tof2PositionX;
    }
    void SetTof2PositionY( const Double_t Tof2PositionY, const Int_t i = 2 ) {
        myTof2PositionY[i] = Tof2PositionY;
    }
    void SetTof2PositionZ( const Double_t Tof2PositionZ, const Int_t i = 2 ) {
        myTof2PositionZ[i] = Tof2PositionZ;
    }
    void SetTof2MomentumX( const Double_t Tof2MomentumX, const Int_t i = 2 ) {
        myTof2MomentumX[i] = Tof2MomentumX;
    }
    void SetTof2MomentumY( const Double_t Tof2MomentumY, const Int_t i = 2 ) {
        myTof2MomentumY[i] = Tof2MomentumY;
    }
    void SetTof2MomentumZ( const Double_t Tof2MomentumZ, const Int_t i = 2 ) {
        myTof2MomentumZ[i] = Tof2MomentumZ;
    }

    void SetTof2VolumeName( const TString Tof2VolumeName, const Int_t i = 2 ) {
        myTof2VolumeName[i] = Tof2VolumeName;
    }
    void SetTof2VolumeNumber( const Int_t Tof2VolumeNumber, const Int_t i = 2 ) {
        myTof2VolumeNumber[i] = Tof2VolumeNumber;
    }
    void SetTof2( const Double_t Tof2, const Int_t i = 2 ) { myTof2[i] = Tof2; }
    void SetTof2Path( const Double_t Tof2Path, const Int_t i = 2 ) {
        myTof2Path[i] = Tof2Path;
    }
    void SetTof2PosSigmaAlongZ( const Double_t Tof2PosSigmaAlongZ, const Int_t i = 2 ) {
        myTof2PosSigmaAlongZ[i] = Tof2PosSigmaAlongZ;
    }
    void SetTof2PosSigmaAlongT( const Double_t Tof2PosSigmaAlongT, const Int_t i = 2 ) {
        myTof2PosSigmaAlongT[i] = Tof2PosSigmaAlongT;
    }
    void SetTof2PosSigmaAlongX( const Double_t Tof2PosSigmaAlongX, const Int_t i = 2 ) {
        myTof2PosSigmaAlongX[i] = Tof2PosSigmaAlongX;
    }
    void SetTof2PosSigmaAlongY( const Double_t Tof2PosSigmaAlongY, const Int_t i = 2 ) {
        myTof2PosSigmaAlongY[i] = Tof2PosSigmaAlongY;
    }
    void SetTof2ErrorMatrix( const Double_t Tof2ErrorMatrix[6][6], const Int_t k = 2 ) {
        for ( Int_t i = 0; i < 6; i++ )
            for ( Int_t j = 0; j < 6; j++ ) myTof2ErrorMatrix[k][i][j] = Tof2ErrorMatrix[i][j];
    }

    // Emc:
    void SetEmcPositionX( const Double_t EmcPositionX, const Int_t i = 2 ) {
        myEmcPositionX[i] = EmcPositionX;
    }
    void SetEmcPositionY( const Double_t EmcPositionY, const Int_t i = 2 ) {
        myEmcPositionY[i] = EmcPositionY;
    }
    void SetEmcPositionZ( const Double_t EmcPositionZ, const Int_t i = 2 ) {
        myEmcPositionZ[i] = EmcPositionZ;
    }
    void SetEmcMomentumX( const Double_t EmcMomentumX, const Int_t i = 2 ) {
        myEmcMomentumX[i] = EmcMomentumX;
    }
    void SetEmcMomentumY( const Double_t EmcMomentumY, const Int_t i = 2 ) {
        myEmcMomentumY[i] = EmcMomentumY;
    }
    void SetEmcMomentumZ( const Double_t EmcMomentumZ, const Int_t i = 2 ) {
        myEmcMomentumZ[i] = EmcMomentumZ;
    }

    void SetEmcVolumeName( const TString EmcVolumeName, const Int_t i = 2 ) {
        myEmcVolumeName[i] = EmcVolumeName;
    }
    void SetEmcVolumeNumber( const Int_t EmcVolumeNumber, const Int_t i = 2 ) {
        myEmcVolumeNumber[i] = EmcVolumeNumber;
    }

    void SetEmcPosSigmaAlongTheta( const Double_t EmcPosSigmaAlongTheta, const Int_t i = 2 ) {
        myEmcPosSigmaAlongTheta[i] = EmcPosSigmaAlongTheta;
    }
    void SetEmcPosSigmaAlongPhi( const Double_t EmcPosSigmaAlongPhi, const Int_t i = 2 ) {
        myEmcPosSigmaAlongPhi[i] = EmcPosSigmaAlongPhi;
    }

    void SetEmcErrorMatrix( const Double_t EmcErrorMatrix[6][6], const Int_t k = 2 ) {
        for ( Int_t i = 0; i < 6; i++ )
            for ( Int_t j = 0; j < 6; j++ ) myEmcErrorMatrix[k][i][j] = EmcErrorMatrix[i][j];
    }

    void SetEmcPath( Double_t path, const Int_t i = 2 ) { myEmcPath[i] = path; }

    // Muc:
    void SetMucPositionX( const Double_t MucPositionX, const Int_t i = 2 ) {
        myMucPositionX[i] = MucPositionX;
    }
    void SetMucPositionY( const Double_t MucPositionY, const Int_t i = 2 ) {
        myMucPositionY[i] = MucPositionY;
    }
    void SetMucPositionZ( const Double_t MucPositionZ, const Int_t i = 2 ) {
        myMucPositionZ[i] = MucPositionZ;
    }
    void SetMucMomentumX( const Double_t MucMomentumX, const Int_t i = 2 ) {
        myMucMomentumX[i] = MucMomentumX;
    }
    void SetMucMomentumY( const Double_t MucMomentumY, const Int_t i = 2 ) {
        myMucMomentumY[i] = MucMomentumY;
    }
    void SetMucMomentumZ( const Double_t MucMomentumZ, const Int_t i = 2 ) {
        myMucMomentumZ[i] = MucMomentumZ;
    }

    void SetMucVolumeName( const TString MucVolumeName, const Int_t i = 2 ) {
        myMucVolumeName[i] = MucVolumeName;
    }
    void SetMucVolumeNumber( const Int_t MucVolumeNumber, const Int_t i = 2 ) {
        myMucVolumeNumber[i] = MucVolumeNumber;
    }

    void SetMucPosSigmaAlongZ( const Double_t MucPosSigmaAlongZ, const Int_t i = 2 ) {
        myMucPosSigmaAlongZ[i] = MucPosSigmaAlongZ;
    }
    void SetMucPosSigmaAlongT( const Double_t MucPosSigmaAlongT, const Int_t i = 2 ) {
        myMucPosSigmaAlongT[i] = MucPosSigmaAlongT;
    }
    void SetMucPosSigmaAlongX( const Double_t MucPosSigmaAlongX, const Int_t i = 2 ) {
        myMucPosSigmaAlongX[i] = MucPosSigmaAlongX;
    }
    void SetMucPosSigmaAlongY( const Double_t MucPosSigmaAlongY, const Int_t i = 2 ) {
        myMucPosSigmaAlongY[i] = MucPosSigmaAlongY;
    }

    void SetMucErrorMatrix( const Double_t MucErrorMatrix[6][6], const Int_t k = 2 ) {
        for ( Int_t i = 0; i < 6; i++ )
            for ( Int_t j = 0; j < 6; j++ ) myMucErrorMatrix[k][i][j] = MucErrorMatrix[i][j];
    }

    void SetSize( Int_t size, const Int_t i = 2 ) { mySize[i] = size; }
    void SetExtMucHit( Double_t PositionX, Double_t PositionY, Double_t PositionZ,
                       Double_t MomentumX, Double_t MomentumY, Double_t MomentumZ,
                       TString VolumeName, Int_t VolumeNumber, Double_t PosSigmaAlongZ,
                       Double_t PosSigmaAlongT, Double_t PosSigmaAlongX,
                       Double_t PosSigmaAlongY, Double_t ErrorMatrix[6][6],
                       const Int_t k = 2 ) {
        myPositionX[k].push_back( PositionX );
        myPositionY[k].push_back( PositionY );
        myPositionZ[k].push_back( PositionZ );
        myMomentumX[k].push_back( MomentumX );
        myMomentumY[k].push_back( MomentumY );
        myMomentumZ[k].push_back( MomentumZ );
        myVolumeName[k].push_back( VolumeName );
        myVolumeNumber[k].push_back( VolumeNumber );
        myPosSigmaAlongZ[k].push_back( PosSigmaAlongZ );
        myPosSigmaAlongT[k].push_back( PosSigmaAlongT );
        myPosSigmaAlongX[k].push_back( PosSigmaAlongX );
        myPosSigmaAlongY[k].push_back( PosSigmaAlongY );
        vector<Double_t> vecError;
        for ( int i = 0; i < 6; i++ )
            for ( int j = 0; j < 6; j++ ) { vecError.push_back( ErrorMatrix[i][j] ); }
        myErrorMatrix[k].push_back( vecError );
    }

    // extractors
    Int_t GetTrackId() const { return m_trackId; }
    // Tof layer1:
    Double_t GetTof1PositionX( const Int_t i = 2 ) const { return myTof1PositionX[i]; }
    Double_t GetTof1PositionY( const Int_t i = 2 ) const { return myTof1PositionY[i]; }
    Double_t GetTof1PositionZ( const Int_t i = 2 ) const { return myTof1PositionZ[i]; }
    Double_t GetTof1MomentumX( const Int_t i = 2 ) const { return myTof1MomentumX[i]; }
    Double_t GetTof1MomentumY( const Int_t i = 2 ) const { return myTof1MomentumY[i]; }
    Double_t GetTof1MomentumZ( const Int_t i = 2 ) const { return myTof1MomentumZ[i]; }

    TString GetTof1VolumeName( const Int_t i = 2 ) const { return myTof1VolumeName[i]; }
    Int_t GetTof1VolumeNumber( const Int_t i = 2 ) const { return myTof1VolumeNumber[i]; }
    Double_t GetTof1( const Int_t i = 2 ) const { return myTof1[i]; }
    Double_t GetTof1Path( const Int_t i = 2 ) const { return myTof1Path[i]; }
    Double_t GetTof1PosSigmaAlongZ( const Int_t i = 2 ) const {
        return myTof1PosSigmaAlongZ[i];
    }
    Double_t GetTof1PosSigmaAlongT( const Int_t i = 2 ) const {
        return myTof1PosSigmaAlongT[i];
    }
    Double_t GetTof1PosSigmaAlongX( const Int_t i = 2 ) const {
        return myTof1PosSigmaAlongX[i];
    }
    Double_t GetTof1PosSigmaAlongY( const Int_t i = 2 ) const {
        return myTof1PosSigmaAlongY[i];
    }
    Double_t GetTof1ErrorMatrix( Int_t i, Int_t j, const Int_t k = 2 ) const {
        return myTof1ErrorMatrix[k][i][j];
    }

    // Tof layer2:
    Double_t GetTof2PositionX( const Int_t i = 2 ) const { return myTof2PositionX[i]; }
    Double_t GetTof2PositionY( const Int_t i = 2 ) const { return myTof2PositionY[i]; }
    Double_t GetTof2PositionZ( const Int_t i = 2 ) const { return myTof2PositionZ[i]; }
    Double_t GetTof2MomentumX( const Int_t i = 2 ) const { return myTof2MomentumX[i]; }
    Double_t GetTof2MomentumY( const Int_t i = 2 ) const { return myTof2MomentumY[i]; }
    Double_t GetTof2MomentumZ( const Int_t i = 2 ) const { return myTof2MomentumZ[i]; }

    TString GetTof2VolumeName( const Int_t i = 2 ) const { return myTof2VolumeName[i]; }
    Int_t GetTof2VolumeNumber( const Int_t i = 2 ) const { return myTof2VolumeNumber[i]; }
    Double_t GetTof2( const Int_t i = 2 ) const { return myTof2[i]; }
    Double_t GetTof2Path( const Int_t i = 2 ) const { return myTof2Path[i]; }
    Double_t GetTof2PosSigmaAlongZ( const Int_t i = 2 ) const {
        return myTof2PosSigmaAlongZ[i];
    }
    Double_t GetTof2PosSigmaAlongT( const Int_t i = 2 ) const {
        return myTof2PosSigmaAlongT[i];
    }
    Double_t GetTof2PosSigmaAlongX( const Int_t i = 2 ) const {
        return myTof2PosSigmaAlongX[i];
    }
    Double_t GetTof2PosSigmaAlongY( const Int_t i = 2 ) const {
        return myTof2PosSigmaAlongY[i];
    }
    Double_t GetTof2ErrorMatrix( Int_t i, Int_t j, const Int_t k = 2 ) const {
        return myTof2ErrorMatrix[k][i][j];
    }

    // Emc
    Double_t GetEmcPositionX( const Int_t i = 2 ) const { return myEmcPositionX[i]; }
    Double_t GetEmcPositionY( const Int_t i = 2 ) const { return myEmcPositionY[i]; }
    Double_t GetEmcPositionZ( const Int_t i = 2 ) const { return myEmcPositionZ[i]; }
    Double_t GetEmcMomentumX( const Int_t i = 2 ) const { return myEmcMomentumX[i]; }
    Double_t GetEmcMomentumY( const Int_t i = 2 ) const { return myEmcMomentumY[i]; }
    Double_t GetEmcMomentumZ( const Int_t i = 2 ) const { return myEmcMomentumZ[i]; }

    TString GetEmcVolumeName( const Int_t i = 2 ) const { return myEmcVolumeName[i]; }
    Int_t GetEmcVolumeNumber( const Int_t i = 2 ) const { return myEmcVolumeNumber[i]; }
    Double_t GetEmcPosSigmaAlongTheta( const Int_t i = 2 ) const {
        return myEmcPosSigmaAlongTheta[i];
    }
    Double_t GetEmcPosSigmaAlongPhi( const Int_t i = 2 ) const {
        return myEmcPosSigmaAlongPhi[i];
    }
    Double_t GetEmcErrorMatrix( Int_t i, Int_t j, const Int_t k = 2 ) const {
        return myEmcErrorMatrix[k][i][j];
    }
    Double_t emcPath( const Int_t i = 2 ) const { return myEmcPath[i]; }

    // Muc
    Double_t GetMucPositionX( const Int_t i = 2 ) const { return myMucPositionX[i]; }
    Double_t GetMucPositionY( const Int_t i = 2 ) const { return myMucPositionY[i]; }
    Double_t GetMucPositionZ( const Int_t i = 2 ) const { return myMucPositionZ[i]; }
    Double_t GetMucMomentumX( const Int_t i = 2 ) const { return myMucMomentumX[i]; }
    Double_t GetMucMomentumY( const Int_t i = 2 ) const { return myMucMomentumY[i]; }
    Double_t GetMucMomentumZ( const Int_t i = 2 ) const { return myMucMomentumZ[i]; }

    TString GetMucVolumeName( const Int_t i = 2 ) const { return myMucVolumeName[i]; }
    Int_t GetMucVolumeNumber( const Int_t i = 2 ) const { return myMucVolumeNumber[i]; }
    Double_t GetMucPosSigmaAlongZ( const Int_t i = 2 ) const { return myMucPosSigmaAlongZ[i]; }
    Double_t GetMucPosSigmaAlongT( const Int_t i = 2 ) const { return myMucPosSigmaAlongT[i]; }
    Double_t GetMucPosSigmaAlongX( const Int_t i = 2 ) const { return myMucPosSigmaAlongX[i]; }
    Double_t GetMucPosSigmaAlongY( const Int_t i = 2 ) const { return myMucPosSigmaAlongY[i]; }
    Double_t GetMucErrorMatrix( Int_t i, Int_t j, const Int_t k = 2 ) const {
        return myMucErrorMatrix[k][i][j];
    }

    // ExtMucHitVet
    Int_t GetSize( const Int_t i = 2 ) const { return mySize[i]; };
    Double_t GetPositionX( Int_t i, const Int_t k = 2 ) const { return myPositionX[k][i]; }
    Double_t GetPositionY( Int_t i, const Int_t k = 2 ) const { return myPositionY[k][i]; }
    Double_t GetPositionZ( Int_t i, const Int_t k = 2 ) const { return myPositionZ[k][i]; }
    Double_t GetMomentumX( Int_t i, const Int_t k = 2 ) const { return myMomentumX[k][i]; }
    Double_t GetMomentumY( Int_t i, const Int_t k = 2 ) const { return myMomentumY[k][i]; }
    Double_t GetMomentumZ( Int_t i, const Int_t k = 2 ) const { return myMomentumZ[k][i]; }
    TString GetVolumeName( Int_t i, const Int_t k = 2 ) const { return myVolumeName[k][i]; }
    Int_t GetVolumeNumber( Int_t i, const Int_t k = 2 ) const { return myVolumeNumber[k][i]; }
    Double_t GetPosSigmaAlongZ( Int_t i, const Int_t k = 2 ) const {
        return myPosSigmaAlongZ[k][i];
    }
    Double_t GetPosSigmaAlongT( Int_t i, const Int_t k = 2 ) const {
        return myPosSigmaAlongT[k][i];
    }
    Double_t GetPosSigmaAlongX( Int_t i, const Int_t k = 2 ) const {
        return myPosSigmaAlongX[k][i];
    }
    Double_t GetPosSigmaAlongY( Int_t i, const Int_t k = 2 ) const {
        return myPosSigmaAlongY[k][i];
    }
    vector<Double_t> GetErrorMatrix( Int_t i, const Int_t k = 2 ) const {
        return myErrorMatrix[k][i];
    }

  private:
    // Tof TrkExt data.
    Int_t m_trackId; // Track Id wensp Add 2005-10-19
    //
    // Tof layer1:
    Double_t myTof1PositionX[5]; // Position when the particle enters the TOF layer1.
    Double_t myTof1PositionY[5]; // Position when the particle enters the TOF layer1
    Double_t myTof1PositionZ[5]; // Position when the particle enters the TOF layer1
    Double_t myTof1MomentumX[5]; // Momentum when the particle enters the TOF layer1.
    Double_t myTof1MomentumY[5]; // Momentum when the particle enters the TOF layer1.
    Double_t myTof1MomentumZ[5]; // Momentum when the particle enters the TOF layer1.

    TString myTof1VolumeName[5];         // Scintillator volume name
    Int_t myTof1VolumeNumber[5];         // Scintillator volume number
    Double_t myTof1[5];                  // Time of flight
    Double_t myTof1Path[5];              // Path of flight
    Double_t myTof1PosSigmaAlongZ[5];    // Sigma Z
    Double_t myTof1PosSigmaAlongT[5];    // Sigma along Z x R
    Double_t myTof1PosSigmaAlongX[5];    // Sigma X
    Double_t myTof1PosSigmaAlongY[5];    // Sigma Y
    Double_t myTof1ErrorMatrix[5][6][6]; // Error matrix 6x6 (x,p)

    // Tof layer2:
    Double_t myTof2PositionX[5]; // Position when the particle enters the TOF layer2.
    Double_t myTof2PositionY[5]; // Position when the particle enters the TOF layer2
    Double_t myTof2PositionZ[5]; // Position when the particle enters the TOF layer2
    Double_t myTof2MomentumX[5]; // Momentum when the particle enters the TOF layer2
    Double_t myTof2MomentumY[5]; // Momentum when the particle enters the TOF layer2
    Double_t myTof2MomentumZ[5]; // Momentum when the particle enters the TOF layer2

    TString myTof2VolumeName[5];         // Scintillator volume name
    Int_t myTof2VolumeNumber[5];         // Scintillator volume number
    Double_t myTof2[5];                  // Time of flight
    Double_t myTof2Path[5];              // Path of flight
    Double_t myTof2PosSigmaAlongZ[5];    // Sigma Z
    Double_t myTof2PosSigmaAlongT[5];    // Sigma along Z x R
    Double_t myTof2PosSigmaAlongX[5];    // Sigma X
    Double_t myTof2PosSigmaAlongY[5];    // Sigma Y
    Double_t myTof2ErrorMatrix[5][6][6]; // Error matrix 6x6 (x,p)

    // Emc TrkExt data,which is similar to TOF data.
    Double_t myEmcPositionX[5]; // Position 2.
    Double_t myEmcPositionY[5]; // Position 2
    Double_t myEmcPositionZ[5]; // Position 2
    Double_t myEmcMomentumX[5]; // Momentum
    Double_t myEmcMomentumY[5]; // Momentum
    Double_t myEmcMomentumZ[5]; // Momentum

    TString myEmcVolumeName[5]; // Scintillator volume name
    Int_t myEmcVolumeNumber[5]; // Scintillator volume number
    Double_t myEmcPosSigmaAlongTheta[5];
    Double_t myEmcPosSigmaAlongPhi[5];
    Double_t myEmcErrorMatrix[5][6][6]; // Error matrix 6x6 (x,p)

    Double_t myEmcPath[5];

    // Muc TrkExt data,which is similar to TOF data.
    Double_t myMucPositionX[5]; // Position 2.
    Double_t myMucPositionY[5]; // Position 2
    Double_t myMucPositionZ[5]; // Position 2
    Double_t myMucMomentumX[5]; // Momentum
    Double_t myMucMomentumY[5]; // Momentum
    Double_t myMucMomentumZ[5]; // Momentum

    TString myMucVolumeName[5]; // Scintillator volume name
    Int_t myMucVolumeNumber[5]; // Scintillator volume number

    Double_t myMucPosSigmaAlongZ[5];
    Double_t myMucPosSigmaAlongT[5];
    Double_t myMucPosSigmaAlongX[5];
    Double_t myMucPosSigmaAlongY[5];
    Double_t myMucErrorMatrix[5][6][6];

    // for  ExtMucHitVec
    Int_t mySize[5]; // size of the vector
    vector<Double_t> myPositionX[5];
    vector<Double_t> myPositionY[5];
    vector<Double_t> myPositionZ[5];
    vector<Double_t> myMomentumX[5];
    vector<Double_t> myMomentumY[5];
    vector<Double_t> myMomentumZ[5];
    vector<TString> myVolumeName[5];
    vector<Int_t> myVolumeNumber[5];
    vector<Double_t> myPosSigmaAlongZ[5];
    vector<Double_t> myPosSigmaAlongT[5];
    vector<Double_t> myPosSigmaAlongX[5];
    vector<Double_t> myPosSigmaAlongY[5];
    vector<vector<Double_t>> myErrorMatrix[5];

    ClassDef( TRecExtTrack, 3 )
};

#endif
