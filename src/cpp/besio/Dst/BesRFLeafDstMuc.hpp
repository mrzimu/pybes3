#pragma once

#include <awkward/LayoutBuilder.h>

#include "RootEventData/TDstEvent.h"
#include "RootEventData/TMucTrack.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using DstMucRecord = RecordBuilder<RaggedItemField<0, int>,     // trackIndex
                                   RaggedItemField<1, int>,     // MUC identify
                                   RaggedItemField<2, int>,     // status
                                   RaggedItemField<3, int>,     // type
                                   RaggedItemField<4, int>,     // startPart
                                   RaggedItemField<5, int>,     // endPart
                                   RaggedItemField<6, int>,     // brLastLayer
                                   RaggedItemField<7, int>,     // ecLastLayer
                                   RaggedItemField<8, int>,     // nHits
                                   RaggedItemField<9, int>,     // nLayers
                                   RaggedItemField<10, int>,    // maxHitsInLayer
                                   RaggedItemField<11, double>, // depth
                                   RaggedItemField<12, double>, // chi2
                                   RaggedItemField<13, int>,    // ndof
                                   RaggedItemField<14, double>, // rms
                                   RaggedItemField<15, double>, // x
                                   RaggedItemField<16, double>, // y
                                   RaggedItemField<17, double>, // z
                                   RaggedItemField<18, double>, // x sigma
                                   RaggedItemField<19, double>, // y sigma
                                   RaggedItemField<20, double>, // z sigma
                                   RaggedItemField<21, double>, // px
                                   RaggedItemField<22, double>, // py
                                   RaggedItemField<23, double>, // pz
                                   RaggedItemField<24, double>, // distance
                                   RaggedItemField<25, double>, // delta phi
                                   RaggedItemField<26, double>, // kalrechi2
                                   RaggedItemField<27, int>,    // kaldof
                                   RaggedItemField<28, int>,    // kalbrLastLayer
                                   RaggedItemField<29, int>     // kalecLastLayer
                                   >;

const FieldMap field_map_dst_muc = { { 0, BesFieldNames::Dst::Muc::trackIndex },
                                     { 1, BesFieldNames::Dst::Muc::id },
                                     { 2, BesFieldNames::Dst::Muc::status },
                                     { 3, BesFieldNames::Dst::Muc::type },
                                     { 4, BesFieldNames::Dst::Muc::startPart },
                                     { 5, BesFieldNames::Dst::Muc::endPart },
                                     { 6, BesFieldNames::Dst::Muc::brLastLayer },
                                     { 7, BesFieldNames::Dst::Muc::ecLastLayer },
                                     { 8, BesFieldNames::Dst::Muc::nHits },
                                     { 9, BesFieldNames::Dst::Muc::nLayers },
                                     { 10, BesFieldNames::Dst::Muc::maxHitsInLayer },
                                     { 11, BesFieldNames::Dst::Muc::depth },
                                     { 12, BesFieldNames::Dst::Muc::chi2 },
                                     { 13, BesFieldNames::Dst::Muc::dof },
                                     { 14, BesFieldNames::Dst::Muc::rms },
                                     { 15, BesFieldNames::Dst::Muc::x },
                                     { 16, BesFieldNames::Dst::Muc::y },
                                     { 17, BesFieldNames::Dst::Muc::z },
                                     { 18, BesFieldNames::Dst::Muc::xSigma },
                                     { 19, BesFieldNames::Dst::Muc::ySigma },
                                     { 20, BesFieldNames::Dst::Muc::zSigma },
                                     { 21, BesFieldNames::Dst::Muc::px },
                                     { 22, BesFieldNames::Dst::Muc::py },
                                     { 23, BesFieldNames::Dst::Muc::pz },
                                     { 24, BesFieldNames::Dst::Muc::distance },
                                     { 25, BesFieldNames::Dst::Muc::deltaPhi },
                                     { 26, BesFieldNames::Dst::Muc::kalrechi2 },
                                     { 27, BesFieldNames::Dst::Muc::kaldof },
                                     { 28, BesFieldNames::Dst::Muc::kalbrLastLayer },
                                     { 29, BesFieldNames::Dst::Muc::kalecLastLayer } };

class BesRFLeafDstMuc : public BesRootFieldLeaf<TDstEvent, DstMucRecord> {
  public:
    BesRFLeafDstMuc( TDstEvent* obj )
        : BesRootFieldLeaf<TDstEvent, DstMucRecord>( obj, BesFieldNames::Dst::Muc::rpath,
                                                     field_map_dst_muc ) {}

    void init() { m_builder.set_fields( field_map_dst_muc ); }

    void fill() {
        auto& trackIndex     = m_builder.content<0>().begin_list();
        auto& id             = m_builder.content<1>().begin_list();
        auto& status         = m_builder.content<2>().begin_list();
        auto& type           = m_builder.content<3>().begin_list();
        auto& startPart      = m_builder.content<4>().begin_list();
        auto& endPart        = m_builder.content<5>().begin_list();
        auto& brLastLayer    = m_builder.content<6>().begin_list();
        auto& ecLastLayer    = m_builder.content<7>().begin_list();
        auto& nHits          = m_builder.content<8>().begin_list();
        auto& nLayers        = m_builder.content<9>().begin_list();
        auto& maxHitsInLayer = m_builder.content<10>().begin_list();
        auto& depth          = m_builder.content<11>().begin_list();
        auto& chi2           = m_builder.content<12>().begin_list();
        auto& dof            = m_builder.content<13>().begin_list();
        auto& rms            = m_builder.content<14>().begin_list();
        auto& x              = m_builder.content<15>().begin_list();
        auto& y              = m_builder.content<16>().begin_list();
        auto& z              = m_builder.content<17>().begin_list();
        auto& xSigma         = m_builder.content<18>().begin_list();
        auto& ySigma         = m_builder.content<19>().begin_list();
        auto& zSigma         = m_builder.content<20>().begin_list();
        auto& px             = m_builder.content<21>().begin_list();
        auto& py             = m_builder.content<22>().begin_list();
        auto& pz             = m_builder.content<23>().begin_list();
        auto& distance       = m_builder.content<24>().begin_list();
        auto& deltaPhi       = m_builder.content<25>().begin_list();
        auto& kalrechi2      = m_builder.content<26>().begin_list();
        auto& kaldof         = m_builder.content<27>().begin_list();
        auto& kalbrLastLayer = m_builder.content<28>().begin_list();
        auto& kalecLastLayer = m_builder.content<29>().begin_list();

        for ( auto tobj : ( *m_obj->getMucTrackCol() ) )
        {
            TMucTrack* trk = static_cast<TMucTrack*>( tobj );

            trackIndex.append( trk->trackId() );
            id.append( trk->id() );
            status.append( trk->status() );
            type.append( trk->type() );
            startPart.append( trk->startPart() );
            endPart.append( trk->endPart() );
            brLastLayer.append( trk->brLastLayer() );
            ecLastLayer.append( trk->ecLastLayer() );
            nHits.append( trk->numHits() );
            nLayers.append( trk->numLayers() );
            maxHitsInLayer.append( trk->maxHitsInLayer() );
            depth.append( trk->depth() );
            chi2.append( trk->chi2() );
            dof.append( trk->dof() );
            rms.append( trk->rms() );
            x.append( trk->xPos() );
            y.append( trk->yPos() );
            z.append( trk->zPos() );
            xSigma.append( trk->xPosSigma() );
            ySigma.append( trk->yPosSigma() );
            zSigma.append( trk->zPosSigma() );
            px.append( trk->px() );
            py.append( trk->py() );
            pz.append( trk->pz() );
            distance.append( trk->distance() );
            deltaPhi.append( trk->deltaPhi() );
            kalrechi2.append( trk->kalRechi2() );
            kaldof.append( trk->kaldof() );
            kalbrLastLayer.append( trk->kalbrLastLayer() );
            kalecLastLayer.append( trk->kalecLastLayer() );
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
        m_builder.content<28>().end_list();
        m_builder.content<29>().end_list();
    }
};