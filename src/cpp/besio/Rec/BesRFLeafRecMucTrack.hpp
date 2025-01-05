#pragma once

#include "RootEventData/TRecMucTrack.h"
#include "RootEventData/TRecTrackEvent.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using RecMucTrackRecord = RecordBuilder<RaggedItemField<0, int>,     // trackId
                                        RaggedItemField<1, int>,     // id
                                        RaggedItemField<2, int>,     // status
                                        RaggedItemField<3, int>,     // type
                                        RaggedItemField<4, int>,     // startPart
                                        RaggedItemField<5, int>,     // endPart
                                        RaggedItemField<6, int>,     // brLastLayer
                                        RaggedItemField<7, int>,     // ecLastLayer
                                        RaggedItemField<8, int>,     // numHits
                                        RaggedItemField<9, int>,     // numLayers
                                        RaggedItemField<10, int>,    // maxHitsInLayer
                                        RaggedItemField<11, double>, // depth
                                        RaggedItemField<12, double>, // chi2
                                        RaggedItemField<13, int>,    // dof
                                        RaggedItemField<14, double>, // rms
                                        RaggedItemField<15, double>, // xPos
                                        RaggedItemField<16, double>, // yPos
                                        RaggedItemField<17, double>, // zPos
                                        RaggedItemField<18, double>, // xPosSigma
                                        RaggedItemField<19, double>, // yPosSigma
                                        RaggedItemField<20, double>, // zPosSigma
                                        RaggedItemField<21, double>, // px
                                        RaggedItemField<22, double>, // py
                                        RaggedItemField<23, double>, // pz
                                        RaggedItemField<24, double>, // distance
                                        RaggedItemField<25, double>, // deltaPhi
                                        RaggedRaggedField<26, int>,  // hits
                                        RaggedRaggedField<27, int>,  // expHits
                                        RaggedRaggedField<28, int>,  // distHits
                                        RaggedItemField<29, double>, // kalrechi2
                                        RaggedItemField<30, int>,    // kaldof
                                        RaggedItemField<31, double>, // kaldepth
                                        RaggedItemField<32, int>,    // kalbrLastLayer
                                        RaggedItemField<33, int>     // kalecLastLayer
                                        >;

const FieldMap field_map_rec_muctrack = {
    { 0, BesFieldNames::Rec::MucTrack::trackId },
    { 1, BesFieldNames::Rec::MucTrack::id },
    { 2, BesFieldNames::Rec::MucTrack::status },
    { 3, BesFieldNames::Rec::MucTrack::type },
    { 4, BesFieldNames::Rec::MucTrack::startPart },
    { 5, BesFieldNames::Rec::MucTrack::endPart },
    { 6, BesFieldNames::Rec::MucTrack::brLastLayer },
    { 7, BesFieldNames::Rec::MucTrack::ecLastLayer },
    { 8, BesFieldNames::Rec::MucTrack::numHits },
    { 9, BesFieldNames::Rec::MucTrack::numLayers },
    { 10, BesFieldNames::Rec::MucTrack::maxHitsInLayer },
    { 11, BesFieldNames::Rec::MucTrack::depth },
    { 12, BesFieldNames::Rec::MucTrack::chi2 },
    { 13, BesFieldNames::Rec::MucTrack::dof },
    { 14, BesFieldNames::Rec::MucTrack::rms },
    { 15, BesFieldNames::Rec::MucTrack::xPos },
    { 16, BesFieldNames::Rec::MucTrack::yPos },
    { 17, BesFieldNames::Rec::MucTrack::zPos },
    { 18, BesFieldNames::Rec::MucTrack::xPosSigma },
    { 19, BesFieldNames::Rec::MucTrack::yPosSigma },
    { 20, BesFieldNames::Rec::MucTrack::zPosSigma },
    { 21, BesFieldNames::Rec::MucTrack::px },
    { 22, BesFieldNames::Rec::MucTrack::py },
    { 23, BesFieldNames::Rec::MucTrack::pz },
    { 24, BesFieldNames::Rec::MucTrack::distance },
    { 25, BesFieldNames::Rec::MucTrack::deltaPhi },
    { 26, BesFieldNames::Rec::MucTrack::hits },
    { 27, BesFieldNames::Rec::MucTrack::expHits },
    { 28, BesFieldNames::Rec::MucTrack::distHits },
    { 29, BesFieldNames::Rec::MucTrack::kalrechi2 },
    { 30, BesFieldNames::Rec::MucTrack::kaldof },
    { 31, BesFieldNames::Rec::MucTrack::kaldepth },
    { 32, BesFieldNames::Rec::MucTrack::kalbrLastLayer },
    { 33, BesFieldNames::Rec::MucTrack::kalecLastLayer },
};
class BesRFLeafRecMucTrack : public BesRootFieldLeaf<TRecTrackEvent, RecMucTrackRecord> {
  public:
    BesRFLeafRecMucTrack( TRecTrackEvent* obj )
        : BesRootFieldLeaf<TRecTrackEvent, RecMucTrackRecord>(
              obj, BesFieldNames::Rec::MucTrack::rpath, field_map_rec_muctrack ) {}

    void fill() {
        auto& trackId        = m_builder.content<0>().begin_list();
        auto& id             = m_builder.content<1>().begin_list();
        auto& status         = m_builder.content<2>().begin_list();
        auto& type           = m_builder.content<3>().begin_list();
        auto& startPart      = m_builder.content<4>().begin_list();
        auto& endPart        = m_builder.content<5>().begin_list();
        auto& brLastLayer    = m_builder.content<6>().begin_list();
        auto& ecLastLayer    = m_builder.content<7>().begin_list();
        auto& numHits        = m_builder.content<8>().begin_list();
        auto& numLayers      = m_builder.content<9>().begin_list();
        auto& maxHitsInLayer = m_builder.content<10>().begin_list();
        auto& depth          = m_builder.content<11>().begin_list();
        auto& chi2           = m_builder.content<12>().begin_list();
        auto& dof            = m_builder.content<13>().begin_list();
        auto& rms            = m_builder.content<14>().begin_list();
        auto& xPos           = m_builder.content<15>().begin_list();
        auto& yPos           = m_builder.content<16>().begin_list();
        auto& zPos           = m_builder.content<17>().begin_list();
        auto& xPosSigma      = m_builder.content<18>().begin_list();
        auto& yPosSigma      = m_builder.content<19>().begin_list();
        auto& zPosSigma      = m_builder.content<20>().begin_list();
        auto& px             = m_builder.content<21>().begin_list();
        auto& py             = m_builder.content<22>().begin_list();
        auto& pz             = m_builder.content<23>().begin_list();
        auto& distance       = m_builder.content<24>().begin_list();
        auto& deltaPhi       = m_builder.content<25>().begin_list();
        auto& hits           = m_builder.content<26>().begin_list();
        auto& expHits        = m_builder.content<27>().begin_list();
        auto& distHits       = m_builder.content<28>().begin_list();
        auto& kalrechi2      = m_builder.content<29>().begin_list();
        auto& kaldof         = m_builder.content<30>().begin_list();
        auto& kaldepth       = m_builder.content<31>().begin_list();
        auto& kalbrLastLayer = m_builder.content<32>().begin_list();
        auto& kalecLastLayer = m_builder.content<33>().begin_list();

        for ( auto tobj : *m_obj->getMucTrackCol() )
        {
            TRecMucTrack* obj = static_cast<TRecMucTrack*>( tobj );

            trackId.append( obj->trackId() );
            id.append( obj->id() );
            status.append( obj->status() );
            type.append( obj->type() );
            startPart.append( obj->startPart() );
            endPart.append( obj->endPart() );
            brLastLayer.append( obj->brLastLayer() );
            ecLastLayer.append( obj->ecLastLayer() );
            numHits.append( obj->numHits() );
            numLayers.append( obj->numLayers() );
            maxHitsInLayer.append( obj->maxHitsInLayer() );
            depth.append( obj->depth() );
            chi2.append( obj->chi2() );
            dof.append( obj->dof() );
            rms.append( obj->rms() );
            xPos.append( obj->xPos() );
            yPos.append( obj->yPos() );
            zPos.append( obj->zPos() );
            xPosSigma.append( obj->xPosSigma() );
            yPosSigma.append( obj->yPosSigma() );
            zPosSigma.append( obj->zPosSigma() );
            px.append( obj->px() );
            py.append( obj->py() );
            pz.append( obj->pz() );
            distance.append( obj->distance() );
            deltaPhi.append( obj->deltaPhi() );

            auto& subhits = hits.begin_list();
            for ( auto hit : obj->vecHits() ) subhits.append( hit );
            hits.end_list();

            auto& subexpHits = expHits.begin_list();
            for ( auto expHit : obj->expHits() ) subexpHits.append( expHit );
            expHits.end_list();

            auto& subdistHits = distHits.begin_list();
            for ( auto distHit : obj->distHits() ) subdistHits.append( distHit );
            distHits.end_list();

            kalrechi2.append( obj->kalRechi2() );
            kaldof.append( obj->kaldof() );
            kaldepth.append( obj->kaldepth() );
            kalbrLastLayer.append( obj->kalbrLastLayer() );
            kalecLastLayer.append( obj->kalecLastLayer() );
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
        m_builder.content<30>().end_list();
        m_builder.content<31>().end_list();
        m_builder.content<32>().end_list();
        m_builder.content<33>().end_list();
    }
};
