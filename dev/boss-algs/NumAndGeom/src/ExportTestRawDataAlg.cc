#include <GaudiKernel/Algorithm.h>
#include <GaudiKernel/NTuple.h>
#include <GaudiKernel/SmartDataPtr.h>
#include <cstdint>

#include <CgemRawEvent/CgemDigi.h>
#include <EmcRawEvent/EmcDigi.h>
#include <EventModel/EventHeader.h>
#include <MdcRawEvent/MdcDigi.h>
#include <MucRawEvent/MucDigi.h>
#include <TofRawEvent/TofDigi.h>
#include <TrigEvent/TrigGTD.h>

class ExportTestRawDataAlg : public Algorithm {
  private:
    NTuple::Tuple* m_tuple_evt_header;
    NTuple::Item<uint32_t> m_evt_no;
    NTuple::Item<uint32_t> m_run_no;
    NTuple::Item<uint32_t> m_time;
    NTuple::Item<uint32_t> m_flag1;
    NTuple::Item<uint32_t> m_flag2;
    NTuple::Item<uint32_t> m_etsT1;
    NTuple::Item<uint32_t> m_etsT2;

    NTuple::Tuple* m_tuple_mdc;
    NTuple::Item<int> m_mdc_index;
    NTuple::Array<uint32_t> m_mdc_id;
    NTuple::Array<uint32_t> m_mdc_adc;
    NTuple::Array<uint32_t> m_mdc_tdc;
    NTuple::Array<uint32_t> m_mdc_overflow;

    NTuple::Tuple* m_tuple_tof;
    NTuple::Item<int> m_tof_index;
    NTuple::Array<uint32_t> m_tof_id;
    NTuple::Array<uint32_t> m_tof_adc;
    NTuple::Array<uint32_t> m_tof_tdc;
    NTuple::Array<uint32_t> m_tof_overflow;

    NTuple::Tuple* m_tuple_emc;
    NTuple::Item<int> m_emc_index;
    NTuple::Array<uint32_t> m_emc_id;
    NTuple::Array<uint32_t> m_emc_adc;
    NTuple::Array<uint32_t> m_emc_tdc;
    NTuple::Array<uint32_t> m_emc_measure;

    NTuple::Tuple* m_tuple_muc;
    NTuple::Item<int> m_muc_index;
    NTuple::Array<uint32_t> m_muc_id;

    NTuple::Tuple* m_tuple_cgem;
    NTuple::Item<int> m_cgem_index;
    NTuple::Array<uint32_t> m_cgem_id;
    NTuple::Array<uint32_t> m_cgem_adc;
    NTuple::Array<uint32_t> m_cgem_tdc;
    NTuple::Array<double> m_cgem_charge;
    NTuple::Array<double> m_cgem_time;

    NTuple::Tuple* m_tuple_trigGTD;
    NTuple::Item<int> m_trigGTD_index;
    NTuple::Array<uint32_t> m_trigGTD_id;
    NTuple::Array<uint32_t> m_trigGTD_data_size;
    NTuple::Array<uint32_t> m_trigGTD_time_window;
    NTuple::Array<uint32_t> m_trigGTD_data_type;

  public:
    using Algorithm::Algorithm;

    StatusCode initialize() override {
        NTuplePtr nt_evt( ntupleSvc(), "FILE1/evt_header" );
        if ( nt_evt ) m_tuple_evt_header = nt_evt;
        else
        {
            m_tuple_evt_header =
                ntupleSvc()->book( "FILE1/evt_header", CLID_ColumnWiseTuple, "event header" );
            if ( !m_tuple_evt_header )
            {
                error() << "Cannot book ntuple for event header" << endmsg;
                return StatusCode::FAILURE;
            }

            m_tuple_evt_header->addItem( "evt_no", m_evt_no ).ignore();
            m_tuple_evt_header->addItem( "run_no", m_run_no ).ignore();
            m_tuple_evt_header->addItem( "time", m_time ).ignore();
            m_tuple_evt_header->addItem( "flag1", m_flag1 ).ignore();
            m_tuple_evt_header->addItem( "flag2", m_flag2 ).ignore();
            m_tuple_evt_header->addItem( "etsT1", m_etsT1 ).ignore();
            m_tuple_evt_header->addItem( "etsT2", m_etsT2 ).ignore();
        }

        NTuplePtr nt_mdc( ntupleSvc(), "FILE1/mdc" );
        if ( nt_mdc ) m_tuple_mdc = nt_mdc;
        else
        {
            m_tuple_mdc = ntupleSvc()->book( "FILE1/mdc", CLID_ColumnWiseTuple, "MDC digi" );
            if ( !m_tuple_mdc )
            {
                error() << "Cannot book ntuple for MDC digi" << endmsg;
                return StatusCode::FAILURE;
            }

            m_tuple_mdc->addItem( "index", m_mdc_index, 0, 10000 ).ignore();
            m_tuple_mdc->addIndexedItem( "m_intId", m_mdc_index, m_mdc_id ).ignore();
            m_tuple_mdc->addIndexedItem( "m_chargeChannel", m_mdc_index, m_mdc_adc ).ignore();
            m_tuple_mdc->addIndexedItem( "m_timeChannel", m_mdc_index, m_mdc_tdc ).ignore();
            m_tuple_mdc->addIndexedItem( "m_overflow", m_mdc_index, m_mdc_overflow ).ignore();
        }

        NTuplePtr nt_tof( ntupleSvc(), "FILE1/tof" );
        if ( nt_tof ) m_tuple_tof = nt_tof;
        else
        {
            m_tuple_tof = ntupleSvc()->book( "FILE1/tof", CLID_ColumnWiseTuple, "TOF digi" );
            if ( !m_tuple_tof )
            {
                error() << "Cannot book ntuple for TOF digi" << endmsg;
                return StatusCode::FAILURE;
            }

            m_tuple_tof->addItem( "index", m_tof_index, 0, 10000 ).ignore();
            m_tuple_tof->addIndexedItem( "m_intId", m_tof_index, m_tof_id ).ignore();
            m_tuple_tof->addIndexedItem( "m_chargeChannel", m_tof_index, m_tof_adc ).ignore();
            m_tuple_tof->addIndexedItem( "m_timeChannel", m_tof_index, m_tof_tdc ).ignore();
            m_tuple_tof->addIndexedItem( "m_overflow", m_tof_index, m_tof_overflow ).ignore();
        }

        NTuplePtr nt_emc( ntupleSvc(), "FILE1/emc" );
        if ( nt_emc ) m_tuple_emc = nt_emc;
        else
        {
            m_tuple_emc = ntupleSvc()->book( "FILE1/emc", CLID_ColumnWiseTuple, "emc digi" );
            if ( !m_tuple_emc )
            {
                error() << "Cannot book ntuple for emc digi" << endmsg;
                return StatusCode::FAILURE;
            }

            m_tuple_emc->addItem( "index", m_emc_index, 0, 10000 ).ignore();
            m_tuple_emc->addIndexedItem( "m_intId", m_emc_index, m_emc_id ).ignore();
            m_tuple_emc->addIndexedItem( "m_chargeChannel", m_emc_index, m_emc_adc ).ignore();
            m_tuple_emc->addIndexedItem( "m_timeChannel", m_emc_index, m_emc_tdc ).ignore();
            m_tuple_emc->addIndexedItem( "m_measure", m_emc_index, m_emc_measure ).ignore();
        }

        NTuplePtr nt_muc( ntupleSvc(), "FILE1/muc" );
        if ( nt_muc ) m_tuple_muc = nt_muc;
        else
        {
            m_tuple_muc = ntupleSvc()->book( "FILE1/muc", CLID_ColumnWiseTuple, "muc digi" );
            if ( !m_tuple_muc )
            {
                error() << "Cannot book ntuple for muc digi" << endmsg;
                return StatusCode::FAILURE;
            }

            m_tuple_muc->addItem( "index", m_muc_index, 0, 10000 ).ignore();
            m_tuple_muc->addIndexedItem( "m_intId", m_muc_index, m_muc_id ).ignore();
        }

        NTuplePtr nt_cgem( ntupleSvc(), "FILE1/cgem" );
        if ( nt_cgem ) m_tuple_cgem = nt_cgem;
        else
        {
            m_tuple_cgem =
                ntupleSvc()->book( "FILE1/cgem", CLID_ColumnWiseTuple, "cgem digi" );
            if ( !m_tuple_cgem )
            {
                error() << "Cannot book ntuple for cgem digi" << endmsg;
                return StatusCode::FAILURE;
            }

            m_tuple_cgem->addItem( "index", m_cgem_index, 0, 10000 ).ignore();
            m_tuple_cgem->addIndexedItem( "m_intId", m_cgem_index, m_cgem_id ).ignore();
            m_tuple_cgem->addIndexedItem( "m_chargeChannel", m_cgem_index, m_cgem_adc )
                .ignore();
            m_tuple_cgem->addIndexedItem( "m_timeChannel", m_cgem_index, m_cgem_tdc ).ignore();
            m_tuple_cgem->addIndexedItem( "m_charge_fc", m_cgem_index, m_cgem_charge )
                .ignore();
            m_tuple_cgem->addIndexedItem( "m_time_ns", m_cgem_index, m_cgem_time ).ignore();
        }

        NTuplePtr nt_trigGTD( ntupleSvc(), "FILE1/trigGTD" );
        if ( nt_trigGTD ) m_tuple_trigGTD = nt_trigGTD;
        else
        {
            m_tuple_trigGTD =
                ntupleSvc()->book( "FILE1/trigGTD", CLID_ColumnWiseTuple, "trigGTD digi" );
            if ( !m_tuple_trigGTD )
            {
                error() << "Cannot book ntuple for trigGTD digi" << endmsg;
                return StatusCode::FAILURE;
            }

            m_tuple_trigGTD->addItem( "index", m_trigGTD_index, 0, 10000 ).ignore();
            m_tuple_trigGTD->addIndexedItem( "m_id", m_trigGTD_index, m_trigGTD_id ).ignore();
            m_tuple_trigGTD
                ->addIndexedItem( "m_dataSize", m_trigGTD_index, m_trigGTD_data_size )
                .ignore();
            m_tuple_trigGTD
                ->addIndexedItem( "m_timeWindow", m_trigGTD_index, m_trigGTD_time_window )
                .ignore();
            m_tuple_trigGTD
                ->addIndexedItem( "m_dataType", m_trigGTD_index, m_trigGTD_data_type )
                .ignore();
        }

        return StatusCode::SUCCESS;
    }

    StatusCode execute() override {
        SmartDataPtr<Event::EventHeader> eventHeader( eventSvc(), "/Event/EventHeader" );
        m_evt_no = eventHeader->eventNumber();
        m_run_no = eventHeader->runNumber();
        m_time   = eventHeader->time();
        m_flag1  = eventHeader->flag1();
        m_flag2  = eventHeader->flag2();
        m_etsT1  = eventHeader->etsT1();
        m_etsT2  = eventHeader->etsT2();
        m_tuple_evt_header->write().ignore();

        SmartDataPtr<MdcDigiCol> mdcDigiCol( eventSvc(), "/Event/Digi/MdcDigiCol" );
        m_mdc_index = 0;
        for ( auto digi : *mdcDigiCol )
        {
            m_mdc_id[m_mdc_index]       = digi->getIntId();
            m_mdc_adc[m_mdc_index]      = digi->getChargeChannel();
            m_mdc_tdc[m_mdc_index]      = digi->getTimeChannel();
            m_mdc_overflow[m_mdc_index] = digi->getOverflow();
            m_mdc_index++;
        }
        m_tuple_mdc->write().ignore();

        SmartDataPtr<TofDigiCol> tofDigiCol( eventSvc(), "/Event/Digi/TofDigiCol" );
        m_tof_index = 0;
        for ( auto digi : *tofDigiCol )
        {
            m_tof_id[m_tof_index]       = digi->getIntId();
            m_tof_adc[m_tof_index]      = digi->getChargeChannel();
            m_tof_tdc[m_tof_index]      = digi->getTimeChannel();
            m_tof_overflow[m_tof_index] = digi->getOverflow();
            m_tof_index++;
        }
        m_tuple_tof->write().ignore();

        SmartDataPtr<EmcDigiCol> emcDigiCol( eventSvc(), "/Event/Digi/EmcDigiCol" );
        m_emc_index = 0;
        for ( auto digi : *emcDigiCol )
        {
            m_emc_id[m_emc_index]      = digi->getIntId();
            m_emc_adc[m_emc_index]     = digi->getChargeChannel();
            m_emc_tdc[m_emc_index]     = digi->getTimeChannel();
            m_emc_measure[m_emc_index] = digi->getMeasure();
            m_emc_index++;
        }
        m_tuple_emc->write().ignore();

        SmartDataPtr<MucDigiCol> mucDigiCol( eventSvc(), "/Event/Digi/MucDigiCol" );
        m_muc_index = 0;
        for ( auto digi : *mucDigiCol )
        {
            m_muc_id[m_muc_index] = digi->getIntId();
            m_muc_index++;
        }
        m_tuple_muc->write().ignore();

        SmartDataPtr<CgemDigiCol> cgemDigiCol( eventSvc(), "/Event/Digi/CgemDigiCol" );
        m_cgem_index = 0;
        for ( auto digi : *cgemDigiCol )
        {
            m_cgem_id[m_cgem_index]     = digi->getIntId();
            m_cgem_adc[m_cgem_index]    = digi->getChargeChannel();
            m_cgem_tdc[m_cgem_index]    = digi->getTimeChannel();
            m_cgem_charge[m_cgem_index] = digi->getCharge_fc();
            m_cgem_time[m_cgem_index]   = digi->getTime_ns();
            m_cgem_index++;
        }
        m_tuple_cgem->write().ignore();

        SmartDataPtr<TrigGTDCol> trigGTDCol( eventSvc(), "/Event/Trig/TrigGTDCol" );
        m_trigGTD_index = 0;
        for ( auto trig : *trigGTDCol )
        {
            m_trigGTD_id[m_trigGTD_index]          = trig->getId();
            m_trigGTD_data_size[m_trigGTD_index]   = trig->getDataSize();
            m_trigGTD_time_window[m_trigGTD_index] = trig->getTimeWindow();
            m_trigGTD_data_type[m_trigGTD_index]   = trig->getDataType();
            m_trigGTD_index++;
        }
        m_tuple_trigGTD->write().ignore();

        return StatusCode::SUCCESS;
    }
};

DECLARE_COMPONENT( ExportTestRawDataAlg )
