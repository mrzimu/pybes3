#pragma once

#include "RootEventData/TMcEvent.h"
#include "RootEventData/TMcParticle.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using McParticleRecord = RecordBuilder<RaggedItemField<0, int>,          // PDGId
                                       RaggedItemField<1, int>,          // trackIndex
                                       RaggedItemField<2, int>,          // vertexIndex0
                                       RaggedItemField<3, int>,          // vertexIndex1
                                       RaggedItemField<4, unsigned int>, // statusFlags
                                       RaggedItemField<5, double>,       // motherIndex
                                       RaggedRaggedField<6, int>,        // daughterIndexes
                                       RaggedItemField<7, double>,       // xInit
                                       RaggedItemField<8, double>,       // yInit
                                       RaggedItemField<9, double>,       // zInit
                                       RaggedItemField<10, double>,      // tInit
                                       RaggedItemField<11, double>,      // xFinal
                                       RaggedItemField<12, double>,      // yFinal
                                       RaggedItemField<13, double>,      // zFinal
                                       RaggedItemField<14, double>,      // tFinal
                                       RaggedItemField<15, double>,      // pxInit
                                       RaggedItemField<16, double>,      // pyInit
                                       RaggedItemField<17, double>,      // pzInit
                                       RaggedItemField<18, double>       // eInit
                                       >;

const FieldMap field_map_mc_particle = { { 0, BesFieldNames::Mc::McParticle::PDGId },
                                         { 1, BesFieldNames::Mc::McParticle::trackIndex },
                                         { 2, BesFieldNames::Mc::McParticle::vertexIndex0 },
                                         { 3, BesFieldNames::Mc::McParticle::vertexIndex1 },
                                         { 4, BesFieldNames::Mc::McParticle::statusFlags },
                                         { 5, BesFieldNames::Mc::McParticle::motherIndex },
                                         { 6, BesFieldNames::Mc::McParticle::daughterIndexes },
                                         { 7, BesFieldNames::Mc::McParticle::xInit },
                                         { 8, BesFieldNames::Mc::McParticle::yInit },
                                         { 9, BesFieldNames::Mc::McParticle::zInit },
                                         { 10, BesFieldNames::Mc::McParticle::tInit },
                                         { 11, BesFieldNames::Mc::McParticle::xFinal },
                                         { 12, BesFieldNames::Mc::McParticle::yFinal },
                                         { 13, BesFieldNames::Mc::McParticle::zFinal },
                                         { 14, BesFieldNames::Mc::McParticle::tFinal },
                                         { 15, BesFieldNames::Mc::McParticle::pxInit },
                                         { 16, BesFieldNames::Mc::McParticle::pyInit },
                                         { 17, BesFieldNames::Mc::McParticle::pzInit },
                                         { 18, BesFieldNames::Mc::McParticle::eInit } };

class BesRFLeafMcParticle : public BesRootFieldLeaf<TMcEvent, McParticleRecord> {
  public:
    BesRFLeafMcParticle( TMcEvent* obj )
        : BesRootFieldLeaf<TMcEvent, McParticleRecord>(
              obj, BesFieldNames::Mc::McParticle::rpath, field_map_mc_particle ) {}

    void init() { m_builder.set_fields( field_map_mc_particle ); }

    void fill() {
        auto& PDGId           = m_builder.content<0>().begin_list();
        auto& trackIndex      = m_builder.content<1>().begin_list();
        auto& vertexIndex0    = m_builder.content<2>().begin_list();
        auto& vertexIndex1    = m_builder.content<3>().begin_list();
        auto& statusFlags     = m_builder.content<4>().begin_list();
        auto& motherIndex     = m_builder.content<5>().begin_list();
        auto& daughterIndexes = m_builder.content<6>().begin_list();
        auto& xInit           = m_builder.content<7>().begin_list();
        auto& yInit           = m_builder.content<8>().begin_list();
        auto& zInit           = m_builder.content<9>().begin_list();
        auto& tInit           = m_builder.content<10>().begin_list();
        auto& xFinal          = m_builder.content<11>().begin_list();
        auto& yFinal          = m_builder.content<12>().begin_list();
        auto& zFinal          = m_builder.content<13>().begin_list();
        auto& tFinal          = m_builder.content<14>().begin_list();
        auto& pxInit          = m_builder.content<15>().begin_list();
        auto& pyInit          = m_builder.content<16>().begin_list();
        auto& pzInit          = m_builder.content<17>().begin_list();
        auto& eInit           = m_builder.content<18>().begin_list();

        for ( auto tobj : ( *m_obj->getMcParticleCol() ) )
        {
            TMcParticle* particle = static_cast<TMcParticle*>( tobj );

            PDGId.append( particle->getParticleID() );
            trackIndex.append( particle->getTrackIndex() );
            vertexIndex0.append( particle->getVertexIndex0() );
            vertexIndex1.append( particle->getVertexIndex1() );
            statusFlags.append( particle->getStatusFlags() );
            motherIndex.append( particle->getMother() );

            auto& subdaughterIndexes = daughterIndexes.begin_list();
            for ( const auto daughter : particle->getDaughters() )
            { subdaughterIndexes.append( daughter ); }
            daughterIndexes.end_list();

            xInit.append( particle->getInitialPositionX() );
            yInit.append( particle->getInitialPositionY() );
            zInit.append( particle->getInitialPositionZ() );
            tInit.append( particle->getInitialPositionT() );
            xFinal.append( particle->getFinalPositionX() );
            yFinal.append( particle->getFinalPositionY() );
            zFinal.append( particle->getFinalPositionZ() );
            tFinal.append( particle->getFinalPositionT() );
            pxInit.append( particle->getInitialMomentumX() );
            pyInit.append( particle->getInitialMomentumY() );
            pzInit.append( particle->getInitialMomentumZ() );
            eInit.append( particle->getInitialMomentumE() );
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
    }
};