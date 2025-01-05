#ifndef RootEventData_TEvtRecTrack_H
#define RootEventData_TEvtRecTrack_H

#include "TObject.h"
#include <vector>

class TEvtRecTrack : public TObject {

  public:
    TEvtRecTrack();
    virtual ~TEvtRecTrack();

    Int_t trackId() const { return m_trackId; }
    Int_t partId() const { return m_partId; }
    Int_t quality() const { return m_quality; }
    Int_t mdcTrackId() const { return m_mdcTrackId; }
    Int_t mdcKalTrackId() const { return m_mdcKalTrackId; }
    Int_t mdcDedxId() const { return m_mdcDedxId; }
    Int_t extTrackId() const { return m_extTrackId; }
    Int_t emcShowerId() const { return m_emcShowerId; }
    Int_t mucTrackId() const { return m_mucTrackId; }

    const std::vector<Int_t>& tofTrackIds() const { return m_tofTrackIds; }

    void setTrackId( const int trackId ) { m_trackId = trackId; }
    void setPartId( const int partId ) { m_partId = partId; }
    void setQuality( const int quality ) { m_quality = quality; }
    void setMdcTrackId( const int mdcTrackId ) { m_mdcTrackId = mdcTrackId; }
    void setMdcKalTrackId( const int mdcKalTrackId ) { m_mdcKalTrackId = mdcKalTrackId; }
    void setMdcDedxId( const int mdcDedxId ) { m_mdcDedxId = mdcDedxId; }
    void setExtTrackId( const int extTrackId ) { m_extTrackId = extTrackId; }
    void setEmcShowerId( const int emcShowerId ) { m_emcShowerId = emcShowerId; }
    void setMucTrackId( const int mucTrackId ) { m_mucTrackId = mucTrackId; }

    void setTofTrackIds( const std::vector<Int_t>& tofTrackIds ) {
        m_tofTrackIds = tofTrackIds;
    }
    void addTofTrackId( const int tofTrackId ) { m_tofTrackIds.push_back( tofTrackId ); }

  private:
    Int_t m_trackId;
    Int_t m_partId;
    Int_t m_quality;

    Int_t m_mdcTrackId;
    Int_t m_mdcKalTrackId;
    Int_t m_mdcDedxId;
    Int_t m_extTrackId;
    Int_t m_emcShowerId;
    Int_t m_mucTrackId;

    std::vector<Int_t> m_tofTrackIds;

    ClassDef( TEvtRecTrack, 3 )
};

#endif
