#include "RootEventData/TEvtRecDTag.h"

ClassImp( TEvtRecDTag );

TEvtRecDTag::TEvtRecDTag()
    : m_decayMode( 0 )
    , m_type( 0 )
    , m_beamE( 0 )
    , m_mass( 0 )
    , m_mBC( 0 )
    , m_deltaE( 0 )
    , m_charge( 0 )
    , m_charm( 0 )
    , m_numOfChildren( 0 )
    , m_px( 0 )
    , m_py( 0 )
    , m_pz( 0 )
    , m_pe( 0 ) {
    m_tracks.clear();
    m_showers.clear();
    m_otherTracks.clear();
    m_otherShowers.clear();
    m_pionId.clear();
    m_kaonId.clear();
}

TEvtRecDTag::~TEvtRecDTag() {}
