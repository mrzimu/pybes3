#include "ROOTGeo/SubDetectorROOTGeo.h"

#include <TGeoArb8.h>
#include <TGeoBBox.h>
#include <TGeoManager.h>
#include <TGeoMatrix.h>
#include <TGeoNode.h>
#include <TGeoShape.h>
#include <TGeoTrd2.h>
#include <TGeoVolume.h>

#include <format>
#include <fstream>
#include <string>

constexpr int N_PART = 3;

constexpr int N_LAYERS_BARREL = 2;
constexpr int N_SCINT_BARREL  = 88;

constexpr int N_MODULES_ENDCAP = 36;
constexpr int N_STRIPS_ENDCAP  = 12;

constexpr int CONTAINER_NODE_NB = 0;
constexpr int CHAMBER_NODE_NB   = 6;
constexpr int BOARD1_NODE_NB    = 30;

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

bool shape_vertices( const std::vector<TGeoNode*>& chain, double v[8][3],
                     std::string& shapeClass, bool& exact ) {
    TGeoShape* s = chain.back()->GetVolume()->GetShape();
    shapeClass   = s->ClassName();
    exact        = true;

    TGeoHMatrix m = chain_matrix( chain );
    double loc[8][3];
    const double sx[4] = { -1, -1, 1, 1 };
    const double sy[4] = { -1, 1, 1, -1 };

    if ( TGeoArb8* arb = dynamic_cast<TGeoArb8*>( s ) )
    {
        const Double_t* lv = arb->GetVertices();
        for ( int i = 0; i < 8; ++i )
        {
            loc[i][0] = lv[2 * i];
            loc[i][1] = lv[2 * i + 1];
            loc[i][2] = ( i < 4 ? -arb->GetDz() : arb->GetDz() );
        }
    }
    else if ( TGeoTrd2* trd = dynamic_cast<TGeoTrd2*>( s ) )
    {
        const double X[2] = { trd->GetDx1(), trd->GetDx2() };
        const double Y[2] = { trd->GetDy1(), trd->GetDy2() };
        for ( int f = 0; f < 2; ++f )
            for ( int k = 0; k < 4; ++k )
            {
                loc[4 * f + k][0] = sx[k] * X[f];
                loc[4 * f + k][1] = sy[k] * Y[f];
                loc[4 * f + k][2] = ( f == 0 ? -trd->GetDz() : trd->GetDz() );
            }
    }
    else
    {
        TGeoBBox* b = dynamic_cast<TGeoBBox*>( s );
        if ( !b ) return false;
        exact             = false;
        const Double_t* o = b->GetOrigin();
        for ( int f = 0; f < 2; ++f )
            for ( int k = 0; k < 4; ++k )
            {
                loc[4 * f + k][0] = o[0] + sx[k] * b->GetDX();
                loc[4 * f + k][1] = o[1] + sy[k] * b->GetDY();
                loc[4 * f + k][2] = o[2] + ( f == 0 ? -b->GetDZ() : b->GetDZ() );
            }
    }

    for ( int i = 0; i < 8; ++i )
    {
        Double_t mas[3];
        m.LocalToMaster( loc[i], mas );
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

    auto gdml_file = std::string( r ) + "/dat/Tof_mrpc.gdml";

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

    // Loop MRPC
    int gid  = ( 88 + 48 ) * 2; // scintilator offset for MRPC
    int n_ok = 0, n_bad = 0, n_approx = 0;

    for ( int part : { 3, 4 } )
    {
        const int ipart = part == 3 ? 0 : 1;
        auto node_part  = sub.GetTopVolume()->GetNode( ipart );

        for ( int module = 0; module < N_MODULES_ENDCAP; module++ )
        {
            int mIdx;
            if ( part == 3 ) mIdx = ( module % 2 == 0 ) ? 0 : 3;
            else mIdx = ( module % 2 == 0 ) ? 1 : 2;

            std::vector<std::string> base;
            base.push_back( std::format( "pv_logical_container_m{}_{}", mIdx, module ) );
            base.push_back(
                std::format( "pv_logical_gasContainer_m{}_{}", mIdx, CONTAINER_NODE_NB ) );
            base.push_back( std::format( "pv_logical_bareChamber_{}", CHAMBER_NODE_NB ) );
            base.push_back( std::format( "pv_logical_pcbBoard1_{}", BOARD1_NODE_NB ) );

            std::vector<TGeoNode*> base_chain;
            std::string bad;
            if ( !resolve( sub, base, base_chain, bad ) )
            {
                n_bad++;
                std::cerr << "ERROR: Could not resolve base chain for module " << module
                          << " in ipart " << ipart << ". Bad node: " << bad << std::endl;
                abort();
            }
            base_chain.insert( base_chain.begin(), node_part );

            for ( int strip = 0; strip < N_STRIPS_ENDCAP; strip++ )
            {
                std::vector<std::string> names = base;
                names.push_back( std::format( "pv_logical_strip_{}_{}",
                                              ( N_STRIPS_ENDCAP - 1 ) - strip, strip ) );

                std::vector<TGeoNode*> chain;
                if ( !resolve( sub, names, chain, bad ) )
                {
                    n_bad++;
                    std::cerr << "ERROR: Could not resolve chain for strip " << strip
                              << " in module " << module << " of ipart " << ipart
                              << ". Bad node: " << bad << std::endl;
                    abort();
                }
                chain.insert( chain.begin(), node_part );

                double v[8][3];
                std::string shape;
                bool exact = true;

                if ( !shape_vertices( chain, v, shape, exact ) )
                {
                    n_bad++;
                    std::cerr << "ERROR: Could not get shape vertices for strip " << strip
                              << " in module " << module << " of ipart " << ipart
                              << ". Bad node: " << bad << std::endl;
                    abort();
                }
                if ( !exact ) n_approx++;

                TGeoHMatrix m    = chain_matrix( chain );
                const double* tr = m.GetTranslation();
                double pos[3]    = { tr[0], tr[1], tr[2] };

                fout << gid << "," << part << "," << module << "," << strip << ",";
                for ( int i = 0; i < 8; i++ )
                {
                    for ( int j = 0; j < 3; j++ )
                        fout << v[i][j] / 10.0 << ( ( i == 7 && j == 2 ) ? "\n" : "," );
                }

                n_ok++;
                gid++;
            }
        }
    }

    fout.close();

    std::cout << std::format( "Summary: {} successful, {} bad, {} approximate\n", n_ok, n_bad,
                              n_approx );

    return ( n_bad || n_approx ) ? 2 : 0;
}
