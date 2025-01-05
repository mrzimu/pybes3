#pragma once

#include <awkward/LayoutBuilder.h>

#include "RootEventData/TEvtRecEtaToGG.h"
#include "RootEventData/TEvtRecObject.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using EvtRecEtaToGGRecord = RecordBuilder<RaggedItemField<0, double>, // unconMass
                                          RaggedItemField<1, double>, // chi2
                                          RaggedItemField<2, double>, // hiPx
                                          RaggedItemField<3, double>, // hiPy
                                          RaggedItemField<4, double>, // hiPz
                                          RaggedItemField<5, double>, // hiE
                                          RaggedItemField<6, double>, // loPx
                                          RaggedItemField<7, double>, // loPy
                                          RaggedItemField<8, double>, // loPz
                                          RaggedItemField<9, double>, // loE
                                          RaggedItemField<10, int>,   // hiEnGamma
                                          RaggedItemField<11, int>    // loEnGamma
                                          >;

const FieldMap field_map_recobj_eta = { { 0, BesFieldNames::EvtRec::EtaToGG::unconMass },
                                        { 1, BesFieldNames::EvtRec::EtaToGG::chi2 },
                                        { 2, BesFieldNames::EvtRec::EtaToGG::hiPx },
                                        { 3, BesFieldNames::EvtRec::EtaToGG::hiPy },
                                        { 4, BesFieldNames::EvtRec::EtaToGG::hiPz },
                                        { 5, BesFieldNames::EvtRec::EtaToGG::hiE },
                                        { 6, BesFieldNames::EvtRec::EtaToGG::loPx },
                                        { 7, BesFieldNames::EvtRec::EtaToGG::loPy },
                                        { 8, BesFieldNames::EvtRec::EtaToGG::loPz },
                                        { 9, BesFieldNames::EvtRec::EtaToGG::loE },
                                        { 10, BesFieldNames::EvtRec::EtaToGG::hiEnGamma },
                                        { 11, BesFieldNames::EvtRec::EtaToGG::loEnGamma } };

class BesRFLeafEvtRecEtaToGG : public BesRootFieldLeaf<TEvtRecObject, EvtRecEtaToGGRecord> {
  public:
    BesRFLeafEvtRecEtaToGG( TEvtRecObject* obj )
        : BesRootFieldLeaf<TEvtRecObject, EvtRecEtaToGGRecord>(
              obj, BesFieldNames::EvtRec::EtaToGG::rpath, field_map_recobj_eta ) {}

    void fill() {
        auto& unconMass = m_builder.content<0>().begin_list();
        auto& chi2      = m_builder.content<1>().begin_list();
        auto& hiPx      = m_builder.content<2>().begin_list();
        auto& hiPy      = m_builder.content<3>().begin_list();
        auto& hiPz      = m_builder.content<4>().begin_list();
        auto& hiE       = m_builder.content<5>().begin_list();
        auto& loPx      = m_builder.content<6>().begin_list();
        auto& loPy      = m_builder.content<7>().begin_list();
        auto& loPz      = m_builder.content<8>().begin_list();
        auto& loE       = m_builder.content<9>().begin_list();
        auto& hiEnGamma = m_builder.content<10>().begin_list();
        auto& loEnGamma = m_builder.content<11>().begin_list();

        for ( auto* tobj : ( *m_obj->getEvtRecEtaToGGCol() ) )
        {
            TEvtRecEtaToGG* obj = static_cast<TEvtRecEtaToGG*>( tobj );

            unconMass.append( obj->unconMass() );
            chi2.append( obj->chisq() );
            hiPx.append( obj->hiPxfit() );
            hiPy.append( obj->hiPyfit() );
            hiPz.append( obj->hiPzfit() );
            hiE.append( obj->hiPefit() );
            loPx.append( obj->loPxfit() );
            loPy.append( obj->loPyfit() );
            loPz.append( obj->loPzfit() );
            loE.append( obj->loPefit() );
            hiEnGamma.append( obj->hiEnGamma() );
            loEnGamma.append( obj->loEnGamma() );
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
    }
};