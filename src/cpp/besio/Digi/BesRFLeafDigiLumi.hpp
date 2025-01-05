#pragma once

#include <awkward/LayoutBuilder.h>

#include "RootEventData/TDigiEvent.h"
#include "RootEventData/TLumiDigi.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using DigiLumiRecord = RecordBuilder<RaggedItemField<0, unsigned int>, // id
                                     RaggedItemField<1, unsigned int>, // adc
                                     RaggedItemField<2, unsigned int>, // tdc
                                     RaggedItemField<3, int>,          // trackIndex
                                     RaggedItemField<4, unsigned int>  // overflow
                                     >;

const FieldMap field_map_digi_lumi = { { 0, BesFieldNames::Digi::Lumi::id },
                                       { 1, BesFieldNames::Digi::Lumi::adc },
                                       { 2, BesFieldNames::Digi::Lumi::tdc },
                                       { 3, BesFieldNames::Digi::Lumi::trackIndex },
                                       { 4, BesFieldNames::Digi::Lumi::overflow } };

class BesRFLeafDigiLumi : public BesRootFieldLeaf<TDigiEvent, DigiLumiRecord> {
  public:
    BesRFLeafDigiLumi( TDigiEvent* obj )
        : BesRootFieldLeaf<TDigiEvent, DigiLumiRecord>( obj, BesFieldNames::Digi::Lumi::rpath,
                                                        field_map_digi_lumi ) {}

    void fill() {
        auto& id         = m_builder.content<0>().begin_list();
        auto& adc        = m_builder.content<1>().begin_list();
        auto& tdc        = m_builder.content<2>().begin_list();
        auto& trackIndex = m_builder.content<3>().begin_list();
        auto& overflow   = m_builder.content<4>().begin_list();

        for ( auto tobj : ( *m_obj->getLumiDigiCol() ) )
        {
            TLumiDigi* digi = static_cast<TLumiDigi*>( tobj );

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