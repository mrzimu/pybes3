#pragma once

#include <awkward/LayoutBuilder.h>

#include "RootEventData/TEvtRecObject.h"
#include "RootEventData/TEvtRecTrack.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using EvtRecTrackRecord = RecordBuilder<RaggedItemField<0, int>,  // trackId
                                        RaggedItemField<1, int>,  // partId
                                        RaggedItemField<2, int>,  // quality
                                        RaggedItemField<3, int>,  // mdcTrackId
                                        RaggedItemField<4, int>,  // mdcKalTrackId
                                        RaggedItemField<5, int>,  // mdcDedxId
                                        RaggedItemField<6, int>,  // extTrackId
                                        RaggedItemField<7, int>,  // emcShowerId
                                        RaggedItemField<8, int>,  // mucTrackId
                                        RaggedRaggedField<9, int> // tofTrackIds
                                        >;

const FieldMap field_map_recobj_trk = { { 0, BesFieldNames::EvtRec::Trk::trackId },
                                        { 1, BesFieldNames::EvtRec::Trk::partId },
                                        { 2, BesFieldNames::EvtRec::Trk::quality },
                                        { 3, BesFieldNames::EvtRec::Trk::mdcTrackId },
                                        { 4, BesFieldNames::EvtRec::Trk::mdcKalTrackId },
                                        { 5, BesFieldNames::EvtRec::Trk::mdcDedxId },
                                        { 6, BesFieldNames::EvtRec::Trk::extTrackId },
                                        { 7, BesFieldNames::EvtRec::Trk::emcShowerId },
                                        { 8, BesFieldNames::EvtRec::Trk::mucTrackId },
                                        { 9, BesFieldNames::EvtRec::Trk::tofTrackIds } };

class BesRFLeafEvtRecTracks : public BesRootFieldLeaf<TEvtRecObject, EvtRecTrackRecord> {
  public:
    BesRFLeafEvtRecTracks( TEvtRecObject* obj )
        : BesRootFieldLeaf<TEvtRecObject, EvtRecTrackRecord>(
              obj, BesFieldNames::EvtRec::Trk::rpath, field_map_recobj_trk ) {}

    void fill() {
        auto& trackId       = m_builder.content<0>().begin_list();
        auto& partId        = m_builder.content<1>().begin_list();
        auto& quality       = m_builder.content<2>().begin_list();
        auto& mdcTrackId    = m_builder.content<3>().begin_list();
        auto& mdcKalTrackId = m_builder.content<4>().begin_list();
        auto& mdcDedxId     = m_builder.content<5>().begin_list();
        auto& extTrackId    = m_builder.content<6>().begin_list();
        auto& emcShowerId   = m_builder.content<7>().begin_list();
        auto& mucTrackId    = m_builder.content<8>().begin_list();
        auto& tofTrackIds   = m_builder.content<9>().begin_list();

        for ( auto* tobj : ( *m_obj->getEvtRecTrackCol() ) )
        {
            TEvtRecTrack* obj = static_cast<TEvtRecTrack*>( tobj );

            trackId.append( obj->trackId() );
            partId.append( obj->partId() );
            quality.append( obj->quality() );
            mdcTrackId.append( obj->mdcTrackId() );
            mdcKalTrackId.append( obj->mdcKalTrackId() );
            mdcDedxId.append( obj->mdcDedxId() );
            extTrackId.append( obj->extTrackId() );
            emcShowerId.append( obj->emcShowerId() );
            mucTrackId.append( obj->mucTrackId() );

            auto& subtof = tofTrackIds.begin_list();
            for ( auto& tof : obj->tofTrackIds() ) { subtof.append( tof ); }
            tofTrackIds.end_list();
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
    }
};