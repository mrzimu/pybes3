#include <GaudiKernel/Algorithm.h>
#include <GaudiKernel/NTuple.h>
#include <GaudiKernel/SmartDataPtr.h>

#include <DstEvent/DstTofTrack.h>
#include <DstEvent/TofHitStatus.h>

class ExportTofHitStatusAlg : public Algorithm {
  private:
    NTuple::Tuple* m_tuple;
    NTuple::Item<int> m_index;
    NTuple::Array<uint32_t> m_status;
    NTuple::Array<bool> m_is_raw;
    NTuple::Array<bool> m_is_readout;
    NTuple::Array<bool> m_is_counter;
    NTuple::Array<bool> m_is_cluster;
    NTuple::Array<bool> m_is_barrel;
    NTuple::Array<bool> m_is_east;
    NTuple::Array<bool> m_is_overflow;
    NTuple::Array<bool> m_is_multihit;
    NTuple::Array<bool> m_is_mrpc;
    NTuple::Array<int> m_layer;
    NTuple::Array<int> m_ncounter;
    NTuple::Array<int> m_neast;
    NTuple::Array<int> m_nwest;

  public:
    using Algorithm::Algorithm;

    StatusCode initialize() override {
        NTuplePtr nt( ntupleSvc(), "FILE1/tof_hit_status" );
        if ( nt ) m_tuple = nt;
        else
        {
            m_tuple = ntupleSvc()->book( "FILE1/tof_hit_status", CLID_ColumnWiseTuple,
                                         "TOF hit status" );
            if ( !m_tuple )
            {
                error() << "Cannot book ntuple for TOF hit status" << endmsg;
                return StatusCode::FAILURE;
            }

            m_tuple->addItem( "index", m_index, 0, 10000 ).ignore();
            m_tuple->addIndexedItem( "status", m_index, m_status ).ignore();
            m_tuple->addIndexedItem( "is_raw", m_index, m_is_raw ).ignore();
            m_tuple->addIndexedItem( "is_readout", m_index, m_is_readout ).ignore();
            m_tuple->addIndexedItem( "is_counter", m_index, m_is_counter ).ignore();
            m_tuple->addIndexedItem( "is_cluster", m_index, m_is_cluster ).ignore();
            m_tuple->addIndexedItem( "is_barrel", m_index, m_is_barrel ).ignore();
            m_tuple->addIndexedItem( "is_east", m_index, m_is_east ).ignore();
            m_tuple->addIndexedItem( "is_overflow", m_index, m_is_overflow ).ignore();
            m_tuple->addIndexedItem( "is_multihit", m_index, m_is_multihit ).ignore();
            m_tuple->addIndexedItem( "is_mrpc", m_index, m_is_mrpc ).ignore();
            m_tuple->addIndexedItem( "layer", m_index, m_layer ).ignore();
            m_tuple->addIndexedItem( "n_counter", m_index, m_ncounter ).ignore();
            m_tuple->addIndexedItem( "n_east", m_index, m_neast ).ignore();
            m_tuple->addIndexedItem( "n_west", m_index, m_nwest ).ignore();
        }

        return StatusCode::SUCCESS;
    }

    StatusCode execute() override {
        SmartDataPtr<DstTofTrackCol> tofTrackCol( eventSvc(), "/Event/Dst/DstTofTrackCol" );
        m_index = 0;
        for ( auto tofTrack : *tofTrackCol )
        {
            TofHitStatus status;
            status.setStatus( tofTrack->status() );

            m_status[m_index]      = tofTrack->status();
            m_is_raw[m_index]      = status.is_raw();
            m_is_readout[m_index]  = status.is_readout();
            m_is_counter[m_index]  = status.is_counter();
            m_is_cluster[m_index]  = status.is_cluster();
            m_is_barrel[m_index]   = status.is_barrel();
            m_is_east[m_index]     = status.is_east();
            m_is_overflow[m_index] = status.is_overflow();
            m_is_multihit[m_index] = status.is_multihit();
            m_is_mrpc[m_index]     = status.is_mrpc();
            m_layer[m_index]       = status.layer();
            m_ncounter[m_index]    = status.ncounter();
            m_neast[m_index]       = status.neast();
            m_nwest[m_index]       = status.nwest();
            m_index++;
        }
        m_tuple->write().ignore();
        return StatusCode::SUCCESS;
    }
};

DECLARE_COMPONENT( ExportTofHitStatusAlg )
