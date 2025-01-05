#pragma once

#include <awkward/LayoutBuilder.h>

#include "RootEventData/TEvtRecObject.h"
#include "RootEventData/TEvtRecVeeVertex.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using EvtRecVeeVertexRecord = RecordBuilder<RaggedItemField<0, bool>,         // vtxId
                                            RaggedItemField<1, int>,          // vtxType
                                            RaggedItemField<2, double>,       // chi2
                                            RaggedItemField<3, int>,          // ndof
                                            RaggedItemField<4, double>,       // mass
                                            RaggedItemField<5, double>,       // px
                                            RaggedItemField<6, double>,       // py
                                            RaggedItemField<7, double>,       // pz
                                            RaggedItemField<8, double>,       // E
                                            RaggedItemField<9, double>,       // x
                                            RaggedItemField<10, double>,      // y
                                            RaggedItemField<11, double>,      // z
                                            RaggedArrayField<12, 28, double>, // err
                                            RaggedArrayField<13, 2, int>,     // pair
                                            RaggedItemField<14, int>,         // nCharge
                                            RaggedItemField<15, int>,         // nTracks
                                            RaggedArrayField<16, 2, int>      // daughters
                                            >;

const FieldMap field_map_recobj_vvtx = { { 0, BesFieldNames::EvtRec::VeeVertex::vtxId },
                                         { 1, BesFieldNames::EvtRec::VeeVertex::vtxType },
                                         { 2, BesFieldNames::EvtRec::VeeVertex::chi2 },
                                         { 3, BesFieldNames::EvtRec::VeeVertex::ndof },
                                         { 4, BesFieldNames::EvtRec::VeeVertex::mass },
                                         { 5, BesFieldNames::EvtRec::VeeVertex::px },
                                         { 6, BesFieldNames::EvtRec::VeeVertex::py },
                                         { 7, BesFieldNames::EvtRec::VeeVertex::pz },
                                         { 8, BesFieldNames::EvtRec::VeeVertex::E },
                                         { 9, BesFieldNames::EvtRec::VeeVertex::x },
                                         { 10, BesFieldNames::EvtRec::VeeVertex::y },
                                         { 11, BesFieldNames::EvtRec::VeeVertex::z },
                                         { 12, BesFieldNames::EvtRec::VeeVertex::err },
                                         { 13, BesFieldNames::EvtRec::VeeVertex::pair },
                                         { 14, BesFieldNames::EvtRec::VeeVertex::nCharge },
                                         { 15, BesFieldNames::EvtRec::VeeVertex::nTracks },
                                         { 16, BesFieldNames::EvtRec::VeeVertex::daughters } };

class BesRFLeafEvtRecVeeVertex
    : public BesRootFieldLeaf<TEvtRecObject, EvtRecVeeVertexRecord> {
  public:
    BesRFLeafEvtRecVeeVertex( TEvtRecObject* obj )
        : BesRootFieldLeaf<TEvtRecObject, EvtRecVeeVertexRecord>(
              obj, BesFieldNames::EvtRec::VeeVertex::rpath, field_map_recobj_vvtx ) {}

    void fill() {
        auto& vtxId     = m_builder.content<0>().begin_list();
        auto& vtxType   = m_builder.content<1>().begin_list();
        auto& chi2      = m_builder.content<2>().begin_list();
        auto& ndof      = m_builder.content<3>().begin_list();
        auto& mass      = m_builder.content<4>().begin_list();
        auto& px        = m_builder.content<5>().begin_list();
        auto& py        = m_builder.content<6>().begin_list();
        auto& pz        = m_builder.content<7>().begin_list();
        auto& E         = m_builder.content<8>().begin_list();
        auto& x         = m_builder.content<9>().begin_list();
        auto& y         = m_builder.content<10>().begin_list();
        auto& z         = m_builder.content<11>().begin_list();
        auto& err       = m_builder.content<12>().begin_list();
        auto& pair      = m_builder.content<13>().begin_list();
        auto& nCharge   = m_builder.content<14>().begin_list();
        auto& nTracks   = m_builder.content<15>().begin_list();
        auto& daughters = m_builder.content<16>().begin_list();

        for ( auto tobj : ( *m_obj->getEvtRecVeeVertexCol() ) )
        {
            TEvtRecVeeVertex* obj = static_cast<TEvtRecVeeVertex*>( tobj );

            vtxId.append( obj->vertexId() );
            vtxType.append( obj->vertexType() );
            chi2.append( obj->chi2() );
            ndof.append( obj->ndof() );
            mass.append( obj->mass() );
            px.append( obj->w( 0 ) );
            py.append( obj->w( 1 ) );
            pz.append( obj->w( 2 ) );
            E.append( obj->w( 3 ) );
            x.append( obj->w( 4 ) );
            y.append( obj->w( 5 ) );
            z.append( obj->w( 6 ) );

            auto& suberr = err.begin_list();
            for ( int i = 0; i < 28; i++ ) { suberr.append( obj->Ew( i ) ); }
            err.end_list();

            auto& subpair = pair.begin_list();
            subpair.append( obj->pair( 0 ) );
            subpair.append( obj->pair( 1 ) );
            pair.end_list();

            nCharge.append( obj->nCharge() );
            nTracks.append( obj->nTracks() );

            auto& subdaughters = daughters.begin_list();
            subdaughters.append( obj->daughter( 0 ) );
            subdaughters.append( obj->daughter( 1 ) );
            daughters.end_list();
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
    }
};