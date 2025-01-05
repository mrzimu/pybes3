#pragma once

#include <awkward/LayoutBuilder.h>

#include "RootEventData/TDstEvent.h"
#include "RootEventData/TTofTrack.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using DstTofRecord = RecordBuilder<RaggedItemField<0, int>,          // trackIndex
                                   RaggedItemField<1, int>,          // inTrackId
                                   RaggedItemField<2, int>,          // tofId
                                   RaggedItemField<3, unsigned int>, // status
                                   RaggedItemField<4, double>,       // path
                                   RaggedItemField<5, double>,       // arhig
                                   RaggedItemField<6, double>,       // ph
                                   RaggedItemField<7, double>,       // tof
                                   RaggedItemField<8, double>,       // beta
                                   RaggedArrayField<9, 5, double>,   // texp
                                   RaggedArrayField<9, 6, double>,   // toffset
                                   RaggedArrayField<9, 6, double>,   // sigma
                                   RaggedItemField<12, int>,         // quality
                                   RaggedItemField<13, double>,      // t0
                                   RaggedItemField<14, double>,      // errt0
                                   RaggedItemField<15, double>,      // errz
                                   RaggedItemField<16, double>,      // phi
                                   RaggedItemField<17, double>,      // errphi
                                   RaggedItemField<18, double>,      // energy
                                   RaggedItemField<19, double>       // errenergy
                                   >;

const FieldMap field_map_dst_tof = {
    { 0, BesFieldNames::Dst::Tof::trackIndex }, { 1, BesFieldNames::Dst::Tof::inTrackId },
    { 2, BesFieldNames::Dst::Tof::tofId },      { 3, BesFieldNames::Dst::Tof::status },
    { 4, BesFieldNames::Dst::Tof::path },       { 5, BesFieldNames::Dst::Tof::zrhit },
    { 6, BesFieldNames::Dst::Tof::ph },         { 7, BesFieldNames::Dst::Tof::tof },
    { 8, BesFieldNames::Dst::Tof::beta },       { 9, BesFieldNames::Dst::Tof::texp },
    { 10, BesFieldNames::Dst::Tof::toffset },   { 11, BesFieldNames::Dst::Tof::sigma },
    { 12, BesFieldNames::Dst::Tof::quality },   { 13, BesFieldNames::Dst::Tof::t0 },
    { 14, BesFieldNames::Dst::Tof::t0Err },     { 15, BesFieldNames::Dst::Tof::zErr },
    { 16, BesFieldNames::Dst::Tof::phi },       { 17, BesFieldNames::Dst::Tof::errphi },
    { 18, BesFieldNames::Dst::Tof::energy },    { 19, BesFieldNames::Dst::Tof::energyErr } };

class BesRFLeafDstTof : public BesRootFieldLeaf<TDstEvent, DstTofRecord> {
  public:
    BesRFLeafDstTof( TDstEvent* obj )
        : BesRootFieldLeaf<TDstEvent, DstTofRecord>( obj, BesFieldNames::Dst::Tof::rpath,
                                                     field_map_dst_tof ) {}

    void init() { m_builder.set_fields( field_map_dst_tof ); }

    void fill() {
        auto& trackIndex = m_builder.content<0>().begin_list();
        auto& inTrackId  = m_builder.content<1>().begin_list();
        auto& tofId      = m_builder.content<2>().begin_list();
        auto& status     = m_builder.content<3>().begin_list();
        auto& path       = m_builder.content<4>().begin_list();
        auto& zrhit      = m_builder.content<5>().begin_list();
        auto& ph         = m_builder.content<6>().begin_list();
        auto& tof        = m_builder.content<7>().begin_list();
        auto& beta       = m_builder.content<8>().begin_list();
        auto& texp       = m_builder.content<9>().begin_list();
        auto& toffset    = m_builder.content<10>().begin_list();
        auto& sigma      = m_builder.content<11>().begin_list();
        auto& quality    = m_builder.content<12>().begin_list();
        auto& t0         = m_builder.content<13>().begin_list();
        auto& errt0      = m_builder.content<14>().begin_list();
        auto& errz       = m_builder.content<15>().begin_list();
        auto& phi        = m_builder.content<16>().begin_list();
        auto& errphi     = m_builder.content<17>().begin_list();
        auto& energy     = m_builder.content<18>().begin_list();
        auto& errenergy  = m_builder.content<19>().begin_list();

        for ( auto tobj : ( *m_obj->getTofTrackCol() ) )
        {
            TTofTrack* trk = static_cast<TTofTrack*>( tobj );

            trackIndex.append( trk->tofTrackID() );
            inTrackId.append( trk->trackID() );
            tofId.append( trk->tofID() );
            status.append( trk->status() );
            path.append( trk->path() );
            zrhit.append( trk->zrhit() );
            ph.append( trk->ph() );
            tof.append( trk->tof() );
            beta.append( trk->beta() );

            auto& sub_texp = texp.begin_list();
            sub_texp.append( trk->texpElectron() );
            sub_texp.append( trk->texpMuon() );
            sub_texp.append( trk->texpPion() );
            sub_texp.append( trk->texpKaon() );
            sub_texp.append( trk->texpProton() );
            texp.end_list();

            auto& sub_toffset = toffset.begin_list();
            sub_toffset.append( trk->toffsetElectron() );
            sub_toffset.append( trk->toffsetMuon() );
            sub_toffset.append( trk->toffsetPion() );
            sub_toffset.append( trk->toffsetKaon() );
            sub_toffset.append( trk->toffsetProton() );
            sub_toffset.append( trk->toffsetAntiProton() );
            toffset.end_list();

            auto& sub_sigma = sigma.begin_list();
            sub_sigma.append( trk->sigmaElectron() );
            sub_sigma.append( trk->sigmaMuon() );
            sub_sigma.append( trk->sigmaPion() );
            sub_sigma.append( trk->sigmaKaon() );
            sub_sigma.append( trk->sigmaProton() );
            sub_sigma.append( trk->sigmaAntiProton() );
            sigma.end_list();

            quality.append( trk->quality() );
            t0.append( trk->t0() );
            errt0.append( trk->errt0() );
            errz.append( trk->errz() );
            phi.append( trk->phi() );
            errphi.append( trk->errphi() );
            energy.append( trk->energy() );
            errenergy.append( trk->errenergy() );
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
    }
};