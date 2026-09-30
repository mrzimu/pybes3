#include "MucCalib/MucIdTransform.h"
#include "ROOTGeo/SubDetectorROOTGeo.h"

#include <TGeoArb8.h>
#include <TGeoBBox.h>
#include <TGeoManager.h>
#include <TGeoMatrix.h>
#include <TGeoNode.h>
#include <TGeoShape.h>
#include <TGeoTrd2.h>
#include <TGeoVolume.h>

#include <cstdarg>
#include <cstdio>
#include <cstdlib>
#include <format>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

/// Obtain global transformation matrix for a chain of TGeoNodes
TGeoHMatrix chain_matrix( const std::vector<TGeoNode*>& chain ) {
    TGeoHMatrix m;
    for ( size_t i = 0; i < chain.size(); ++i ) m.Multiply( chain[i]->GetMatrix() );
    return m;
}

void strip_vertices( const std::vector<TGeoNode*>& chain, double dx, double dy, double dz,
                     double v[8][3] ) {
    const double sx[8] = { -1, 1, 1, -1, -1, 1, 1, -1 };
    const double sy[8] = { -1, -1, 1, 1, -1, -1, 1, 1 };
    const double sz[8] = { -1, -1, -1, -1, 1, 1, 1, 1 };

    TGeoHMatrix m = chain_matrix( chain );
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
    const char* r = getenv( "GDMLMANAGEMENTDATAROOT" );
    if ( !r )
    {
        std::cerr << "Environment variable GDMLMANAGEMENTDATAROOT is not set." << std::endl;
        return 1;
    }

    if ( argc != 2 )
    {
        std::cerr << "Usage: " << argv[0] << " <output_file>" << std::endl;
        return 1;
    }

    auto gdml_file = std::string( r ) + "/dat/Muc.gdml";

    // Open GDML
    std::string top_name;
    if ( !gGeoManager ) gGeoManager = new TGeoManager( "BesGeo", "Bes geometry" );
    SubDetectorROOTGeo sub;
    sub.ReadGdml( gdml_file.c_str(), "Default" );
    if ( sub.GetTopVolume() )
    {
        top_name = sub.GetTopVolume()->GetName();
        if ( !gGeoManager->GetTopVolume() ) gGeoManager->SetTopVolume( sub.GetTopVolume() );
    }
    else
    {
        std::cerr << "ERROR: Top volume not found in GDML file " << gdml_file << std::endl;
        return 1;
    }

    auto top = sub.GetTopVolume();

    // Output file
    std::ofstream fout( argv[1] );
    if ( !fout.is_open() )
    {
        std::cerr << "ERROR: Could not open output file " << argv[1] << std::endl;
        return 1;
    }

    // Table header
    fout << "gid,part,segment,layer,strip,cx,cy,cz,dx,dy,dz,";
    for ( int i = 0; i < 8; i++ )
    {
        fout << "x" << i << ",";
        fout << "y" << i << ",";
        fout << "z" << i << ( i == 7 ? "\n" : "," );
    }

    // Loop
    MucIdTransform muc_trans;
    int n_ok = 0, n_bad = 0;

    const int N_SEGS[3]   = { 4, 8, 4 };
    const int N_LAYERS[3] = { 8, 9, 8 };

    int gap_count = 0;
    for ( int part = 0; part < 3; part++ )
    {
        for ( int segment = 0; segment < N_SEGS[part]; segment++ )
        {
            const int seg_in_gdml = ( part == 1 && segment == 2 ) ? 2 : 0;

            for ( int layer = 0; layer < N_LAYERS[part]; layer++, gap_count++ )
            {
                TGeoNode* node_layer = sub.GetNode(
                    std::format( "pv_lMucP{}S{}G{}_{}", part, segment, layer, gap_count ) );

                if ( !node_layer )
                {
                    std::cerr << "ERROR: Node not found for layer " << layer << " in segment "
                              << segment << " of part " << part << std::endl;
                    abort();
                }

                TGeoNode* box = node_layer->GetVolume()->GetNode( 0 );
                TGeoNode* sp  = box->GetVolume()->GetNode( 0 );
                if ( !box || !sp )
                {
                    std::cerr << "ERROR: Box or SP node not found for layer " << layer
                              << " in segment " << segment << " of part " << part << std::endl;
                    abort();
                }

                const int n_strips = sp->GetVolume()->GetNdaughters();

                for ( int strip = 0; strip < n_strips; strip++ )
                {
                    TGeoNode* node = sp->GetVolume()->GetNode( strip );
                    if ( !node )
                    {
                        std::cerr << "ERROR: Strip node not found for strip " << strip
                                  << " in layer " << layer << " of segment " << segment
                                  << " of part " << part << std::endl;
                        abort();
                    }

                    std::vector<TGeoNode*> chain;
                    chain.push_back( node_layer );
                    chain.push_back( box );
                    chain.push_back( sp );
                    chain.push_back( node );

                    TGeoShape* shape = node->GetVolume()->GetShape();
                    TGeoBBox* b      = dynamic_cast<TGeoBBox*>( shape );
                    if ( !b )
                    {
                        std::cerr << "ERROR: Strip shape is not a TGeoBBox for strip " << strip
                                  << " in layer " << layer << " of segment " << segment
                                  << " of part " << part << std::endl;
                        abort();
                    }

                    const double dx = b->GetDX(), dy = b->GetDY(), dz = b->GetDZ();

                    TGeoHMatrix m      = chain_matrix( chain );
                    const Double_t* tr = m.GetTranslation();
                    double pos[3]      = { tr[0], tr[1], tr[2] };

                    double v[8][3];
                    strip_vertices( chain, dx, dy, dz, v );

                    int gid = muc_trans.GetStripId( part, segment, layer, strip );

                    fout << std::format( "{},{},{},{},{},{:.6},{:.6},{:.6},{},{},{},", gid,
                                         part, segment, layer, strip, pos[0] / 10.0,
                                         pos[1] / 10.0, pos[2] / 10.0, dx / 10.0, dy / 10.0,
                                         dz / 10.0 );
                    for ( int i = 0; i < 8; i++ )
                    {
                        for ( int j = 0; j < 3; j++ )
                        { fout << v[i][j] / 10.0 << ( ( i == 7 && j == 2 ) ? "\n" : "," ); }
                    }

                    n_ok++;
                }
            }
        }
    }

    fout.close();

    std::cout << std::format( "Summary: {} successful", n_ok ) << std::endl;

    return n_bad ? 2 : 0;
}
