#pragma once

#include "RootEventData/THltEvent.h"
#include "RootEventData/THltRaw.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using HltRawRecord = RecordBuilder<RaggedItemField<0, uint>, // id
                                   RaggedItemField<1, uint>, // adc
                                   RaggedItemField<2, uint>, // tdc
                                   RaggedItemField<3, int>   // trackIndex
                                   >;

const FieldMap field_map_hlt_raw = {
    { 0, BesFieldNames::Hlt::Raw::id },
    { 1, BesFieldNames::Hlt::Raw::adc },
    { 2, BesFieldNames::Hlt::Raw::tdc },
    { 3, BesFieldNames::Hlt::Raw::trackIndex },
};
class BesRFLeafHltRaw : public BesRootFieldLeaf<THltEvent, HltRawRecord> {
  public:
    BesRFLeafHltRaw( THltEvent* obj )
        : BesRootFieldLeaf<THltEvent, HltRawRecord>( obj, BesFieldNames::Hlt::Raw::rpath,
                                                     field_map_hlt_raw ) {}

    void fill() {
        auto& id         = m_builder.content<0>().begin_list();
        auto& adc        = m_builder.content<1>().begin_list();
        auto& tdc        = m_builder.content<2>().begin_list();
        auto& trackIndex = m_builder.content<3>().begin_list();

        for ( auto tobj : *m_obj->getHltRawCol() )
        {
            auto obj = static_cast<THltRaw*>( tobj );

            id.append( obj->getIntId() );
            adc.append( obj->getChargeChannel() );
            tdc.append( obj->getTimeChannel() );
            trackIndex.append( obj->getTrackIndex() );
        }

        m_builder.content<0>().end_list();
        m_builder.content<1>().end_list();
        m_builder.content<2>().end_list();
        m_builder.content<3>().end_list();
    }
};
