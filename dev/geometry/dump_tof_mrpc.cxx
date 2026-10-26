//-----------------------------------------------------------------------------------
// Export the TOF MRPC readout strips as CSV (including the 8 vertex coordinates)
//
//   geometry file : $GDMLMANAGEMENTDATAROOT/dat/Tof_mrpc.gdml  (setup "Default")
//                   that file also contains the barrel scintillators; the display side
//                   sets fTofMrpc = 1 based on the file name containing "Tof_mrpc.gdml"
//                   (TofROOTGeo.cxx lines 95-96)
//   reference     : EventDisplay/BesVisLib/src/TofROOTGeo.cxx
//                   - SetNode()         lines 345-425 (MRPC branch)
//                   - SetPhysicalNode() lines 809-846 (MRPC branch)
//
// Index convention (identical to TofID):
//   part  : 3 = East endcap, 4 = West endcap (the numbering of ExportTofMrpcGeom and of
//           pybes3; the display side uses 0/2 internally, see the ipart mapping below)
//   module: 0..35 (m_kModuleEc=36) x strip 0..11 (m_kStripEc=12)
//
// Node name formulas (taken from TofROOTGeo::SetNode()):
//   the m index of the module volume depends on part and module parity:
//     East (part 3): even -> logical_container_m0_<module>, odd ->
//     logical_container_m3_<module> West (part 4): even -> logical_container_m1_<module>, odd
//     -> logical_container_m2_<module>
//   gasContainer = pv_logical_gasContainer_m<K>_0   (m_kContainerNodeNb = 0)
//   bareChamber  = pv_logical_bareChamber_6          (m_kChamberNodeNb   = 6)
//   pcbBoard1    = pv_logical_pcbBoard1_30           (m_kBoard1NodeNb    = 30)
//   strip        = pv_logical_strip_<11-strip>_<strip>
//   path         : <part>/<module>/<gasContainer>/<bareChamber>/<pcbBoard1>/<strip>
//
// About the vertices:
//   the endcap strips are TGeoTrd2 (which does NOT inherit TGeoArb8!); their vertices are
//   built from dx1/dx2/dy1/dy2/dz with i=0..3 on the low-z face and i=4..7 on the high-z
//   face.
//   Note: the MRPC branch of TofROOTGeo::Init2DGeometry() casts with
//   (TGeoArb8*)mrpcPhyNode->GetShape() -- an illegal cross-class cast for TGeoTrd2, so
//   that 2D code path is not trustworthy. This file gives the vertices computed from the
//   real TGeoTrd2 geometry.
//
// Output: gid,part,layer_or_module,phi_or_strip,x0,y0,z0,...,x7,y7,z7
//   This is exactly the CSV written by ExportTofMrpcGeom of dev/boss-algs, i.e. the file
//   dev/geometry/export-tof-geom.py reads: coordinates in cm, layer_or_module = module,
//   phi_or_strip = strip, and gid starting at 272 (the 272 barrel scintillators come
//   first, see dump_tof_scin_vtx).
//
// Usage: ./dump_tof_mrpc > tof-mrpc-vertices.csv
//-----------------------------------------------------------------------------------
#include "geomdump_common.h"

int main( int argc, char** argv ) {
    (void)argc;
    (void)argv;

    // ---- same constants as in TofROOTGeo.h ----
    const int m_kModuleEc = 36, m_kStripEc = 12;
    const int m_kChamberNodeNb = 6, m_kContainerNodeNb = 0, m_kBoard1NodeNb = 30;

    ::SubDetectorROOTGeo* sub = gd::OpenGdml( gd::GdmlDir() + "Tof_mrpc.gdml" );
    if ( !sub->GetTopVolume() ) return 1;

    // ---------- header ----------
    printf( "gid,part,layer_or_module,phi_or_strip" );
    for ( int i = 0; i < 8; ++i ) printf( ",x%d,y%d,z%d", i, i, i );
    printf( "\n" );

    int nOk = 0, nBad = 0, nApprox = 0, nMismatch = 0;

    // ================= Endcap MRPC readout strips =================
    // gid continues after the 272 barrel scintillators (see ExportTofMrpcGeom); part 3 =
    // East, 4 = West. The barrel scintillators of this GDML are exported by
    // dump_tof_scin_vtx, so they are not repeated here.
    int gid = ( 88 + 48 ) * 2;
    for ( int part : { 3, 4 } )
    {
        int ipart          = ( part == 3 ) ? 0 : 1;
        TGeoNode* nodePart = sub->GetTopVolume()->GetNode( ipart );

        for ( int module = 0; module < m_kModuleEc; ++module )
        {
            // m index of the module logical volume (see TofROOTGeo::SetNode())
            int mIdx;
            if ( part == 3 ) mIdx = ( module % 2 == 0 ) ? 0 : 3;
            else mIdx = ( module % 2 == 0 ) ? 1 : 2;

            std::vector<std::string> base;
            base.push_back( gd::Fmt( "pv_logical_container_m%d_%d", mIdx, module ) );
            base.push_back(
                gd::Fmt( "pv_logical_gasContainer_m%d_%d", mIdx, m_kContainerNodeNb ) );
            base.push_back( gd::Fmt( "pv_logical_bareChamber_%d", m_kChamberNodeNb ) );
            base.push_back( gd::Fmt( "pv_logical_pcbBoard1_%d", m_kBoard1NodeNb ) );

            std::vector<TGeoNode*> baseChain;
            std::string bad;
            if ( !gd::Resolve( sub, base, baseChain, &bad ) )
            {
                ++nBad;
                fprintf( stderr, "[warn] part=%d module=%d parent chain node not found: %s\n",
                         part, module, bad.c_str() );
                continue;
            }
            baseChain.insert( baseChain.begin(), nodePart );

            for ( int strip = 0; strip < m_kStripEc; ++strip )
            {
                std::vector<std::string> names = base;
                names.push_back(
                    gd::Fmt( "pv_logical_strip_%d_%d", ( m_kStripEc - 1 ) - strip, strip ) );

                std::vector<TGeoNode*> chain;
                if ( !gd::Resolve( sub, names, chain, &bad ) )
                {
                    ++nBad;
                    fprintf( stderr, "[warn] part=%d module=%d strip=%d node not found: %s\n",
                             part, module, strip, bad.c_str() );
                    continue;
                }
                chain.insert( chain.begin(), nodePart );

                double v[8][3];
                std::string shape;
                bool exact = true;
                if ( !gd::ShapeVertices( chain, v, &shape, &exact ) )
                {
                    ++nBad;
                    fprintf( stderr,
                             "[warn] part=%d module=%d strip=%d shape %s gives no vertices\n",
                             part, module, strip, shape.c_str() );
                    continue;
                }
                if ( !exact ) ++nApprox;

                // cross check: strip resolved by name vs strip taken by copy index in
                // pcbBoard1
                TGeoNode* byIdx = chain[4]->GetVolume()->GetNode( strip );
                if ( byIdx != chain[5] )
                {
                    ++nMismatch;
                    fprintf(
                        stderr,
                        "[warn] part=%d module=%d strip=%d name/index mismatch: %s vs %s\n",
                        part, module, strip, chain[5]->GetName(),
                        byIdx ? byIdx->GetName() : "<null>" );
                }

                // one row per strip, coordinates in cm (%g keeps the same 6 significant
                // digits as the BOSS exporter)
                printf( "%d,%d,%d,%d", gid, part, module, strip );
                for ( int i = 0; i < 8; ++i )
                    for ( int j = 0; j < 3; ++j ) printf( ",%g", v[i][j] / 10.0 );
                printf( "\n" );
                ++gid;
                ++nOk;
            }
        }
    }

    fprintf( stderr,
             "[info] %d rows ok (%d vertices), %d failed; %d approximated by bounding box; "
             "%d name/index mismatches\n",
             nOk, nOk * 8, nBad, nApprox, nMismatch );
    return ( nBad || nApprox || nMismatch ) ? 2 : 0;
}
