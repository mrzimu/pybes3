#pragma once

#include "RootEventData/TRecEmcHit.h"
#include "RootEventData/TRecTrackEvent.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using RecEmcHitRecord = RecordBuilder<RaggedItemField<0, int>,    // cellId
                                      RaggedItemField<1, double>, // energy
                                      RaggedItemField<2, double>  // time
                                      >;

const FieldMap field_map_rec_emchit = { { 0, BesFieldNames::Rec::EmcHit::cellId },
                                        { 1, BesFieldNames::Rec::EmcHit::energy },
                                        { 2, BesFieldNames::Rec::EmcHit::time } };

class BesRFLeafRecEmcHit : public BesRootFieldLeaf<TRecTrackEvent, RecEmcHitRecord> {
  public:
    BesRFLeafRecEmcHit( TRecTrackEvent* obj )
        : BesRootFieldLeaf<TRecTrackEvent, RecEmcHitRecord>(
              obj, BesFieldNames::Rec::EmcHit::rpath, field_map_rec_emchit ) {}

    void fill() {
        auto& cellId = m_builder.content<0>().begin_list();
        auto& energy = m_builder.content<1>().begin_list();
        auto& time   = m_builder.content<2>().begin_list();

        for ( auto tobj : *m_obj->getTofTrackCol() )
        {
            TRecEmcHit* obj = static_cast<TRecEmcHit*>( tobj );

            cellId.append( obj->cellId() );
            energy.append( obj->energy() );
            time.append( obj->time() );
        }

        m_builder.content<0>().end_list();
        m_builder.content<1>().end_list();
        m_builder.content<2>().end_list();
    }
};