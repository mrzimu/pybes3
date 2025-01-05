#pragma once

#include "RootEventData/TRecTrackEvent.h"
#include "RootEventData/TRecZddChannel.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using RecZddRecord = RecordBuilder<RaggedItemField<0, int>,    // channelId
                                   RaggedItemField<1, int>,    // scanCode
                                   RaggedItemField<2, int>,    // baseLine
                                   RaggedItemField<3, int>,    // phase
                                   RaggedRaggedField<4, int>,  // fragTime
                                   RaggedRaggedField<5, float> // fragEnergy
                                   >;

const FieldMap field_map_rec_reczdd = {
    { 0, BesFieldNames::Rec::Zdd::channelId }, { 1, BesFieldNames::Rec::Zdd::scanCode },
    { 2, BesFieldNames::Rec::Zdd::baseLine },  { 3, BesFieldNames::Rec::Zdd::phase },
    { 4, BesFieldNames::Rec::Zdd::fragTime },  { 5, BesFieldNames::Rec::Zdd::fragEnergy },
};
class BesRFLeafRecZdd : public BesRootFieldLeaf<TRecTrackEvent, RecZddRecord> {
  public:
    BesRFLeafRecZdd( TRecTrackEvent* obj )
        : BesRootFieldLeaf<TRecTrackEvent, RecZddRecord>( obj, BesFieldNames::Rec::Zdd::rpath,
                                                          field_map_rec_reczdd ) {}

    void fill() {
        auto& channelId  = m_builder.content<0>().begin_list();
        auto& scanCode   = m_builder.content<1>().begin_list();
        auto& baseLine   = m_builder.content<2>().begin_list();
        auto& phase      = m_builder.content<3>().begin_list();
        auto& fragTime   = m_builder.content<4>().begin_list();
        auto& fragEnergy = m_builder.content<5>().begin_list();

        for ( auto tobj : *m_obj->getRecZddChannelCol() )
        {
            TRecZddChannel* obj = static_cast<TRecZddChannel*>( tobj );

            channelId.append( obj->channelId() );
            scanCode.append( obj->scanCode() );
            baseLine.append( obj->baseLine() );
            phase.append( obj->phase() );

            auto& subfragTime   = fragTime.begin_list();
            auto& subfragEnergy = fragEnergy.begin_list();
            for ( auto frag : obj->fragments() )
            {
                subfragTime.append( frag.first );
                subfragEnergy.append( frag.second );
            }
            fragTime.end_list();
            fragEnergy.end_list();
        }

        m_builder.content<0>().end_list();
        m_builder.content<1>().end_list();
        m_builder.content<2>().end_list();
        m_builder.content<3>().end_list();
        m_builder.content<4>().end_list();
        m_builder.content<5>().end_list();
    }
};
