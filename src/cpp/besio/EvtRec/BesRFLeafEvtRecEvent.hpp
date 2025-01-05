#pragma once

#include <awkward/LayoutBuilder.h>

#include "RootEventData/TEvtRecObject.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using EvtRecEventRecord = RecordBuilder<SimpleItemField<0, int>, // nTotal
                                        SimpleItemField<1, int>, // nCharge
                                        SimpleItemField<2, int>, // nNeutral
                                        SimpleItemField<3, int>, // nVEE
                                        SimpleItemField<4, int>, // npi0
                                        SimpleItemField<5, int>, // nEta2gg
                                        SimpleItemField<6, int>  // nDTag
                                        >;

const FieldMap field_map_recobj_evt = {
    { 0, BesFieldNames::EvtRec::Evt::nTotal },   { 1, BesFieldNames::EvtRec::Evt::nCharged },
    { 2, BesFieldNames::EvtRec::Evt::nNeutral }, { 3, BesFieldNames::EvtRec::Evt::nVee },
    { 4, BesFieldNames::EvtRec::Evt::nPi0 },     { 5, BesFieldNames::EvtRec::Evt::nEta2gg },
    { 6, BesFieldNames::EvtRec::Evt::nDTag } };

class BesRFLeafEvtRecEvent : public BesRootFieldLeaf<TEvtRecObject, EvtRecEventRecord> {
  public:
    BesRFLeafEvtRecEvent( TEvtRecObject* obj )
        : BesRootFieldLeaf<TEvtRecObject, EvtRecEventRecord>(
              obj, BesFieldNames::EvtRec::Evt::rpath, field_map_recobj_evt ) {}

    void fill() {
        m_builder.content<0>().append( m_obj->getEvtRecEvent()->totalTracks() );
        m_builder.content<1>().append( m_obj->getEvtRecEvent()->totalCharged() );
        m_builder.content<2>().append( m_obj->getEvtRecEvent()->totalNeutral() );
        m_builder.content<3>().append( m_obj->getEvtRecEvent()->numberOfVee() );
        m_builder.content<4>().append( m_obj->getEvtRecEvent()->numberOfPi0() );
        m_builder.content<5>().append( m_obj->getEvtRecEvent()->numberOfEtaToGG() );
        m_builder.content<6>().append( m_obj->getEvtRecEvent()->numberOfDTag() );
    }
};