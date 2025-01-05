#pragma once

#include "RootEventData/TRecEmcShower.h"
#include "RootEventData/TRecTrackEvent.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using RecEmcShowerRecord = RecordBuilder<RaggedItemField<0, int>,         // trackId
                                         RaggedItemField<1, int>,         // nhits
                                         RaggedItemField<2, int>,         // status
                                         RaggedItemField<3, int>,         // cellId
                                         RaggedItemField<4, int>,         // module
                                         RaggedItemField<5, double>,      // x
                                         RaggedItemField<6, double>,      // y
                                         RaggedItemField<7, double>,      // z
                                         RaggedItemField<8, double>,      // dTheta
                                         RaggedItemField<9, double>,      // dPhi
                                         RaggedItemField<10, double>,     // energy
                                         RaggedItemField<11, double>,     // dE
                                         RaggedItemField<12, double>,     // eSeed
                                         RaggedItemField<13, double>,     // e3x3
                                         RaggedItemField<14, double>,     // e5x5
                                         RaggedItemField<15, double>,     // eall
                                         RaggedItemField<16, double>,     // eLepton
                                         RaggedItemField<17, double>,     // time
                                         RaggedItemField<18, double>,     // secondMoment
                                         RaggedItemField<19, double>,     // latMoment
                                         RaggedItemField<20, double>,     // a20Moment
                                         RaggedItemField<21, double>,     // a42Moment
                                         RaggedArrayField<22, 6, double>, // err
                                         RaggedRaggedField<23, int>,      // cellIdMapId
                                         RaggedRaggedField<24, double>,   // cellIdMapEnergy
                                         RaggedRaggedField<25, int>,      // cellId3x3
                                         RaggedRaggedField<26, int>,      // cellId5x5
                                         RaggedItemField<27, int>         // clusterId
                                         >;

const FieldMap field_map_rec_emcshower = {
    { 0, BesFieldNames::Rec::EmcShower::trackId },
    { 1, BesFieldNames::Rec::EmcShower::nhits },
    { 2, BesFieldNames::Rec::EmcShower::status },
    { 3, BesFieldNames::Rec::EmcShower::cellId },
    { 4, BesFieldNames::Rec::EmcShower::module },
    { 5, BesFieldNames::Rec::EmcShower::x },
    { 6, BesFieldNames::Rec::EmcShower::y },
    { 7, BesFieldNames::Rec::EmcShower::z },
    { 8, BesFieldNames::Rec::EmcShower::dTheta },
    { 9, BesFieldNames::Rec::EmcShower::dPhi },
    { 10, BesFieldNames::Rec::EmcShower::energy },
    { 11, BesFieldNames::Rec::EmcShower::dE },
    { 12, BesFieldNames::Rec::EmcShower::eSeed },
    { 13, BesFieldNames::Rec::EmcShower::e3x3 },
    { 14, BesFieldNames::Rec::EmcShower::e5x5 },
    { 15, BesFieldNames::Rec::EmcShower::eall },
    { 16, BesFieldNames::Rec::EmcShower::eLepton },
    { 17, BesFieldNames::Rec::EmcShower::time },
    { 18, BesFieldNames::Rec::EmcShower::secondMoment },
    { 19, BesFieldNames::Rec::EmcShower::latMoment },
    { 20, BesFieldNames::Rec::EmcShower::a20Moment },
    { 21, BesFieldNames::Rec::EmcShower::a42Moment },
    { 22, BesFieldNames::Rec::EmcShower::err },
    { 23, BesFieldNames::Rec::EmcShower::cellIdMapId },
    { 24, BesFieldNames::Rec::EmcShower::cellIdMapEnergy },
    { 25, BesFieldNames::Rec::EmcShower::cellId3x3 },
    { 26, BesFieldNames::Rec::EmcShower::cellId5x5 },
    { 27, BesFieldNames::Rec::EmcShower::clusterId } };

class BesRFLeafRecEmcShower : public BesRootFieldLeaf<TRecTrackEvent, RecEmcShowerRecord> {
  public:
    BesRFLeafRecEmcShower( TRecTrackEvent* obj )
        : BesRootFieldLeaf<TRecTrackEvent, RecEmcShowerRecord>(
              obj, BesFieldNames::Rec::EmcShower::rpath, field_map_rec_emcshower ) {}

    void fill() {
        auto& trackId         = m_builder.content<0>().begin_list();
        auto& nhits           = m_builder.content<1>().begin_list();
        auto& status          = m_builder.content<2>().begin_list();
        auto& cellId          = m_builder.content<3>().begin_list();
        auto& module          = m_builder.content<4>().begin_list();
        auto& x               = m_builder.content<5>().begin_list();
        auto& y               = m_builder.content<6>().begin_list();
        auto& z               = m_builder.content<7>().begin_list();
        auto& dTheta          = m_builder.content<8>().begin_list();
        auto& dPhi            = m_builder.content<9>().begin_list();
        auto& energy          = m_builder.content<10>().begin_list();
        auto& dE              = m_builder.content<11>().begin_list();
        auto& eSeed           = m_builder.content<12>().begin_list();
        auto& e3x3            = m_builder.content<13>().begin_list();
        auto& e5x5            = m_builder.content<14>().begin_list();
        auto& eall            = m_builder.content<15>().begin_list();
        auto& eLepton         = m_builder.content<16>().begin_list();
        auto& time            = m_builder.content<17>().begin_list();
        auto& secondMoment    = m_builder.content<18>().begin_list();
        auto& latMoment       = m_builder.content<19>().begin_list();
        auto& a20Moment       = m_builder.content<20>().begin_list();
        auto& a42Moment       = m_builder.content<21>().begin_list();
        auto& err             = m_builder.content<22>().begin_list();
        auto& cellIdMapId     = m_builder.content<23>().begin_list();
        auto& cellIdMapEnergy = m_builder.content<24>().begin_list();
        auto& cellId3x3       = m_builder.content<25>().begin_list();
        auto& cellId5x5       = m_builder.content<26>().begin_list();
        auto& clusterId       = m_builder.content<27>().begin_list();

        for ( auto tobj : *m_obj->getEmcShowerCol() )
        {
            TRecEmcShower* obj = static_cast<TRecEmcShower*>( tobj );

            trackId.append( obj->trackId() );
            nhits.append( obj->numHits() );
            status.append( obj->status() );
            cellId.append( obj->cellId() );
            module.append( obj->module() );
            x.append( obj->x() );
            y.append( obj->y() );
            z.append( obj->z() );
            dTheta.append( obj->dtheta() );
            dPhi.append( obj->dphi() );
            energy.append( obj->energy() );
            dE.append( obj->dE() );
            eSeed.append( obj->eSeed() );
            e3x3.append( obj->e3x3() );
            e5x5.append( obj->e5x5() );
            eall.append( obj->eAll() );
            eLepton.append( obj->eLepton() );
            time.append( obj->time() );
            secondMoment.append( obj->secondMoment() );
            latMoment.append( obj->latMoment() );
            a20Moment.append( obj->a20Moment() );
            a42Moment.append( obj->a42Moment() );

            auto& suberr = err.begin_list();
            for ( int i = 0; i < 6; i++ ) suberr.append( obj->err( i ) );
            err.end_list();

            auto& subcellIdMapId     = cellIdMapId.begin_list();
            auto& subcellIdMapEnergy = cellIdMapEnergy.begin_list();
            for ( auto& [id, energy] : obj->cellIdMap() )
            {
                subcellIdMapId.append( id );
                subcellIdMapEnergy.append( energy );
            }
            cellIdMapId.end_list();
            cellIdMapEnergy.end_list();

            auto& subcellId3x3 = cellId3x3.begin_list();
            for ( auto id : obj->cellId3x3() ) subcellId3x3.append( id );
            cellId3x3.end_list();

            auto& subcellId5x5 = cellId5x5.begin_list();
            for ( auto id : obj->cellId5x5() ) subcellId5x5.append( id );
            cellId5x5.end_list();

            clusterId.append( obj->clusterId() );
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
        m_builder.content<20>().end_list();
        m_builder.content<21>().end_list();
        m_builder.content<22>().end_list();
        m_builder.content<23>().end_list();
        m_builder.content<24>().end_list();
        m_builder.content<25>().end_list();
        m_builder.content<26>().end_list();
        m_builder.content<27>().end_list();
    }
};
