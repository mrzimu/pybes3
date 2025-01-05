#include "RootEventData/TEvtRecPrimaryVertex.h"

ClassImp( TEvtRecPrimaryVertex );

TEvtRecPrimaryVertex::TEvtRecPrimaryVertex()
    : m_isValid( false )
    , m_nTracks( -1 )
    , m_trackIdList( 0 )
    , m_chi2( 999.9 )
    , m_ndof( -3 )
    , m_fitMethod( -1 ) {
    for ( int i = 0; i < 3; i++ ) { m_vtx[i] = 0.; }
    for ( int i = 0; i < 6; i++ ) { m_Evtx[i] = 0.; }
}

TEvtRecPrimaryVertex::~TEvtRecPrimaryVertex() {}
