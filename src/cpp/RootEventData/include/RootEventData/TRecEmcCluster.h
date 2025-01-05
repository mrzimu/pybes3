#ifndef RootEventData_TRecEmcCluster_H
#define RootEventData_TRecEmcCluster_H 1

#include "TObject.h"
#include <iostream>

using namespace std;

class TRecEmcCluster : public TObject {

  public:
    TRecEmcCluster();
    ~TRecEmcCluster();

    // Get
    Int_t clusterId() const { return m_clusterId; }
    vector<Int_t> vecHits() const { return m_vecHits; }
    vector<Int_t> vecSeeds() const { return m_vecSeeds; }
    vector<Int_t> vecShowers() const { return m_vecShowers; }

    // Set
    void setClusterId( const Int_t id ) { m_clusterId = id; }
    void setVecHits( const vector<Int_t>& vecHits ) { m_vecHits = vecHits; }
    void setVecSeeds( const vector<Int_t>& vecSeeds ) { m_vecSeeds = vecSeeds; }
    void setVecShowers( const vector<Int_t>& vecShowers ) { m_vecShowers = vecShowers; }

  private:
    Int_t m_clusterId;
    vector<Int_t> m_vecHits;
    vector<Int_t> m_vecSeeds;
    vector<Int_t> m_vecShowers;

    ClassDef( TRecEmcCluster, 3 )
};

#endif // TrackRootData_TRecEmcCluster_H
