#pragma once

#include "RootEventData/TRecTofTrack.h"
#include "RootEventData/TRecTrackEvent.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using RecTofTrackRecord = RecordBuilder<RaggedItemField<0, int>,         // trackId
                                        RaggedItemField<1, int>,         // inTrackId
                                        RaggedItemField<2, int>,         // tofId
                                        RaggedItemField<3, unsigned>,    // status
                                        RaggedItemField<4, double>,      // path
                                        RaggedItemField<5, double>,      // zrhit
                                        RaggedItemField<6, double>,      // ph
                                        RaggedItemField<7, double>,      // tof
                                        RaggedItemField<8, double>,      // beta
                                        RaggedArrayField<9, 5, double>,  // texp
                                        RaggedArrayField<10, 6, double>, // toffset
                                        RaggedArrayField<11, 6, double>, // sigma
                                        RaggedItemField<12, int>,        // quality
                                        RaggedItemField<13, double>,     // t0
                                        RaggedItemField<14, double>,     // errt0
                                        RaggedItemField<15, double>,     // errz
                                        RaggedItemField<16, double>,     // phi
                                        RaggedItemField<17, double>,     // errphi
                                        RaggedItemField<18, double>,     // energy
                                        RaggedItemField<19, double>      // errenergy
                                        >;

const FieldMap field_map_rec_toftrack = { { 0, BesFieldNames::Rec::TofTrack::trackId },
                                          { 1, BesFieldNames::Rec::TofTrack::inTrackId },
                                          { 2, BesFieldNames::Rec::TofTrack::tofId },
                                          { 3, BesFieldNames::Rec::TofTrack::status },
                                          { 4, BesFieldNames::Rec::TofTrack::path },
                                          { 5, BesFieldNames::Rec::TofTrack::zrhit },
                                          { 6, BesFieldNames::Rec::TofTrack::ph },
                                          { 7, BesFieldNames::Rec::TofTrack::tof },
                                          { 8, BesFieldNames::Rec::TofTrack::beta },
                                          { 9, BesFieldNames::Rec::TofTrack::texp },
                                          { 10, BesFieldNames::Rec::TofTrack::toffset },
                                          { 11, BesFieldNames::Rec::TofTrack::sigma },
                                          { 12, BesFieldNames::Rec::TofTrack::quality },
                                          { 13, BesFieldNames::Rec::TofTrack::t0 },
                                          { 14, BesFieldNames::Rec::TofTrack::errt0 },
                                          { 15, BesFieldNames::Rec::TofTrack::errz },
                                          { 16, BesFieldNames::Rec::TofTrack::phi },
                                          { 17, BesFieldNames::Rec::TofTrack::errphi },
                                          { 18, BesFieldNames::Rec::TofTrack::energy },
                                          { 19, BesFieldNames::Rec::TofTrack::errenergy } };

class BesRFLeafRecTofTrack : public BesRootFieldLeaf<TRecTrackEvent, RecTofTrackRecord> {
  public:
    BesRFLeafRecTofTrack( TRecTrackEvent* obj )
        : BesRootFieldLeaf<TRecTrackEvent, RecTofTrackRecord>(
              obj, BesFieldNames::Rec::TofTrack::rpath, field_map_rec_toftrack ) {}

    void fill() {
        auto& trackId   = m_builder.content<0>().begin_list();
        auto& inTrackId = m_builder.content<1>().begin_list();
        auto& tofId     = m_builder.content<2>().begin_list();
        auto& status    = m_builder.content<3>().begin_list();
        auto& path      = m_builder.content<4>().begin_list();
        auto& zrhit     = m_builder.content<5>().begin_list();
        auto& ph        = m_builder.content<6>().begin_list();
        auto& tof       = m_builder.content<7>().begin_list();
        auto& beta      = m_builder.content<8>().begin_list();
        auto& texp      = m_builder.content<9>().begin_list();
        auto& toffset   = m_builder.content<10>().begin_list();
        auto& sigma     = m_builder.content<11>().begin_list();
        auto& quality   = m_builder.content<12>().begin_list();
        auto& t0        = m_builder.content<13>().begin_list();
        auto& errt0     = m_builder.content<14>().begin_list();
        auto& errz      = m_builder.content<15>().begin_list();
        auto& phi       = m_builder.content<16>().begin_list();
        auto& errphi    = m_builder.content<17>().begin_list();
        auto& energy    = m_builder.content<18>().begin_list();
        auto& errenergy = m_builder.content<19>().begin_list();

        for ( auto tobj : *m_obj->getTofTrackCol() )
        {
            TRecTofTrack* obj = static_cast<TRecTofTrack*>( tobj );

            trackId.append( obj->tofTrackID() );
            inTrackId.append( obj->trackID() );
            tofId.append( obj->tofID() );
            status.append( obj->status() );
            path.append( obj->path() );
            zrhit.append( obj->zrhit() );
            ph.append( obj->ph() );
            tof.append( obj->tof() );
            beta.append( obj->beta() );

            auto& subtexp = texp.begin_list();
            for ( int i = 0; i < 5; i++ ) subtexp.append( obj->texp( i ) );
            texp.end_list();

            auto& subtoffset = toffset.begin_list();
            for ( int i = 0; i < 6; i++ ) subtoffset.append( obj->toffset( i ) );
            toffset.end_list();

            auto& subsigma = sigma.begin_list();
            for ( int i = 0; i < 6; i++ ) subsigma.append( obj->sigma( i ) );
            sigma.end_list();

            quality.append( obj->quality() );
            t0.append( obj->t0() );
            errt0.append( obj->errt0() );
            errz.append( obj->errz() );
            phi.append( obj->phi() );
            errphi.append( obj->errphi() );
            energy.append( obj->energy() );
            errenergy.append( obj->errenergy() );
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