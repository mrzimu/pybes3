#pragma once

#include <awkward/LayoutBuilder.h>

#include "RootEventData/TMcEvent.h"
#include "RootEventData/TMdcMc.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using McMdcRecord = RecordBuilder<RaggedItemField<0, unsigned int>, // identify
                                  RaggedItemField<1, unsigned int>, // trackIndex
                                  RaggedItemField<2, int>,          // currentTrkPID
                                  RaggedItemField<3, int>,          // isSecondary
                                  RaggedItemField<4, double>,       // x
                                  RaggedItemField<5, double>,       // y
                                  RaggedItemField<6, double>,       // z
                                  RaggedItemField<7, double>,       // px
                                  RaggedItemField<8, double>,       // py
                                  RaggedItemField<9, double>,       // pz
                                  RaggedItemField<10, double>,      // driftDistance
                                  RaggedItemField<11, double>,      // depositEnergy
                                  RaggedItemField<12, int>,         // posFlag
                                  RaggedItemField<13, double>,      // flightLength
                                  RaggedStringField<14>,            // creatorProcess
                                  RaggedItemField<15, int>          // digiIndex
                                  >;

const FieldMap field_map_mc_mdc = { { 0, BesFieldNames::Mc::Mdc::identify },
                                    { 1, BesFieldNames::Mc::Mdc::trackIndex },
                                    { 2, BesFieldNames::Mc::Mdc::curTrkPID },
                                    { 3, BesFieldNames::Mc::Mdc::isSecondary },
                                    { 4, BesFieldNames::Mc::Mdc::x },
                                    { 5, BesFieldNames::Mc::Mdc::y },
                                    { 6, BesFieldNames::Mc::Mdc::z },
                                    { 7, BesFieldNames::Mc::Mdc::px },
                                    { 8, BesFieldNames::Mc::Mdc::py },
                                    { 9, BesFieldNames::Mc::Mdc::pz },
                                    { 10, BesFieldNames::Mc::Mdc::driftDistance },
                                    { 11, BesFieldNames::Mc::Mdc::depositEnergy },
                                    { 12, BesFieldNames::Mc::Mdc::posFlag },
                                    { 13, BesFieldNames::Mc::Mdc::flightLength },
                                    { 14, BesFieldNames::Mc::Mdc::creatorProcess },
                                    { 15, BesFieldNames::Mc::Mdc::digiIndex } };

class BesRFLeafMcMdc : public BesRootFieldLeaf<TMcEvent, McMdcRecord> {
  public:
    BesRFLeafMcMdc( TMcEvent* obj )
        : BesRootFieldLeaf<TMcEvent, McMdcRecord>( obj, BesFieldNames::Mc::Mdc::rpath,
                                                   field_map_mc_mdc ) {}

    void fill() {
        auto& identify       = m_builder.content<0>().begin_list();
        auto& trackIndex     = m_builder.content<1>().begin_list();
        auto& curTrkPID      = m_builder.content<2>().begin_list();
        auto& isSecondary    = m_builder.content<3>().begin_list();
        auto& x              = m_builder.content<4>().begin_list();
        auto& y              = m_builder.content<5>().begin_list();
        auto& z              = m_builder.content<6>().begin_list();
        auto& px             = m_builder.content<7>().begin_list();
        auto& py             = m_builder.content<8>().begin_list();
        auto& pz             = m_builder.content<9>().begin_list();
        auto& driftDistance  = m_builder.content<10>().begin_list();
        auto& depositEnergy  = m_builder.content<11>().begin_list();
        auto& posFlag        = m_builder.content<12>().begin_list();
        auto& flightLength   = m_builder.content<13>().begin_list();
        auto& creatorProcess = m_builder.content<14>().begin_list();
        auto& digiIndex      = m_builder.content<15>().begin_list();

        for ( auto tobj : ( *m_obj->getMdcMcHitCol() ) )
        {
            TMdcMc* mdc = static_cast<TMdcMc*>( tobj );

            identify.append( mdc->getId() );
            trackIndex.append( mdc->getTrackIndex() );
            curTrkPID.append( mdc->getCurrentTrackPID() );
            isSecondary.append( mdc->getIsSecondary() );
            x.append( mdc->getPositionX() );
            y.append( mdc->getPositionY() );
            z.append( mdc->getPositionZ() );
            px.append( mdc->getMomentumX() );
            py.append( mdc->getMomentumY() );
            pz.append( mdc->getMomentumZ() );
            driftDistance.append( mdc->getDriftDistance() );
            depositEnergy.append( mdc->getDepositEnergy() );
            posFlag.append( mdc->getPositionFlag() );
            flightLength.append( mdc->getFlightLength() );
            creatorProcess.append( mdc->getCreatorProcess().Data() );
            digiIndex.append( mdc->getDigiIdx() );
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
        m_builder.content<15>().end_list();
    }
};