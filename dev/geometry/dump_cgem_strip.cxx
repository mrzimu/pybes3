//-----------------------------------------------------------------------------------
// Export the *analytic parameters* of the CGEM X strips and V strips (no polygon
// vertices: only the quantities from which a strip can be solved)
//
//   The event display (EventDisplay/BesVisLib/src/CgemROOTGeo.cxx + Cgem2DStrip.cxx)
//   and the reconstruction (Cgem/CgemGeomSvc) use the same parametric model:
//
//   source 1 (layer parameters): $CGEMGEOMSVCROOT/dat/cgem_model_<N>_default.txt
//      read like CgemGeomSvc::initGeom() (CgemGeomSvc.cxx:227-300)
//      R_Layer L_Layer N_Sheet W_Sheet A_Stero W_Pitch_X W_Pitch_V W_Strip_X W_Strip_V
//      N_Channel_Phi N_Channel_V Phi_start1 Phi_start2 dX_start1 dX_start2 dV_start1
//      dV_start2 Gap_D Orientation
//   source 2 (radius of the strip shell): Anode_X_Strip_solid<L> / Anode_V_Strip_solid<L>
//      (G4Tubs) inside $GDMLMANAGEMENTDATAROOT/dat/Cgem.gdml
//      rmin = inner radius of the cylindrical shell holding the strips; it equals
//      getInnerROfAnodeCu2() (X strips) and getInnerROfAnode() (V strips) of CgemGeomSvc;
//      z = full length of that layer, cross checkable against L_Layer
//
//   From those, the plane constants are computed as in the CgemGeoReadoutPlane constructor
//   (CgemGeoReadoutPlane.cxx:20-80):
//      RX, RV           = radii of the X strips / V strips
//      Rmid             = (RX+RV)/2               (mean radius of the unfolded plane)
//      Xmin, Width      = Phimin*Rmid, RX*2pi/N_Sheet    (sheet rectangle, arc length mm)
//      Zmin, Length     = -L_Layer/2, L_Layer
//      XPitch, VPitch, WStrip_X, WStrip_V, Alpha (stereo angle in degrees), K = sign(Alpha)
//      NX, NV           = N_Channel_{Phi,V} / N_Sheet    (number of strips per sheet)
//      Xmin_strip       = (2pi*Rmid - N_Channel_Phi*XPitch)/(2*N_Sheet) * RX/Rmid
//      Vtot             = NX*XPitch*cos + L*|sin|
//      Vmin             = (Vtot - NV*VPitch)/2,  Vmax = Vmin + NV*VPitch
//
//   Per-strip quantities (one row per strip):
//      X strip: centre azimuth phi = (Xmin_strip + (strip+0.5)*XPitch + Xmin)/Rmid
//               centre arc length x = phi*Rmid ; z runs from zmin to zmin+length
//               (along z, through the whole sheet)
//               -> (RX, WStrip_X) then locate the strip
//      V strip: centre V = Vmin + (strip+0.5)*VPitch
//               in the unfolded plane (x = phi*Rmid, z) the strip is a straight line
//                 V = (x - x0)*cos(alpha) - (z - zref)*sin(alpha)
//                 zref = (K<0) ? zmin : zmin+length
//               where x0 is the origin of the V frame (arc length, column x0 in the table),
//               taken from the display side:
//                 x0 = phiFromXID(0)*Rmid - WStrip_X/2  (~= start of the sensitive area,
//                                                         slightly inside the sheet edge)
//               getZFromXV() of the service uses localX = X - m_Xmin_strip; the two
//               origins differ by only (XPitch-WStrip_X)/2 = 0.04 mm
//               (measured: the end points satisfy the formula above to 1e-9)
//               The strip is clipped to the x sensitive rectangle (a bit smaller than the
//               sheet, ~0.8 mm on each side)
//                 [x0, x0 + (nx-1)*XPitch + WStrip_X] x [zmin, zmin+length]
//               (measured: all 12234 end points lie exactly on the boundary of that
//                rectangle)
//               The intersection end points (phis,zs)-(phie,ze) and the strip length
//               striplen are given directly here; the formulas are identical to
//               CgemVStripCalculator::getStartPointFromV/getEndPointFromV
//               (Cgem2DStrip.cxx:429-521; the end case is decided by the different
//                clipping-edge branches)
//
//   Note (the export gives the true values, never the drawing-only quantities of the
//   display side):
//      * the display hard-codes the strip thickness to 0.1 mm and discretises V strips
//        into polylines every 30 mm -- these are rendering parameters only and are not
//        exported here; use wstrip_x / wstrip_v for the strip width.
//      * the X strip centre phi is converted with the plane Rmid (same as getPhiFromXID
//        on the display side).
//
//   Output: gid,layer,sheet,strip_type,strip,r,phi0,dphi,z0,dz,width,thick
//     These are exactly the columns (and the units) of the `cgem_strip` ntuple written
//     by ExportCgemGeomAlg of dev/boss-algs, which reads the same model through the Gaudi
//     service:
//       strip_type : 0 = X strip, 1 = V strip (same convention as cgem_elec_table.npz of
//                    dev/export-cgem-tables.py)
//       r          : radius of the strip (x -> RX, v -> RV), in cm
//       phi0       : azimuth of the centre line at the *most negative z* end (rad)
//       dphi       : total signed azimuth change from that end towards +z
//       z0         : most negative z of the centre line (cm)
//       dz         : total z change towards +z (>= 0), in cm
//       width      : transverse width of the strip (cm); x strip = arc direction,
//                    v strip = perpendicular direction
//       thick      : *radial thickness* of the strip (cm) = rmax-rmin of the strip shell
//                    (Anode_X_Strip_solid<L> / Anode_V_Strip_solid<L> in the GDML, i.e.
//                     the thickness of the Cu electrode of that layer)
//     (r, phi0, dphi, z0, dz) give the centre line, (width, thick) give the cross section
//     -> the strip is uniquely reconstructed; X strips run along z, hence dphi = 0 and
//     dz = full sheet length.
//     (centre-line length = sqrt((dphi*r)^2+dz^2), computed when needed, not listed)
//
//   Usage: ./dump_cgem_strip           > cgem_strip.csv
//          ./dump_cgem_strip --model 6 (default 6; selects cgem_model_6_default.txt)
//-----------------------------------------------------------------------------------
#include <cmath>
#include <cstdarg>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

// ============================== small helpers ==============================
static std::string Fmt( const char* fmt, ... ) {
    char buf[512];
    va_list ap;
    va_start( ap, fmt );
    vsnprintf( buf, sizeof( buf ), fmt, ap );
    va_end( ap );
    return std::string( buf );
}

/// split a line into whitespace-separated tokens
static std::vector<std::string> Tokens( const std::string& line ) {
    std::vector<std::string> t;
    std::istringstream is( line );
    std::string w;
    while ( is >> w ) t.push_back( w );
    return t;
}

static bool IsNumber( const std::string& s ) {
    if ( s.empty() ) return false;
    char* end = 0;
    strtod( s.c_str(), &end );
    return end && *end == '\0';
}

/// extract an attribute from an element such as
/// "<tube ... name=\"xxx\" rmin=\"1.2\" .../>"
static bool Attr( const std::string& elem, const std::string& key, double& out ) {
    std::string pat = key + "=\"";
    size_t p        = elem.find( pat );
    if ( p == std::string::npos ) return false;
    p += pat.size();
    size_t q = elem.find( '"', p );
    if ( q == std::string::npos ) return false;
    out = atof( elem.substr( p, q - p ).c_str() );
    return true;
}

// ============================== data structures ==============================
struct Layer {
    int index;
    double rLayer, lenLayer;
    int nSheet;
    double wSheet; // W_Sheet from the file (informational only, the service does not use it)
    double aStereoDeg; // stereo angle (degrees)
    double pitchX, pitchV, wStripX, wStripV;
    int nChannelX, nChannelV;
    double phiStart[2];
};

struct StripSolid // from the GDML: Anode_{X,V}_Strip_solid<L>
{
    bool found      = false;
    double rmin     = 0.0;
    double rmax     = 0.0;
    double z        = 0.0;
    double deltaphi = 0.0;
    std::string name;
};

struct Plane {
    int layer, sheet;
    double rx, rv, rmid;
    double xmin, width, zmin, length;
    double alphaDeg, alpha, k;
    double xpitch, vpitch, wstripX, wstripV;
    int nx, nv;
    double xminStrip;
    double vtot, vmin, vmax;
    double zref;      // reference end of the V line formula
    double clipXmin;  // xmin handed to the V calculator by the display (= phiFromXID(0)*Rmid
                      // - WStrip_X/2)
    double clipWidth; // width handed to the V calculator by the display (= arc length span of
                      // the X sensitive area + WStrip_X)
};

// ============ V strip end point formulas (copied from CgemVStripCalculator) ============
// status codes
enum { NORMAL = 0, INVALID = -1 };

struct VCalc {
    double R, len, wid, ang, xmin, zmin, pit;

    VCalc( double r, double l, double w, double a, double x0, double z0, double p )
        : R( r ), len( l ), wid( w ), ang( a ), xmin( x0 ), zmin( z0 ), pit( p ) {
        while ( ang > M_PI / 2 ) ang -= M_PI;
        while ( ang < -M_PI / 2 ) ang += M_PI;
    }

    /// copied from getStartPointFromV() (Cgem2DStrip.cxx:429)
    int Start( double v, double& phi, double& z ) const {
        double x_temp = v / std::cos( ang );
        double z_temp;
        if ( ang < 0 )
        {
            if ( x_temp < 0 ) return INVALID;
            if ( x_temp <= wid )
            {
                phi = ( x_temp + xmin ) / R;
                z   = zmin;
                return NORMAL;
            }
            z_temp = ( x_temp - wid ) / std::tan( -ang );
            if ( z_temp <= len )
            {
                phi = ( xmin + wid ) / R;
                z   = z_temp + zmin;
                return NORMAL;
            }
        }
        else
        {
            if ( x_temp < 0 ) return INVALID;
            if ( x_temp <= wid )
            {
                phi = ( x_temp + xmin ) / R;
                z   = zmin + len;
                return NORMAL;
            }
            z_temp = ( x_temp - wid ) / std::tan( ang );
            if ( z_temp <= len )
            {
                phi = ( xmin + wid ) / R;
                z   = zmin + len - z_temp;
                return NORMAL;
            }
        }
        return INVALID;
    }

    /// copied from getEndPointFromV() (Cgem2DStrip.cxx:476)
    int End( double v, double& phi, double& z ) const {
        double x_temp = v / std::cos( ang );
        double z_temp;
        if ( ang < 0 )
        {
            if ( x_temp < 0 ) return INVALID;
            z_temp = x_temp / std::tan( -ang );
            if ( z_temp <= len )
            {
                phi = xmin / R;
                z   = z_temp + zmin;
                return NORMAL;
            }
            if ( x_temp - len * std::tan( -ang ) <= wid )
            {
                phi = ( x_temp - len * std::tan( -ang ) + xmin ) / R;
                z   = len + zmin;
                return NORMAL;
            }
        }
        else
        {
            if ( x_temp < 0 ) return INVALID;
            z_temp = x_temp / std::tan( ang );
            if ( z_temp <= len )
            {
                phi = xmin / R;
                z   = zmin + len - z_temp;
                return NORMAL;
            }
            if ( x_temp - len * std::tan( ang ) <= wid )
            {
                phi = ( x_temp - len * std::tan( ang ) + xmin ) / R;
                z   = zmin;
                return NORMAL;
            }
        }
        return INVALID;
    }

    double Length( double v ) const {
        double p1 = 0, z1 = 0, p2 = 0, z2 = 0;
        Start( v, p1, z1 );
        End( v, p2, z2 );
        return std::sqrt( R * R * ( p1 - p2 ) * ( p1 - p2 ) + ( z1 - z2 ) * ( z1 - z2 ) );
    }
};

// ============================== output ==============================
/// One strip per row: gid,layer,sheet,strip_type,strip,r,phi0,dphi,z0,dz,width,thick
/// All lengths are in cm (the plane constants above are in mm).
static void PrintStripRow( int gid, int layer, int sheet, int stripType, int strip, double r,
                           double phi0, double dphi, double z0, double dz, double width,
                           double thick ) {
    printf( "%d,%d,%d,%d,%d,%.6f,%.8f,%.8f,%.6f,%.6f,%.6f,%.6f\n", gid, layer, sheet,
            stripType, strip, r, phi0, dphi, z0, dz, width, thick );
}

int main( int argc, char** argv ) {
    int model = 6;
    for ( int i = 1; i < argc; ++i )
    {
        if ( strcmp( argv[i], "--model" ) == 0 && i + 1 < argc ) model = atoi( argv[++i] );
    }

    const char* envCm  = getenv( "CGEMGEOMSVCROOT" );
    const char* envGdm = getenv( "GDMLMANAGEMENTDATAROOT" );
    if ( !envCm || !envGdm )
    {
        fprintf( stderr, "[error] CGEMGEOMSVCROOT and/or GDMLMANAGEMENTDATAROOT is not set "
                         "(they come from the BOSS environment setup)\n" );
        return 1;
    }
    std::string paramFile = Fmt( "%s/dat/cgem_model_%d_default.txt", envCm, model );
    std::string gdmlFile  = Fmt( "%s/dat/Cgem.gdml", envGdm );

    // ---------- 1) read the layer parameter file ----------
    std::ifstream fin( paramFile.c_str() );
    if ( !fin )
    {
        fprintf( stderr, "[error] cannot open the parameter file: %s\n", paramFile.c_str() );
        return 1;
    }
    std::vector<std::string> lines;
    {
        std::string l;
        while ( std::getline( fin, l ) ) lines.push_back( l );
    }

    int nLayer = 0, nFoil = 0, nSheetMax = 0;
    std::vector<Layer> layers;
    for ( size_t i = 0; i < lines.size(); ++i )
    {
        if ( lines[i].find( "N_CgemLayer" ) == std::string::npos ) continue;
        for ( size_t j = i + 1; j < lines.size(); ++j )
        {
            std::vector<std::string> t = Tokens( lines[j] );
            if ( t.size() >= 2 && IsNumber( t[0] ) && IsNumber( t[1] ) )
            {
                nLayer = atoi( t[0].c_str() );
                nFoil  = atoi( t[1].c_str() );
                // the nLayer lines that follow are the layer parameters (19 fields)
                size_t k = j;
                while ( (int)layers.size() < nLayer && ++k < lines.size() )
                {
                    std::vector<std::string> d = Tokens( lines[k] );
                    if ( d.size() < 19 || !IsNumber( d[0] ) ) continue;
                    Layer L;
                    L.index       = (int)layers.size();
                    L.rLayer      = atof( d[0].c_str() );
                    L.lenLayer    = atof( d[1].c_str() );
                    L.nSheet      = atoi( d[2].c_str() );
                    L.wSheet      = atof( d[3].c_str() );
                    L.aStereoDeg  = atof( d[4].c_str() );
                    L.pitchX      = atof( d[5].c_str() );
                    L.pitchV      = atof( d[6].c_str() );
                    L.wStripX     = atof( d[7].c_str() );
                    L.wStripV     = atof( d[8].c_str() );
                    L.nChannelX   = atoi( d[9].c_str() );
                    L.nChannelV   = atoi( d[10].c_str() );
                    L.phiStart[0] = atof( d[11].c_str() );
                    L.phiStart[1] = atof( d[12].c_str() );
                    layers.push_back( L );
                    if ( L.nSheet > nSheetMax ) nSheetMax = L.nSheet;
                }
                break;
            }
        }
        break;
    }
    if ( (int)layers.size() != nLayer || nLayer <= 0 )
    {
        fprintf( stderr,
                 "[error] cannot parse the layer parameters (%s): nLayer=%d, read %zu\n",
                 paramFile.c_str(), nLayer, layers.size() );
        return 1;
    }

    // ---------- 2) take the strip shell radii from the GDML (Anode_{X,V}_Strip_solid<L>) ----
    std::vector<StripSolid> solidX( nLayer ), solidV( nLayer );
    {
        std::ifstream gin( gdmlFile.c_str() );
        if ( !gin )
        {
            fprintf( stderr, "[error] cannot open the GDML: %s\n", gdmlFile.c_str() );
            return 1;
        }
        std::string l;
        while ( std::getline( gin, l ) )
        {
            if ( l.find( "Anode_X_Strip_solid" ) == std::string::npos &&
                 l.find( "Anode_V_Strip_solid" ) == std::string::npos )
                continue;
            if ( l.find( "<tube" ) == std::string::npos ) continue;
            bool isX        = ( l.find( "Anode_X_Strip_solid" ) != std::string::npos );
            std::string tag = isX ? "Anode_X_Strip_solid" : "Anode_V_Strip_solid";
            int lay         = -1;
            for ( int i = 0; i < nLayer; ++i )
                if ( l.find( tag + Fmt( "%d", i ) + "\"" ) != std::string::npos ) lay = i;
            if ( lay < 0 ) continue;
            StripSolid s;
            s.found = Attr( l, "rmin", s.rmin ) && Attr( l, "rmax", s.rmax );
            Attr( l, "z", s.z );
            Attr( l, "deltaphi", s.deltaphi );
            s.name                         = tag + Fmt( "%d", lay );
            ( isX ? solidX : solidV )[lay] = s;
        }
    }

    // ---------- 3) compute the plane constants with the CgemGeoReadoutPlane formulas ----
    std::vector<Plane> planes;
    for ( int i = 0; i < nLayer; ++i )
    {
        const Layer& L = layers[i];
        if ( !solidX[i].found || !solidV[i].found )
        {
            fprintf( stderr,
                     "[error] layer %d: strip shells not found in the GDML (%s / %s)\n", i,
                     solidX[i].name.c_str(), solidV[i].name.c_str() );
            return 1;
        }
        double rX    = solidX[i].rmin;
        double rV    = solidV[i].rmin;
        double rmid  = 0.5 * ( rX + rV );
        double width = rX * 2.0 * M_PI / L.nSheet; // sheet arc length (service formula)
        for ( int j = 0; j < L.nSheet; ++j )
        {
            Plane p;
            p.layer     = i;
            p.sheet     = j;
            p.rx        = rX;
            p.rv        = rV;
            p.rmid      = rmid;
            p.width     = width;
            p.zmin      = -0.5 * L.lenLayer;
            p.length    = L.lenLayer;
            p.alphaDeg  = L.aStereoDeg;
            p.alpha     = L.aStereoDeg / 180.0 * M_PI;
            p.k         = ( L.aStereoDeg >= 0 ) ? 1.0 : -1.0;
            p.xpitch    = L.pitchX;
            p.vpitch    = L.pitchV;
            p.wstripX   = L.wStripX;
            p.wstripV   = L.wStripV;
            p.nx        = L.nChannelX / L.nSheet;
            p.nv        = L.nChannelV / L.nSheet;
            p.xmin      = L.phiStart[j] * rmid; // m_Xmin
            p.xminStrip = ( 2.0 * M_PI * rmid - L.nChannelX * p.xpitch ) / ( 2.0 * L.nSheet ) *
                          rX / rmid; // dX_start_strip
            p.vtot = p.nx * p.xpitch * std::cos( p.alpha ) +
                     L.lenLayer * std::fabs( std::sin( p.alpha ) );
            p.vmin = ( p.vtot - p.nv * p.vpitch ) / 2.0;
            p.vmax = p.vmin + p.nv * p.vpitch;
            p.zref = ( p.k < 0 ) ? p.zmin : p.zmin + p.length; // z0 of getZFromXV

            // the two quantities the display hands to the V calculator
            // (CgemROOTGeo::InitGeometry)
            double phiFirst = ( p.xminStrip + 0.5 * p.xpitch + p.xmin ) / rmid;
            double phiLast  = ( p.xminStrip + ( p.nx - 0.5 ) * p.xpitch + p.xmin ) / rmid;
            p.clipXmin      = phiFirst * rmid - 0.5 * p.wstripX;
            p.clipWidth     = ( phiLast - phiFirst ) * rmid + p.wstripX;

            planes.push_back( p );
        }
    }

    // cross checks of the layer constants against the GDML
    for ( int i = 0; i < nLayer; ++i )
        fprintf( stderr,
                 "[info] layer%d cross check: L_Layer=%.1f vs GDML X shell z=%.4f (same layer "
                 "length); XPitch=%.4f vs GDML dphi*rmin=%.4f; V shell dphi=%.1f r=%.4f..%.4f "
                 "z(slice)=%.4f\n",
                 i, layers[i].lenLayer, solidX[i].z, layers[i].pitchX,
                 solidX[i].deltaphi / 180.0 * M_PI * solidX[i].rmin, solidV[i].deltaphi,
                 solidV[i].rmin, solidV[i].rmax, solidV[i].z );

    // ---------- 4) output the per-strip parameters ----------
    printf( "gid,layer,sheet,strip_type,strip,r,phi0,dphi,z0,dz,width,thick\n" );

    int gid = 0;
    int nX = 0, nV = 0, nVBad = 0, nLenDiff = 0;
    double maxLenDiff = 0.0;

    for ( size_t ip = 0; ip < planes.size(); ++ip )
    {
        const Plane& p = planes[ip];
        VCalc calc( p.rmid, p.length, p.clipWidth, p.alpha, p.clipXmin, p.zmin, p.vpitch );

        // ---- X strips: they run through z, only the centre phi is needed ----
        for ( int s = 0; s < p.nx; ++s )
        {
            double x =
                ( s + 0.5 ) * p.xpitch + p.xminStrip + p.xmin; // getCentralXFromXID + m_Xmin
            double phi = x / p.rmid;                           // getPhiFromXID
            // X strips run along z: dphi = 0, dz = full sheet length; thick = shell radial
            // thickness
            const double thick = ( solidX[p.layer].rmax - solidX[p.layer].rmin ) / 10.0;
            PrintStripRow( gid, p.layer, p.sheet, 0, s, p.rx / 10.0, phi, 0.0, p.zmin / 10.0,
                           p.length / 10.0, p.wstripX / 10.0, thick );
            ++gid;
            ++nX;
        }

        // ---- V strips: centre V plus the intersections with the sheet ----
        for ( int s = 0; s < p.nv; ++s )
        {
            double v   = p.vmin + ( s + 0.5 ) * p.vpitch; // getCentralVFromVID
            double ph1 = 0, z1 = 0, ph2 = 0, z2 = 0;
            int ok1 = calc.Start( v, ph1, z1 );
            int ok2 = calc.End( v, ph2, z2 );
            if ( ok1 != NORMAL || ok2 != NORMAL )
            {
                ++nVBad; // outside the sheet: the display does not draw it either
                continue;
            }
            // independent cross check: the three-branch strip length formula of the service,
            // getVStripLength()
            double len = calc.Length( v );
            double Lz  = v / std::fabs( std::sin( p.alpha ) );
            double len2;
            if ( Lz <= p.length ) len2 = Lz / std::cos( p.alpha );
            else if ( v / std::cos( p.alpha ) <= p.nx * p.xpitch )
                len2 = p.length / std::cos( p.alpha );
            else
                len2 = ( p.vtot - v ) / std::fabs( std::sin( p.alpha ) * std::cos( p.alpha ) );
            if ( std::fabs( len - len2 ) > 1e-6 )
            {
                ++nLenDiff;
                if ( std::fabs( len - len2 ) > maxLenDiff )
                    maxLenDiff = std::fabs( len - len2 );
            }

            // phi0/z0 take the end of the centre line with the most negative z; dphi/dz are
            // the extensions along the centre line towards +z
            double phi0 = 0, z0 = 0, phZ = 0, zZ = 0;
            if ( z1 <= z2 )
            {
                phi0 = ph1;
                z0   = z1;
                phZ  = ph2;
                zZ   = z2;
            }
            else
            {
                phi0 = ph2;
                z0   = z2;
                phZ  = ph1;
                zZ   = z1;
            }
            const double thick = ( solidV[p.layer].rmax - solidV[p.layer].rmin ) / 10.0;
            PrintStripRow( gid, p.layer, p.sheet, 1, s, p.rv / 10.0, phi0, phZ - phi0,
                           z0 / 10.0, ( zZ - z0 ) / 10.0, p.wstripV / 10.0, thick );
            ++gid;
            ++nV;
        }
    }

    fprintf( stderr,
             "[info] parameter file %s, GDML %s, %d layers / %zu readout planes\n"
             "[info] %d X strips + %d V strips (%d V strips outside the sheet / invalid, "
             "not drawn by the display)\n"
             "[info] strip length cross-check vs CgemGeoReadoutPlane::getVStripLength():"
             " at most %.3f mm over %d strips\n",
             paramFile.c_str(), gdmlFile.c_str(), nLayer, planes.size(), nX, nV, nVBad,
             maxLenDiff, nLenDiff );
    return 0;
}
