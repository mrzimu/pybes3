#include "RootEventData/TEvtRecVeeVertex.h"

ClassImp( TEvtRecVeeVertex );

TEvtRecVeeVertex::TEvtRecVeeVertex()
    : m_vertexId( -1 )
    , m_vertexType( -1 )
    , m_chi2( 999.9 )
    , m_ndof( -3 )
    , m_mass( 0. )
    , m_nCharge( -1 )
    , m_nTracks( -1 ) {
    for ( int i = 0; i < 7; i++ ) { m_w[i] = 0; }
    for ( int i = 0; i < 28; i++ ) { m_Ew[i] = 0; }
    m_pair[0] = m_pair[1] = -1;
    m_daughter[0] = m_daughter[1] = -1;
}

TEvtRecVeeVertex::~TEvtRecVeeVertex() {}
