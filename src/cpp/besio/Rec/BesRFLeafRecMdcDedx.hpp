#pragma once

#include "RootEventData/TRecMdcDedx.h"
#include "RootEventData/TRecTrackEvent.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using RecMdcDedxRecord = RecordBuilder<RaggedItemField<0, double>,      // dedx_hit
                                       RaggedItemField<1, double>,      // dedx_esat
                                       RaggedItemField<2, double>,      // dedx_norun
                                       RaggedItemField<3, double>,      // dedx_momentum
                                       RaggedItemField<4, int>,         // trackId
                                       RaggedItemField<5, int>,         // mdcTrackId
                                       RaggedItemField<6, int>,         // mdcKalTrackId
                                       RaggedItemField<7, int>,         // particleId
                                       RaggedItemField<8, int>,         // status
                                       RaggedItemField<9, int>,         // trunc_alg
                                       RaggedItemField<10, double>,     // chiE
                                       RaggedItemField<11, double>,     // chiMu
                                       RaggedItemField<12, double>,     // chiPi
                                       RaggedItemField<13, double>,     // chiK
                                       RaggedItemField<14, double>,     // chiP
                                       RaggedItemField<15, int>,        // numGoodHits
                                       RaggedItemField<16, int>,        // numTotalHits
                                       RaggedItemField<17, double>,     // probPH
                                       RaggedItemField<18, double>,     // normPH
                                       RaggedItemField<19, double>,     // errorPH
                                       RaggedItemField<20, double>,     // twentyPH
                                       RaggedArrayField<21, 5, double>, // chi
                                       RaggedArrayField<22, 5, double>, // dedx_exp
                                       RaggedArrayField<23, 5, double>, // sigma_dedx
                                       RaggedArrayField<24, 5, double>  // pid_prob
                                       >;

const FieldMap field_map_rec_mdcdedx = {
    { 0, BesFieldNames::Rec::MdcDedx::dedx_hit },
    { 1, BesFieldNames::Rec::MdcDedx::dedx_esat },
    { 2, BesFieldNames::Rec::MdcDedx::dedx_norun },
    { 3, BesFieldNames::Rec::MdcDedx::dedx_momentum },
    { 4, BesFieldNames::Rec::MdcDedx::trackId },
    { 5, BesFieldNames::Rec::MdcDedx::mdcTrackId },
    { 6, BesFieldNames::Rec::MdcDedx::mdcKalTrackId },
    { 7, BesFieldNames::Rec::MdcDedx::particleId },
    { 8, BesFieldNames::Rec::MdcDedx::status },
    { 9, BesFieldNames::Rec::MdcDedx::trunc_alg },
    { 10, BesFieldNames::Rec::MdcDedx::chiE },
    { 11, BesFieldNames::Rec::MdcDedx::chiMu },
    { 12, BesFieldNames::Rec::MdcDedx::chiPi },
    { 13, BesFieldNames::Rec::MdcDedx::chiK },
    { 14, BesFieldNames::Rec::MdcDedx::chiP },
    { 15, BesFieldNames::Rec::MdcDedx::numGoodHits },
    { 16, BesFieldNames::Rec::MdcDedx::numTotalHits },
    { 17, BesFieldNames::Rec::MdcDedx::probPH },
    { 18, BesFieldNames::Rec::MdcDedx::normPH },
    { 19, BesFieldNames::Rec::MdcDedx::errorPH },
    { 20, BesFieldNames::Rec::MdcDedx::twentyPH },
    { 21, BesFieldNames::Rec::MdcDedx::chi },
    { 22, BesFieldNames::Rec::MdcDedx::dedx_exp },
    { 23, BesFieldNames::Rec::MdcDedx::sigma_dedx },
    { 24, BesFieldNames::Rec::MdcDedx::pid_prob },
};
class BesRFLeafRecMdcDedx : public BesRootFieldLeaf<TRecTrackEvent, RecMdcDedxRecord> {
  public:
    BesRFLeafRecMdcDedx( TRecTrackEvent* obj )
        : BesRootFieldLeaf<TRecTrackEvent, RecMdcDedxRecord>(
              obj, BesFieldNames::Rec::MdcDedx::rpath, field_map_rec_mdcdedx ) {}

    void fill() {
        auto& dedx_hit      = m_builder.content<0>().begin_list();
        auto& dedx_esat     = m_builder.content<1>().begin_list();
        auto& dedx_norun    = m_builder.content<2>().begin_list();
        auto& dedx_momentum = m_builder.content<3>().begin_list();
        auto& trackId       = m_builder.content<4>().begin_list();
        auto& mdcTrackId    = m_builder.content<5>().begin_list();
        auto& mdcKalTrackId = m_builder.content<6>().begin_list();
        auto& particleId    = m_builder.content<7>().begin_list();
        auto& status        = m_builder.content<8>().begin_list();
        auto& trunc_alg     = m_builder.content<9>().begin_list();
        auto& chiE          = m_builder.content<10>().begin_list();
        auto& chiMu         = m_builder.content<11>().begin_list();
        auto& chiPi         = m_builder.content<12>().begin_list();
        auto& chiK          = m_builder.content<13>().begin_list();
        auto& chiP          = m_builder.content<14>().begin_list();
        auto& numGoodHits   = m_builder.content<15>().begin_list();
        auto& numTotalHits  = m_builder.content<16>().begin_list();
        auto& probPH        = m_builder.content<17>().begin_list();
        auto& normPH        = m_builder.content<18>().begin_list();
        auto& errorPH       = m_builder.content<19>().begin_list();
        auto& twentyPH      = m_builder.content<20>().begin_list();
        auto& chi           = m_builder.content<21>().begin_list();
        auto& dedx_exp      = m_builder.content<22>().begin_list();
        auto& sigma_dedx    = m_builder.content<23>().begin_list();
        auto& pid_prob      = m_builder.content<24>().begin_list();

        for ( auto tobj : *m_obj->getRecMdcDedxCol() )
        {
            TRecMdcDedx* obj = static_cast<TRecMdcDedx*>( tobj );

            dedx_hit.append( obj->dedxHit() );
            dedx_esat.append( obj->dedxEsat() );
            dedx_norun.append( obj->dedxNoRun() );
            dedx_momentum.append( obj->dedxMoment() );
            trackId.append( obj->trackId() );
            mdcTrackId.append( obj->mdcTrackId() );
            mdcKalTrackId.append( obj->mdcKalTrackId() );
            particleId.append( obj->particleId() );
            status.append( obj->status() );
            trunc_alg.append( obj->truncAlg() );
            chiE.append( obj->chiE() );
            chiMu.append( obj->chiMu() );
            chiPi.append( obj->chiPi() );
            chiK.append( obj->chiK() );
            chiP.append( obj->chiP() );
            numGoodHits.append( obj->numGoodHits() );
            numTotalHits.append( obj->numTotalHits() );
            probPH.append( obj->probPH() );
            normPH.append( obj->normPH() );
            errorPH.append( obj->errorPH() );
            twentyPH.append( obj->twentyPH() );

            auto& subchi = chi.begin_list();
            for ( int i = 0; i < 5; i++ ) subchi.append( obj->chi( i ) );
            chi.end_list();

            auto& subdedx_exp = dedx_exp.begin_list();
            for ( int i = 0; i < 5; i++ ) subdedx_exp.append( obj->dedxExpect( i ) );
            dedx_exp.end_list();

            auto& subsigma_dedx = sigma_dedx.begin_list();
            for ( int i = 0; i < 5; i++ ) subsigma_dedx.append( obj->sigmaDedx( i ) );
            sigma_dedx.end_list();

            auto& subpid_prob = pid_prob.begin_list();
            for ( int i = 0; i < 5; i++ ) subpid_prob.append( obj->pidProb( i ) );
            pid_prob.end_list();
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
    }
};
