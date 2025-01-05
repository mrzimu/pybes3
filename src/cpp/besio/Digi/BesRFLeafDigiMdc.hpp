#pragma once

#include <awkward/LayoutBuilder.h>

#include "RootEventData/TDigiEvent.h"
#include "RootEventData/TMdcDigi.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using DigiMdcRecord = RecordBuilder<RaggedItemField<0, unsigned int>, // id
                                    RaggedItemField<1, unsigned int>, // adc
                                    RaggedItemField<2, unsigned int>, // tdc
                                    RaggedItemField<3, int>,          // trackIndex
                                    RaggedItemField<4, unsigned int>  // overflow
                                    >;

const FieldMap field_map_digi_mdc = { { 0, BesFieldNames::Digi::Mdc::id },
                                      { 1, BesFieldNames::Digi::Mdc::adc },
                                      { 2, BesFieldNames::Digi::Mdc::tdc },
                                      { 3, BesFieldNames::Digi::Mdc::trackIndex },
                                      { 4, BesFieldNames::Digi::Mdc::overflow } };

class BesRFLeafDigiMdc : public BesRootFieldLeaf<TDigiEvent, DigiMdcRecord> {
  public:
    BesRFLeafDigiMdc( TDigiEvent* obj )
        : BesRootFieldLeaf<TDigiEvent, DigiMdcRecord>( obj, BesFieldNames::Digi::Mdc::rpath,
                                                       field_map_digi_mdc ) {}

    void fill() {
        auto& id         = m_builder.content<0>().begin_list();
        auto& adc        = m_builder.content<1>().begin_list();
        auto& tdc        = m_builder.content<2>().begin_list();
        auto& trackIndex = m_builder.content<3>().begin_list();
        auto& overflow   = m_builder.content<4>().begin_list();

        for ( auto tobj : ( *m_obj->getMdcDigiCol() ) )
        {
            TMdcDigi* digi = static_cast<TMdcDigi*>( tobj );

            id.append( digi->getIntId() );
            adc.append( digi->getChargeChannel() );
            tdc.append( digi->getTimeChannel() );
            trackIndex.append( digi->getTrackIndex() );
            overflow.append( digi->getOverflow() );
        }

        m_builder.content<0>().end_list();
        m_builder.content<1>().end_list();
        m_builder.content<2>().end_list();
        m_builder.content<3>().end_list();
        m_builder.content<4>().end_list();
    }
};