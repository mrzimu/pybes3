//-----------------------------------------------------------------------------------
// Export the 8 vertex coordinates (CSV) of the MUC readout strips
//
//   geometry file : $GDMLMANAGEMENTDATAROOT/dat/Muc.gdml   (setup "Default")
//   reference     : EventDisplay/BesVisLib/src/MucROOTGeo.cxx
//                   - SetNode()         lines 608-704  (node name formulas)
//                   - SetPhysicalNode() lines 1097-1140 (strip path)
//                   - Init2DGeometry()  lines 521-606  (the 8 local strip vertices)
//
// Index convention (identical to MucID):
//   part : 0 = East endcap, 1 = Barrel, 2 = West endcap
//   seg  : m_kSeg[3] = {4, 8, 4}
//   gap  : m_kGap[3] = {8, 9, 8}      (the layer of MucID)
//   strip: index of the strip inside the strip plane of that gap; the number of strips is
//          not constant: 64 per gap for the endcaps, alternating 48/96 for the barrel,
//          and seg 2 uses another set of volumes (9152 strips in total)
//
// Node name formulas (MucROOTGeo::SetNode(); note the display-side names carry the pv_
// prefix):
//   gap        = pv_lMucP<part>S<seg>G<gap>_<gapCount>
//                (gapCount increases from 0 in the (part,seg,gap) loop = daughter index
//                 of logicalMuc)
//   stripPlane = pv_lMucP<part>S<segment>G<gap>SP_0    segment = (part==1 && seg==2) ? 2 : 0
//   strip      = pv_lMucP<part>S<segment>G<gap>s<strip zero-padded to 3 digits>_<strip>
//   path       = <gap> / <box> / <stripPlane> / <strip>
//                (box = daughter 0 of gap, stripPlane = daughter 0 of box)
//   This program walks down by "daughter index inside the parent volume" (equivalent to
//   the path resolution of TGeoPhysicalNode on the display side) and compares the result
//   with the node found by name (the names do not contain seg, so several segs of one
//   part share the same named instances, see the info on stderr).
//
// Vertex rule (copied from the strip loop of MucROOTGeo::Init2DGeometry()):
//   the 8 local corners (fixed order, not a convex-hull order):
//     i=0:(-dx,-dy,-dz) 1:(+dx,-dy,-dz) 2:(+dx,+dy,-dz) 3:(-dx,+dy,-dz)
//     i=4:(-dx,-dy,+dz) 5:(+dx,-dy,+dz) 6:(+dx,+dy,+dz) 7:(-dx,+dy,+dz)
//   The display side scales dz by m_kStripZMuliple = 12 before drawing (the strips are
//   too thin to be visible otherwise); this tool never does that, it always exports the
//   true geometry, because that is what the reconstruction needs.
//   The 8 points are then transformed to global coordinates (mm) with the matrix chain
//   of <gap>/<box>/<stripPlane>/<strip>.
//
//   The display side afterwards collapses these 8 points into two polygons (not exported
//   here, given for reference):
//     XY (4 points): barrel (P1+P2)/2,(P0+P3)/2,(P4+P7)/2,(P5+P6)/2 ; endcap (P[i]+P[i+4])/2
//     ZR (6 points): barrel i={4,5,1,2,6,7} ; endcap i={1,2,3,7,6,5}
//
// Output: gid,part,segment,layer,strip,cx,cy,cz,dx,dy,dz,x0,y0,z0,...,x7,y7,z7
//   This is exactly the CSV written by ExportMucGeom of dev/boss-algs, i.e. the file
//   dev/geometry/export-muc-geom.py reads: coordinates in cm, gid = running index over the
//   rows (0..9151), dz = true half thickness (no display scaling).
//
// Usage: ./dump_muc_strip_vtx > muc-vtx.csv
//-----------------------------------------------------------------------------------
#include "geomdump_common.h"

#include <map>
#include <set>

/// Vertex rule of the display side: i=0..3 on the -dz face, 4..7 on the +dz face, going
/// around the face as (-x,-y) (+x,-y) (+x,+y) (-x,+y) (one-to-one with the MucROOTGeo switch)
static void StripVertices( const std::vector<TGeoNode*>& chain, double dx, double dy,
                           double dz, double v[8][3] ) {
    const double sx[8] = { -1, 1, 1, -1, -1, 1, 1, -1 };
    const double sy[8] = { -1, -1, 1, 1, -1, -1, 1, 1 };
    const double sz[8] = { -1, -1, -1, -1, 1, 1, 1, 1 };

    TGeoHMatrix m = gd::ChainMatrix( chain );
    for ( int i = 0; i < 8; ++i )
    {
        Double_t loc[3] = { sx[i] * dx, sy[i] * dy, sz[i] * dz };
        Double_t mas[3];
        m.LocalToMaster( loc, mas );
        v[i][0] = mas[0];
        v[i][1] = mas[1];
        v[i][2] = mas[2];
    }
}

int main( int argc, char** argv ) {
    (void)argc;
    (void)argv;

    // ---- same constants as in MucROOTGeo.h ----
    const int m_kSeg[3] = { 4, 8, 4 };
    const int m_kGap[3] = { 8, 9, 8 };

    ::SubDetectorROOTGeo* sub = gd::OpenGdml( gd::GdmlDir() + "Muc.gdml" );
    TGeoVolume* top           = sub->GetTopVolume();
    if ( !top ) return 1;

    // ---------- header ----------
    printf( "gid,part,segment,layer,strip,cx,cy,cz,dx,dy,dz" );
    for ( int i = 0; i < 8; ++i ) printf( ",x%d,y%d,z%d", i, i, i );
    printf( "\n" );

    int gid = 0;
    int nOk = 0, nBad = 0, nNotBox = 0, nOrigin = 0, nNameDiff = 0, nExpected = 0;

    std::map<int, std::set<std::string>> yz; // (dy,dz) combinations seen per part
    std::map<int, std::set<double>> dxs;     // dx values seen per part

    int gapCount = 0;
    for ( int part = 0; part < 3; ++part )
    {
        for ( int seg = 0; seg < m_kSeg[part]; ++seg )
        {
            const int segment = ( part == 1 && seg == 2 ) ? 2 : 0; // S number substitution

            for ( int gap = 0; gap < m_kGap[part]; ++gap, ++gapCount )
            {
                // gap node (its name contains gapCount, hence it is unique)
                TGeoNode* nodeGap =
                    sub->GetNode( gd::Fmt( "pv_lMucP%dS%dG%d_%d", part, seg, gap, gapCount ) );
                if ( !nodeGap )
                {
                    fprintf( stderr, "[warn] gap node not found: pv_lMucP%dS%dG%d_%d\n", part,
                             seg, gap, gapCount );
                    continue;
                }
                // walk down the display-side path: <gap> -> <box> -> <stripPlane> -> <strip>
                TGeoNode* box = nodeGap->GetVolume()->GetNode( 0 );
                TGeoNode* sp  = box->GetVolume()->GetNode( 0 );
                if ( !box || !sp )
                {
                    fprintf( stderr, "[warn] part=%d seg=%d gap=%d: box/stripPlane missing\n",
                             part, seg, gap );
                    continue;
                }

                const int nStrip = sp->GetVolume()->GetNdaughters();
                nExpected += nStrip;

                for ( int strip = 0; strip < nStrip; ++strip )
                {
                    TGeoNode* node = sp->GetVolume()->GetNode( strip );
                    if ( !node )
                    {
                        ++nBad;
                        continue;
                    }

                    // cross check: the name (display-side SetNode() syntax) and "by index"
                    // must refer to the same node
                    TGeoNode* byName = sub->GetNode( gd::Fmt( "pv_lMucP%dS%dG%ds%03d_%d", part,
                                                              segment, gap, strip, strip ) );
                    if ( byName != node ) ++nNameDiff;

                    std::vector<TGeoNode*> chain;
                    chain.push_back( nodeGap );
                    chain.push_back( box );
                    chain.push_back( sp );
                    chain.push_back( node );

                    TGeoShape* shape = node->GetVolume()->GetShape();
                    TGeoBBox* b      = dynamic_cast<TGeoBBox*>( shape );
                    if ( !b )
                    {
                        ++nNotBox;
                        continue;
                    }
                    const Double_t* o = b->GetOrigin();
                    if ( o[0] != 0.0 || o[1] != 0.0 || o[2] != 0.0 ) ++nOrigin;

                    const double dx = b->GetDX(), dy = b->GetDY(), dz = b->GetDZ();

                    TGeoHMatrix m      = gd::ChainMatrix( chain );
                    const Double_t* tr = m.GetTranslation();
                    double pos[3]      = { tr[0], tr[1], tr[2] };

                    double v[8][3];
                    StripVertices( chain, dx, dy, dz, v );

                    yz[part].insert( gd::Fmt( "dy=%g dz=%g", dy, dz ) );
                    dxs[part].insert( dx );

                    // one row per strip, coordinates in cm (%g keeps the same 6
                    // significant digits as the BOSS exporter)
                    printf( "%d,%d,%d,%d,%d", gid, part, seg, gap, strip );
                    printf( ",%g,%g,%g,%g,%g,%g", pos[0] / 10.0, pos[1] / 10.0, pos[2] / 10.0,
                            dx / 10.0, dy / 10.0, dz / 10.0 );
                    for ( int i = 0; i < 8; ++i )
                        for ( int j = 0; j < 3; ++j ) printf( ",%g", v[i][j] / 10.0 );
                    printf( "\n" );
                    ++gid;
                    ++nOk;
                }
            }
        }
    }

    fprintf( stderr,
             "[info] %d rows ok (%d vertices), %d failed; %d expected; "
             "%d not TGeoBBox; %d shapes with non-zero origin; %d name/index "
             "mismatches\n",
             nOk, nOk * 8, nBad, nExpected, nNotBox, nOrigin, nNameDiff );
    for ( std::map<int, std::set<double>>::iterator it = dxs.begin(); it != dxs.end(); ++it )
    {
        const int part = it->first;
        fprintf(
            stderr,
            "[info] part=%d: dx has %zu values, range %g .. %g; %zu (dy,dz) combos:", part,
            it->second.size(), *it->second.begin(), *it->second.rbegin(), yz[part].size() );
        for ( std::set<std::string>::iterator s = yz[part].begin(); s != yz[part].end(); ++s )
            fprintf( stderr, " [%s]", s->c_str() );
        fprintf( stderr, "\n" );
    }
    return ( nBad || nNotBox || nOk != nExpected || nOk != 9152 ) ? 2 : 0;
}
