#include "HepPDT/ParticleData.hh"
#include "HepPDT/ParticleDataTable.hh"
#include <CLHEP/Random/RandFlat.h>
#include <CLHEP/Random/RandomEngine.h>
#include <CLHEP/Vector/LorentzVector.h>
#include <Gaudi/Functional/Transformer.h>
#include <Gaudi/Property.h>
#include <GaudiKernel/IPartPropSvc.h>
#include <GaudiKernel/SmartIF.h>
#include <GaudiKernel/StatusCode.h>
#include <HepMC/GenParticle.h>
#include <HepMC/GenVertex.h>
#include <HepMC/SimpleVector.h>
#include <cmath>

#include "BesRndmGenSvc/IBesRndmGenSvc.h"
#include "GeneratorObject/McGenEvent.h"

using Gaudi::Functional::Transformer;
class Pybes3ParticleGun : public Transformer<McGenEventCol( const EventContext& )> {
  public:
    Pybes3ParticleGun( const std::string& name, ISvcLocator* pSvcLocator )
        : Transformer( name, pSvcLocator, { "McGenEventLocation", "/Event/Gen" } ) {}

    StatusCode initialize() override {
        info() << "Initializing Pybes3ParticleGun" << endmsg;

        StatusCode sc = Transformer::initialize();
        if ( !sc.isSuccess() ) return sc;

        // check args
        if ( m_parts.size() == 0 )
        {
            error() << "No PDG codes specified" << endmsg;
            return StatusCode::FAILURE;
        }

        if ( m_p_range.size() != 2 )
        {
            error() << "Momentum range must be of size 2" << endmsg;
            return StatusCode::FAILURE;
        }

        if ( m_costheta_range.size() != 2 )
        {
            error() << "Cos(theta) range must be of size 2" << endmsg;
            return StatusCode::FAILURE;
        }

        if ( m_phi_range.size() != 2 )
        {
            error() << "Phi range must be of size 2" << endmsg;
            return StatusCode::FAILURE;
        }

        // set ranges
        m_p1        = m_p_range[0];
        m_p2        = m_p_range[1];
        m_costheta1 = m_costheta_range[0];
        m_costheta2 = m_costheta_range[1];
        m_phi1      = m_phi_range[0];
        m_phi2      = m_phi_range[1];

        if ( m_sample_mode == 1 && m_costheta1 < 0 ) m_costheta1 = 0.0;
        if ( m_p2 <= m_p1 ) m_p2 = m_p1;
        if ( m_costheta2 <= m_costheta1 ) m_costheta2 = m_costheta1;
        if ( m_phi2 <= m_phi1 ) m_phi2 = m_phi1;

        // retrieve random enging
        m_rndm_svc = service<IBesRndmGenSvc>( "BesRndmGenSvc" );
        if ( !m_rndm_svc )
        {
            error() << "Could not get random number service" << endmsg;
            return StatusCode::FAILURE;
        }

        m_rndm_engine = m_rndm_svc->GetEngine( "Pybes3ParticleGun" );
        if ( !m_rndm_engine )
        {
            error() << "Could not get random engine" << endmsg;
            return StatusCode::FAILURE;
        }

        // retrieve particle data table
        auto part_prop_svc = service<IPartPropSvc>( "PartPropSvc" );
        if ( !part_prop_svc )
        {
            error() << "Could not get Particle Properties Service" << endmsg;
            return StatusCode::FAILURE;
        }

        m_particle_table = part_prop_svc->PDT();
        if ( !m_particle_table )
        {
            error() << "Could not get Particle Data Table" << endmsg;
            return StatusCode::FAILURE;
        }

        return StatusCode::SUCCESS;
    }

    McGenEventCol operator()( const EventContext& ctx ) const override {
        GenEvent* evt = new GenEvent( 1, 1 );

        // make vertex (0, 0, 0, 0)
        GenVertex* vtx = new GenVertex();
        evt->add_vertex( vtx );

        // sample particles
        for ( auto pdg_code : m_parts.value() )
        {
            const HepPDT::ParticleData* part =
                m_particle_table->particle( HepPDT::ParticleID( abs( pdg_code ) ) );

            double mass = part ? part->mass().value() : 0.0;

            // sample momentum
            double p = CLHEP::RandFlat::shoot( m_rndm_engine, m_p1, m_p2 );
            double cos_theta =
                CLHEP::RandFlat::shoot( m_rndm_engine, m_costheta1, m_costheta2 );

            if ( m_sample_mode == 1 )
                cos_theta *=
                    ( CLHEP::RandFlat::shoot( m_rndm_engine, 0.0, 1.0 ) > 0.5 ? 1.0 : -1.0 );

            double phi = CLHEP::RandFlat::shoot( m_rndm_engine, m_phi1, m_phi2 );

            // calculate px, py, pz
            double sin_theta = sqrt( 1.0 - cos_theta * cos_theta );
            double pt        = p * sin_theta;

            double px = pt * cos( phi );
            double py = pt * sin( phi );
            double pz = p * cos_theta;

            CLHEP::HepLorentzVector p4;
            p4.setVectM( CLHEP::Hep3Vector( px, py, pz ), mass );

            vtx->add_particle_out( new GenParticle( p4, pdg_code, 1 ) );
        }

        std::vector<long> seeds{ m_rndm_engine->getSeeds()[0], m_rndm_engine->getSeeds()[1] };
        evt->set_random_states( seeds );

        // add event to collection
        McGenEventCol mc_col;
        mc_col.push_back( new McGenEvent( evt ) );
        return mc_col;
    };

  private:
    IntegerArrayProperty m_parts{
        this, "PdgList", { 11, -11 }, "List of PDG codes to be generated" };

    IntegerProperty m_sample_mode{
        this, "Mode", 0, "Sampling mode: 0 for p-costheta-phi, 1 for p-|costheta|-phi" };

    DoubleArrayProperty m_p_range{
        this, "PRange", { 0.1, 1.8 }, "Range of momentum to be sampled" };

    DoubleArrayProperty m_costheta_range{
        this, "CosthetaRange", { -1.0, 1.0 }, "Range of cos(theta) to be sampled" };

    DoubleArrayProperty m_phi_range{
        this, "PhiRange", { -M_PI, M_PI }, "Range of phi to be sampled" };

    SmartIF<IBesRndmGenSvc> m_rndm_svc;

    CLHEP::HepRandomEngine* m_rndm_engine{ nullptr };
    HepPDT::ParticleDataTable* m_particle_table{ nullptr };

    double m_p1{ 0.0 };
    double m_p2{ 0.0 };
    double m_costheta1{ 0.0 };
    double m_costheta2{ 0.0 };
    double m_phi1{ 0.0 };
    double m_phi2{ 0.0 };
};

DECLARE_COMPONENT( Pybes3ParticleGun )
