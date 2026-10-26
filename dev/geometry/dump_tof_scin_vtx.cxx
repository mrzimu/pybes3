//-----------------------------------------------------------------------------------
// Export the 8 vertex coordinates (global, mm) of the TOF scintillators, CSV format
//
//   geometry file : $GDMLMANAGEMENTDATAROOT/dat/Tof.gdml  (setup "Default")
//   reference     : EventDisplay/BesVisLib/src/TofROOTGeo.cxx::Init2DGeometry()
//                   lines 286-338 (non-MRPC branch):
//                     localArb8Point = ((TGeoArb8*)scinPhyNode->GetShape())->GetVertices();
//                     local[2] = (i < 4) ? -GetDz() : +GetDz();
//                     scinPhyNode->GetMatrix(-1*GetLevel())->LocalToMaster(local, master);
//                   The same algorithm is reproduced here by gd::Arb8Vertices().
//
// Vertex order (same as the display side, it defines the 2D polygons):
//   i = 0..3 -> local z = -Dz ; i = 4..7 -> local z = +Dz
//   XY polygon : ( P[j] + P[j+4] ) / 2      (j = 0..3)
//   ZR polygon : ( P[iSeq[2i]] + P[iSeq[2i+1]] ) / 2 , iSeq = {0,3,1,2,5,6,4,7}
//
// Output: gid,part,layer_or_module,phi_or_strip,x0,y0,z0,...,x7,y7,z7
//   This is exactly the CSV written by ExportTofScintGeom of dev/boss-algs, i.e. the
//   file dev/geometry/export-tof-geom.py reads: coordinates in cm, gid = running index over
//   (part, layer, scin), so 0..271.
//
// Usage: ./dump_tof_scin_vtx > tof-scint-vertices.csv
//-----------------------------------------------------------------------------------
#include "geomdump_common.h"

int main( int argc, char** argv ) {
    (void)argc;
    (void)argv;

    // ---- same constants as in TofROOTGeo.h ----
    const int m_kPart = 3, m_kLayerBr = 2, m_kLayerEc = 1;
    const int m_kScinBr = 88, m_kScinEc = 48;

    ::SubDetectorROOTGeo* sub = gd::OpenGdml( gd::GdmlDir() + "Tof.gdml" );
    if ( !sub->GetTopVolume() ) return 1;

    // ---------- header ----------
    printf( "gid,part,layer_or_module,phi_or_strip" );
    for ( int i = 0; i < 8; ++i ) printf( ",x%d,y%d,z%d", i, i, i );
    printf( "\n" );

    // ---------- scintillator by scintillator ----------
    int gid = 0;
    int nOk = 0, nBad = 0, nNoArb8 = 0;
    for ( int part = 0; part < m_kPart; ++part )
    {
        int ipart          = ( part == 1 ) ? 2 : ( ( part == 2 ) ? 1 : 0 );
        TGeoNode* nodePart = sub->GetTopVolume()->GetNode( ipart );

        int nLayer = ( part == 1 ) ? m_kLayerBr : m_kLayerEc;
        int nScin  = ( part == 1 ) ? m_kScinBr : m_kScinEc;

        for ( int layer = 0; layer < nLayer; ++layer )
        {
            for ( int scin = 0; scin < nScin; ++scin )
            {
                // node name formulas copied from TofROOTGeo::SetNode()
                std::vector<std::string> names;
                if ( part == 1 )
                {
                    int idx = ( 2 * m_kScinBr * 3 - 1 ) - ( layer * m_kScinBr + scin ) * 3;
                    names.push_back( gd::Fmt( "pv_logicalPVFBr%d_%d", layer + 1, idx ) );
                    names.push_back( gd::Fmt( "pv_logicalAlBr%d_0", layer + 1 ) );
                    names.push_back( gd::Fmt( "pv_logicalScinBr%d_0", layer + 1 ) );
                }
                else
                {
                    const char* side = ( part == 0 ) ? "East" : "West";
                    int idx          = ( 2 * m_kScinEc - 1 ) - scin * 2;
                    names.push_back( gd::Fmt( "pv_logicalPVFEc%s_%d", side, idx ) );
                    names.push_back( gd::Fmt( "pv_logicalAlEc%s_0", side ) );
                    names.push_back( gd::Fmt( "pv_logicalScinEc%s_0", side ) );
                }

                std::vector<TGeoNode*> chain;
                std::string bad;
                if ( !gd::Resolve( sub, names, chain, &bad ) )
                {
                    ++nBad;
                    fprintf( stderr, "[warn] part=%d layer=%d scin=%d node not found: %s\n",
                             part, layer, scin, bad.c_str() );
                    continue;
                }
                chain.insert( chain.begin(), nodePart );

                double v[8][3];
                if ( !gd::Arb8Vertices( chain, v ) )
                {
                    ++nNoArb8;
                    fprintf( stderr,
                             "[warn] part=%d layer=%d scin=%d shape is not TGeoArb8, skip\n",
                             part, layer, scin );
                    continue;
                }

                // one row per scintillator, coordinates in cm (%g keeps the same 6
                // significant digits as the BOSS exporter)
                printf( "%d,%d,%d,%d", gid, part, layer, scin );
                for ( int i = 0; i < 8; ++i )
                    for ( int j = 0; j < 3; ++j ) printf( ",%g", v[i][j] / 10.0 );
                printf( "\n" );
                ++gid;
                ++nOk;
            }
        }
    }

    fprintf( stderr, "[info] %d scintillators ok, %d failed, %d not TGeoArb8\n", nOk, nBad,
             nNoArb8 );
    return ( nBad || nNoArb8 ) ? 2 : 0;
}
