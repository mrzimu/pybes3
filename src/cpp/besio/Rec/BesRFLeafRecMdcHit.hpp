#pragma once

#include "RootEventData/TRecMdcHit.h"
#include "RootEventData/TRecTrackEvent.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using RecMdcHitRecord = RecordBuilder<RaggedItemField<0, bool>,      // isGrouped
                                      RaggedItemField<1, int>,       // id
                                      RaggedItemField<2, int>,       // trkId
                                      RaggedItemField<3, double>,    // driftDistLeft
                                      RaggedItemField<4, double>,    // driftDistRight
                                      RaggedItemField<5, double>,    // errDriftDistLeft
                                      RaggedItemField<6, double>,    // errDriftDistRight
                                      RaggedItemField<7, double>,    // chi2Contrib
                                      RaggedItemField<8, int>,       // leftOrRight
                                      RaggedItemField<9, int>,       // stat
                                      RaggedItemField<10, unsigned>, // mdcId
                                      RaggedItemField<11, double>,   // tdc
                                      RaggedItemField<12, double>,   // adc
                                      RaggedItemField<13, double>,   // driftTime
                                      RaggedItemField<14, double>,   // doca
                                      RaggedItemField<15, double>,   // entranceAngle
                                      RaggedItemField<16, double>,   // zHit
                                      RaggedItemField<17, double>    // flightLength
                                      >;

const FieldMap field_map_rec_mdchit = { { 0, BesFieldNames::Rec::MdcHit::isGrouped },
                                        { 1, BesFieldNames::Rec::MdcHit::id },
                                        { 2, BesFieldNames::Rec::MdcHit::trkId },
                                        { 3, BesFieldNames::Rec::MdcHit::driftDistLeft },
                                        { 4, BesFieldNames::Rec::MdcHit::driftDistRight },
                                        { 5, BesFieldNames::Rec::MdcHit::errDriftDistLeft },
                                        { 6, BesFieldNames::Rec::MdcHit::errDriftDistRight },
                                        { 7, BesFieldNames::Rec::MdcHit::chi2Contrib },
                                        { 8, BesFieldNames::Rec::MdcHit::leftOrRight },
                                        { 9, BesFieldNames::Rec::MdcHit::stat },
                                        { 10, BesFieldNames::Rec::MdcHit::mdcId },
                                        { 11, BesFieldNames::Rec::MdcHit::tdc },
                                        { 12, BesFieldNames::Rec::MdcHit::adc },
                                        { 13, BesFieldNames::Rec::MdcHit::driftTime },
                                        { 14, BesFieldNames::Rec::MdcHit::doca },
                                        { 15, BesFieldNames::Rec::MdcHit::entranceAngle },
                                        { 16, BesFieldNames::Rec::MdcHit::zHit },
                                        { 17, BesFieldNames::Rec::MdcHit::flightLength } };

class BesRFLeafRecMdcHit : public BesRootFieldLeaf<TRecTrackEvent, RecMdcHitRecord> {
  public:
    BesRFLeafRecMdcHit( TRecTrackEvent* obj )
        : BesRootFieldLeaf<TRecTrackEvent, RecMdcHitRecord>(
              obj, BesFieldNames::Rec::MdcHit::rpath, field_map_rec_mdchit ) {}

    void fill() {
        auto& isGrouped         = m_builder.content<0>().begin_list();
        auto& id                = m_builder.content<1>().begin_list();
        auto& trkId             = m_builder.content<2>().begin_list();
        auto& driftDistLeft     = m_builder.content<3>().begin_list();
        auto& driftDistRight    = m_builder.content<4>().begin_list();
        auto& errDriftDistLeft  = m_builder.content<5>().begin_list();
        auto& errDriftDistRight = m_builder.content<6>().begin_list();
        auto& chi2Contrib       = m_builder.content<7>().begin_list();
        auto& leftOrRight       = m_builder.content<8>().begin_list();
        auto& stat              = m_builder.content<9>().begin_list();
        auto& mdcId             = m_builder.content<10>().begin_list();
        auto& tdc               = m_builder.content<11>().begin_list();
        auto& adc               = m_builder.content<12>().begin_list();
        auto& driftTime         = m_builder.content<13>().begin_list();
        auto& doca              = m_builder.content<14>().begin_list();
        auto& entranceAngle     = m_builder.content<15>().begin_list();
        auto& zHit              = m_builder.content<16>().begin_list();
        auto& flightLength      = m_builder.content<17>().begin_list();

        for ( auto tobj : *m_obj->getRecMdcHitCol() )
        {
            TRecMdcHit* obj = static_cast<TRecMdcHit*>( tobj );

            isGrouped.append( obj->isGrouped() );
            id.append( obj->getId() );
            trkId.append( obj->getTrkId() );
            driftDistLeft.append( obj->getDriftDistLeft() );
            driftDistRight.append( obj->getDriftDistRight() );
            errDriftDistLeft.append( obj->getErrDriftDistLeft() );
            errDriftDistRight.append( obj->getErrDriftDistRight() );
            chi2Contrib.append( obj->getChisqAdd() );
            leftOrRight.append( obj->getFlagLR() );
            stat.append( obj->getStat() );
            mdcId.append( obj->getMdcId() );
            tdc.append( obj->getTdc() );
            adc.append( obj->getAdc() );
            driftTime.append( obj->getDriftT() );
            doca.append( obj->getDoca() );
            entranceAngle.append( obj->getEntra() );
            zHit.append( obj->getZhit() );
            flightLength.append( obj->getFltLen() );
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
        m_builder.content<16>().end_list();
        m_builder.content<17>().end_list();
    }
};