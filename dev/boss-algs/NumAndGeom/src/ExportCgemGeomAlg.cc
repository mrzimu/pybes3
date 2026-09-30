//-----------------------------------------------------------------------------------
// Export the CGEM X-strip / V-strip geometry parameters straight from the BOSS
// service ICgemGeomSvc.
//
//   == The same columns as pybes3's `dump_cgem_strip --simple` ==
//      layer,sheet,strip_type,strip,r,phi0,dphi,z0,dz,width,thick
//
//   All data comes from CgemGeomSvc (the single parametrised model shared by
//   reconstruction / simulation / display); no text file is read and no GDML is
//   consulted:
//     - plane constants : CgemGeoReadoutPlane's getRX/getRV/getWidth/getZmin/getLength/
//                    getXPitch/getVPitch/getStereoAngle/getNXstrips/getNVstrips/
//                    getPhimin/getPhiMin_strip
//     - X-strip central phi : getPhiFromXID()      (not inline, links CgemGeomSvcLib)
//     - V-strip central V   : getCentralVFromVID() (inline)
//     - line of a V strip   : V = localX*cos(a) + (zref - zeta - zmin)*sin(a)
//                       (i.e. the formula of getVFromLocalXZ(); localX is measured
//                       from the centre of the first strip)
//     - sensitive rectangle : localX in [0, NX*XPitch], zeta in [0, L]
//                       (the same criterion as getVFromLocalXZ())
//     - strip width         : CgemGeoLayer::getWidthOfStripX()/getWidthOfStripV()
//     - strip thickness     : radial thickness of the read-out copper layer:
//                             X strips -> getOuterROfAnodeCu2()-getInnerROfAnodeCu2()  (Cu2)
//                             V strips -> getOuterROfAnodeCu1()-getInnerROfAnodeCu1()  (Cu1,
//                                         whose inner radius is getInnerROfAnode() = getRV())
//   The service has no ready-made "clip out the two end points" function, so the two
//   constraints above are solved analytically here (one solution per rectangle edge,
//   keeping the two intersections that fall inside the rectangle), and the result is
//   cross-checked against the service's own approximate formula getVStripLength();
//   the difference is reported in the log.
//
//   Output: NTuple "FILE1/cgem_strip" (written to a ROOT file via NTupleSvc)
//     strip_type : 0 = X strip, 1 = V strip (same convention as cgem_elec_table.npz in
//                  dev/export-cgem-tables.py)
//     r    : radius of the strip (X -> getRX(), V -> getRV())
//     phi0 : azimuth of the centre line at the **most negative z** end
//            (rad, global xy azimuth)
//     dphi : total signed azimuth change from that end along the centre line towards +z
//     z0   : most negative z of the centre line (mm); dz : total z change towards +z (>=0)
//     width: X strip = width along the arc direction; V strip = width perpendicular to
//            the strip
//     thick: radial thickness of the strip (mm)
//
//   Note: the length along the centre line is sqrt((dphi*r)^2+dz^2); it is not written out
//         (it follows from the other columns).
//
//   Run (see NumAndGeom/opts/ExportCgemGeom.txt):
//     ApplicationMgr.EvtSel = "NONE"; EvtMax = 1;
//     NTupleSvc.Output = { "FILE1 DATAFILE='...ref_cgem_geom.root' OPT='NEW' TYP='ROOT'" };
//     boss.exe <that opts file>
//-----------------------------------------------------------------------------------
#include <GaudiKernel/Algorithm.h>
#include <GaudiKernel/NTuple.h>
#include <GaudiKernel/SmartIF.h>

#include <CgemGeomSvc/CgemGeoLayer.h>
#include <CgemGeomSvc/CgemGeoReadoutPlane.h>
#include <CgemGeomSvc/ICgemGeomSvc.h>

#include <algorithm>
#include <cmath>
#include <vector>

namespace {

    /// One end point of a V strip (azimuth + z)
    struct EndPoint {
        double phi{ 0.0 };
        double z{ 0.0 };
    };

    /// Clip the centre line of a V strip to the sensitive rectangle and return its two
    /// end points (ordered by increasing z).
    /// Rectangle: localX in [0, W] (W = NX*XPitch, measured from the centre of the first
    /// strip), zeta in [0, L] (measured from Zmin)
    /// Line: V = localX*cos(a) + S*sin(a), with S = zref - zeta - zmin
    ///       (zref = zmax when k>0 -> S = L - zeta; zref = zmin when k<0 -> S = -zeta)
    /// Returns false when this strip does not fall inside the rectangle (the display
    /// would not draw it either).
    bool clip_v_strip( CgemGeoReadoutPlane* p, double v, EndPoint& lo, EndPoint& hi ) {
        const double a  = p->getStereoAngle(); // rad
        const double sa = std::sin( a );
        const double ca = std::cos( a );
        const bool kpos = ( a >= 0.0 );

        const double L       = p->getLength();
        const double W       = p->getNXstrips() * p->getXPitch();
        const double RX      = p->getRX();
        const double RV      = p->getRV();
        const double Rmid    = 0.5 * ( RX + RV );
        const double phiMin  = p->getPhimin();
        const double xMinStr = ( p->getPhiMin_strip() - phiMin ) * Rmid; // m_Xmin_strip

        // azimuth from localX/zeta
        const auto toPhi = [&]( double localX ) {
            return phiMin + ( localX + xMinStr ) / Rmid;
        };

        std::vector<EndPoint> pts;
        const double eps = 1e-6;

        // given localX, solve for zeta (S = (v - localX*ca)/sa)
        const auto addByLocalX = [&]( double localX ) {
            if ( localX < -eps || localX > W + eps ) return;
            const double S    = ( v - localX * ca ) / sa; // = zref - zeta - zmin
            const double zeta = kpos ? ( L - S ) : ( -S );
            if ( zeta < -eps || zeta > L + eps ) return;
            pts.push_back( { toPhi( localX ), p->getZmin() + zeta } );
        };
        // given zeta, solve for localX
        const auto addByZeta = [&]( double zeta ) {
            if ( zeta < -eps || zeta > L + eps ) return;
            const double S      = ( kpos ? ( L - zeta ) : ( -zeta ) );
            const double localX = ( v - S * sa ) / ca;
            if ( localX < -eps || localX > W + eps ) return;
            pts.push_back( { toPhi( localX ), p->getZmin() + zeta } );
        };

        addByZeta( 0.0 );   // zeta = 0 edge
        addByZeta( L );     // zeta = L edge
        addByLocalX( 0.0 ); // localX = 0 edge
        addByLocalX( W );   // localX = W edge

        if ( pts.size() < 2 ) return false;
        std::sort( pts.begin(), pts.end(),
                   []( const EndPoint& x, const EndPoint& y ) { return x.z < y.z; } );
        lo = pts.front();
        hi = pts.back();
        return true;
    }

} // namespace

class ExportCgemGeomAlg : public Algorithm {
  private:
    NTuple::Tuple* m_tuple{ nullptr };

    NTuple::Item<int> m_gid, m_layer, m_sheet, m_strip_type, m_strip;
    NTuple::Item<double> m_r, m_phi0, m_dphi, m_z0, m_dz, m_width, m_thick;

    SmartIF<ICgemGeomSvc> m_geom_svc;

  public:
    using Algorithm::Algorithm;

    StatusCode initialize() override {
        NTuplePtr nt( ntupleSvc(), "FILE1/cgem_strip" );
        if ( nt ) { m_tuple = nt; }
        else
        {
            m_tuple = ntupleSvc()->book( "FILE1/cgem_strip", CLID_ColumnWiseTuple,
                                         "CGEM X/V strip geometry" );
            if ( !m_tuple )
            {
                error() << "Cannot book ntuple for CGEM strip geometry" << endmsg;
                return StatusCode::FAILURE;
            }
            m_tuple->addItem( "gid", m_gid ).ignore();
            m_tuple->addItem( "layer", m_layer ).ignore();
            m_tuple->addItem( "sheet", m_sheet ).ignore();
            m_tuple->addItem( "strip_type", m_strip_type ).ignore();
            m_tuple->addItem( "strip", m_strip ).ignore();
            m_tuple->addItem( "r", m_r ).ignore();
            m_tuple->addItem( "phi0", m_phi0 ).ignore();
            m_tuple->addItem( "dphi", m_dphi ).ignore();
            m_tuple->addItem( "z0", m_z0 ).ignore();
            m_tuple->addItem( "dz", m_dz ).ignore();
            m_tuple->addItem( "width", m_width ).ignore();
            m_tuple->addItem( "thick", m_thick ).ignore();
        }

        // CgemGeomSvc::initialize() calls initGeom() itself, do not call it again here
        m_geom_svc = service( "CgemGeomSvc" );
        if ( !m_geom_svc )
        {
            error() << "Cannot get CgemGeomSvc" << endmsg;
            return StatusCode::FAILURE;
        }
        return StatusCode::SUCCESS;
    }

    StatusCode execute() override { return StatusCode::SUCCESS; }

    StatusCode finalize() override {
        if ( !m_geom_svc ) return StatusCode::FAILURE;

        int gid = 0;
        int n_x = 0, n_v = 0, n_v_bad = 0, n_len_diff = 0;
        double max_len_diff = 0.0;

        for ( int ilayer = 0; ilayer < m_geom_svc->getNumberOfCgemLayer(); ++ilayer )
        {
            CgemGeoLayer* layer = m_geom_svc->getCgemLayer( ilayer );
            if ( !layer )
            {
                error() << "No CgemGeoLayer " << ilayer << endmsg;
                return StatusCode::FAILURE;
            }
            const int nSheet = layer->getNumberOfSheet();

            for ( int isheet = 0; isheet < nSheet; ++isheet )
            {
                CgemGeoReadoutPlane* plane = m_geom_svc->getReadoutPlane( ilayer, isheet );
                if ( !plane )
                {
                    error() << "No readout plane " << ilayer << " " << isheet << endmsg;
                    return StatusCode::FAILURE;
                }
                const double rmid = 0.5 * ( plane->getRX() + plane->getRV() );

                // ---- X strips: run through the whole sheet along z ----
                for ( int s = 0; s < plane->getNXstrips(); ++s )
                {
                    const double z_min = plane->getZmin();
                    const double dz    = plane->getLength();
                    m_gid              = gid;
                    m_layer            = ilayer;
                    m_sheet            = isheet;
                    m_strip_type       = 0; // X
                    m_strip            = s;
                    m_r                = plane->getRX() / 10.0; // mm -> cm
                    m_phi0             = plane->getPhiFromXID( s );
                    m_dphi             = 0.0;
                    m_z0               = z_min / 10.0;                     // mm -> cm
                    m_dz               = dz / 10.0;                        // mm -> cm
                    m_width            = layer->getWidthOfStripX() / 10.0; // mm -> cm
                    m_thick = ( layer->getOuterROfAnodeCu2() - layer->getInnerROfAnodeCu2() ) /
                              10.0; // mm -> cm
                    m_tuple->write().ignore();
                    ++n_x;
                    ++gid;
                }

                // ---- V strips: stereo strips, end points obtained analytically by clipping
                // ----
                for ( int s = 0; s < plane->getNVstrips(); ++s )
                {
                    const double v = plane->getCentralVFromVID( s );
                    EndPoint lo{ 0.0, -1.0 }, hi{ 0.0, -1.0 };
                    if ( !clip_v_strip( plane, v, lo, hi ) )
                    {
                        ++n_v_bad;
                        continue;
                    }

                    const double dphi = hi.phi - lo.phi;
                    const double dz   = hi.z - lo.z;
                    const double rv   = plane->getRV();

                    // cross-check against the service's approximate strip-length formula
                    // (up to ~0.16 mm difference in corner cases)
                    const double len_me  = std::sqrt( dphi * rv * dphi * rv + dz * dz );
                    const double len_svc = plane->getVStripLength( s );
                    if ( std::fabs( len_me - len_svc ) > 1e-6 )
                    {
                        ++n_len_diff;
                        max_len_diff = std::max( max_len_diff, std::fabs( len_me - len_svc ) );
                    }

                    m_gid        = gid;
                    m_layer      = ilayer;
                    m_sheet      = isheet;
                    m_strip_type = 1; // V
                    m_strip      = s;
                    m_r          = rv / 10.0; // mm -> cm
                    m_phi0       = lo.phi;
                    m_dphi       = dphi;
                    m_z0         = lo.z / 10.0;                      // mm -> cm
                    m_dz         = dz / 10.0;                        // mm -> cm
                    m_width      = layer->getWidthOfStripV() / 10.0; // mm -> cm
                    m_thick = ( layer->getOuterROfAnodeCu1() - layer->getInnerROfAnodeCu1() ) /
                              10.0; // mm -> cm
                    m_tuple->write().ignore();
                    ++n_v;
                    ++gid;
                }
                (void)rmid;
            }
        }

        info() << "[ExportCgemGeomAlg] X strips " << n_x << " + V strips " << n_v
               << " (invalid/outside sheet: " << n_v_bad
               << "); length cross-check vs CgemGeoReadoutPlane::getVStripLength(): max diff "
               << max_len_diff << " mm over " << n_len_diff << " strips" << endmsg;
        return StatusCode::SUCCESS;
    }
};

DECLARE_COMPONENT( ExportCgemGeomAlg )
