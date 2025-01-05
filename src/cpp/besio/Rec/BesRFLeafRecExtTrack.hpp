#pragma once

#include "RootEventData/TRecExtTrack.h"
#include "RootEventData/TRecTrackEvent.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using RecExtTrackRecord =
    RecordBuilder<RaggedItemField<0, int>,                         // trackId
                  RaggedArrayField<1, 5, double>,                  // tof1X
                  RaggedArrayField<2, 5, double>,                  // tof1Y
                  RaggedArrayField<3, 5, double>,                  // tof1Z
                  RaggedArrayField<4, 5, double>,                  // tof1Px
                  RaggedArrayField<5, 5, double>,                  // tof1Py
                  RaggedArrayField<6, 5, double>,                  // tof1Pz
                  RaggedArrayStringField<7, 5>,                    // tof1VolumeName
                  RaggedArrayField<8, 5, int>,                     // tof1VolumeNumber
                  RaggedArrayField<9, 5, double>,                  // tof1
                  RaggedArrayField<10, 5, double>,                 // tof1Path
                  RaggedArrayField<11, 5, double>,                 // tof1PosSigmaAlongZ
                  RaggedArrayField<12, 5, double>,                 // tof1PosSigmaAlongT
                  RaggedArrayField<13, 5, double>,                 // tof1PosSigmaAlongX
                  RaggedArrayField<14, 5, double>,                 // tof1PosSigmaAlongY
                  RaggedArrayArrayArrayField<15, 5, 6, 6, double>, // tof1ErrorMatrix
                  RaggedArrayField<16, 5, double>,                 // tof2X
                  RaggedArrayField<17, 5, double>,                 // tof2Y
                  RaggedArrayField<18, 5, double>,                 // tof2Z
                  RaggedArrayField<19, 5, double>,                 // tof2Px
                  RaggedArrayField<20, 5, double>,                 // tof2Py
                  RaggedArrayField<21, 5, double>,                 // tof2Pz
                  RaggedArrayStringField<22, 5>,                   // tof2VolumeName
                  RaggedArrayField<23, 5, int>,                    // tof2VolumeNumber
                  RaggedArrayField<24, 5, double>,                 // tof2
                  RaggedArrayField<25, 5, double>,                 // tof2Path
                  RaggedArrayField<26, 5, double>,                 // tof2PosSigmaAlongZ
                  RaggedArrayField<27, 5, double>,                 // tof2PosSigmaAlongT
                  RaggedArrayField<28, 5, double>,                 // tof2PosSigmaAlongX
                  RaggedArrayField<29, 5, double>,                 // tof2PosSigmaAlongY
                  RaggedArrayArrayArrayField<30, 5, 6, 6, double>, // tof2ErrorMatrix
                  RaggedArrayField<31, 5, double>,                 // emcX
                  RaggedArrayField<32, 5, double>,                 // emcY
                  RaggedArrayField<33, 5, double>,                 // emcZ
                  RaggedArrayField<34, 5, double>,                 // emcPx
                  RaggedArrayField<35, 5, double>,                 // emcPy
                  RaggedArrayField<36, 5, double>,                 // emcPz
                  RaggedArrayStringField<37, 5>,                   // emcVolumeName
                  RaggedArrayField<38, 5, int>,                    // emcVolumeNumber
                  RaggedArrayField<39, 5, double>,                 // emcPosSigmaAlongTheta
                  RaggedArrayField<40, 5, double>,                 // emcPosSigmaAlongPhi
                  RaggedArrayArrayArrayField<41, 5, 6, 6, double>, // emcErrorMatrix
                  RaggedArrayField<42, 5, double>,                 // emcPath
                  RaggedArrayField<43, 5, double>,                 // mucX
                  RaggedArrayField<44, 5, double>,                 // mucY
                  RaggedArrayField<45, 5, double>,                 // mucZ
                  RaggedArrayField<46, 5, double>,                 // mucPx
                  RaggedArrayField<47, 5, double>,                 // mucPy
                  RaggedArrayField<48, 5, double>,                 // mucPz
                  RaggedArrayStringField<49, 5>,                   // mucVolumeName
                  RaggedArrayField<50, 5, int>,                    // mucVolumeNumber
                  RaggedArrayField<51, 5, double>,                 // mucPosSigmaAlongZ
                  RaggedArrayField<52, 5, double>,                 // mucPosSigmaAlongT
                  RaggedArrayField<53, 5, double>,                 // mucPosSigmaAlongX
                  RaggedArrayField<54, 5, double>,                 // mucPosSigmaAlongY
                  RaggedArrayArrayArrayField<55, 5, 6, 6, double>, // mucErrorMatrix
                  RaggedArrayField<56, 5, int>,                    // mucHitVecSize
                  RaggedArrayRaggedField<57, 5, double>,           // mucHitX
                  RaggedArrayRaggedField<58, 5, double>,           // mucHitY
                  RaggedArrayRaggedField<59, 5, double>,           // mucHitZ
                  RaggedArrayRaggedField<60, 5, double>,           // mucHitPx
                  RaggedArrayRaggedField<61, 5, double>,           // mucHitPy
                  RaggedArrayRaggedField<62, 5, double>,           // mucHitPz
                  RaggedArrayRaggedStringField<63, 5>,             // mucHitVolumeName
                  RaggedArrayRaggedField<64, 5, int>,              // mucHitVolumeNumber
                  RaggedArrayRaggedField<65, 5, double>,           // mucHitPosSigmaAlongZ
                  RaggedArrayRaggedField<66, 5, double>,           // mucHitPosSigmaAlongT
                  RaggedArrayRaggedField<67, 5, double>,           // mucHitPosSigmaAlongX
                  RaggedArrayRaggedField<68, 5, double>,           // mucHitPosSigmaAlongY
                  RaggedArrayRaggedRaggedField<69, 5, double>      // mucHitErrorMatrix
                  >;

const FieldMap field_map_rec_exttrack = {
    { 0, BesFieldNames::Rec::ExtTrack::trackId },
    { 1, BesFieldNames::Rec::ExtTrack::tof1X },
    { 2, BesFieldNames::Rec::ExtTrack::tof1Y },
    { 3, BesFieldNames::Rec::ExtTrack::tof1Z },
    { 4, BesFieldNames::Rec::ExtTrack::tof1Px },
    { 5, BesFieldNames::Rec::ExtTrack::tof1Py },
    { 6, BesFieldNames::Rec::ExtTrack::tof1Pz },
    { 7, BesFieldNames::Rec::ExtTrack::tof1VolumeName },
    { 8, BesFieldNames::Rec::ExtTrack::tof1VolumeNumber },
    { 9, BesFieldNames::Rec::ExtTrack::tof1 },
    { 10, BesFieldNames::Rec::ExtTrack::tof1Path },
    { 11, BesFieldNames::Rec::ExtTrack::tof1PosSigmaAlongZ },
    { 12, BesFieldNames::Rec::ExtTrack::tof1PosSigmaAlongT },
    { 13, BesFieldNames::Rec::ExtTrack::tof1PosSigmaAlongX },
    { 14, BesFieldNames::Rec::ExtTrack::tof1PosSigmaAlongY },
    { 15, BesFieldNames::Rec::ExtTrack::tof1ErrorMatrix },
    { 16, BesFieldNames::Rec::ExtTrack::tof2X },
    { 17, BesFieldNames::Rec::ExtTrack::tof2Y },
    { 18, BesFieldNames::Rec::ExtTrack::tof2Z },
    { 19, BesFieldNames::Rec::ExtTrack::tof2Px },
    { 20, BesFieldNames::Rec::ExtTrack::tof2Py },
    { 21, BesFieldNames::Rec::ExtTrack::tof2Pz },
    { 22, BesFieldNames::Rec::ExtTrack::tof2VolumeName },
    { 23, BesFieldNames::Rec::ExtTrack::tof2VolumeNumber },
    { 24, BesFieldNames::Rec::ExtTrack::tof2 },
    { 25, BesFieldNames::Rec::ExtTrack::tof2Path },
    { 26, BesFieldNames::Rec::ExtTrack::tof2PosSigmaAlongZ },
    { 27, BesFieldNames::Rec::ExtTrack::tof2PosSigmaAlongT },
    { 28, BesFieldNames::Rec::ExtTrack::tof2PosSigmaAlongX },
    { 29, BesFieldNames::Rec::ExtTrack::tof2PosSigmaAlongY },
    { 30, BesFieldNames::Rec::ExtTrack::tof2ErrorMatrix },
    { 31, BesFieldNames::Rec::ExtTrack::emcX },
    { 32, BesFieldNames::Rec::ExtTrack::emcY },
    { 33, BesFieldNames::Rec::ExtTrack::emcZ },
    { 34, BesFieldNames::Rec::ExtTrack::emcPx },
    { 35, BesFieldNames::Rec::ExtTrack::emcPy },
    { 36, BesFieldNames::Rec::ExtTrack::emcPz },
    { 37, BesFieldNames::Rec::ExtTrack::emcVolumeName },
    { 38, BesFieldNames::Rec::ExtTrack::emcVolumeNumber },
    { 39, BesFieldNames::Rec::ExtTrack::emcPosSigmaAlongTheta },
    { 40, BesFieldNames::Rec::ExtTrack::emcPosSigmaAlongPhi },
    { 41, BesFieldNames::Rec::ExtTrack::emcErrorMatrix },
    { 42, BesFieldNames::Rec::ExtTrack::emcPath },
    { 43, BesFieldNames::Rec::ExtTrack::mucX },
    { 44, BesFieldNames::Rec::ExtTrack::mucY },
    { 45, BesFieldNames::Rec::ExtTrack::mucZ },
    { 46, BesFieldNames::Rec::ExtTrack::mucPx },
    { 47, BesFieldNames::Rec::ExtTrack::mucPy },
    { 48, BesFieldNames::Rec::ExtTrack::mucPz },
    { 49, BesFieldNames::Rec::ExtTrack::mucVolumeName },
    { 50, BesFieldNames::Rec::ExtTrack::mucVolumeNumber },
    { 51, BesFieldNames::Rec::ExtTrack::mucPosSigmaAlongZ },
    { 52, BesFieldNames::Rec::ExtTrack::mucPosSigmaAlongT },
    { 53, BesFieldNames::Rec::ExtTrack::mucPosSigmaAlongX },
    { 54, BesFieldNames::Rec::ExtTrack::mucPosSigmaAlongY },
    { 55, BesFieldNames::Rec::ExtTrack::mucErrorMatrix },
    { 56, BesFieldNames::Rec::ExtTrack::mucHitVecSize },
    { 57, BesFieldNames::Rec::ExtTrack::mucHitX },
    { 58, BesFieldNames::Rec::ExtTrack::mucHitY },
    { 59, BesFieldNames::Rec::ExtTrack::mucHitZ },
    { 60, BesFieldNames::Rec::ExtTrack::mucHitPx },
    { 61, BesFieldNames::Rec::ExtTrack::mucHitPy },
    { 62, BesFieldNames::Rec::ExtTrack::mucHitPz },
    { 63, BesFieldNames::Rec::ExtTrack::mucHitVolumeName },
    { 64, BesFieldNames::Rec::ExtTrack::mucHitVolumeNumber },
    { 65, BesFieldNames::Rec::ExtTrack::mucHitPosSigmaAlongZ },
    { 66, BesFieldNames::Rec::ExtTrack::mucHitPosSigmaAlongT },
    { 67, BesFieldNames::Rec::ExtTrack::mucHitPosSigmaAlongX },
    { 68, BesFieldNames::Rec::ExtTrack::mucHitPosSigmaAlongY },
    { 69, BesFieldNames::Rec::ExtTrack::mucHitErrorMatrix },
};
class BesRFLeafRecExtTrack : public BesRootFieldLeaf<TRecTrackEvent, RecExtTrackRecord> {
  public:
    BesRFLeafRecExtTrack( TRecTrackEvent* obj )
        : BesRootFieldLeaf<TRecTrackEvent, RecExtTrackRecord>(
              obj, BesFieldNames::Rec::ExtTrack::rpath, field_map_rec_exttrack ) {}

    void fill() {
        auto& trackId               = m_builder.content<0>().begin_list();
        auto& tof1X                 = m_builder.content<1>().begin_list();
        auto& tof1Y                 = m_builder.content<2>().begin_list();
        auto& tof1Z                 = m_builder.content<3>().begin_list();
        auto& tof1Px                = m_builder.content<4>().begin_list();
        auto& tof1Py                = m_builder.content<5>().begin_list();
        auto& tof1Pz                = m_builder.content<6>().begin_list();
        auto& tof1VolumeName        = m_builder.content<7>().begin_list();
        auto& tof1VolumeNumber      = m_builder.content<8>().begin_list();
        auto& tof1                  = m_builder.content<9>().begin_list();
        auto& tof1Path              = m_builder.content<10>().begin_list();
        auto& tof1PosSigmaAlongZ    = m_builder.content<11>().begin_list();
        auto& tof1PosSigmaAlongT    = m_builder.content<12>().begin_list();
        auto& tof1PosSigmaAlongX    = m_builder.content<13>().begin_list();
        auto& tof1PosSigmaAlongY    = m_builder.content<14>().begin_list();
        auto& tof1ErrorMatrix       = m_builder.content<15>().begin_list();
        auto& tof2X                 = m_builder.content<16>().begin_list();
        auto& tof2Y                 = m_builder.content<17>().begin_list();
        auto& tof2Z                 = m_builder.content<18>().begin_list();
        auto& tof2Px                = m_builder.content<19>().begin_list();
        auto& tof2Py                = m_builder.content<20>().begin_list();
        auto& tof2Pz                = m_builder.content<21>().begin_list();
        auto& tof2VolumeName        = m_builder.content<22>().begin_list();
        auto& tof2VolumeNumber      = m_builder.content<23>().begin_list();
        auto& tof2                  = m_builder.content<24>().begin_list();
        auto& tof2Path              = m_builder.content<25>().begin_list();
        auto& tof2PosSigmaAlongZ    = m_builder.content<26>().begin_list();
        auto& tof2PosSigmaAlongT    = m_builder.content<27>().begin_list();
        auto& tof2PosSigmaAlongX    = m_builder.content<28>().begin_list();
        auto& tof2PosSigmaAlongY    = m_builder.content<29>().begin_list();
        auto& tof2ErrorMatrix       = m_builder.content<30>().begin_list();
        auto& emcX                  = m_builder.content<31>().begin_list();
        auto& emcY                  = m_builder.content<32>().begin_list();
        auto& emcZ                  = m_builder.content<33>().begin_list();
        auto& emcPx                 = m_builder.content<34>().begin_list();
        auto& emcPy                 = m_builder.content<35>().begin_list();
        auto& emcPz                 = m_builder.content<36>().begin_list();
        auto& emcVolumeName         = m_builder.content<37>().begin_list();
        auto& emcVolumeNumber       = m_builder.content<38>().begin_list();
        auto& emcPosSigmaAlongTheta = m_builder.content<39>().begin_list();
        auto& emcPosSigmaAlongPhi   = m_builder.content<40>().begin_list();
        auto& emcErrorMatrix        = m_builder.content<41>().begin_list();
        auto& emcPath               = m_builder.content<42>().begin_list();
        auto& mucX                  = m_builder.content<43>().begin_list();
        auto& mucY                  = m_builder.content<44>().begin_list();
        auto& mucZ                  = m_builder.content<45>().begin_list();
        auto& mucPx                 = m_builder.content<46>().begin_list();
        auto& mucPy                 = m_builder.content<47>().begin_list();
        auto& mucPz                 = m_builder.content<48>().begin_list();
        auto& mucVolumeName         = m_builder.content<49>().begin_list();
        auto& mucVolumeNumber       = m_builder.content<50>().begin_list();
        auto& mucPosSigmaAlongZ     = m_builder.content<51>().begin_list();
        auto& mucPosSigmaAlongT     = m_builder.content<52>().begin_list();
        auto& mucPosSigmaAlongX     = m_builder.content<53>().begin_list();
        auto& mucPosSigmaAlongY     = m_builder.content<54>().begin_list();
        auto& mucErrorMatrix        = m_builder.content<55>().begin_list();
        auto& mucHitVecSize         = m_builder.content<56>().begin_list();
        auto& mucHitX               = m_builder.content<57>().begin_list();
        auto& mucHitY               = m_builder.content<58>().begin_list();
        auto& mucHitZ               = m_builder.content<59>().begin_list();
        auto& mucHitPx              = m_builder.content<60>().begin_list();
        auto& mucHitPy              = m_builder.content<61>().begin_list();
        auto& mucHitPz              = m_builder.content<62>().begin_list();
        auto& mucHitVolumeName      = m_builder.content<63>().begin_list();
        auto& mucHitVolumeNumber    = m_builder.content<64>().begin_list();
        auto& mucHitPosSigmaAlongZ  = m_builder.content<65>().begin_list();
        auto& mucHitPosSigmaAlongT  = m_builder.content<66>().begin_list();
        auto& mucHitPosSigmaAlongX  = m_builder.content<67>().begin_list();
        auto& mucHitPosSigmaAlongY  = m_builder.content<68>().begin_list();
        auto& mucHitErrorMatrix     = m_builder.content<69>().begin_list();

        for ( auto tobj : *m_obj->getExtTrackCol() )
        {
            TRecExtTrack* obj = static_cast<TRecExtTrack*>( tobj );

            trackId.append( obj->GetTrackId() );

            auto& subtof1X              = tof1X.begin_list();
            auto& subtof1Y              = tof1Y.begin_list();
            auto& subtof1Z              = tof1Z.begin_list();
            auto& subtof1Px             = tof1Px.begin_list();
            auto& subtof1Py             = tof1Py.begin_list();
            auto& subtof1Pz             = tof1Pz.begin_list();
            auto& subtof1VolumeName     = tof1VolumeName.begin_list();
            auto& subtof1VolumeNumber   = tof1VolumeNumber.begin_list();
            auto& subtof1               = tof1.begin_list();
            auto& subtof1Path           = tof1Path.begin_list();
            auto& subtof1PosSigmaAlongZ = tof1PosSigmaAlongZ.begin_list();
            auto& subtof1PosSigmaAlongT = tof1PosSigmaAlongT.begin_list();
            auto& subtof1PosSigmaAlongX = tof1PosSigmaAlongX.begin_list();
            auto& subtof1PosSigmaAlongY = tof1PosSigmaAlongY.begin_list();
            auto& subtof1ErrorMatrix    = tof1ErrorMatrix.begin_list();

            auto& subtof2X              = tof2X.begin_list();
            auto& subtof2Y              = tof2Y.begin_list();
            auto& subtof2Z              = tof2Z.begin_list();
            auto& subtof2Px             = tof2Px.begin_list();
            auto& subtof2Py             = tof2Py.begin_list();
            auto& subtof2Pz             = tof2Pz.begin_list();
            auto& subtof2VolumeName     = tof2VolumeName.begin_list();
            auto& subtof2VolumeNumber   = tof2VolumeNumber.begin_list();
            auto& subtof2               = tof2.begin_list();
            auto& subtof2Path           = tof2Path.begin_list();
            auto& subtof2PosSigmaAlongZ = tof2PosSigmaAlongZ.begin_list();
            auto& subtof2PosSigmaAlongT = tof2PosSigmaAlongT.begin_list();
            auto& subtof2PosSigmaAlongX = tof2PosSigmaAlongX.begin_list();
            auto& subtof2PosSigmaAlongY = tof2PosSigmaAlongY.begin_list();
            auto& subtof2ErrorMatrix    = tof2ErrorMatrix.begin_list();

            auto& subemcX                  = emcX.begin_list();
            auto& subemcY                  = emcY.begin_list();
            auto& subemcZ                  = emcZ.begin_list();
            auto& subemcPx                 = emcPx.begin_list();
            auto& subemcPy                 = emcPy.begin_list();
            auto& subemcPz                 = emcPz.begin_list();
            auto& subemcVolumeName         = emcVolumeName.begin_list();
            auto& subemcVolumeNumber       = emcVolumeNumber.begin_list();
            auto& subemcPosSigmaAlongTheta = emcPosSigmaAlongTheta.begin_list();
            auto& subemcPosSigmaAlongPhi   = emcPosSigmaAlongPhi.begin_list();
            auto& subemcErrorMatrix        = emcErrorMatrix.begin_list();
            auto& subemcPath               = emcPath.begin_list();

            auto& submucX              = mucX.begin_list();
            auto& submucY              = mucY.begin_list();
            auto& submucZ              = mucZ.begin_list();
            auto& submucPx             = mucPx.begin_list();
            auto& submucPy             = mucPy.begin_list();
            auto& submucPz             = mucPz.begin_list();
            auto& submucVolumeName     = mucVolumeName.begin_list();
            auto& submucVolumeNumber   = mucVolumeNumber.begin_list();
            auto& submucPosSigmaAlongZ = mucPosSigmaAlongZ.begin_list();
            auto& submucPosSigmaAlongT = mucPosSigmaAlongT.begin_list();
            auto& submucPosSigmaAlongX = mucPosSigmaAlongX.begin_list();
            auto& submucPosSigmaAlongY = mucPosSigmaAlongY.begin_list();
            auto& submucErrorMatrix    = mucErrorMatrix.begin_list();

            auto& submucHitVecSize        = mucHitVecSize.begin_list();
            auto& submucHitX              = mucHitX.begin_list();
            auto& submucHitY              = mucHitY.begin_list();
            auto& submucHitZ              = mucHitZ.begin_list();
            auto& submucHitPx             = mucHitPx.begin_list();
            auto& submucHitPy             = mucHitPy.begin_list();
            auto& submucHitPz             = mucHitPz.begin_list();
            auto& submucHitVolumeName     = mucHitVolumeName.begin_list();
            auto& submucHitVolumeNumber   = mucHitVolumeNumber.begin_list();
            auto& submucHitPosSigmaAlongZ = mucHitPosSigmaAlongZ.begin_list();
            auto& submucHitPosSigmaAlongT = mucHitPosSigmaAlongT.begin_list();
            auto& submucHitPosSigmaAlongX = mucHitPosSigmaAlongX.begin_list();
            auto& submucHitPosSigmaAlongY = mucHitPosSigmaAlongY.begin_list();
            auto& submucHitErrorMatrix    = mucHitErrorMatrix.begin_list();

            for ( int i = 0; i < 5; i++ )
            {
                subtof1X.append( obj->GetTof1PositionX( i ) );
                subtof1Y.append( obj->GetTof1PositionY( i ) );
                subtof1Z.append( obj->GetTof1PositionZ( i ) );
                subtof1Px.append( obj->GetTof1MomentumX( i ) );
                subtof1Py.append( obj->GetTof1MomentumY( i ) );
                subtof1Pz.append( obj->GetTof1MomentumZ( i ) );
                subtof1VolumeName.append( obj->GetTof1VolumeName( i ).Data() );
                subtof1VolumeNumber.append( obj->GetTof1VolumeNumber( i ) );
                subtof1.append( obj->GetTof1( i ) );
                subtof1Path.append( obj->GetTof1Path( i ) );
                subtof1PosSigmaAlongZ.append( obj->GetTof1PosSigmaAlongZ( i ) );
                subtof1PosSigmaAlongT.append( obj->GetTof1PosSigmaAlongT( i ) );
                subtof1PosSigmaAlongX.append( obj->GetTof1PosSigmaAlongX( i ) );
                subtof1PosSigmaAlongY.append( obj->GetTof1PosSigmaAlongY( i ) );

                subtof2X.append( obj->GetTof2PositionX( i ) );
                subtof2Y.append( obj->GetTof2PositionY( i ) );
                subtof2Z.append( obj->GetTof2PositionZ( i ) );
                subtof2Px.append( obj->GetTof2MomentumX( i ) );
                subtof2Py.append( obj->GetTof2MomentumY( i ) );
                subtof2Pz.append( obj->GetTof2MomentumZ( i ) );
                subtof2VolumeName.append( obj->GetTof2VolumeName( i ).Data() );
                subtof2VolumeNumber.append( obj->GetTof2VolumeNumber( i ) );
                subtof2.append( obj->GetTof2( i ) );
                subtof2Path.append( obj->GetTof2Path( i ) );
                subtof2PosSigmaAlongZ.append( obj->GetTof2PosSigmaAlongZ( i ) );
                subtof2PosSigmaAlongT.append( obj->GetTof2PosSigmaAlongT( i ) );
                subtof2PosSigmaAlongX.append( obj->GetTof2PosSigmaAlongX( i ) );
                subtof2PosSigmaAlongY.append( obj->GetTof2PosSigmaAlongY( i ) );

                subemcX.append( obj->GetEmcPositionX( i ) );
                subemcY.append( obj->GetEmcPositionY( i ) );
                subemcZ.append( obj->GetEmcPositionZ( i ) );
                subemcPx.append( obj->GetEmcMomentumX( i ) );
                subemcPy.append( obj->GetEmcMomentumY( i ) );
                subemcPz.append( obj->GetEmcMomentumZ( i ) );
                subemcVolumeName.append( obj->GetEmcVolumeName( i ).Data() );
                subemcVolumeNumber.append( obj->GetEmcVolumeNumber( i ) );
                subemcPosSigmaAlongTheta.append( obj->GetEmcPosSigmaAlongTheta( i ) );
                subemcPosSigmaAlongPhi.append( obj->GetEmcPosSigmaAlongPhi( i ) );
                subemcPath.append( obj->emcPath( i ) );

                submucX.append( obj->GetMucPositionX( i ) );
                submucY.append( obj->GetMucPositionY( i ) );
                submucZ.append( obj->GetMucPositionZ( i ) );
                submucPx.append( obj->GetMucMomentumX( i ) );
                submucPy.append( obj->GetMucMomentumY( i ) );
                submucPz.append( obj->GetMucMomentumZ( i ) );
                submucVolumeName.append( obj->GetMucVolumeName( i ).Data() );
                submucVolumeNumber.append( obj->GetMucVolumeNumber( i ) );
                submucPosSigmaAlongZ.append( obj->GetMucPosSigmaAlongZ( i ) );
                submucPosSigmaAlongT.append( obj->GetMucPosSigmaAlongT( i ) );
                submucPosSigmaAlongX.append( obj->GetMucPosSigmaAlongX( i ) );
                submucPosSigmaAlongY.append( obj->GetMucPosSigmaAlongY( i ) );

                submucHitVecSize.append( obj->GetSize( i ) );

                auto& ssubmucHitX              = submucHitX.begin_list();
                auto& ssubmucHitY              = submucHitY.begin_list();
                auto& ssubmucHitZ              = submucHitZ.begin_list();
                auto& ssubmucHitPx             = submucHitPx.begin_list();
                auto& ssubmucHitPy             = submucHitPy.begin_list();
                auto& ssubmucHitPz             = submucHitPz.begin_list();
                auto& ssubmucHitVolumeName     = submucHitVolumeName.begin_list();
                auto& ssubmucHitVolumeNumber   = submucHitVolumeNumber.begin_list();
                auto& ssubmucHitPosSigmaAlongZ = submucHitPosSigmaAlongZ.begin_list();
                auto& ssubmucHitPosSigmaAlongT = submucHitPosSigmaAlongT.begin_list();
                auto& ssubmucHitPosSigmaAlongX = submucHitPosSigmaAlongX.begin_list();
                auto& ssubmucHitPosSigmaAlongY = submucHitPosSigmaAlongY.begin_list();
                auto& ssubmucHitErrorMatrix    = submucHitErrorMatrix.begin_list();

                for ( int j = 0; j < obj->GetSize( i ); j++ )
                {
                    ssubmucHitX.append( obj->GetPositionX( j, i ) );
                    ssubmucHitY.append( obj->GetPositionY( j, i ) );
                    ssubmucHitZ.append( obj->GetPositionZ( j, i ) );
                    ssubmucHitPx.append( obj->GetMomentumX( j, i ) );
                    ssubmucHitPy.append( obj->GetMomentumY( j, i ) );
                    ssubmucHitPz.append( obj->GetMomentumZ( j, i ) );
                    ssubmucHitVolumeName.append( obj->GetVolumeName( j, i ).Data() );
                    ssubmucHitVolumeNumber.append( obj->GetVolumeNumber( j, i ) );
                    ssubmucHitPosSigmaAlongZ.append( obj->GetPosSigmaAlongZ( j, i ) );
                    ssubmucHitPosSigmaAlongT.append( obj->GetPosSigmaAlongT( j, i ) );
                    ssubmucHitPosSigmaAlongX.append( obj->GetPosSigmaAlongX( j, i ) );
                    ssubmucHitPosSigmaAlongY.append( obj->GetPosSigmaAlongY( j, i ) );

                    auto& sssubmucHitErrorMatrix = ssubmucHitErrorMatrix.begin_list();
                    for ( double v : obj->GetErrorMatrix( j, i ) )
                    { sssubmucHitErrorMatrix.append( v ); }
                    ssubmucHitErrorMatrix.end_list();
                }

                // error matrix
                auto& ssubtof1ErrorMatrix = subtof1ErrorMatrix.begin_list();
                auto& ssubtof2ErrorMatrix = subtof2ErrorMatrix.begin_list();
                auto& ssubemcErrorMatrix  = subemcErrorMatrix.begin_list();
                auto& ssubmucErrorMatrix  = submucErrorMatrix.begin_list();
                for ( int j = 0; j < 6; j++ )
                {
                    auto& sssubtof1ErrorMatrix = ssubtof1ErrorMatrix.begin_list();
                    auto& sssubtof2ErrorMatrix = ssubtof2ErrorMatrix.begin_list();
                    auto& sssubemcErrorMatrix  = ssubemcErrorMatrix.begin_list();
                    auto& sssubmucErrorMatrix  = ssubmucErrorMatrix.begin_list();
                    for ( int k = 0; k < 6; k++ )
                    {
                        sssubtof1ErrorMatrix.append( obj->GetTof1ErrorMatrix( i, j, k ) );
                        sssubtof2ErrorMatrix.append( obj->GetTof2ErrorMatrix( i, j, k ) );
                        sssubemcErrorMatrix.append( obj->GetEmcErrorMatrix( i, j, k ) );
                        sssubmucErrorMatrix.append( obj->GetMucErrorMatrix( i, j, k ) );
                    }
                    ssubtof1ErrorMatrix.end_list();
                    ssubtof2ErrorMatrix.end_list();
                    ssubemcErrorMatrix.end_list();
                    ssubmucErrorMatrix.end_list();
                }
                subtof1ErrorMatrix.end_list();
                subtof2ErrorMatrix.end_list();
                subemcErrorMatrix.end_list();
                submucErrorMatrix.end_list();
            }

            m_builder.content<0>().end_list();
            m_builder.content<1>().end_list();
            m_builder.content<2>().end_list();
            m_builder.content<3>().end_list();
            m_builder.content<4>().end_list();
            m_builder.content<5>().end_list();
            m_builder.content<6>().end_list();
            m_builder.content<7>().end_list();
            m_builder.content<8>().end_list();
            m_builder.content<9>().end_list();
            m_builder.content<10>().end_list();
            m_builder.content<11>().end_list();
            m_builder.content<12>().end_list();
            m_builder.content<13>().end_list();
            m_builder.content<14>().end_list();
            m_builder.content<15>().end_list();
            m_builder.content<16>().end_list();
            m_builder.content<17>().end_list();
            m_builder.content<18>().end_list();
            m_builder.content<19>().end_list();
            m_builder.content<20>().end_list();
            m_builder.content<21>().end_list();
            m_builder.content<22>().end_list();
            m_builder.content<23>().end_list();
            m_builder.content<24>().end_list();
            m_builder.content<25>().end_list();
            m_builder.content<26>().end_list();
            m_builder.content<27>().end_list();
            m_builder.content<28>().end_list();
            m_builder.content<29>().end_list();
            m_builder.content<30>().end_list();
            m_builder.content<31>().end_list();
            m_builder.content<32>().end_list();
            m_builder.content<33>().end_list();
            m_builder.content<34>().end_list();
            m_builder.content<35>().end_list();
            m_builder.content<36>().end_list();
            m_builder.content<37>().end_list();
            m_builder.content<38>().end_list();
            m_builder.content<39>().end_list();
            m_builder.content<40>().end_list();
            m_builder.content<41>().end_list();
            m_builder.content<42>().end_list();
            m_builder.content<43>().end_list();
            m_builder.content<44>().end_list();
            m_builder.content<45>().end_list();
            m_builder.content<46>().end_list();
            m_builder.content<47>().end_list();
            m_builder.content<48>().end_list();
            m_builder.content<49>().end_list();
            m_builder.content<50>().end_list();
            m_builder.content<51>().end_list();
            m_builder.content<52>().end_list();
            m_builder.content<53>().end_list();
            m_builder.content<54>().end_list();
            m_builder.content<55>().end_list();
            m_builder.content<56>().end_list();
            m_builder.content<57>().end_list();
            m_builder.content<58>().end_list();
            m_builder.content<59>().end_list();
            m_builder.content<60>().end_list();
            m_builder.content<61>().end_list();
            m_builder.content<62>().end_list();
            m_builder.content<63>().end_list();
            m_builder.content<64>().end_list();
            m_builder.content<65>().end_list();
            m_builder.content<66>().end_list();
            m_builder.content<67>().end_list();
            m_builder.content<68>().end_list();
            m_builder.content<69>().end_list();
        }
    }
};
