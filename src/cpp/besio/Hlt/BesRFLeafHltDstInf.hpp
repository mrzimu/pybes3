#pragma once

#include "RootEventData/TDstHltInf.h"
#include "RootEventData/THltEvent.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using HltDstInfRecord = RecordBuilder<SimpleItemField<0, int>,    // evtType
                                      SimpleItemField<1, int>,    // algProcess
                                      SimpleItemField<2, int>,    // criTable
                                      SimpleItemField<3, int>,    // verNumber
                                      SimpleItemField<4, double>, // eTotal
                                      SimpleItemField<5, int>,    // subNumber
                                      SimpleItemField<6, int>     // conNumber
                                      >;

const FieldMap field_map_hlt_dstinf = {
    { 0, BesFieldNames::Hlt::DstInf::evtType },
    { 1, BesFieldNames::Hlt::DstInf::algProcess },
    { 2, BesFieldNames::Hlt::DstInf::criTable },
    { 3, BesFieldNames::Hlt::DstInf::verNumber },
    { 4, BesFieldNames::Hlt::DstInf::eTotal },
    { 5, BesFieldNames::Hlt::DstInf::subNumber },
    { 6, BesFieldNames::Hlt::DstInf::conNumber },
};
class BesRFLeafHltDstInf : public BesRootFieldLeaf<THltEvent, HltDstInfRecord> {
  public:
    BesRFLeafHltDstInf( THltEvent* obj )
        : BesRootFieldLeaf<THltEvent, HltDstInfRecord>( obj, BesFieldNames::Hlt::DstInf::rpath,
                                                        field_map_hlt_dstinf ) {}

    void fill() {
        const TDstHltInf* obj = m_obj->getDstHltInf();

        m_builder.content<0>().append( obj->getEventType() );
        m_builder.content<1>().append( obj->getAlgProcess() );
        m_builder.content<2>().append( obj->getCriteriaTable() );
        m_builder.content<3>().append( obj->getVersion() );
        m_builder.content<4>().append( obj->getTotalEnergy() );
        m_builder.content<5>().append( obj->getNumber() );
        m_builder.content<6>().append( obj->getNCON() );
    }
};
