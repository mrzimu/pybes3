#pragma once

#include <awkward/LayoutBuilder.h>

#include "RootEventData/TEvtRecObject.h"
#include "RootEventData/TEvtRecPrimaryVertex.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using EvtRecPrimaryVertexRecord = RecordBuilder<SimpleItemField<0, bool>,      // isValid
                                                SimpleItemField<1, int>,       // nTracks
                                                RaggedItemField<2, int>,       // trackIdList
                                                SimpleItemField<3, double>,    // chi2
                                                SimpleItemField<4, int>,       // ndof
                                                SimpleItemField<5, int>,       // fitMethod
                                                SimpleItemField<6, double>,    // x
                                                SimpleItemField<7, double>,    // y
                                                SimpleItemField<8, double>,    // z
                                                SimpleArrayField<9, 6, double> // errVtx
                                                >;

const FieldMap field_map_recobj_pvtx = {
    { 0, BesFieldNames::EvtRec::PrimaryVertex::isValid },
    { 1, BesFieldNames::EvtRec::PrimaryVertex::nTracks },
    { 2, BesFieldNames::EvtRec::PrimaryVertex::trackIdList },
    { 3, BesFieldNames::EvtRec::PrimaryVertex::chi2 },
    { 4, BesFieldNames::EvtRec::PrimaryVertex::ndof },
    { 5, BesFieldNames::EvtRec::PrimaryVertex::fitMethod },
    { 6, BesFieldNames::EvtRec::PrimaryVertex::x },
    { 7, BesFieldNames::EvtRec::PrimaryVertex::y },
    { 8, BesFieldNames::EvtRec::PrimaryVertex::z },
    { 9, BesFieldNames::EvtRec::PrimaryVertex::errVtx } };

class BesRFLeafEvtRecPrimaryVertex
    : public BesRootFieldLeaf<TEvtRecObject, EvtRecPrimaryVertexRecord> {
  public:
    BesRFLeafEvtRecPrimaryVertex( TEvtRecObject* obj )
        : BesRootFieldLeaf<TEvtRecObject, EvtRecPrimaryVertexRecord>(
              obj, BesFieldNames::EvtRec::Evt::rpath, field_map_recobj_pvtx ) {}

    void fill() {
        const TEvtRecPrimaryVertex* vtx = m_obj->getEvtRecPrimaryVertex();

        m_builder.content<0>().append( vtx->isValid() );
        m_builder.content<1>().append( vtx->nTracks() );

        auto& trkidlist = m_builder.content<2>().begin_list();
        for ( auto& trkid : vtx->trackIdList() ) { trkidlist.append( trkid ); }
        m_builder.content<2>().end_list();

        m_builder.content<3>().append( vtx->chi2() );
        m_builder.content<4>().append( vtx->ndof() );
        m_builder.content<5>().append( vtx->fitMethod() );
        m_builder.content<6>().append( vtx->vertex( 0 ) );
        m_builder.content<7>().append( vtx->vertex( 1 ) );
        m_builder.content<8>().append( vtx->vertex( 2 ) );

        auto& errvtx = m_builder.content<9>().begin_list();
        for ( int i = 0; i < 6; i++ ) { errvtx.append( vtx->errorVertex( i ) ); }
        m_builder.content<9>().end_list();
    }
};