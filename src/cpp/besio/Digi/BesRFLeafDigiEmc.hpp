#pragma once

#include <awkward/LayoutBuilder.h>

#include "RootEventData/TDigiEvent.h"
#include "RootEventData/TEmcDigi.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using DigiEmcRecord = RecordBuilder<RaggedItemField<0, unsigned int>, // id
                                    RaggedItemField<1, unsigned int>, // adc
                                    RaggedItemField<2, unsigned int>, // tdc
                                    RaggedItemField<3, int>,          // trackIndex
                                    RaggedItemField<4, unsigned int>  // measure
                                    >;

const FieldMap field_map_digi_emc = { { 0, BesFieldNames::Digi::Emc::id },
                                      { 1, BesFieldNames::Digi::Emc::adc },
                                      { 2, BesFieldNames::Digi::Emc::tdc },
                                      { 3, BesFieldNames::Digi::Emc::trackIndex },
                                      { 4, BesFieldNames::Digi::Emc::measure } };

class BesRFLeafDigiEmc : public BesRootFieldLeaf<TDigiEvent, DigiEmcRecord> {
  public:
    BesRFLeafDigiEmc( TDigiEvent* obj )
        : BesRootFieldLeaf<TDigiEvent, DigiEmcRecord>( obj, BesFieldNames::Digi::Emc::rpath,
                                                       field_map_digi_emc ) {}

    void fill() {
        auto& id         = m_builder.content<0>().begin_list();
        auto& adc        = m_builder.content<1>().begin_list();
        auto& tdc        = m_builder.content<2>().begin_list();
        auto& trackIndex = m_builder.content<3>().begin_list();
        auto& measure    = m_builder.content<4>().begin_list();

        for ( auto tobj : ( *m_obj->getEmcDigiCol() ) )
        {
            TEmcDigi* digi = static_cast<TEmcDigi*>( tobj );

            id.append( digi->getIntId() );
            adc.append( digi->getChargeChannel() );
            tdc.append( digi->getTimeChannel() );
            trackIndex.append( digi->getTrackIndex() );
            measure.append( digi->getMeasure() );
        }

        m_builder.content<0>().end_list();
        m_builder.content<1>().end_list();
        m_builder.content<2>().end_list();
        m_builder.content<3>().end_list();
        m_builder.content<4>().end_list();
    }
};