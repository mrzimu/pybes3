#pragma once

#include <awkward/LayoutBuilder.h>

#include "RootEventData/TDigiEvent.h"
#include "RootEventData/TMucDigi.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using DigiMucRecord = RecordBuilder<RaggedItemField<0, unsigned int>, // id
                                    RaggedItemField<1, unsigned int>, // adc
                                    RaggedItemField<2, unsigned int>, // tdc
                                    RaggedItemField<3, int>           // trackIndex
                                    >;

const FieldMap field_map_digi_muc = { { 0, BesFieldNames::Digi::Muc::id },
                                      { 1, BesFieldNames::Digi::Muc::adc },
                                      { 2, BesFieldNames::Digi::Muc::tdc },
                                      { 3, BesFieldNames::Digi::Muc::trackIndex } };

class BesRFLeafDigiMuc : public BesRootFieldLeaf<TDigiEvent, DigiMucRecord> {
  public:
    BesRFLeafDigiMuc( TDigiEvent* obj )
        : BesRootFieldLeaf<TDigiEvent, DigiMucRecord>( obj, BesFieldNames::Digi::Muc::rpath,
                                                       field_map_digi_muc ) {}

    void fill() {
        auto& id         = m_builder.content<0>().begin_list();
        auto& adc        = m_builder.content<1>().begin_list();
        auto& tdc        = m_builder.content<2>().begin_list();
        auto& trackIndex = m_builder.content<3>().begin_list();

        for ( auto tobj : ( *m_obj->getMucDigiCol() ) )
        {
            TMucDigi* digi = static_cast<TMucDigi*>( tobj );

            id.append( digi->getIntId() );
            adc.append( digi->getChargeChannel() );
            tdc.append( digi->getTimeChannel() );
            trackIndex.append( digi->getTrackIndex() );
        }

        m_builder.content<0>().end_list();
        m_builder.content<1>().end_list();
        m_builder.content<2>().end_list();
        m_builder.content<3>().end_list();
    }
};