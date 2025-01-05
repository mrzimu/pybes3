#pragma once

#include <awkward/LayoutBuilder.h>

#include "RootEventData/TDstEvent.h"
#include "RootEventData/TExtTrack.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using DstExtRecord = RecordBuilder<
    // trackIndex
    RaggedItemField<0, int>,

    // Tof Layer 1
    RaggedItemField<1, double>,       // x
    RaggedItemField<2, double>,       // y
    RaggedItemField<3, double>,       // z
    RaggedItemField<4, double>,       // px
    RaggedItemField<5, double>,       // py
    RaggedItemField<6, double>,       // pz
    RaggedStringField<7>,             // Tof volume name
    RaggedItemField<8, int>,          // Tof volume number
    RaggedItemField<9, double>,       // Time of flight
    RaggedItemField<10, double>,      // Path of flight
    RaggedItemField<11, double>,      // PosSigmaAlongZ
    RaggedItemField<12, double>,      // PosSigmaAlong Z x R
    RaggedItemField<13, double>,      // PosSigmaAlongX
    RaggedItemField<14, double>,      // PosSigmaAlongY
    RaggedArrayField<15, 21, double>, // ErrorMatrix

    // Tof Layer 2
    RaggedItemField<16, double>,      // x
    RaggedItemField<17, double>,      // y
    RaggedItemField<18, double>,      // z
    RaggedItemField<19, double>,      // px
    RaggedItemField<20, double>,      // py
    RaggedItemField<21, double>,      // pz
    RaggedStringField<22>,            // Tof volume name
    RaggedItemField<23, int>,         // Tof volume number
    RaggedItemField<24, double>,      // Time of flight
    RaggedItemField<25, double>,      // Path of flight
    RaggedItemField<26, double>,      // PosSigmaAlongZ
    RaggedItemField<27, double>,      // PosSigmaAlong Z x R
    RaggedItemField<28, double>,      // PosSigmaAlongX
    RaggedItemField<29, double>,      // PosSigmaAlongY
    RaggedArrayField<30, 21, double>, // ErrorMatrix

    // Emc
    RaggedItemField<31, double>,      // x
    RaggedItemField<32, double>,      // y
    RaggedItemField<33, double>,      // z
    RaggedItemField<34, double>,      // px
    RaggedItemField<35, double>,      // py
    RaggedItemField<36, double>,      // pz
    RaggedStringField<37>,            // volume name
    RaggedItemField<38, int>,         // volume number
    RaggedItemField<39, double>,      // PosSigmaAlongTheta
    RaggedItemField<40, double>,      // PosSigmaAlongPhi
    RaggedArrayField<41, 21, double>, // ErrorMatrix
    RaggedItemField<42, double>,      // Path

    // Muc
    RaggedItemField<43, double>,     // x
    RaggedItemField<44, double>,     // y
    RaggedItemField<45, double>,     // z
    RaggedItemField<46, double>,     // px
    RaggedItemField<47, double>,     // py
    RaggedItemField<48, double>,     // pz
    RaggedStringField<49>,           // volume name
    RaggedItemField<50, int>,        // volume number
    RaggedItemField<51, double>,     // PosSigmaAlongZ
    RaggedItemField<52, double>,     // PosSigmaAlongT
    RaggedItemField<53, double>,     // PosSigmaAlongX
    RaggedItemField<54, double>,     // PosSigmaAlongY
    RaggedArrayField<55, 21, double> // ErrorMatrix
    >;

const FieldMap field_map_dst_ext = { { 0, BesFieldNames::Dst::Ext::trackIndex },

                                     // Tof Layer 1
                                     { 1, BesFieldNames::Dst::Ext::Tof1X },
                                     { 2, BesFieldNames::Dst::Ext::Tof1Y },
                                     { 3, BesFieldNames::Dst::Ext::Tof1Z },
                                     { 4, BesFieldNames::Dst::Ext::Tof1Px },
                                     { 5, BesFieldNames::Dst::Ext::Tof1Py },
                                     { 6, BesFieldNames::Dst::Ext::Tof1Pz },
                                     { 7, BesFieldNames::Dst::Ext::Tof1VolumeName },
                                     { 8, BesFieldNames::Dst::Ext::Tof1VolumeNumber },
                                     { 9, BesFieldNames::Dst::Ext::Tof1 },
                                     { 10, BesFieldNames::Dst::Ext::Tof1Path },
                                     { 11, BesFieldNames::Dst::Ext::Tof1PosSigmaAlongZ },
                                     { 12, BesFieldNames::Dst::Ext::Tof1PosSigmaAlongT },
                                     { 13, BesFieldNames::Dst::Ext::Tof1PosSigmaAlongX },
                                     { 14, BesFieldNames::Dst::Ext::Tof1PosSigmaAlongY },
                                     { 15, BesFieldNames::Dst::Ext::Tof1ErrorMatrix },

                                     // Tof Layer 2
                                     { 16, BesFieldNames::Dst::Ext::Tof2X },
                                     { 17, BesFieldNames::Dst::Ext::Tof2Y },
                                     { 18, BesFieldNames::Dst::Ext::Tof2Z },
                                     { 19, BesFieldNames::Dst::Ext::Tof2Px },
                                     { 20, BesFieldNames::Dst::Ext::Tof2Py },
                                     { 21, BesFieldNames::Dst::Ext::Tof2Pz },
                                     { 22, BesFieldNames::Dst::Ext::Tof2VolumeName },
                                     { 23, BesFieldNames::Dst::Ext::Tof2VolumeNumber },
                                     { 24, BesFieldNames::Dst::Ext::Tof2 },
                                     { 25, BesFieldNames::Dst::Ext::Tof2Path },
                                     { 26, BesFieldNames::Dst::Ext::Tof2PosSigmaAlongZ },
                                     { 27, BesFieldNames::Dst::Ext::Tof2PosSigmaAlongT },
                                     { 28, BesFieldNames::Dst::Ext::Tof2PosSigmaAlongX },
                                     { 29, BesFieldNames::Dst::Ext::Tof2PosSigmaAlongY },
                                     { 30, BesFieldNames::Dst::Ext::Tof2ErrorMatrix },

                                     // Emc
                                     { 31, BesFieldNames::Dst::Ext::EmcX },
                                     { 32, BesFieldNames::Dst::Ext::EmcY },
                                     { 33, BesFieldNames::Dst::Ext::EmcZ },
                                     { 34, BesFieldNames::Dst::Ext::EmcPx },
                                     { 35, BesFieldNames::Dst::Ext::EmcPy },
                                     { 36, BesFieldNames::Dst::Ext::EmcPz },
                                     { 37, BesFieldNames::Dst::Ext::EmcVolumeName },
                                     { 38, BesFieldNames::Dst::Ext::EmcVolumeNumber },
                                     { 39, BesFieldNames::Dst::Ext::EmcPosSigmaAlongTheta },
                                     { 40, BesFieldNames::Dst::Ext::EmcPosSigmaAlongPhi },
                                     { 41, BesFieldNames::Dst::Ext::EmcErrorMatrix },
                                     { 42, BesFieldNames::Dst::Ext::EmcPath },

                                     // Muc
                                     { 43, BesFieldNames::Dst::Ext::MucX },
                                     { 44, BesFieldNames::Dst::Ext::MucY },
                                     { 45, BesFieldNames::Dst::Ext::MucZ },
                                     { 46, BesFieldNames::Dst::Ext::MucPx },
                                     { 47, BesFieldNames::Dst::Ext::MucPy },
                                     { 48, BesFieldNames::Dst::Ext::MucPz },
                                     { 49, BesFieldNames::Dst::Ext::MucVolumeName },
                                     { 50, BesFieldNames::Dst::Ext::MucVolumeNumber },
                                     { 51, BesFieldNames::Dst::Ext::MucPosSigmaAlongZ },
                                     { 52, BesFieldNames::Dst::Ext::MucPosSigmaAlongT },
                                     { 53, BesFieldNames::Dst::Ext::MucPosSigmaAlongX },
                                     { 54, BesFieldNames::Dst::Ext::MucPosSigmaAlongY },
                                     { 55, BesFieldNames::Dst::Ext::MucErrorMatrix } };

class BesRFLeafDstExt : public BesRootFieldLeaf<TDstEvent, DstExtRecord> {
  public:
    BesRFLeafDstExt( TDstEvent* obj )
        : BesRootFieldLeaf<TDstEvent, DstExtRecord>( obj, BesFieldNames::Dst::Ext::rpath,
                                                     field_map_dst_ext ) {}

    void fill() {
        auto& trackIndex = m_builder.content<0>().begin_list();

        // Tof Layer 1
        auto& tof1_x                 = m_builder.content<1>().begin_list();
        auto& tof1_y                 = m_builder.content<2>().begin_list();
        auto& tof1_z                 = m_builder.content<3>().begin_list();
        auto& tof1_px                = m_builder.content<4>().begin_list();
        auto& tof1_py                = m_builder.content<5>().begin_list();
        auto& tof1_pz                = m_builder.content<6>().begin_list();
        auto& tof1_volume_name       = m_builder.content<7>().begin_list();
        auto& tof1_volume_number     = m_builder.content<8>().begin_list();
        auto& tof1_time              = m_builder.content<9>().begin_list();
        auto& tof1_path              = m_builder.content<10>().begin_list();
        auto& tof1_pos_sigma_along_z = m_builder.content<11>().begin_list();
        auto& tof1_pos_sigma_along_t = m_builder.content<12>().begin_list();
        auto& tof1_pos_sigma_along_x = m_builder.content<13>().begin_list();
        auto& tof1_pos_sigma_along_y = m_builder.content<14>().begin_list();
        auto& tof1_err               = m_builder.content<15>().begin_list();

        // Tof Layer 2
        auto& tof2_x                 = m_builder.content<16>().begin_list();
        auto& tof2_y                 = m_builder.content<17>().begin_list();
        auto& tof2_z                 = m_builder.content<18>().begin_list();
        auto& tof2_px                = m_builder.content<19>().begin_list();
        auto& tof2_py                = m_builder.content<20>().begin_list();
        auto& tof2_pz                = m_builder.content<21>().begin_list();
        auto& tof2_volume_name       = m_builder.content<22>().begin_list();
        auto& tof2_volume_number     = m_builder.content<23>().begin_list();
        auto& tof2_time              = m_builder.content<24>().begin_list();
        auto& tof2_path              = m_builder.content<25>().begin_list();
        auto& tof2_pos_sigma_along_z = m_builder.content<26>().begin_list();
        auto& tof2_pos_sigma_along_t = m_builder.content<27>().begin_list();
        auto& tof2_pos_sigma_along_x = m_builder.content<28>().begin_list();
        auto& tof2_pos_sigma_along_y = m_builder.content<29>().begin_list();
        auto& tof2_err               = m_builder.content<30>().begin_list();

        // Emc
        auto& emc_x                     = m_builder.content<31>().begin_list();
        auto& emc_y                     = m_builder.content<32>().begin_list();
        auto& emc_z                     = m_builder.content<33>().begin_list();
        auto& emc_px                    = m_builder.content<34>().begin_list();
        auto& emc_py                    = m_builder.content<35>().begin_list();
        auto& emc_pz                    = m_builder.content<36>().begin_list();
        auto& emc_volume_name           = m_builder.content<37>().begin_list();
        auto& emc_volume_number         = m_builder.content<38>().begin_list();
        auto& emc_pos_sigma_along_theta = m_builder.content<39>().begin_list();
        auto& emc_pos_sigma_along_phi   = m_builder.content<40>().begin_list();
        auto& emc_err                   = m_builder.content<41>().begin_list();
        auto& emc_path                  = m_builder.content<42>().begin_list();

        // Muc
        auto& muc_x                 = m_builder.content<43>().begin_list();
        auto& muc_y                 = m_builder.content<44>().begin_list();
        auto& muc_z                 = m_builder.content<45>().begin_list();
        auto& muc_px                = m_builder.content<46>().begin_list();
        auto& muc_py                = m_builder.content<47>().begin_list();
        auto& muc_pz                = m_builder.content<48>().begin_list();
        auto& muc_volume_name       = m_builder.content<49>().begin_list();
        auto& muc_volume_number     = m_builder.content<50>().begin_list();
        auto& muc_pos_sigma_along_z = m_builder.content<51>().begin_list();
        auto& muc_pos_sigma_along_t = m_builder.content<52>().begin_list();
        auto& muc_pos_sigma_along_x = m_builder.content<53>().begin_list();
        auto& muc_pos_sigma_along_y = m_builder.content<54>().begin_list();
        auto& muc_err               = m_builder.content<55>().begin_list();

        for ( const auto tobj : ( *m_obj->getExtTrackCol() ) )
        {
            TExtTrack* trk = static_cast<TExtTrack*>( tobj );

            trackIndex.append( trk->GetTrackId() );

            // Tof Layer 1
            tof1_x.append( trk->GetTof1PositionX() );
            tof1_y.append( trk->GetTof1PositionY() );
            tof1_z.append( trk->GetTof1PositionZ() );
            tof1_px.append( trk->GetTof1MomentumX() );
            tof1_py.append( trk->GetTof1MomentumY() );
            tof1_pz.append( trk->GetTof1MomentumZ() );
            tof1_volume_name.append( trk->GetTof1VolumeName().Data() );
            tof1_volume_number.append( trk->GetTof1VolumeNumber() );
            tof1_time.append( trk->GetTof1() );
            tof1_path.append( trk->GetTof1Path() );
            tof1_pos_sigma_along_z.append( trk->GetTof1PosSigmaAlongZ() );
            tof1_pos_sigma_along_t.append( trk->GetTof1PosSigmaAlongT() );
            tof1_pos_sigma_along_x.append( trk->GetTof1PosSigmaAlongX() );
            tof1_pos_sigma_along_y.append( trk->GetTof1PosSigmaAlongY() );

            auto& sub_tof1_err = tof1_err.begin_list();
            for ( int i = 0; i < 6; i++ )
            {
                for ( int j = 0; j <= i; j++ )
                { sub_tof1_err.append( trk->GetTof1ErrorMatrix( i, j ) ); }
            }
            tof1_err.end_list();

            // Tof Layer 2
            tof2_x.append( trk->GetTof2PositionX() );
            tof2_y.append( trk->GetTof2PositionY() );
            tof2_z.append( trk->GetTof2PositionZ() );
            tof2_px.append( trk->GetTof2MomentumX() );
            tof2_py.append( trk->GetTof2MomentumY() );
            tof2_pz.append( trk->GetTof2MomentumZ() );
            tof2_volume_name.append( trk->GetTof2VolumeName().Data() );
            tof2_volume_number.append( trk->GetTof2VolumeNumber() );
            tof2_time.append( trk->GetTof2() );
            tof2_path.append( trk->GetTof2Path() );
            tof2_pos_sigma_along_z.append( trk->GetTof2PosSigmaAlongZ() );
            tof2_pos_sigma_along_t.append( trk->GetTof2PosSigmaAlongT() );
            tof2_pos_sigma_along_x.append( trk->GetTof2PosSigmaAlongX() );
            tof2_pos_sigma_along_y.append( trk->GetTof2PosSigmaAlongY() );

            auto& sub_tof2_err = tof2_err.begin_list();
            for ( int i = 0; i < 6; i++ )
            {
                for ( int j = 0; j <= i; j++ )
                { sub_tof2_err.append( trk->GetTof2ErrorMatrix( i, j ) ); }
            }
            tof2_err.end_list();

            // Emc
            emc_x.append( trk->GetEmcPositionX() );
            emc_y.append( trk->GetEmcPositionY() );
            emc_z.append( trk->GetEmcPositionZ() );
            emc_px.append( trk->GetEmcMomentumX() );
            emc_py.append( trk->GetEmcMomentumY() );
            emc_pz.append( trk->GetEmcMomentumZ() );
            emc_volume_name.append( trk->GetEmcVolumeName().Data() );
            emc_volume_number.append( trk->GetEmcVolumeNumber() );
            emc_pos_sigma_along_theta.append( trk->GetEmcPosSigmaAlongTheta() );
            emc_pos_sigma_along_phi.append( trk->GetEmcPosSigmaAlongPhi() );

            auto& sub_emc_err = emc_err.begin_list();
            for ( int i = 0; i < 6; i++ )
            {
                for ( int j = 0; j <= i; j++ )
                { sub_emc_err.append( trk->GetEmcErrorMatrix( i, j ) ); }
            }
            emc_err.end_list();

            emc_path.append( trk->emcPath() );

            // Muc
            muc_x.append( trk->GetMucPositionX() );
            muc_y.append( trk->GetMucPositionY() );
            muc_z.append( trk->GetMucPositionZ() );
            muc_px.append( trk->GetMucMomentumX() );
            muc_py.append( trk->GetMucMomentumY() );
            muc_pz.append( trk->GetMucMomentumZ() );
            muc_volume_name.append( trk->GetMucVolumeName().Data() );
            muc_volume_number.append( trk->GetMucVolumeNumber() );

            auto& sub_muc_err = muc_err.begin_list();
            for ( int i = 0; i < 6; i++ )
            {
                for ( int j = 0; j <= i; j++ )
                { sub_muc_err.append( trk->GetMucErrorMatrix( i, j ) ); }
            }
            muc_err.end_list();
        }

        m_builder.content<0>().end_list();

        // Tof Layer 1
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

        // Tof Layer 2
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

        // Emc
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

        // Muc
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
    }
};