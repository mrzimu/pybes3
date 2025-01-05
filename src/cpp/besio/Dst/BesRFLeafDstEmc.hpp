#pragma once

#include <awkward/LayoutBuilder.h>

#include "RootEventData/TDstEvent.h"
#include "RootEventData/TEmcTrack.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using DstEmcRecord = RecordBuilder<RaggedItemField<0, int>,        // trackIndex
                                   RaggedItemField<1, int>,        // nHits
                                   RaggedItemField<2, int>,        // status
                                   RaggedItemField<3, int>,        // module
                                   RaggedItemField<4, double>,     // x
                                   RaggedItemField<5, double>,     // y
                                   RaggedItemField<6, double>,     // z
                                   RaggedItemField<7, double>,     // dTheta
                                   RaggedItemField<8, double>,     // dPhi
                                   RaggedItemField<9, double>,     // energy
                                   RaggedItemField<10, double>,    // dE
                                   RaggedItemField<11, double>,    // eSeed
                                   RaggedItemField<12, double>,    // e3x3
                                   RaggedItemField<13, double>,    // e5x5
                                   RaggedItemField<14, double>,    // time
                                   RaggedItemField<15, double>,    // secondMoment
                                   RaggedItemField<16, double>,    // latMoment
                                   RaggedItemField<17, double>,    // a20Moment
                                   RaggedItemField<18, double>,    // a42Moment
                                   RaggedArrayField<19, 6, double> // err[6]
                                   >;

const FieldMap field_map_dst_emc = {
    { 0, BesFieldNames::Dst::Emc::trackIndex }, { 1, BesFieldNames::Dst::Emc::nHits },
    { 2, BesFieldNames::Dst::Emc::status },     { 3, BesFieldNames::Dst::Emc::moduleId },
    { 5, BesFieldNames::Dst::Emc::x },          { 6, BesFieldNames::Dst::Emc::y },
    { 7, BesFieldNames::Dst::Emc::z },          { 8, BesFieldNames::Dst::Emc::dTheta },
    { 9, BesFieldNames::Dst::Emc::dPhi },       { 10, BesFieldNames::Dst::Emc::energy },
    { 11, BesFieldNames::Dst::Emc::dE },        { 12, BesFieldNames::Dst::Emc::eSeed },
    { 13, BesFieldNames::Dst::Emc::e3x3 },      { 14, BesFieldNames::Dst::Emc::e5x5 },
    { 15, BesFieldNames::Dst::Emc::time },      { 16, BesFieldNames::Dst::Emc::secondMoment },
    { 17, BesFieldNames::Dst::Emc::latMoment }, { 18, BesFieldNames::Dst::Emc::a20Moment },
    { 19, BesFieldNames::Dst::Emc::a42Moment }, { 20, BesFieldNames::Dst::Emc::err } };

class BesRFLeafDstEmc : public BesRootFieldLeaf<TDstEvent, DstEmcRecord> {
  public:
    BesRFLeafDstEmc( TDstEvent* obj )
        : BesRootFieldLeaf<TDstEvent, DstEmcRecord>( obj, BesFieldNames::Dst::Emc::rpath,
                                                     field_map_dst_emc ) {}

    void fill() {
        auto& trackIndex   = m_builder.content<0>().begin_list();
        auto& nHits        = m_builder.content<1>().begin_list();
        auto& status       = m_builder.content<2>().begin_list();
        auto& moduleId     = m_builder.content<3>().begin_list();
        auto& x            = m_builder.content<4>().begin_list();
        auto& y            = m_builder.content<5>().begin_list();
        auto& z            = m_builder.content<6>().begin_list();
        auto& dTheta       = m_builder.content<7>().begin_list();
        auto& dPhi         = m_builder.content<8>().begin_list();
        auto& energy       = m_builder.content<9>().begin_list();
        auto& dE           = m_builder.content<10>().begin_list();
        auto& eSeed        = m_builder.content<11>().begin_list();
        auto& e3x3         = m_builder.content<12>().begin_list();
        auto& e5x5         = m_builder.content<13>().begin_list();
        auto& time         = m_builder.content<14>().begin_list();
        auto& secondMoment = m_builder.content<15>().begin_list();
        auto& latMoment    = m_builder.content<16>().begin_list();
        auto& a20Moment    = m_builder.content<17>().begin_list();
        auto& a42Moment    = m_builder.content<18>().begin_list();
        auto& err          = m_builder.content<19>().begin_list();

        for ( auto tobj : ( *m_obj->getEmcTrackCol() ) )
        {
            TEmcTrack* trk = static_cast<TEmcTrack*>( tobj );

            trackIndex.append( trk->trackId() );
            nHits.append( trk->numHits() );
            status.append( trk->status() );
            moduleId.append( trk->module() );
            x.append( trk->x() );
            y.append( trk->y() );
            z.append( trk->z() );
            dTheta.append( trk->dtheta() );
            dPhi.append( trk->dphi() );
            energy.append( trk->energy() );
            dE.append( trk->dE() );
            eSeed.append( trk->eSeed() );
            e3x3.append( trk->e3x3() );
            e5x5.append( trk->e5x5() );
            time.append( trk->time() );
            secondMoment.append( trk->secondMoment() );
            latMoment.append( trk->latMoment() );
            a20Moment.append( trk->a20Moment() );
            a42Moment.append( trk->a42Moment() );

            auto& suberr = err.begin_list();
            for ( int i = 0; i < 6; i++ ) { suberr.append( trk->err( i ) ); }
            err.end_list();
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
        m_builder.content<18>().end_list();
        m_builder.content<19>().end_list();
    }
};