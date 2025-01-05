#pragma once

#include "RootEventData/TTrigData.h"
#include "RootEventData/TTrigEvent.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using TrigDataRecord = RecordBuilder<SimpleItemField<0, bool>,     // preScale
                                     SimpleArrayField<1, 48, int>, // trigConditions
                                     SimpleArrayField<2, 16, int>, // trigChannel
                                     SimpleItemField<3, int>,      // timeWindows
                                     SimpleItemField<4, int>       // timingType
                                     >;

const FieldMap field_map_trig_data = {
    { 0, BesFieldNames::Trig::preScale },    { 1, BesFieldNames::Trig::trigConditions },
    { 2, BesFieldNames::Trig::trigChannel }, { 3, BesFieldNames::Trig::timeWindows },
    { 4, BesFieldNames::Trig::timingType },
};

class BesRFLeafTrigData : public BesRootFieldLeaf<TTrigEvent, TrigDataRecord> {
  public:
    BesRFLeafTrigData( TTrigEvent* obj )
        : BesRootFieldLeaf<TTrigEvent, TrigDataRecord>( obj, BesFieldNames::Trig::rpath,
                                                        field_map_trig_data ) {}

    void fill() {
        const TTrigData* obj = m_obj->getTrigData();

        m_builder.content<0>().append( obj->getPreScale() );

        auto& trigConditions = m_builder.content<1>().begin_list();
        for ( int i = 0; i < 48; i++ ) { trigConditions.append( obj->getTrigCondition( i ) ); }
        m_builder.content<1>().end_list();

        auto& trigChannel = m_builder.content<2>().begin_list();
        for ( int i = 0; i < 16; i++ ) { trigChannel.append( obj->getTrigChannel( i ) ); }
        m_builder.content<2>().end_list();

        m_builder.content<3>().append( obj->getTimeWindow() );
        m_builder.content<4>().append( obj->getTimingType() );
    }
};
