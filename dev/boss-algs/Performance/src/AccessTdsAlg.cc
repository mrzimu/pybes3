#include <GaudiKernel/Algorithm.h>
#include <GaudiKernel/SmartDataPtr.h>

#include <CgemRawEvent/CgemDigi.h>
#include <DstEvent/DstEmcShower.h>
#include <DstEvent/DstExtTrack.h>
#include <DstEvent/DstMdcDedx.h>
#include <DstEvent/DstMdcKalTrack.h>
#include <DstEvent/DstMdcTrack.h>
#include <DstEvent/DstMucTrack.h>
#include <DstEvent/DstTofTrack.h>
#include <EmcRawEvent/EmcDigi.h>
#include <EmcRecEventModel/RecEmcShower.h>
#include <EventModel/EventHeader.h>
#include <EventModel/EventModel.h>
#include <ExtEvent/RecExtTrack.h>
#include <LumiDigi/LumiDigi.h>
#include <McTruth/McParticle.h>
#include <MdcRawEvent/MdcDigi.h>
#include <MdcRecEvent/RecMdcDedx.h>
#include <MdcRecEvent/RecMdcKalTrack.h>
#include <MdcRecEvent/RecMdcTrack.h>
#include <MucRawEvent/MucDigi.h>
#include <MucRecEvent/RecMucTrack.h>
#include <TofRawEvent/TofDigi.h>
#include <TofRecEvent/RecTofTrack.h>

#include <string>

// Compile-time selection of the TDS objects that execute() reads.
// Comment out a section to compile its accesses out completely, so that what is
// measured is the access itself and no per-event path lookup.
// begin access config
// #define READ_HEADER
// #define READ_MC
// #define READ_DIGI
#define READ_DST
// #define READ_REC
// end access config

class AccessTdsAlg : public Algorithm {
  private:
    IntegerProperty m_printFreq{ this, "PrintFreq", 1000 };

    unsigned long long m_nEvents{ 0 };
    unsigned long long m_nHits{ 0 };

    template <typename T>
    void accessTds( const std::string& path ) {
        SmartDataPtr<T> ptr( eventSvc(), path );

        if ( ptr ) { ++m_nHits; }
        else { debug() << "Could not retrieve " << path << endmsg; }
    }

  public:
    using Algorithm::Algorithm;

    StatusCode execute() override {
        ++m_nEvents;

        const auto print_freq = static_cast<unsigned long long>( m_printFreq.value() );

        // Use always() so that the progress line stays visible whatever the output level is.
        if ( print_freq > 0 && m_nEvents % print_freq == 0 )
        { always() << "Processed " << m_nEvents << " events" << endmsg; }

#ifdef READ_HEADER
        accessTds<Event::EventHeader>( EventModel::EventHeader );
#endif

#ifdef READ_MC
        accessTds<Event::McParticleCol>( EventModel::MC::McParticleCol );
#endif

        // Digi
#ifdef READ_DIGI
        accessTds<MdcDigiCol>( EventModel::Digi::MdcDigiCol );
        accessTds<EmcDigiCol>( EventModel::Digi::EmcDigiCol );
        accessTds<TofDigiCol>( EventModel::Digi::TofDigiCol );
        accessTds<MucDigiCol>( EventModel::Digi::MucDigiCol );
        accessTds<CgemDigiCol>( EventModel::Digi::CgemDigiCol );
        accessTds<LumiDigiCol>( EventModel::Digi::LumiDigiCol );
#endif

        // Dst
#ifdef READ_DST
        accessTds<DstMdcTrackCol>( EventModel::Dst::DstMdcTrackCol );
        accessTds<DstMdcKalTrackCol>( EventModel::Dst::DstMdcKalTrackCol );
        accessTds<DstMdcDedxCol>( EventModel::Dst::DstMdcDedxCol );
        accessTds<DstExtTrackCol>( EventModel::Dst::DstExtTrackCol );
        accessTds<DstTofTrackCol>( EventModel::Dst::DstTofTrackCol );
        accessTds<DstEmcShowerCol>( EventModel::Dst::DstEmcShowerCol );
        accessTds<DstMucTrackCol>( EventModel::Dst::DstMucTrackCol );
#endif

        // Rec
#ifdef READ_REC
        accessTds<RecMdcTrackCol>( EventModel::Recon::RecMdcTrackCol );
        accessTds<RecMdcKalTrackCol>( EventModel::Recon::RecMdcKalTrackCol );
        accessTds<RecMdcDedxCol>( EventModel::Recon::RecMdcDedxCol );
        accessTds<RecExtTrackCol>( EventModel::Recon::RecExtTrackCol );
        accessTds<RecTofTrackCol>( EventModel::Recon::RecTofTrackCol );
        accessTds<RecEmcShowerCol>( EventModel::Recon::RecEmcShowerCol );
        accessTds<RecMucTrackCol>( EventModel::Recon::RecMucTrackCol );
#endif

        return StatusCode::SUCCESS;
    }

    StatusCode finalize() override {
        always() << "Processed " << m_nEvents << " events, " << m_nHits
                 << " TDS object(s) retrieved" << endmsg;

        return StatusCode::SUCCESS;
    }
};

DECLARE_COMPONENT( AccessTdsAlg )
