#pragma once

#include "RootEventData/TRecMdcDedxHit.h"
#include "RootEventData/TRecTrackEvent.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using RecMdcDedxHitRecord = RecordBuilder<RaggedItemField<0, bool>,     // isGrouped
                                          RaggedItemField<1, int>,      // trkId
                                          RaggedItemField<2, int>,      // mdcHitId
                                          RaggedItemField<3, int>,      // mdcKalHelixSegId
                                          RaggedItemField<4, int>,      // leftOrRight
                                          RaggedItemField<5, unsigned>, // mdcId
                                          RaggedItemField<6, double>,   // path
                                          RaggedItemField<7, double>    // dedx
                                          >;

const FieldMap field_map_rec_mdcdedxhit = {
    { 0, BesFieldNames::Rec::MdcDedxHit::isGrouped },
    { 1, BesFieldNames::Rec::MdcDedxHit::trkId },
    { 2, BesFieldNames::Rec::MdcDedxHit::mdcHitId },
    { 3, BesFieldNames::Rec::MdcDedxHit::mdcKalHelixSegId },
    { 4, BesFieldNames::Rec::MdcDedxHit::leftOrRight },
    { 5, BesFieldNames::Rec::MdcDedxHit::mdcId },
    { 6, BesFieldNames::Rec::MdcDedxHit::path },
    { 7, BesFieldNames::Rec::MdcDedxHit::dedx },
};

class BesRFLeafRecMdcDedxHit : public BesRootFieldLeaf<TRecTrackEvent, RecMdcDedxHitRecord> {
  public:
    BesRFLeafRecMdcDedxHit( TRecTrackEvent* obj )
        : BesRootFieldLeaf<TRecTrackEvent, RecMdcDedxHitRecord>(
              obj, BesFieldNames::Rec::MdcDedxHit::rpath, field_map_rec_mdcdedxhit ) {}

    void fill() {
        auto& isGrouped        = m_builder.content<0>().begin_list();
        auto& trkId            = m_builder.content<1>().begin_list();
        auto& mdcHitId         = m_builder.content<2>().begin_list();
        auto& mdcKalHelixSegId = m_builder.content<3>().begin_list();
        auto& leftOrRight      = m_builder.content<4>().begin_list();
        auto& mdcId            = m_builder.content<5>().begin_list();
        auto& path             = m_builder.content<6>().begin_list();
        auto& dedx             = m_builder.content<7>().begin_list();

        for ( auto tobj : *m_obj->getRecMdcDedxHitCol() )
        {
            TRecMdcDedxHit* obj = static_cast<TRecMdcDedxHit*>( tobj );

            isGrouped.append( obj->isGrouped() );
            trkId.append( obj->trkId() );
            mdcHitId.append( obj->mdcHitId() );
            mdcKalHelixSegId.append( obj->mdcKalHelixSegId() );
            leftOrRight.append( obj->flagLR() );
            mdcId.append( obj->mdcId() );
            path.append( obj->pathLength() );
            dedx.append( obj->getDedx() );
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
