#pragma once

#include "RootEventData/TMcEvent.h"
#include "RootEventData/TMucMc.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using McMucRecord = RecordBuilder<RaggedItemField<0, unsigned int>, // identify
                                  RaggedItemField<1, unsigned int>, // trackIndex
                                  RaggedItemField<2, double>,       // x
                                  RaggedItemField<3, double>,       // y
                                  RaggedItemField<4, double>,       // z
                                  RaggedItemField<5, double>,       // px
                                  RaggedItemField<6, double>,       // py
                                  RaggedItemField<7, double>        // pz
                                  >;

const FieldMap field_map_mc_muc = {
    { 0, BesFieldNames::Mc::Muc::identify }, { 1, BesFieldNames::Mc::Muc::trackIndex },
    { 2, BesFieldNames::Mc::Muc::x },        { 3, BesFieldNames::Mc::Muc::y },
    { 4, BesFieldNames::Mc::Muc::z },        { 5, BesFieldNames::Mc::Muc::px },
    { 6, BesFieldNames::Mc::Muc::py },       { 7, BesFieldNames::Mc::Muc::pz } };

class BesRFLeafMcMuc : public BesRootFieldLeaf<TMcEvent, McMucRecord> {
  public:
    BesRFLeafMcMuc( TMcEvent* obj )
        : BesRootFieldLeaf<TMcEvent, McMucRecord>( obj, BesFieldNames::Mc::Muc::rpath,
                                                   field_map_mc_muc ) {}

    void fill() {
        auto& identify   = m_builder.content<0>().begin_list();
        auto& trackIndex = m_builder.content<1>().begin_list();
        auto& x          = m_builder.content<2>().begin_list();
        auto& y          = m_builder.content<3>().begin_list();
        auto& z          = m_builder.content<4>().begin_list();
        auto& px         = m_builder.content<5>().begin_list();
        auto& py         = m_builder.content<6>().begin_list();
        auto& pz         = m_builder.content<7>().begin_list();

        for ( auto tobj : ( *m_obj->getMucMcHitCol() ) )
        {
            TMucMc* muc = static_cast<TMucMc*>( tobj );

            identify.append( muc->getId() );
            trackIndex.append( muc->getTrackIndex() );
            x.append( muc->getPositionX() );
            y.append( muc->getPositionY() );
            z.append( muc->getPositionZ() );
            px.append( muc->getPositionX() );
            py.append( muc->getPy() );
            pz.append( muc->getPz() );
            // No depositEnergy in TMucMc
        }

        m_builder.content<0>().end_list();
        m_builder.content<1>().end_list();
        m_builder.content<2>().end_list();
        m_builder.content<3>().end_list();
        m_builder.content<4>().end_list();
        m_builder.content<5>().end_list();
        m_builder.content<6>().end_list();
        m_builder.content<7>().end_list();
    }
};