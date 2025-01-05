#include <TFile.h>
#include <TROOT.h>
#include <TTree.h>
#include <pybind11/pytypes.h>
#include <pyerrors.h>
#include <regex>
#include <string>
#include <vector>

#include "RootEventData/TEvtHeader.h"

#include "BesEventModel.hh"
#include "BesEventReader.hh"
#include "Digi/BesRFLeafDigiEmc.hpp"
#include "Digi/BesRFLeafDigiFromMc.hpp"
#include "Digi/BesRFLeafDigiLumi.hpp"
#include "Digi/BesRFLeafDigiMdc.hpp"
#include "Digi/BesRFLeafDigiMuc.hpp"
#include "Digi/BesRFLeafDigiTof.hpp"
#include "Dst/BesRFLeafDstDedx.hpp"
#include "Dst/BesRFLeafDstEmc.hpp"
#include "Dst/BesRFLeafDstExt.hpp"
#include "Dst/BesRFLeafDstMdc.hpp"
#include "Dst/BesRFLeafDstMuc.hpp"
#include "Dst/BesRFLeafDstTof.hpp"
#include "Event/BesRFLeafEvtHeader.hpp"
#include "EvtRec/BesRFLeafEvtRecDTag.hpp"
#include "EvtRec/BesRFLeafEvtRecEtaToGG.hpp"
#include "EvtRec/BesRFLeafEvtRecEvent.hpp"
#include "EvtRec/BesRFLeafEvtRecPi0.hpp"
#include "EvtRec/BesRFLeafEvtRecPrimaryVertex.hpp"
#include "EvtRec/BesRFLeafEvtRecTracks.hpp"
#include "EvtRec/BesRFLeafEvtRecVeeVertex.hpp"
#include "Hlt/BesRFLeafHltDstInf.hpp"
#include "Hlt/BesRFLeafHltInf.hpp"
#include "Hlt/BesRFLeafHltRaw.hpp"
#include "Mc/BesRFLeafMcEmc.hpp"
#include "Mc/BesRFLeafMcMdc.hpp"
#include "Mc/BesRFLeafMcMuc.hpp"
#include "Mc/BesRFLeafMcParticle.hpp"
#include "Mc/BesRFLeafMcTof.hpp"
#include "Rec/BesRFLeafRecEmcCluster.hpp"
#include "Rec/BesRFLeafRecEmcHit.hpp"
#include "Rec/BesRFLeafRecEmcShower.hpp"
#include "Rec/BesRFLeafRecEvTime.hpp"
#include "Rec/BesRFLeafRecExtTrack.hpp"
#include "Rec/BesRFLeafRecMdcDedx.hpp"
#include "Rec/BesRFLeafRecMdcDedxHit.hpp"
#include "Rec/BesRFLeafRecMdcHit.hpp"
#include "Rec/BesRFLeafRecMdcKalHelixSeg.hpp"
#include "Rec/BesRFLeafRecMdcKalTrack.hpp"
#include "Rec/BesRFLeafRecMdcTrack.hpp"
#include "Rec/BesRFLeafRecMucTrack.hpp"
#include "Rec/BesRFLeafRecTofTrack.hpp"
#include "Rec/BesRFLeafRecZdd.hpp"
#include "Trig/BesRFLeafTrigData.hpp"

BesEventReader::~BesEventReader() {
    if ( m_evt_header ) delete m_evt_header;
    if ( m_evt_mc ) delete m_evt_mc;
    if ( m_evt_digi ) delete m_evt_digi;
    if ( m_evt_dst ) delete m_evt_dst;
    if ( m_evt_rec ) delete m_evt_rec;
}

BesEventReader::BesEventReader( const std::vector<std::string> filepaths )
    : m_chain( "Event", "Event" ) {

    ROOT::EnableThreadSafety();

    /* Open file */
    for ( const auto& filepath : filepaths ) m_chain.Add( filepath.c_str() );

    m_entries = m_chain.GetEntries();

    /* Set branch addresses */
    if ( m_chain.GetBranch( "TEvtHeader" ) )
    {
        m_evt_header = new TEvtHeader();
        m_chain.SetBranchAddress( "TEvtHeader", &m_evt_header );
        m_branch_names.insert( "TEvtHeader" );

        m_fields[BesFieldNames::EvtHeader::rpath] =
            std::make_unique<BesRFLeafEvtHeader>( BesRFLeafEvtHeader( m_evt_header ) );
    }

    if ( m_chain.GetBranch( "TEvtRecObject" ) )
    {
        m_evt_rec = new TEvtRecObject();
        m_chain.SetBranchAddress( "TEvtRecObject", &m_evt_rec );
        m_branch_names.insert( "TEvtRecObject" );

        m_fields[BesFieldNames::EvtRec::Evt::rpath] =
            std::make_unique<BesRFLeafEvtRecEvent>( BesRFLeafEvtRecEvent( m_evt_rec ) );

        m_fields[BesFieldNames::EvtRec::Trk::rpath] =
            std::make_unique<BesRFLeafEvtRecTracks>( BesRFLeafEvtRecTracks( m_evt_rec ) );

        m_fields[BesFieldNames::EvtRec::Pi0::rpath] =
            std::make_unique<BesRFLeafEvtRecPi0>( BesRFLeafEvtRecPi0( m_evt_rec ) );

        m_fields[BesFieldNames::EvtRec::EtaToGG::rpath] =
            std::make_unique<BesRFLeafEvtRecEtaToGG>( BesRFLeafEvtRecEtaToGG( m_evt_rec ) );

        m_fields[BesFieldNames::EvtRec::PrimaryVertex::rpath] =
            std::make_unique<BesRFLeafEvtRecPrimaryVertex>(
                BesRFLeafEvtRecPrimaryVertex( m_evt_rec ) );

        m_fields[BesFieldNames::EvtRec::VeeVertex::rpath] =
            std::make_unique<BesRFLeafEvtRecVeeVertex>(
                BesRFLeafEvtRecVeeVertex( m_evt_rec ) );

        m_fields[BesFieldNames::EvtRec::DTag::rpath] =
            std::make_unique<BesRFLeafEvtRecDTag>( BesRFLeafEvtRecDTag( m_evt_rec ) );
    }

    if ( m_chain.GetBranch( "TMcEvent" ) )
    {
        m_evt_mc = new TMcEvent();
        m_chain.SetBranchAddress( "TMcEvent", &m_evt_mc );
        m_branch_names.insert( "TMcEvent" );

        m_fields[BesFieldNames::Mc::Mdc::rpath] =
            std::make_unique<BesRFLeafMcMdc>( BesRFLeafMcMdc( m_evt_mc ) );

        m_fields[BesFieldNames::Mc::Emc::rpath] =
            std::make_unique<BesRFLeafMcEmc>( BesRFLeafMcEmc( m_evt_mc ) );

        m_fields[BesFieldNames::Mc::Tof::rpath] =
            std::make_unique<BesRFLeafMcTof>( BesRFLeafMcTof( m_evt_mc ) );

        m_fields[BesFieldNames::Mc::Muc::rpath] =
            std::make_unique<BesRFLeafMcMuc>( BesRFLeafMcMuc( m_evt_mc ) );

        m_fields[BesFieldNames::Mc::McParticle::rpath] =
            std::make_unique<BesRFLeafMcParticle>( BesRFLeafMcParticle( m_evt_mc ) );
    }

    if ( m_chain.GetBranch( "TDigiEvent" ) )
    {
        m_evt_digi = new TDigiEvent();
        m_chain.SetBranchAddress( "TDigiEvent", &m_evt_digi );
        m_branch_names.insert( "TDigiEvent" );

        m_fields[BesFieldNames::Digi::Mdc::rpath] =
            std::make_unique<BesRFLeafDigiMdc>( BesRFLeafDigiMdc( m_evt_digi ) );

        m_fields[BesFieldNames::Digi::Tof::rpath] =
            std::make_unique<BesRFLeafDigiTof>( BesRFLeafDigiTof( m_evt_digi ) );

        m_fields[BesFieldNames::Digi::Emc::rpath] =
            std::make_unique<BesRFLeafDigiEmc>( BesRFLeafDigiEmc( m_evt_digi ) );

        m_fields[BesFieldNames::Digi::Muc::rpath] =
            std::make_unique<BesRFLeafDigiMuc>( BesRFLeafDigiMuc( m_evt_digi ) );

        m_fields[BesFieldNames::Digi::Lumi::rpath] =
            std::make_unique<BesRFLeafDigiLumi>( BesRFLeafDigiLumi( m_evt_digi ) );

        m_fields[BesFieldNames::Digi::FromMc::rpath] =
            std::make_unique<BesRFLeafDigiFromMc>( BesRFLeafDigiFromMc( m_evt_digi ) );
    }

    if ( m_chain.GetBranch( "TDstEvent" ) )
    {
        m_evt_dst = new TDstEvent();
        m_chain.SetBranchAddress( "TDstEvent", &m_evt_dst );
        m_branch_names.insert( "TDstEvent" );

        m_fields[BesFieldNames::Dst::Mdc::rpath] =
            std::make_unique<BesRFLeafDstMdc>( BesRFLeafDstMdc( m_evt_dst ) );

        m_fields[BesFieldNames::Dst::Emc::rpath] =
            std::make_unique<BesRFLeafDstEmc>( BesRFLeafDstEmc( m_evt_dst ) );

        m_fields[BesFieldNames::Dst::Tof::rpath] =
            std::make_unique<BesRFLeafDstTof>( BesRFLeafDstTof( m_evt_dst ) );

        m_fields[BesFieldNames::Dst::Muc::rpath] =
            std::make_unique<BesRFLeafDstMuc>( BesRFLeafDstMuc( m_evt_dst ) );

        m_fields[BesFieldNames::Dst::Dedx::rpath] =
            std::make_unique<BesRFLeafDstDedx>( BesRFLeafDstDedx( m_evt_dst ) );

        m_fields[BesFieldNames::Dst::Ext::rpath] =
            std::make_unique<BesRFLeafDstExt>( BesRFLeafDstExt( m_evt_dst ) );
    }

    if ( m_chain.GetBranch( "TRecEvent" ) )
    {
        m_rec_trk_event = new TRecTrackEvent();
        m_chain.SetBranchAddress( "TRecEvent", &m_rec_trk_event );
        m_branch_names.insert( "TRecEvent" );

        m_fields[BesFieldNames::Rec::EmcCluster::rpath] =
            std::make_unique<BesRFLeafRecEmcCluster>(
                BesRFLeafRecEmcCluster( m_rec_trk_event ) );

        m_fields[BesFieldNames::Rec::EmcHit::rpath] =
            std::make_unique<BesRFLeafRecEmcHit>( BesRFLeafRecEmcHit( m_rec_trk_event ) );

        m_fields[BesFieldNames::Rec::EmcShower::rpath] =
            std::make_unique<BesRFLeafRecEmcShower>(
                BesRFLeafRecEmcShower( m_rec_trk_event ) );

        m_fields[BesFieldNames::Rec::EvTime::rpath] =
            std::make_unique<BesRFLeafRecEvTime>( BesRFLeafRecEvTime( m_rec_trk_event ) );

        m_fields[BesFieldNames::Rec::ExtTrack::rpath] =
            std::make_unique<BesRFLeafRecExtTrack>( BesRFLeafRecExtTrack( m_rec_trk_event ) );

        m_fields[BesFieldNames::Rec::MdcDedx::rpath] =
            std::make_unique<BesRFLeafRecMdcDedx>( BesRFLeafRecMdcDedx( m_rec_trk_event ) );

        m_fields[BesFieldNames::Rec::MdcDedxHit::rpath] =
            std::make_unique<BesRFLeafRecMdcDedxHit>(
                BesRFLeafRecMdcDedxHit( m_rec_trk_event ) );

        m_fields[BesFieldNames::Rec::MdcHit::rpath] =
            std::make_unique<BesRFLeafRecMdcHit>( BesRFLeafRecMdcHit( m_rec_trk_event ) );

        m_fields[BesFieldNames::Rec::MdcKalHelixSeg::rpath] =
            std::make_unique<BesRFLeafRecMdcKalHelixSeg>(
                BesRFLeafRecMdcKalHelixSeg( m_rec_trk_event ) );

        m_fields[BesFieldNames::Rec::MdcKalTrack::rpath] =
            std::make_unique<BesRFLeafRecMdcKalTrack>(
                BesRFLeafRecMdcKalTrack( m_rec_trk_event ) );

        m_fields[BesFieldNames::Rec::MdcTrack::rpath] =
            std::make_unique<BesRFLeafRecMdcTrack>( BesRFLeafRecMdcTrack( m_rec_trk_event ) );

        m_fields[BesFieldNames::Rec::MucTrack::rpath] =
            std::make_unique<BesRFLeafRecMucTrack>( BesRFLeafRecMucTrack( m_rec_trk_event ) );

        m_fields[BesFieldNames::Rec::TofTrack::rpath] =
            std::make_unique<BesRFLeafRecTofTrack>( BesRFLeafRecTofTrack( m_rec_trk_event ) );

        m_fields[BesFieldNames::Rec::Zdd::rpath] =
            std::make_unique<BesRFLeafRecZdd>( BesRFLeafRecZdd( m_rec_trk_event ) );
    }

    if ( m_chain.GetBranch( "THltEvent" ) )
    {
        m_evt_hlt = new THltEvent();
        m_chain.SetBranchAddress( "THltEvent", &m_evt_hlt );
        m_branch_names.insert( "THltEvent" );

        m_fields[BesFieldNames::Hlt::Raw::rpath] =
            std::make_unique<BesRFLeafHltRaw>( BesRFLeafHltRaw( m_evt_hlt ) );

        m_fields[BesFieldNames::Hlt::Inf::rpath] =
            std::make_unique<BesRFLeafHltInf>( BesRFLeafHltInf( m_evt_hlt ) );

        m_fields[BesFieldNames::Hlt::DstInf::rpath] =
            std::make_unique<BesRFLeafHltDstInf>( BesRFLeafHltDstInf( m_evt_hlt ) );
    }

    if ( m_chain.GetBranch( "TTrigEvent" ) )
    {
        m_evt_trig = new TTrigEvent();
        m_chain.SetBranchAddress( "TTrigEvent", &m_evt_trig );
        m_branch_names.insert( "TTrigEvent" );

        m_fields[BesFieldNames::Trig::rpath] =
            std::make_unique<BesRFLeafTrigData>( BesRFLeafTrigData( m_evt_trig ) );
    }
}

const long long BesEventReader::py_get_entries() const { return m_entries; }

py::list BesEventReader::py_get_available_fields() const {
    py::list res;
    for ( const auto& [field, obj_ptr] : m_fields ) res.append( field );
    return res;
}

py::dict BesEventReader::py_arrays( const long long entry_start, const long long entry_stop,
                                    const std::vector<std::string> field_names ) {
    if ( entry_start < 0 || entry_start >= m_entries || entry_stop < 0 ||
         entry_stop > m_entries )
        throw std::runtime_error( "Invalid entry range: [" + std::to_string( entry_start ) +
                                  ", " + std::to_string( entry_stop ) + ")" );

    /* Set field status */
    set_field_status( "*", false ); // deactivate all fields
    if ( field_names.empty() )
    { set_field_status( "*", true ); } // activate all fields if no field is specified
    else                               // activate specified fields
    {
        for ( const auto& field : field_names ) set_field_status( field, true );
    }

    /* Check whether branch can be deactivated */
    optimize_branch_status();

    /* Clear leaves' previous data */
    leaves_clear();

    /* Read data */
    unsigned tmp_counter          = 0;
    const unsigned check_interval = 2000;
    for ( long long entry = entry_start; entry < entry_stop; entry++, tmp_counter++ )
    {
        if ( tmp_counter >= check_interval )
        {
            tmp_counter = 0;
            if ( PyErr_CheckSignals() ) throw py::error_already_set();
        }

        m_chain.GetEntry( entry );
        leaves_i_fill();
    }

    /* Construct Result */
    py::dict res;

    for ( const auto& [field, obj_ptr] : m_fields )
    { res[field.c_str()] = obj_ptr->get_array(); }

    leaves_clear();
    return res;
}

/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

void BesEventReader::optimize_branch_status() {
    set_branch_status( "*", false );

    for ( const auto& [field, obj_ptr] : m_fields )
    {
        if ( obj_ptr->get_status() )
        {
            auto branch_name = BesFieldNames::field2branch.at( field );
            set_branch_status( branch_name, true );
        }
    }
}

void BesEventReader::set_branch_status( const std::string& branch_name, bool status ) {
    std::string pattern = std::regex_replace( branch_name, std::regex( "\\*" ), ".*" );
    pattern             = std::regex_replace( pattern, std::regex( "\\?" ), "." );

    bool isSet = false;
    for ( auto& branch : m_branch_names )
    {
        if ( std::regex_match( branch, std::regex( pattern ) ) )
        {
            m_chain.SetBranchStatus( branch.c_str(), status );
            isSet = true;
        }
    }

    if ( !isSet ) throw std::runtime_error( "Cannot find (any) branch of " + branch_name );
}

void BesEventReader::set_field_status( const std::string& field_name, bool status ) {
    using namespace BesFieldNames;

    std::string pattern = std::regex_replace( field_name, std::regex( "\\*" ), ".*" );
    pattern             = std::regex_replace( pattern, std::regex( "\\?" ), "." );

    bool isSet = false;
    for ( const auto& [field, obj_ptr] : m_fields )
    {
        if ( std::regex_match( field, std::regex( pattern ) ) )
        {
            obj_ptr->set_status( status );

            isSet = true;

            // automatically activate branch if field is activated
            if ( status )
            {
                auto branch_name = BesFieldNames::field2branch.at( field );
                set_branch_status( branch_name, true );
            }
        }
    }

    if ( !isSet )
        throw std::runtime_error( "Cannot find (any) field of '" + field_name + "'" );
}

/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

void BesEventReader::leaves_clear() {
    for ( auto& [field, obj_ptr] : m_fields ) { obj_ptr->clear(); }
}

void BesEventReader::leaves_i_fill() {
    for ( auto& [field, obj_ptr] : m_fields ) { obj_ptr->i_fill(); }
}