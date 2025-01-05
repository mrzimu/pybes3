#include "RootEventData/TEvtRecTrack.h"

ClassImp( TEvtRecTrack );

TEvtRecTrack::TEvtRecTrack()
    : m_trackId( -1 )
    , m_partId( 0x80000000 )
    , m_quality( -1 )
    , m_mdcTrackId( -1 )
    , m_mdcKalTrackId( -1 )
    , m_mdcDedxId( -1 )
    , m_extTrackId( -1 )
    , m_emcShowerId( -1 )
    , m_mucTrackId( -1 )
    , m_tofTrackIds( 0 ) {}

TEvtRecTrack::~TEvtRecTrack() {}
