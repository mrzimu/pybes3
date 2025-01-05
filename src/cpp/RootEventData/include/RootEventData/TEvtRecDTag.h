#ifndef RootEventData_TEvtRecDTag_H
#define RootEventData_TEvtRecDTag_H

#include "TObject.h"
#include <vector>

class TEvtRecDTag : public TObject {

  public:
    TEvtRecDTag();
    ~TEvtRecDTag();

    Int_t decayMode() const { return m_decayMode; }
    Int_t type() const { return m_type; }
    Double_t beamE() const { return m_beamE; }
    Double_t mass() const { return m_mass; }
    Double_t mBC() const { return m_mBC; }
    Double_t deltaE() const { return m_deltaE; }
    Int_t charge() const { return m_charge; }
    Int_t charm() const { return m_charm; }
    Int_t numOfChildren() const { return m_numOfChildren; }
    Double_t px() const { return m_px; }
    Double_t py() const { return m_py; }
    Double_t pz() const { return m_pz; }
    Double_t pe() const { return m_pe; }

    const std::vector<Int_t>& tracks() const { return m_tracks; }
    const std::vector<Int_t>& showers() const { return m_showers; }
    const std::vector<Int_t>& otherTracks() const { return m_otherTracks; }
    const std::vector<Int_t>& otherShowers() const { return m_otherShowers; }
    const std::vector<Int_t>& pionId() const { return m_pionId; }
    const std::vector<Int_t>& kaonId() const { return m_kaonId; }

    void setdecayMode( Int_t decayMode ) { m_decayMode = decayMode; }
    void settype( Int_t type ) { m_type = type; }
    void setbeamE( Double_t beamE ) { m_beamE = beamE; }
    void setmass( Double_t mass ) { m_mass = mass; }
    void setmBC( Double_t mBC ) { m_mBC = mBC; }
    void setdeltaE( Double_t deltaE ) { m_deltaE = deltaE; }
    void setcharge( Int_t charge ) { m_charge = charge; }
    void setcharm( Int_t charm ) { m_charm = charm; }
    void setnumOfChildren( Int_t numOfChildren ) { m_numOfChildren = numOfChildren; }
    void setpx( Double_t px ) { m_px = px; }
    void setpy( Double_t py ) { m_py = py; }
    void setpz( Double_t pz ) { m_pz = pz; }
    void setpe( Double_t pe ) { m_pe = pe; }

    void setTracks( const std::vector<Int_t>& tracks ) { m_tracks = tracks; }
    void setShowers( const std::vector<Int_t>& showers ) { m_showers = showers; }
    void setOtherTracks( const std::vector<Int_t>& tracks ) { m_otherTracks = tracks; }
    void setOtherShowers( const std::vector<Int_t>& showers ) { m_otherShowers = showers; }
    void setPionId( const std::vector<Int_t>& pionId ) { m_pionId = pionId; }
    void setKaonId( const std::vector<Int_t>& kaonId ) { m_kaonId = kaonId; }

    void addTrack( Int_t track ) { m_tracks.push_back( track ); }
    void addShower( Int_t shower ) { m_showers.push_back( shower ); }
    void addOtherTrack( Int_t track ) { m_otherTracks.push_back( track ); }
    void addOtherShower( Int_t shower ) { m_otherShowers.push_back( shower ); }
    void addPionId( Int_t pionId ) { m_pionId.push_back( pionId ); }
    void addKaonId( Int_t kaonId ) { m_kaonId.push_back( kaonId ); }

  private:
    Int_t m_decayMode;
    Int_t m_type;
    Double_t m_beamE;
    Double_t m_mass;
    Double_t m_mBC;
    Double_t m_deltaE;
    Int_t m_charge;
    Int_t m_charm;
    UInt_t m_numOfChildren;
    Double_t m_px;
    Double_t m_py;
    Double_t m_pz;
    Double_t m_pe;

    std::vector<Int_t> m_tracks;
    std::vector<Int_t> m_showers;
    std::vector<Int_t> m_otherTracks;
    std::vector<Int_t> m_otherShowers;
    std::vector<Int_t> m_pionId;
    std::vector<Int_t> m_kaonId;

    ClassDef( TEvtRecDTag, 1 )
};
#endif
