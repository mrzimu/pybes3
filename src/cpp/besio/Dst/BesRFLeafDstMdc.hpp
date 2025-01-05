#pragma once

#include <awkward/LayoutBuilder.h>

#include "RootEventData/TDstEvent.h"
#include "RootEventData/TMdcTrack.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using DstMdcRecord = RecordBuilder<RaggedItemField<0, Int_t>,       // trackIndex
                                   RaggedArrayField<1, 5, double>,  // helix[5]
                                   RaggedArrayField<2, 15, double>, // helixErr[15]
                                   RaggedItemField<3, Int_t>,       // stat
                                   RaggedItemField<4, Double_t>,    // chi2
                                   RaggedItemField<5, Int_t>,       // ndof
                                   RaggedItemField<6, Int_t>,       // nster
                                   RaggedItemField<7, Int_t>,       // nlayer
                                   RaggedItemField<8, Int_t>,       // firstLayer
                                   RaggedItemField<9, Int_t>        // lastLayer
                                   >;

const FieldMap field_map_dst_mdc = {
    { 0, BesFieldNames::Dst::Mdc::trackIndex }, { 1, BesFieldNames::Dst::Mdc::helix },
    { 2, BesFieldNames::Dst::Mdc::helixErr },   { 3, BesFieldNames::Dst::Mdc::stat },
    { 4, BesFieldNames::Dst::Mdc::chi2 },       { 5, BesFieldNames::Dst::Mdc::ndof },
    { 6, BesFieldNames::Dst::Mdc::nster },      { 7, BesFieldNames::Dst::Mdc::nlayer },
    { 8, BesFieldNames::Dst::Mdc::firstLayer }, { 9, BesFieldNames::Dst::Mdc::lastLayer } };

class BesRFLeafDstMdc : public BesRootFieldLeaf<TDstEvent, DstMdcRecord> {
  public:
    BesRFLeafDstMdc( TDstEvent* obj )
        : BesRootFieldLeaf<TDstEvent, DstMdcRecord>( obj, BesFieldNames::Dst::Mdc::rpath,
                                                     field_map_dst_mdc ) {}

    void fill() {
        auto& trackIndex = m_builder.content<0>().begin_list();
        auto& helix      = m_builder.content<1>().begin_list();
        auto& helixErr   = m_builder.content<2>().begin_list();
        auto& stat       = m_builder.content<3>().begin_list();
        auto& chi2       = m_builder.content<4>().begin_list();
        auto& ndof       = m_builder.content<5>().begin_list();
        auto& nster      = m_builder.content<6>().begin_list();
        auto& nlayer     = m_builder.content<7>().begin_list();
        auto& firstLayer = m_builder.content<8>().begin_list();
        auto& lastLayer  = m_builder.content<9>().begin_list();

        for ( auto tobj : ( *m_obj->getMdcTrackCol() ) )
        {
            TMdcTrack* trk = static_cast<TMdcTrack*>( tobj );

            trackIndex.append( trk->trackId() );

            auto& subhelix = helix.begin_list();
            for ( int i = 0; i < 5; i++ ) { subhelix.append( trk->helix( i ) ); }
            helix.end_list();

            auto& subhelixErr = helixErr.begin_list();
            for ( int i = 0; i < 15; i++ ) { subhelixErr.append( trk->err( i ) ); }
            helixErr.end_list();

            stat.append( trk->stat() );
            chi2.append( trk->chi2() );
            ndof.append( trk->ndof() );
            nster.append( trk->nster() );
            nlayer.append( trk->nlayer() );
            firstLayer.append( trk->firstLayer() );
            lastLayer.append( trk->lastLayer() );
        }

        m_builder.content<0>().end_list(); // trackIndex
        m_builder.content<1>().end_list(); // helix
        m_builder.content<2>().end_list(); // helixErr
        m_builder.content<3>().end_list(); // stat
        m_builder.content<4>().end_list(); // chi2
        m_builder.content<5>().end_list(); // ndof
        m_builder.content<6>().end_list(); // nster
        m_builder.content<7>().end_list(); // nlayer
        m_builder.content<8>().end_list(); // firstLayer
        m_builder.content<9>().end_list(); // lastLayer
    }
};