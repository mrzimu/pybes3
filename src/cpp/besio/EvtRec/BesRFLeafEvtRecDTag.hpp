#pragma once

#include <awkward/LayoutBuilder.h>

#include "RootEventData/TEvtRecDTag.h"
#include "RootEventData/TEvtRecObject.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using EvtRecDTagRecord = RecordBuilder<RaggedItemField<0, int>,      // decayMode
                                       RaggedItemField<1, int>,      // type
                                       RaggedItemField<2, double>,   // beamE
                                       RaggedItemField<3, double>,   // mass
                                       RaggedItemField<4, double>,   // mBC
                                       RaggedItemField<5, double>,   // deltaE
                                       RaggedItemField<6, int>,      // charge
                                       RaggedItemField<7, int>,      // charm
                                       RaggedItemField<8, unsigned>, // nChild
                                       RaggedItemField<9, double>,   // px
                                       RaggedItemField<10, double>,  // py
                                       RaggedItemField<11, double>,  // pz
                                       RaggedItemField<12, double>,  // e
                                       RaggedRaggedField<13, int>,   // tracks
                                       RaggedRaggedField<14, int>,   // showers
                                       RaggedRaggedField<15, int>,   // otherTracks
                                       RaggedRaggedField<16, int>,   // otherShowers
                                       RaggedRaggedField<17, int>,   // pionId
                                       RaggedRaggedField<18, int>    // kaonId
                                       >;

const FieldMap field_map_recobj_dtag = { { 0, BesFieldNames::EvtRec::DTag::decayMode },
                                         { 1, BesFieldNames::EvtRec::DTag::type },
                                         { 2, BesFieldNames::EvtRec::DTag::beamE },
                                         { 3, BesFieldNames::EvtRec::DTag::mass },
                                         { 4, BesFieldNames::EvtRec::DTag::mBC },
                                         { 5, BesFieldNames::EvtRec::DTag::deltaE },
                                         { 6, BesFieldNames::EvtRec::DTag::charge },
                                         { 7, BesFieldNames::EvtRec::DTag::charm },
                                         { 8, BesFieldNames::EvtRec::DTag::nChild },
                                         { 9, BesFieldNames::EvtRec::DTag::px },
                                         { 10, BesFieldNames::EvtRec::DTag::py },
                                         { 11, BesFieldNames::EvtRec::DTag::pz },
                                         { 12, BesFieldNames::EvtRec::DTag::e },
                                         { 13, BesFieldNames::EvtRec::DTag::tracks },
                                         { 14, BesFieldNames::EvtRec::DTag::showers },
                                         { 15, BesFieldNames::EvtRec::DTag::otherTracks },
                                         { 16, BesFieldNames::EvtRec::DTag::otherShowers },
                                         { 17, BesFieldNames::EvtRec::DTag::pionId },
                                         { 18, BesFieldNames::EvtRec::DTag::kaonId } };

class BesRFLeafEvtRecDTag : public BesRootFieldLeaf<TEvtRecObject, EvtRecDTagRecord> {
  public:
    BesRFLeafEvtRecDTag( TEvtRecObject* obj )
        : BesRootFieldLeaf<TEvtRecObject, EvtRecDTagRecord>(
              obj, BesFieldNames::EvtRec::DTag::rpath, field_map_recobj_dtag ) {}

    void fill() {
        auto& decayMode    = m_builder.content<0>().begin_list();
        auto& type         = m_builder.content<1>().begin_list();
        auto& beamE        = m_builder.content<2>().begin_list();
        auto& mass         = m_builder.content<3>().begin_list();
        auto& mBC          = m_builder.content<4>().begin_list();
        auto& deltaE       = m_builder.content<5>().begin_list();
        auto& charge       = m_builder.content<6>().begin_list();
        auto& charm        = m_builder.content<7>().begin_list();
        auto& nChild       = m_builder.content<8>().begin_list();
        auto& px           = m_builder.content<9>().begin_list();
        auto& py           = m_builder.content<10>().begin_list();
        auto& pz           = m_builder.content<11>().begin_list();
        auto& e            = m_builder.content<12>().begin_list();
        auto& tracks       = m_builder.content<13>().begin_list();
        auto& showers      = m_builder.content<14>().begin_list();
        auto& otherTracks  = m_builder.content<15>().begin_list();
        auto& otherShowers = m_builder.content<16>().begin_list();
        auto& pionId       = m_builder.content<17>().begin_list();
        auto& kaonId       = m_builder.content<18>().begin_list();

        for ( auto* tobj : ( *m_obj->getEvtRecDTagCol() ) )
        {
            TEvtRecDTag* obj = static_cast<TEvtRecDTag*>( tobj );

            decayMode.append( obj->decayMode() );
            type.append( obj->type() );
            beamE.append( obj->beamE() );
            mass.append( obj->mass() );
            mBC.append( obj->mBC() );
            deltaE.append( obj->deltaE() );
            charge.append( obj->charge() );
            charm.append( obj->charm() );
            nChild.append( obj->numOfChildren() );
            px.append( obj->px() );
            py.append( obj->py() );
            pz.append( obj->pz() );
            e.append( obj->pe() );

            auto& subtracks = tracks.begin_list();
            for ( auto& track : obj->tracks() ) { subtracks.append( track ); }
            tracks.end_list();

            auto& subshowers = showers.begin_list();
            for ( auto& shower : obj->showers() ) { subshowers.append( shower ); }
            showers.end_list();

            auto& subothertracks = otherTracks.begin_list();
            for ( auto& track : obj->otherTracks() ) { subothertracks.append( track ); }
            otherTracks.end_list();

            auto& subothershowers = otherShowers.begin_list();
            for ( auto& shower : obj->otherShowers() ) { subothershowers.append( shower ); }
            otherShowers.end_list();

            auto& subpionid = pionId.begin_list();
            for ( auto& id : obj->pionId() ) { subpionid.append( id ); }
            pionId.end_list();

            auto& subkaonid = kaonId.begin_list();
            for ( auto& id : obj->kaonId() ) { subkaonid.append( id ); }
            kaonId.end_list();
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
    }
};