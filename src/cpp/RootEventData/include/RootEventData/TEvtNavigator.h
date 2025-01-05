#ifndef ROOT_TEvtNavigator_H
#define ROOT_TEvtNavigator_H 1

#include "TArray.h"
#include "TArrayD.h"
#include "TMap.h"
#include "TObject.h"

#include <map>

class TEvtNavigator : public TObject {

  public:
    TEvtNavigator();

    ~TEvtNavigator();

    void Clear( Option_t* option = "" );

    void Print( Option_t* option = "" ) const;

    void LoadMcMdcMcHits( std::multimap<int, int>& map ) { m_mcMdcMcHits = map; }
    void LoadMcMdcTracks( std::multimap<int, int>& map ) { m_mcMdcTracks = map; }
    void LoadMcEmcMcHits( std::multimap<int, int>& map ) { m_mcEmcMcHits = map; }
    void LoadMcEmcRecShowers( std::multimap<int, int>& map ) { m_mcEmcRecShowers = map; }

  private:
    std::multimap<int, int> m_mcMdcMcHits; // auxillary list McParticle id <-> MdcMcHit
                                           // (=MdcRecHit) id
    std::multimap<int, int> m_mcMdcTracks; // McParticle id <-> RecMdcTrack (RecMdcKalTrack) id
    std::multimap<int, int> m_mcEmcMcHits; // auxiallry list McParticle id <-> EmcMcHit
                                           // (=EmcRecHit) id
    std::multimap<int, int> m_mcEmcRecShowers; // McParticle id <-> EmcRecShower id

    //    Int_t mode;
    //    TArrayD arr;
    //    TMap map;

    ClassDef( TEvtNavigator, 1 )
};

#endif
