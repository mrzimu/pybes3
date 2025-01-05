#pragma once

#include <awkward/LayoutBuilder.h>

#include "RootEventData/TEmcMc.h"
#include "RootEventData/TMcEvent.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using McEmcRecord = RecordBuilder<RaggedItemField<0, unsigned int>, // identify
                                  RaggedItemField<1, unsigned int>, // trackIndex
                                  RaggedItemField<2, int>,          // hitEmc
                                  RaggedItemField<3, int>,          // PDGCode
                                  RaggedItemField<4, double>,       // PDGCharge
                                  RaggedItemField<5, double>,       // time
                                  RaggedItemField<6, double>,       // x
                                  RaggedItemField<7, double>,       // y
                                  RaggedItemField<8, double>,       // z
                                  RaggedItemField<9, double>,       // px
                                  RaggedItemField<10, double>,      // py
                                  RaggedItemField<11, double>,      // pz
                                  RaggedItemField<12, double>,      // depositEnergy
                                  RaggedRaggedField<13, int>,       // hitMap id
                                  RaggedRaggedField<14, double>     // hitMap energy
                                  >;

const FieldMap field_map_mc_emc = { { 0, BesFieldNames::Mc::Emc::identify },
                                    { 1, BesFieldNames::Mc::Emc::trackIndex },
                                    { 2, BesFieldNames::Mc::Emc::hitEmc },
                                    { 3, BesFieldNames::Mc::Emc::PDGCode },
                                    { 4, BesFieldNames::Mc::Emc::PDGCharge },
                                    { 5, BesFieldNames::Mc::Emc::time },
                                    { 6, BesFieldNames::Mc::Emc::x },
                                    { 7, BesFieldNames::Mc::Emc::y },
                                    { 8, BesFieldNames::Mc::Emc::z },
                                    { 9, BesFieldNames::Mc::Emc::px },
                                    { 10, BesFieldNames::Mc::Emc::py },
                                    { 11, BesFieldNames::Mc::Emc::pz },
                                    { 12, BesFieldNames::Mc::Emc::depositEnergy },
                                    { 13, BesFieldNames::Mc::Emc::hitMapId },
                                    { 14, BesFieldNames::Mc::Emc::hitMapEnergy } };

class BesRFLeafMcEmc : public BesRootFieldLeaf<TMcEvent, McEmcRecord> {
  public:
    BesRFLeafMcEmc( TMcEvent* obj )
        : BesRootFieldLeaf<TMcEvent, McEmcRecord>( obj, BesFieldNames::Mc::Emc::rpath,
                                                   field_map_mc_emc ) {}

    void fill() {
        auto& identify      = m_builder.content<0>().begin_list();
        auto& trackIndex    = m_builder.content<1>().begin_list();
        auto& hitEmc        = m_builder.content<2>().begin_list();
        auto& PDGCode       = m_builder.content<3>().begin_list();
        auto& PDGCharge     = m_builder.content<4>().begin_list();
        auto& time          = m_builder.content<5>().begin_list();
        auto& x             = m_builder.content<6>().begin_list();
        auto& y             = m_builder.content<7>().begin_list();
        auto& z             = m_builder.content<8>().begin_list();
        auto& px            = m_builder.content<9>().begin_list();
        auto& py            = m_builder.content<10>().begin_list();
        auto& pz            = m_builder.content<11>().begin_list();
        auto& depositEnergy = m_builder.content<12>().begin_list();

        auto& hitMapId     = m_builder.content<13>().begin_list();
        auto& hitMapEnergy = m_builder.content<14>().begin_list();

        for ( auto tobj : ( *m_obj->getEmcMcHitCol() ) )
        {
            TEmcMc* emc = static_cast<TEmcMc*>( tobj );

            identify.append( emc->getHitEmc() );
            trackIndex.append( emc->getTrackIndex() );
            hitEmc.append( emc->getHitEmc() );
            PDGCode.append( emc->getPDGCode() );
            PDGCharge.append( emc->getPDGCharge() );
            time.append( emc->getTime() );
            x.append( emc->getPositionX() );
            y.append( emc->getPositionY() );
            z.append( emc->getPositionZ() );
            px.append( emc->getPx() );
            py.append( emc->getPy() );
            pz.append( emc->getPz() );
            depositEnergy.append( emc->getDepositEnergy() );

            auto& sub_hitMapId     = hitMapId.begin_list();
            auto& sub_hitMapEnergy = hitMapEnergy.begin_list();
            auto hitMap            = emc->getHitMap();
            for ( auto& [id, energy] : hitMap )
            {
                sub_hitMapId.append( id );
                sub_hitMapEnergy.append( energy );
            }
            hitMapId.end_list();
            hitMapEnergy.end_list();
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
        m_builder.content<10>().end_list();
        m_builder.content<11>().end_list();
        m_builder.content<12>().end_list();
        m_builder.content<13>().end_list();
        m_builder.content<14>().end_list();
    }
};