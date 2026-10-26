//-----------------------------------------------------------------------------------
// Shared helpers for the BesVis geometry export tools
// (TOF scintillators / TOF MRPC / MUC strips, see README.md)
//
// Every node-name formula and index convention is copied from the event display:
//   EventDisplay/BesVisLib/src/TofROOTGeo.cxx   SetNode() / SetPhysicalNode()
//   EventDisplay/BesVisLib/src/MucROOTGeo.cxx   SetNode() / SetPhysicalNode()
//
// The geometry is read exactly like the event display does, through the BOSS
// TGDMLProcessor (BesVisLib::SubDetectorROOTGeo::ReadGdml and its ROOTGeo variant are
// the same processor). Node names and copy numbers therefore match the display side,
// unlike TGeoManager::Import(), which resets every copy number to 0.
//-----------------------------------------------------------------------------------
#ifndef BESVIS_GEOMDUMP_COMMON_H
#define BESVIS_GEOMDUMP_COMMON_H

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
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

namespace gd {

    /// GDML directory, with the same meaning as the fPath of BesGeometry::InitFromGDML(fPath)
    inline std::string GdmlDir() {
        const char* r = getenv( "GDMLMANAGEMENTDATAROOT" );
        return r ? std::string( r ) + "/dat/" : std::string( "." );
    }

    /// printf-style formatting into a std::string
    inline std::string Fmt( const char* fmt, ... ) {
        char buf[512];
        va_list ap;
        va_start( ap, fmt );
        vsnprintf( buf, sizeof( buf ), fmt, ap );
        va_end( ap );
        return std::string( buf );
    }

    /// Read a GDML file the same way the event display does (setup name defaults to
    /// "Default"). Note: TGDMLProcessor does not call gGeoManager->SetTopVolume(), so we do it
    /// explicitly here to give gGeoManager->GetTopVolume() the same meaning as on the display
    /// side.
    inline SubDetectorROOTGeo* OpenGdml( const std::string& file,
                                         const char* setup = "Default" ) {
        if ( !gGeoManager ) gGeoManager = new TGeoManager( "BesGeo", "Bes geometry" );
        SubDetectorROOTGeo* sub = new SubDetectorROOTGeo();

        // Silence what the BOSS SAXProcessor prints to cout while reading the GDML,
        // so that the exported table stays clean.
        std::ostringstream sink;
        std::streambuf* old = std::cout.rdbuf( sink.rdbuf() );
        sub->ReadGdml( file.c_str(), setup );
        std::cout.rdbuf( old );

        if ( sub->GetTopVolume() )
        {
            if ( !gGeoManager->GetTopVolume() )
                gGeoManager->SetTopVolume( sub->GetTopVolume() );
        }
        else { printf( "ERROR: top volume not found, GDML = %s\n", file.c_str() ); }
        return sub;
    }

    /// Resolve a whole chain of node names (name syntax copied from BesVisLib's SetNode())
    inline bool Resolve( SubDetectorROOTGeo* sub, const std::vector<std::string>& names,
                         std::vector<TGeoNode*>& chain, std::string* bad = 0 ) {
        chain.clear();
        for ( size_t i = 0; i < names.size(); ++i )
        {
            TGeoNode* n = names[i].empty() ? 0 : sub->GetNode( names[i] );
            if ( !n )
            {
                if ( bad ) *bad = names[i];
                chain.clear();
                return false;
            }
            chain.push_back( n );
        }
        return true;
    }

    /// Global transformation matrix of a node chain (same as the accumulated matrix of
    /// a TGeoPhysicalNode)
    inline TGeoHMatrix ChainMatrix( const std::vector<TGeoNode*>& chain ) {
        TGeoHMatrix m;
        for ( size_t i = 0; i < chain.size(); ++i ) m.Multiply( chain[i]->GetMatrix() );
        return m;
    }

    /// The 8 global vertices of a TGeoArb8 (which also covers TGeoTrap/TGeoGtra).
    /// The vertex order and the choice of local z are exactly those of
    /// TofROOTGeo::Init2DGeometry():
    ///   i = 0..3 -> local z = -Dz ; i = 4..7 -> local z = +Dz
    /// so that the 2D polygons of the display side can be reproduced directly:
    ///   XY : ( P[j] + P[j+4] ) / 2     (j = 0..3)
    ///   ZR : ( P[iSeq[2i]] + P[iSeq[2i+1]] ) / 2 , iSeq = {0,3,1,2,5,6,4,7}
    inline bool Arb8Vertices( const std::vector<TGeoNode*>& chain, double v[8][3] ) {
        TGeoShape* shape = chain.back()->GetVolume()->GetShape();
        TGeoArb8* arb    = dynamic_cast<TGeoArb8*>( shape );
        if ( !arb ) return false;

        TGeoHMatrix m      = ChainMatrix( chain );
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

    /// The 8 global vertices of an element (general version).
    ///   TGeoArb8 (which also covers TGeoTrap/TGeoGtra): read fXY[0..7] directly, local
    ///                                                   z = -/+dz, exactly like BesVisLib
    ///                                                   (exact)
    ///   TGeoTrd2                                     : built from dx1/dx2/dy1/dy2/dz (exact)
    ///   anything else (TGeoBBox/CompositeShape/Tube...): bounding-box corners (exact=false)
    /// Vertex order is always: low-z face i=0..3, high-z face i=4..7, i and i+4 belong to the
    /// same edge; inside a face the order is (-x,-y) -> (-x,+y) -> (+x,+y) -> (+x,-y), i.e.
    /// the same rule as the Arb8 order.
    inline bool ShapeVertices( const std::vector<TGeoNode*>& chain, double v[8][3],
                               std::string* shapeClass = 0, bool* exact = 0 ) {
        TGeoShape* s = chain.back()->GetVolume()->GetShape();
        if ( shapeClass ) *shapeClass = s->ClassName();
        if ( exact ) *exact = true;

        TGeoHMatrix m = ChainMatrix( chain );
        double loc[8][3];
        const double sx[4] = { -1, -1, 1, 1 }; // sign of x of the corners inside a face
        const double sy[4] = { -1, 1, 1, -1 }; // sign of y of the corners inside a face

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
            const double X[2] = { trd->GetDx1(),
                                  trd->GetDx2() }; // half x of the low/high z face
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
            if ( exact ) *exact = false;
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

} // namespace gd

#endif // BESVIS_GEOMDUMP_COMMON_H
