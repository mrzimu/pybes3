#pragma once

#include "RootEventData/TRecEmcCluster.h"
#include "RootEventData/TRecTrackEvent.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using RecEmcClusterRecord = RecordBuilder<RaggedItemField<0, int>,   // clusterId
                                          RaggedRaggedField<1, int>, // hits
                                          RaggedRaggedField<2, int>, // seeds
                                          RaggedRaggedField<3, int>  // showers
                                          >;

const FieldMap field_map_rec_emccluster = { { 0, BesFieldNames::Rec::EmcCluster::clusterId },
                                            { 1, BesFieldNames::Rec::EmcCluster::hits },
                                            { 2, BesFieldNames::Rec::EmcCluster::seeds },
                                            { 3, BesFieldNames::Rec::EmcCluster::showers } };

class BesRFLeafRecEmcCluster : public BesRootFieldLeaf<TRecTrackEvent, RecEmcClusterRecord> {
  public:
    BesRFLeafRecEmcCluster( TRecTrackEvent* obj )
        : BesRootFieldLeaf<TRecTrackEvent, RecEmcClusterRecord>(
              obj, BesFieldNames::Rec::EmcCluster::rpath, field_map_rec_emccluster ) {}

    void fill() {
        auto& clusterId = m_builder.content<0>().begin_list();
        auto& hits      = m_builder.content<1>().begin_list();
        auto& seeds     = m_builder.content<2>().begin_list();
        auto& showers   = m_builder.content<3>().begin_list();

        for ( auto tobj : *m_obj->getTofTrackCol() )
        {
            TRecEmcCluster* obj = static_cast<TRecEmcCluster*>( tobj );

            clusterId.append( obj->clusterId() );

            auto& subhits = hits.begin_list();
            for ( auto hit : obj->vecHits() ) subhits.append( hit );
            hits.end_list();

            auto& subseeds = seeds.begin_list();
            for ( auto seed : obj->vecSeeds() ) subseeds.append( seed );
            seeds.end_list();

            auto& subshowers = showers.begin_list();
            for ( auto shower : obj->vecShowers() ) subshowers.append( shower );
            showers.end_list();
        }

        m_builder.content<0>().end_list();
        m_builder.content<1>().end_list();
        m_builder.content<2>().end_list();
        m_builder.content<3>().end_list();
    }
};