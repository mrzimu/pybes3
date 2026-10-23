#include <GaudiKernel/Algorithm.h>
#include <GaudiKernel/NTuple.h>
#include <GaudiKernel/SmartDataPtr.h>

#include <EmcRawEvent/EmcDigi.h>
#include <MdcRawEvent/MdcDigi.h>
#include <RawEvent/RawDataUtil.h>
#include <TofRawEvent/TofDigi.h>

struct CnvTuple {
    NTuple::Tuple* tuple{ nullptr };
    NTuple::Item<uint32_t> adc;
    NTuple::Item<uint32_t> measure;
    NTuple::Item<double> charge;
    NTuple::Item<uint32_t> tdc;
    NTuple::Item<double> time;
};

class ExportRawDataUtilAlg : public Algorithm {
  private:
    CnvTuple m_mdc_tuple;
    CnvTuple m_tof_tuple;
    CnvTuple m_emc_tuple;

  public:
    using Algorithm::Algorithm;

    StatusCode init_tuple( CnvTuple& cnv_tuple, const std::string& tuple_name ) {
        NTuplePtr nt( ntupleSvc(), "FILE1/" + tuple_name );
        if ( nt ) cnv_tuple.tuple = nt;
        else
        {
            cnv_tuple.tuple =
                ntupleSvc()->book( "FILE1/" + tuple_name, CLID_ColumnWiseTuple, tuple_name );
            if ( !cnv_tuple.tuple )
            {
                error() << "Failed to book tuple " << tuple_name << endmsg;
                return StatusCode::FAILURE;
            }

            if ( tuple_name == "emc" )
                cnv_tuple.tuple->addItem( "measure", cnv_tuple.measure ).ignore();

            cnv_tuple.tuple->addItem( "adc", cnv_tuple.adc ).ignore();
            cnv_tuple.tuple->addItem( "charge", cnv_tuple.charge ).ignore();
            cnv_tuple.tuple->addItem( "tdc", cnv_tuple.tdc ).ignore();
            cnv_tuple.tuple->addItem( "time", cnv_tuple.time ).ignore();
        }

        return StatusCode::SUCCESS;
    }

    StatusCode initialize() override {
        StatusCode sc;
        sc = init_tuple( m_mdc_tuple, "mdc" );
        if ( sc.isFailure() ) return sc;

        sc = init_tuple( m_tof_tuple, "tof" );
        if ( sc.isFailure() ) return sc;

        sc = init_tuple( m_emc_tuple, "emc" );
        if ( sc.isFailure() ) return sc;

        return StatusCode::SUCCESS;
    }

    StatusCode execute() override {
        SmartDataPtr<MdcDigiCol> mdc_digis( eventSvc(), "/Event/Digi/MdcDigiCol" );
        SmartDataPtr<TofDigiCol> tof_digis( eventSvc(), "/Event/Digi/TofDigiCol" );
        SmartDataPtr<EmcDigiCol> emc_digis( eventSvc(), "/Event/Digi/EmcDigiCol" );

        if ( !mdc_digis || !tof_digis || !emc_digis )
        {
            error() << "Failed to get digi collections" << endmsg;
            return StatusCode::FAILURE;
        }

        for ( auto digi : *mdc_digis )
        {
            auto adc    = digi->getChargeChannel();
            auto charge = RawDataUtil::MdcCharge( adc );

            auto tdc  = digi->getTimeChannel();
            auto time = RawDataUtil::MdcTime( tdc );

            m_mdc_tuple.adc    = adc;
            m_mdc_tuple.charge = charge;
            m_mdc_tuple.tdc    = tdc;
            m_mdc_tuple.time   = time;

            m_mdc_tuple.tuple->write().ignore();
        }

        for ( auto digi : *tof_digis )
        {
            auto adc    = digi->getChargeChannel();
            auto charge = RawDataUtil::TofCharge( adc );

            auto tdc  = digi->getTimeChannel();
            auto time = RawDataUtil::TofTime( tdc );

            m_tof_tuple.adc    = adc;
            m_tof_tuple.charge = charge;
            m_tof_tuple.tdc    = tdc;
            m_tof_tuple.time   = time;

            m_tof_tuple.tuple->write().ignore();
        }

        for ( auto digi : *emc_digis )
        {
            auto measure = digi->getMeasure();
            auto adc     = digi->getChargeChannel();
            if ( adc > 1023 ) continue;
            auto charge = RawDataUtil::EmcCharge( measure, adc ) / 1000.0;

            auto tdc  = digi->getTimeChannel();
            auto time = RawDataUtil::EmcTime( tdc );

            m_emc_tuple.measure = measure;
            m_emc_tuple.adc     = adc;
            m_emc_tuple.charge  = charge;
            m_emc_tuple.tdc     = tdc;
            m_emc_tuple.time    = time * 50.0;

            m_emc_tuple.tuple->write().ignore();
        }

        return StatusCode::SUCCESS;
    }
};

DECLARE_COMPONENT( ExportRawDataUtilAlg )
