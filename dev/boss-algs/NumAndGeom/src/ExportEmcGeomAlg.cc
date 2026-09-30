#include <GaudiKernel/Algorithm.h>
#include <GaudiKernel/NTuple.h>
#include <GaudiKernel/SmartDataPtr.h>

#include <EmcCalibConstSvc/IEmcCalibConstSvc.h>
#include <EmcRecGeoSvc/IEmcRecGeoSvc.h>

class ExportEmcGeomAlg : public Algorithm {
  private:
    NTuple::Tuple* m_tuple;
    NTuple::Item<int> m_gid;
    NTuple::Item<int> m_id;
    NTuple::Item<int> m_part;
    NTuple::Item<int> m_theta;
    NTuple::Item<int> m_phi;

    NTuple::Array<double> m_vtx_x;
    NTuple::Array<double> m_vtx_y;
    NTuple::Array<double> m_vtx_z;

    NTuple::Item<double> m_center_x;
    NTuple::Item<double> m_center_y;
    NTuple::Item<double> m_center_z;

    NTuple::Item<double> m_front_center_x;
    NTuple::Item<double> m_front_center_y;
    NTuple::Item<double> m_front_center_z;

    SmartIF<IEmcCalibConstSvc> m_calib_const_svc;
    SmartIF<IEmcRecGeoSvc> m_geom_svc;

  public:
    using Algorithm::Algorithm;

    StatusCode initialize() override {
        NTuplePtr nt( ntupleSvc(), "FILE1/emc_geom" );
        if ( nt ) m_tuple = nt;
        else
        {
            m_tuple =
                ntupleSvc()->book( "FILE1/emc_geom", CLID_ColumnWiseTuple, "EMC geometry" );
            if ( !m_tuple )
            {
                error() << "Cannot book ntuple for EMC geometry" << endmsg;
                return StatusCode::FAILURE;
            }

            m_tuple->addItem( "gid", m_gid ).ignore();
            m_tuple->addItem( "id", m_id ).ignore();
            m_tuple->addItem( "part", m_part ).ignore();
            m_tuple->addItem( "theta", m_theta ).ignore();
            m_tuple->addItem( "phi", m_phi ).ignore();

            m_tuple->addItem( "vtx_x", 8, m_vtx_x ).ignore();
            m_tuple->addItem( "vtx_y", 8, m_vtx_y ).ignore();
            m_tuple->addItem( "vtx_z", 8, m_vtx_z ).ignore();

            m_tuple->addItem( "center_x", m_center_x ).ignore();
            m_tuple->addItem( "center_y", m_center_y ).ignore();
            m_tuple->addItem( "center_z", m_center_z ).ignore();

            m_tuple->addItem( "front_center_x", m_front_center_x ).ignore();
            m_tuple->addItem( "front_center_y", m_front_center_y ).ignore();
            m_tuple->addItem( "front_center_z", m_front_center_z ).ignore();
        }

        m_calib_const_svc = service( "EmcCalibConstSvc" );
        if ( !m_calib_const_svc )
        {
            error() << "Cannot get EmcCalibConstSvc" << endmsg;
            return StatusCode::FAILURE;
        }

        m_geom_svc = service( "EmcRecGeoSvc" );
        if ( !m_geom_svc )
        {
            error() << "Cannot get EmcRecGeoSvc" << endmsg;
            return StatusCode::FAILURE;
        }

        return StatusCode::SUCCESS;
    }

    StatusCode execute() override { return StatusCode::SUCCESS; }

    StatusCode finalize() override {
        for ( int gid = 0; gid < 6240; gid++ )
        {
            auto part  = m_calib_const_svc->getPartID( gid );
            auto theta = m_calib_const_svc->getThetaIndex( gid );
            auto phi   = m_calib_const_svc->getPhiIndex( gid );

            auto identifier = EmcID::crystal_id( part, theta, phi );

            m_gid   = gid;
            m_part  = part;
            m_theta = theta;
            m_phi   = phi;
            m_id    = identifier.get_value();

            for ( int i = 0; i < 8; i++ )
            {
                auto point = m_geom_svc->GetCrystalPoint( identifier, i );
                m_vtx_x[i] = point.x();
                m_vtx_y[i] = point.y();
                m_vtx_z[i] = point.z();
            }

            auto center = m_geom_svc->GetCCenter( identifier );
            m_center_x  = center.x();
            m_center_y  = center.y();
            m_center_z  = center.z();

            auto front_center = m_geom_svc->GetCFrontCenter( identifier );
            m_front_center_x  = front_center.x();
            m_front_center_y  = front_center.y();
            m_front_center_z  = front_center.z();

            m_tuple->write().ignore();
        }

        return StatusCode::SUCCESS;
    }
};

DECLARE_COMPONENT( ExportEmcGeomAlg )
