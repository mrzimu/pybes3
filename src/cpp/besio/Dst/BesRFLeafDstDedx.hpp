#pragma once

#include <awkward/LayoutBuilder.h>

#include "RootEventData/TDstEvent.h"
#include "RootEventData/TMdcDedx.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using DstDedxBuilder = RecordBuilder<RaggedItemField<0, int>,     // trackIndex
                                     RaggedItemField<1, int>,     // particleId
                                     RaggedItemField<2, int>,     // status
                                     RaggedItemField<3, int>,     // trunc_alg
                                     RaggedItemField<4, double>,  // chiE
                                     RaggedItemField<5, double>,  // chiMu
                                     RaggedItemField<6, double>,  // chiPi
                                     RaggedItemField<7, double>,  // chiK
                                     RaggedItemField<8, double>,  // chiP
                                     RaggedItemField<9, int>,     // numGoodHits
                                     RaggedItemField<10, int>,    // numTotalHits
                                     RaggedItemField<11, double>, // probPH
                                     RaggedItemField<12, double>, // normPH
                                     RaggedItemField<13, double>, // errorPH
                                     RaggedItemField<14, double>  // twentyPH
                                     >;

const FieldMap field_map_dst_dedx = {
    { 0, BesFieldNames::Dst::Dedx::trackIndex },  { 1, BesFieldNames::Dst::Dedx::particleId },
    { 2, BesFieldNames::Dst::Dedx::status },      { 3, BesFieldNames::Dst::Dedx::trunc_alg },
    { 4, BesFieldNames::Dst::Dedx::chiE },        { 5, BesFieldNames::Dst::Dedx::chiMu },
    { 6, BesFieldNames::Dst::Dedx::chiPi },       { 7, BesFieldNames::Dst::Dedx::chiK },
    { 8, BesFieldNames::Dst::Dedx::chiP },        { 9, BesFieldNames::Dst::Dedx::nGoodHits },
    { 10, BesFieldNames::Dst::Dedx::nTotalHits }, { 11, BesFieldNames::Dst::Dedx::probPH },
    { 12, BesFieldNames::Dst::Dedx::normPH },     { 13, BesFieldNames::Dst::Dedx::errorPH },
    { 14, BesFieldNames::Dst::Dedx::twentyPH } };

class BesRFLeafDstDedx : public BesRootFieldLeaf<TDstEvent, DstDedxBuilder> {
  public:
    BesRFLeafDstDedx( TDstEvent* obj )
        : BesRootFieldLeaf<TDstEvent, DstDedxBuilder>( obj, BesFieldNames::Dst::Dedx::rpath,
                                                       field_map_dst_dedx ) {}

    void fill() {
        auto& trackIndex   = m_builder.content<0>().begin_list();
        auto& particleId   = m_builder.content<1>().begin_list();
        auto& status       = m_builder.content<2>().begin_list();
        auto& trunc_alg    = m_builder.content<3>().begin_list();
        auto& chiE         = m_builder.content<4>().begin_list();
        auto& chiMu        = m_builder.content<5>().begin_list();
        auto& chiPi        = m_builder.content<6>().begin_list();
        auto& chiK         = m_builder.content<7>().begin_list();
        auto& chiP         = m_builder.content<8>().begin_list();
        auto& numGoodHits  = m_builder.content<9>().begin_list();
        auto& numTotalHits = m_builder.content<10>().begin_list();
        auto& probPH       = m_builder.content<11>().begin_list();
        auto& normPH       = m_builder.content<12>().begin_list();
        auto& errorPH      = m_builder.content<13>().begin_list();
        auto& twentyPH     = m_builder.content<14>().begin_list();

        for ( auto tobj : ( *m_obj->getMdcDedxCol() ) )
        {
            TMdcDedx* dedx = static_cast<TMdcDedx*>( tobj );

            trackIndex.append( dedx->trackId() );
            particleId.append( dedx->particleId() );
            status.append( dedx->status() );
            trunc_alg.append( dedx->truncAlg() );
            chiE.append( dedx->chiE() );
            chiMu.append( dedx->chiMu() );
            chiPi.append( dedx->chiPi() );
            chiK.append( dedx->chiK() );
            chiP.append( dedx->chiP() );
            numGoodHits.append( dedx->numGoodHits() );
            numTotalHits.append( dedx->numTotalHits() );
            probPH.append( dedx->probPH() );
            normPH.append( dedx->normPH() );
            errorPH.append( dedx->errorPH() );
            twentyPH.append( dedx->twentyPH() );
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