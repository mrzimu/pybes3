#include "ROOTGeo/SubDetectorROOTGeo.h"

#include <TGeoArb8.h>
#include <TGeoBBox.h>
#include <TGeoManager.h>
#include <TGeoMatrix.h>
#include <TGeoNode.h>
#include <TGeoShape.h>
#include <TGeoVolume.h>

#include <format>
#include <fstream>
#include <string>

constexpr int N_PART = 3;

constexpr int N_LAYERS_BARREL = 2;
constexpr int N_SCINT_BARREL  = 88;

constexpr int N_LAYERS_ENDCAP = 1;
constexpr int N_SCINT_ENDCAP  = 48;

bool resolve( SubDetectorROOTGeo& sub, const std::vector<std::string>& names,
              std::vector<TGeoNode*>& chain, std::string& bad ) {
    chain.clear();
    for ( size_t i = 0; i < names.size(); ++i )
    {
        TGeoNode* n = names[i].empty() ? 0 : sub.GetNode( names[i] );
        if ( !n )
        {
            bad = names[i];
            chain.clear();
            return false;
        }
        chain.push_back( n );
    }
    return true;
}

/// Obtain global transformation matrix for a chain of TGeoNodes
TGeoHMatrix chain_matrix( const std::vector<TGeoNode*>& chain ) {
    TGeoHMatrix m;
    for ( size_t i = 0; i < chain.size(); ++i ) m.Multiply( chain[i]->GetMatrix() );
    return m;
}

/// Obtain the global coordinates of the vertices of a TGeoArb8 shape.
bool arb8_vertices( const std::vector<TGeoNode*>& chain, double v[8][3] ) {
    TGeoShape* shape = chain.back()->GetVolume()->GetShape();
    TGeoArb8* arb    = dynamic_cast<TGeoArb8*>( shape );
    if ( !arb ) return false;

    TGeoHMatrix m      = chain_matrix( chain );
    const Double_t* lv = arb->GetVertices();
    for ( int i = 0; i < 8; ++i )
    {
        Double_t loc[3] = { lv[2 * i], lv[2 * i + 1],
                            ( i < 4 ? -arb->GetDz() : arb->GetDz() ) };
        Double_t mas[3];
        m.LocalToMaster( loc, mas );
        v[i][0] = mas[0];
        v[i][1] = mas[1];
        v[i][2] = mas[2];
    }
    return true;
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

    auto gdml_file = std::string( r ) + "/dat/Tof.gdml";

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

    // Output file
    std::ofstream fout( argv[1] );
    if ( !fout.is_open() )
    {
        std::cerr << "ERROR: Could not open output file " << argv[1] << std::endl;
        return 1;
    }

    // Table header
    fout << "gid,part,layer_or_module,phi_or_strip,";
    for ( int i = 0; i < 8; i++ )
    {
        fout << "x" << i << ",";
        fout << "y" << i << ",";
        fout << "z" << i << ( i == 7 ? "" : "," );
    }
    fout << std::endl;

    // Loop scintillators
    int gid  = 0;
    int n_ok = 0, n_bad = 0, n_no_arb8 = 0;
    for ( int part = 0; part < N_PART; part++ )
    {
        int ipart      = ( part == 1 ) ? 2 : ( ( part == 2 ) ? 1 : 0 ); // 1->2, 2->1, 0->0
        auto node_part = sub.GetTopVolume()->GetNode( ipart );

        int n_layers = ( part == 1 ) ? N_LAYERS_BARREL : N_LAYERS_ENDCAP;
        int n_scints = ( part == 1 ) ? N_SCINT_BARREL : N_SCINT_ENDCAP;

        for ( int layer = 0; layer < n_layers; layer++ )
        {
            for ( int scint = 0; scint < n_scints; scint++ )
            {
                std::vector<std::string> names;
                if ( part == 1 )
                {
                    int idx = ( 2 * N_SCINT_BARREL * 3 - 1 ) -
                              ( layer * N_SCINT_BARREL + scint ) * 3;

                    names.push_back( std::format( "pv_logicalPVFBr{}_{}", layer + 1, idx ) );
                    names.push_back( std::format( "pv_logicalAlBr{}_0", layer + 1 ) );
                    names.push_back( std::format( "pv_logicalScinBr{}_0", layer + 1 ) );
                }
                else
                {
                    const char* side = ( part == 0 ) ? "East" : "West";
                    int idx          = ( 2 * N_SCINT_ENDCAP - 1 ) - scint * 2;
                    names.push_back( std::format( "pv_logicalPVFEc{}_{}", side, idx ) );
                    names.push_back( std::format( "pv_logicalAlEc{}_0", side ) );
                    names.push_back( std::format( "pv_logicalScinEc{}_0", side ) );
                }

                std::vector<TGeoNode*> chain;
                std::string bad;
                if ( !resolve( sub, names, chain, bad ) )
                {
                    n_bad++;
                    std::cerr << "ERROR: Could not resolve chain for scintillator " << scint
                              << " in layer " << layer << " of part " << part
                              << ". Bad node: " << bad << std::endl;
                    abort();
                }
                chain.insert( chain.begin(), node_part );

                double v[8][3];
                if ( !arb8_vertices( chain, v ) )
                {
                    n_no_arb8++;
                    std::cerr << "ERROR: Could not obtain ARB8 vertices for scintillator "
                              << scint << " in layer " << layer << " of part " << part
                              << std::endl;
                    abort();
                }

                // Output vertices to file
                fout << gid << "," << part << "," << layer << "," << scint << ",";
                for ( int i = 0; i < 8; i++ )
                {
                    for ( int j = 0; j < 3; j++ )
                    { fout << v[i][j] / 10.0 << ( ( i == 7 && j == 2 ) ? "\n" : "," ); }
                }

                n_ok++;
                gid++;
            }
        }
    }

    std::cout << std::format( "Summary: {} scintillators processed successfully, {} failed to "
                              "resolve, {} failed to obtain ARB8 vertices\n",
                              n_ok, n_bad, n_no_arb8 );

    return ( n_bad || n_no_arb8 ) ? 2 : 0;
}
