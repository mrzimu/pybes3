#pragma once

#include "RootEventData/TMcEvent.h"
#include "RootEventData/TTofMc.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using McTofRecord = RecordBuilder<RaggedItemField<0, unsigned int>, // identify
                                  RaggedItemField<1, unsigned int>, // trackIndex
                                  RaggedItemField<2, double>,       // x
                                  RaggedItemField<3, double>,       // y
                                  RaggedItemField<4, double>,       // z
                                  RaggedItemField<5, double>,       // px
                                  RaggedItemField<6, double>,       // py
                                  RaggedItemField<7, double>,       // pz
                                  RaggedItemField<8, double>,       // trackLength
                                  RaggedItemField<9, double>        // tof
                                  >;

const FieldMap field_map_mc_tof = {
    { 0, BesFieldNames::Mc::Tof::identify },    { 1, BesFieldNames::Mc::Tof::trackIndex },
    { 2, BesFieldNames::Mc::Tof::x },           { 3, BesFieldNames::Mc::Tof::y },
    { 4, BesFieldNames::Mc::Tof::z },           { 5, BesFieldNames::Mc::Tof::px },
    { 6, BesFieldNames::Mc::Tof::py },          { 7, BesFieldNames::Mc::Tof::pz },
    { 8, BesFieldNames::Mc::Tof::trackLength }, { 9, BesFieldNames::Mc::Tof::tof } };

class BesRFLeafMcTof : public BesRootFieldLeaf<TMcEvent, McTofRecord> {
  public:
    BesRFLeafMcTof( TMcEvent* obj )
        : BesRootFieldLeaf<TMcEvent, McTofRecord>( obj, BesFieldNames::Mc::Tof::rpath,
                                                   field_map_mc_tof ) {}

    void fill() {
        auto& identify    = m_builder.content<0>().begin_list();
        auto& trackIndex  = m_builder.content<1>().begin_list();
        auto& x           = m_builder.content<2>().begin_list();
        auto& y           = m_builder.content<3>().begin_list();
        auto& z           = m_builder.content<4>().begin_list();
        auto& px          = m_builder.content<5>().begin_list();
        auto& py          = m_builder.content<6>().begin_list();
        auto& pz          = m_builder.content<7>().begin_list();
        auto& trackLength = m_builder.content<8>().begin_list();
        auto& tof_arr     = m_builder.content<9>().begin_list();

        for ( auto tobj : ( *m_obj->getTofMcHitCol() ) )
        {
            TTofMc* tof = static_cast<TTofMc*>( tobj );

            identify.append( tof->getId() );
            trackIndex.append( tof->getTrackIndex() );
            x.append( tof->getPositionX() );
            y.append( tof->getPositionY() );
            z.append( tof->getPositionZ() );
            px.append( tof->getPx() );
            py.append( tof->getPy() );
            pz.append( tof->getPz() );
            trackLength.append( tof->getTrackLength() );
            tof_arr.append( tof->getFlightTime() );
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