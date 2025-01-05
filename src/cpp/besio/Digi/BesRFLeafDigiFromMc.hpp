#pragma once

#include <awkward/LayoutBuilder.h>

#include "RootEventData/TDigiEvent.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using DigiFromMcRecord = RecordBuilder<SimpleItemField<0, bool>>; // fromMc

const FieldMap field_map_digi_from_mc = { { 0, BesFieldNames::Digi::FromMc::fromMc } };

class BesRFLeafDigiFromMc : public BesRootFieldLeaf<TDigiEvent, DigiFromMcRecord> {
  public:
    BesRFLeafDigiFromMc( TDigiEvent* obj )
        : BesRootFieldLeaf<TDigiEvent, DigiFromMcRecord>(
              obj, BesFieldNames::Digi::FromMc::rpath, field_map_digi_from_mc ) {}

    void fill() {
        auto& fromMc = m_builder.content<0>();
        fromMc.append( m_obj->getFromMc() );
    }
};