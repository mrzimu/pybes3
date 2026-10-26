#include <GaudiKernel/Algorithm.h>
#include <GaudiKernel/NTuple.h>
#include <GaudiKernel/SmartDataPtr.h>

#include <McTruth/McParticle.h>

using NTuple::Array;
using NTuple::Item;

class ExportParticleStatusAlg : public Algorithm {
  private:
    NTuple::Tuple* m_tuple;
    Item<int> m_index;
    Array<uint32_t> m_status;
    Array<bool> m_is_primary;
    Array<bool> m_is_leaf;
    Array<bool> m_decay_from_generator;
    Array<bool> m_decay_in_flight;

  public:
    using Algorithm::Algorithm;

    StatusCode initialize() override {
        NTuplePtr nt( ntupleSvc(), "FILE1/particle_status" );
        if ( nt ) m_tuple = nt;
        else
        {
            m_tuple = ntupleSvc()->book( "FILE1/particle_status", CLID_ColumnWiseTuple,
                                         "Particle status" );
            if ( !m_tuple )
            {
                error() << "Cannot book ntuple for Particle status" << endmsg;
                return StatusCode::FAILURE;
            }

            m_tuple->addItem( "index", m_index, 0, 100 ).ignore();
            m_tuple->addIndexedItem( "status", m_index, m_status ).ignore();
            m_tuple->addIndexedItem( "is_primary", m_index, m_is_primary ).ignore();
            m_tuple->addIndexedItem( "is_leaf", m_index, m_is_leaf ).ignore();
            m_tuple->addIndexedItem( "decay_from_generator", m_index, m_decay_from_generator )
                .ignore();
            m_tuple->addIndexedItem( "decay_in_flight", m_index, m_decay_in_flight ).ignore();
        }

        return StatusCode::SUCCESS;
    }

    StatusCode execute() override {
        SmartDataPtr<Event::McParticleCol> particle_col( eventSvc(),
                                                         "/Event/MC/McParticleCol" );
        if ( !particle_col ) return StatusCode::FAILURE;

        m_index = 0;
        for ( const auto& particle : *particle_col )
        {
            m_status[m_index]               = particle->statusFlags();
            m_is_primary[m_index]           = particle->primaryParticle();
            m_is_leaf[m_index]              = particle->leafParticle();
            m_decay_from_generator[m_index] = particle->decayFromGenerator();
            m_decay_in_flight[m_index]      = particle->decayInFlight();
            m_index++;
        }

        m_tuple->write().ignore();
        return StatusCode::SUCCESS;
    }
};

DECLARE_COMPONENT( ExportParticleStatusAlg )
