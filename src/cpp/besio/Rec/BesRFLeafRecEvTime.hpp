#pragma once

#include "RootEventData/TRecEvTime.h"
#include "RootEventData/TRecTrackEvent.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using RecEvTimeRecord = RecordBuilder<RaggedItemField<0, int>,    // status
                                      RaggedItemField<1, double>, // estime
                                      RaggedItemField<2, double>  // quality
                                      >;

const FieldMap field_map_rec_recevtime = {
    { 0, BesFieldNames::Rec::EvTime::status },
    { 1, BesFieldNames::Rec::EvTime::estime },
    { 2, BesFieldNames::Rec::EvTime::quality },
};

class BesRFLeafRecEvTime : public BesRootFieldLeaf<TRecTrackEvent, RecEvTimeRecord> {
  public:
    BesRFLeafRecEvTime( TRecTrackEvent* obj )
        : BesRootFieldLeaf<TRecTrackEvent, RecEvTimeRecord>(
              obj, BesFieldNames::Rec::EvTime::rpath, field_map_rec_recevtime ) {}

    void fill() {
        auto& status  = m_builder.content<0>().begin_list();
        auto& estime  = m_builder.content<1>().begin_list();
        auto& quality = m_builder.content<2>().begin_list();

        for ( auto tobj : *m_obj->getEvTimeCol() )
        {
            TRecEvTime* obj = static_cast<TRecEvTime*>( tobj );

            status.append( obj->status() );
            estime.append( obj->estime() );
            quality.append( obj->quality() );
        }

        m_builder.content<0>().end_list();
        m_builder.content<1>().end_list();
        m_builder.content<2>().end_list();
    }
};
