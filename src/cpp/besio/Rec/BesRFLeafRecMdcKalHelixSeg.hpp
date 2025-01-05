#pragma once

#include "RootEventData/TRecMdcKalHelixSeg.h"
#include "RootEventData/TRecTrackEvent.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using RecMdcKalHelixSegRecord = RecordBuilder<RaggedItemField<0, int>,         // trackId
                                              RaggedItemField<1, int>,         // leftOrRight
                                              RaggedItemField<2, unsigned>,    // mdcId
                                              RaggedItemField<3, double>,      // tdc
                                              RaggedItemField<4, double>,      // adc
                                              RaggedItemField<5, double>,      // zhit
                                              RaggedItemField<6, double>,      // tof
                                              RaggedItemField<7, double>,      // docaInCell
                                              RaggedItemField<8, double>,      // docaExCell
                                              RaggedItemField<9, double>,      // driftDistance
                                              RaggedItemField<10, double>,     // entranceAngle
                                              RaggedItemField<11, double>,     // driftTime
                                              RaggedArrayField<12, 5, double>, // helixInCell
                                              RaggedArrayField<13, 5, double>  // helixExCell
                                              >;

const FieldMap field_map_rec_mdckalhelixseg = {
    { 0, BesFieldNames::Rec::MdcKalHelixSeg::trackId },
    { 1, BesFieldNames::Rec::MdcKalHelixSeg::leftOrRight },
    { 2, BesFieldNames::Rec::MdcKalHelixSeg::mdcId },
    { 3, BesFieldNames::Rec::MdcKalHelixSeg::tdc },
    { 4, BesFieldNames::Rec::MdcKalHelixSeg::adc },
    { 5, BesFieldNames::Rec::MdcKalHelixSeg::zhit },
    { 6, BesFieldNames::Rec::MdcKalHelixSeg::tof },
    { 7, BesFieldNames::Rec::MdcKalHelixSeg::docaInCell },
    { 8, BesFieldNames::Rec::MdcKalHelixSeg::docaExCell },
    { 9, BesFieldNames::Rec::MdcKalHelixSeg::driftDistance },
    { 10, BesFieldNames::Rec::MdcKalHelixSeg::entranceAngle },
    { 11, BesFieldNames::Rec::MdcKalHelixSeg::driftTime },
    { 12, BesFieldNames::Rec::MdcKalHelixSeg::helixInCell },
    { 13, BesFieldNames::Rec::MdcKalHelixSeg::helixExCell },
};

class BesRFLeafRecMdcKalHelixSeg
    : public BesRootFieldLeaf<TRecTrackEvent, RecMdcKalHelixSegRecord> {
  public:
    BesRFLeafRecMdcKalHelixSeg( TRecTrackEvent* obj )
        : BesRootFieldLeaf<TRecTrackEvent, RecMdcKalHelixSegRecord>(
              obj, BesFieldNames::Rec::MdcKalHelixSeg::rpath, field_map_rec_mdckalhelixseg ) {}

    void fill() {
        auto& trackId       = m_builder.content<0>().begin_list();
        auto& leftOrRight   = m_builder.content<1>().begin_list();
        auto& mdcId         = m_builder.content<2>().begin_list();
        auto& tdc           = m_builder.content<3>().begin_list();
        auto& adc           = m_builder.content<4>().begin_list();
        auto& zhit          = m_builder.content<5>().begin_list();
        auto& tof           = m_builder.content<6>().begin_list();
        auto& docaInCell    = m_builder.content<7>().begin_list();
        auto& docaExCell    = m_builder.content<8>().begin_list();
        auto& driftDistance = m_builder.content<9>().begin_list();
        auto& entranceAngle = m_builder.content<10>().begin_list();
        auto& driftTime     = m_builder.content<11>().begin_list();
        auto& helixInCell   = m_builder.content<12>().begin_list();
        auto& helixExCell   = m_builder.content<13>().begin_list();

        for ( auto tobj : *m_obj->getRecMdcKalHelixSegCol() )
        {
            TRecMdcKalHelixSeg* obj = static_cast<TRecMdcKalHelixSeg*>( tobj );

            trackId.append( obj->getTrackId() );
            leftOrRight.append( obj->getFlagLR() );
            mdcId.append( obj->getMdcId() );
            tdc.append( obj->getTdc() );
            adc.append( obj->getAdc() );
            zhit.append( obj->getZhit() );
            tof.append( obj->getTof() );
            docaInCell.append( obj->getDocaIncl() );
            docaExCell.append( obj->getDocaIncl() );
            driftDistance.append( obj->getDD() );
            entranceAngle.append( obj->getEntra() );
            driftTime.append( obj->getDT() );

            auto& subhelixInCell = helixInCell.begin_list();
            auto& subhelixExCell = helixExCell.begin_list();
            for ( int i = 0; i < 5; i++ )
            {
                subhelixInCell.append( obj->getHelixIncl( i ) );
                subhelixExCell.append( obj->getHelixExcl( i ) );
            }
            helixInCell.end_list();
            helixExCell.end_list();
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
    }
};
