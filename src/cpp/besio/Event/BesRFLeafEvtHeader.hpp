#pragma once

#include <awkward/LayoutBuilder.h>

#include "RootEventData/TEvtHeader.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using EvtHeaderRecord = RecordBuilder<SimpleItemField<0, int>, // runNo
                                      SimpleItemField<1, int>, // evtNo
                                      SimpleItemField<2, int>, // time
                                      SimpleItemField<3, int>, // evtTag
                                      SimpleItemField<4, int>, // flag1
                                      SimpleItemField<5, int>, // flag2
                                      SimpleItemField<6, int>, // etsT1
                                      SimpleItemField<7, int>  // etsT2
                                      >;

const FieldMap field_map_evtheader = {
    { 0, BesFieldNames::EvtHeader::runNo }, { 1, BesFieldNames::EvtHeader::evtNo },
    { 2, BesFieldNames::EvtHeader::time },  { 3, BesFieldNames::EvtHeader::tag },
    { 4, BesFieldNames::EvtHeader::flag1 }, { 5, BesFieldNames::EvtHeader::flag2 },
    { 6, BesFieldNames::EvtHeader::etsT1 }, { 7, BesFieldNames::EvtHeader::etsT2 } };

class BesRFLeafEvtHeader : public BesRootFieldLeaf<TEvtHeader, EvtHeaderRecord> {
  public:
    BesRFLeafEvtHeader( TEvtHeader* obj )
        : BesRootFieldLeaf<TEvtHeader, EvtHeaderRecord>( obj, BesFieldNames::EvtHeader::rpath,
                                                         field_map_evtheader ) {}

    void fill() {
        m_builder.content<0>().append( m_obj->getRunId() );
        m_builder.content<1>().append( m_obj->getEventId() );
        m_builder.content<2>().append( m_obj->time() );
        m_builder.content<3>().append( m_obj->getEventTag() );
        m_builder.content<4>().append( m_obj->getFlag1() );
        m_builder.content<5>().append( m_obj->getFlag2() );
        m_builder.content<6>().append( m_obj->getEtsT1() );
        m_builder.content<7>().append( m_obj->getEtsT2() );
    }
};