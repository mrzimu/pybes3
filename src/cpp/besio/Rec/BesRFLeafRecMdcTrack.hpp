#pragma once

#include <awkward/LayoutBuilder.h>

#include "RootEventData/TRecMdcTrack.h"
#include "RootEventData/TRecTrackEvent.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"
#include "RootEventData/TRecMdcTrack.h"

using RecMdcTrackRecord = RecordBuilder<RaggedItemField<0, int>,         // trackId
                                        RaggedArrayField<1, 5, double>,  // helix
                                        RaggedItemField<2, int>,         // stat
                                        RaggedItemField<3, double>,      // chi2
                                        RaggedItemField<4, int>,         // ndof
                                        RaggedArrayField<5, 15, double>, // err
                                        RaggedItemField<6, int>,         // nhits
                                        RaggedItemField<7, int>,         // nster
                                        RaggedItemField<8, int>,         // nlayer
                                        RaggedItemField<9, double>,      // vx0
                                        RaggedItemField<10, double>,     // vy0
                                        RaggedItemField<11, double>,     // vz0
                                        RaggedItemField<12, double>      // fiTerm
                                        >;

const FieldMap field_map_rec_mdctrack = {
    { 0, BesFieldNames::Rec::MdcTrack::trackId }, { 1, BesFieldNames::Rec::MdcTrack::helix },
    { 2, BesFieldNames::Rec::MdcTrack::stat },    { 3, BesFieldNames::Rec::MdcTrack::chi2 },
    { 4, BesFieldNames::Rec::MdcTrack::ndof },    { 5, BesFieldNames::Rec::MdcTrack::err },
    { 6, BesFieldNames::Rec::MdcTrack::nhits },   { 7, BesFieldNames::Rec::MdcTrack::nster },
    { 8, BesFieldNames::Rec::MdcTrack::nlayer },  { 9, BesFieldNames::Rec::MdcTrack::vx0 },
    { 10, BesFieldNames::Rec::MdcTrack::vy0 },    { 11, BesFieldNames::Rec::MdcTrack::vz0 },
    { 12, BesFieldNames::Rec::MdcTrack::fiTerm } };

class BesRFLeafRecMdcTrack : public BesRootFieldLeaf<TRecTrackEvent, RecMdcTrackRecord> {
  public:
    BesRFLeafRecMdcTrack( TRecTrackEvent* obj )
        : BesRootFieldLeaf<TRecTrackEvent, RecMdcTrackRecord>(
              obj, BesFieldNames::Rec::MdcTrack::rpath, field_map_rec_mdctrack ) {}

    void fill() {
        auto& tradkId = m_builder.content<0>().begin_list();
        auto& helix   = m_builder.content<1>().begin_list();
        auto& stat    = m_builder.content<2>().begin_list();
        auto& chi2    = m_builder.content<3>().begin_list();
        auto& ndof    = m_builder.content<4>().begin_list();
        auto& err     = m_builder.content<5>().begin_list();
        auto& nhits   = m_builder.content<6>().begin_list();
        auto& nster   = m_builder.content<7>().begin_list();
        auto& nlayer  = m_builder.content<8>().begin_list();
        auto& vx0     = m_builder.content<9>().begin_list();
        auto& vy0     = m_builder.content<10>().begin_list();
        auto& vz0     = m_builder.content<11>().begin_list();
        auto& fiTerm  = m_builder.content<12>().begin_list();

        for ( auto tobj : ( *m_obj->getRecMdcTrackCol() ) )
        {
            TRecMdcTrack* obj = static_cast<TRecMdcTrack*>( tobj );
            tradkId.append( obj->trackId() );

            auto& subhelix = helix.begin_list();
            for ( int i = 0; i < 5; i++ ) subhelix.append( obj->helix( i ) );
            helix.end_list();

            stat.append( obj->stat() );
            chi2.append( obj->chi2() );
            ndof.append( obj->ndof() );

            auto& suberr = err.begin_list();
            for ( int i = 0; i < 15; i++ ) suberr.append( obj->err( i ) );
            err.end_list();

            nhits.append( obj->nhits() );
            nster.append( obj->nster() );
            nlayer.append( obj->nlayer() );
            vx0.append( obj->vx0() );
            vy0.append( obj->vy0() );
            vz0.append( obj->vz0() );
            fiTerm.append( obj->fiTerm() );
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
    }
};