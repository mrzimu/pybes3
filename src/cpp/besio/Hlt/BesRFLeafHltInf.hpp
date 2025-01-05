#pragma once

#include "RootEventData/THltEvent.h"
#include "RootEventData/THltInf.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using HltInfRecord = RecordBuilder<SimpleItemField<0, int>,    // evtType
                                   SimpleItemField<1, int>,    // algProcess
                                   SimpleItemField<2, int>,    // criTable
                                   SimpleItemField<3, int>,    // verNumber
                                   SimpleItemField<4, double>, // eTotal
                                   SimpleItemField<5, int>,    // subNumber
                                   SimpleItemField<6, int>,    // conNumber
                                   RaggedItemField<7, int>,    // mdcData
                                   RaggedItemField<8, int>,    // tofData
                                   RaggedItemField<9, int>,    // emcData
                                   RaggedItemField<10, int>,   // mucData
                                   RaggedItemField<11, int>    // conData
                                   >;

const FieldMap field_map_hlt_inf = {
    { 0, BesFieldNames::Hlt::Inf::evtType },   { 1, BesFieldNames::Hlt::Inf::algProcess },
    { 2, BesFieldNames::Hlt::Inf::criTable },  { 3, BesFieldNames::Hlt::Inf::verNumber },
    { 4, BesFieldNames::Hlt::Inf::eTotal },    { 5, BesFieldNames::Hlt::Inf::subNumber },
    { 6, BesFieldNames::Hlt::Inf::conNumber }, { 7, BesFieldNames::Hlt::Inf::mdcData },
    { 8, BesFieldNames::Hlt::Inf::tofData },   { 9, BesFieldNames::Hlt::Inf::emcData },
    { 10, BesFieldNames::Hlt::Inf::mucData },  { 11, BesFieldNames::Hlt::Inf::conData },
};
class BesRFLeafHltInf : public BesRootFieldLeaf<THltEvent, HltInfRecord> {
  public:
    BesRFLeafHltInf( THltEvent* obj )
        : BesRootFieldLeaf<THltEvent, HltInfRecord>( obj, BesFieldNames::Hlt::Inf::rpath,
                                                     field_map_hlt_inf ) {}

    void fill() {
        const THltInf* obj = m_obj->getHltInf();

        m_builder.content<0>().append( obj->getEventType() );
        m_builder.content<1>().append( obj->getAlgProcess() );
        m_builder.content<2>().append( obj->getCriteriaTable() );
        m_builder.content<3>().append( obj->getVersion() );
        m_builder.content<4>().append( obj->getTotalEnergy() );
        m_builder.content<5>().append( obj->getNumber() );
        m_builder.content<6>().append( obj->getNCON() );

        auto& mdcData = m_builder.content<7>().begin_list();
        for ( auto i : obj->getMdcData() ) { mdcData.append( i ); }
        m_builder.content<7>().end_list();

        auto& tofData = m_builder.content<8>().begin_list();
        for ( auto i : obj->getTofData() ) { tofData.append( i ); }
        m_builder.content<8>().end_list();

        auto& emcData = m_builder.content<9>().begin_list();
        for ( auto i : obj->getEmcData() ) { emcData.append( i ); }
        m_builder.content<9>().end_list();

        auto& mucData = m_builder.content<10>().begin_list();
        for ( auto i : obj->getMucData() ) { mucData.append( i ); }
        m_builder.content<10>().end_list();

        auto& conData = m_builder.content<11>().begin_list();
        for ( auto i : obj->getConData() ) { conData.append( i ); }
        m_builder.content<11>().end_list();
    }
};
