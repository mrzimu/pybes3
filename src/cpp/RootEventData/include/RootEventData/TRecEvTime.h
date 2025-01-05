#ifndef RootEventData_TRecEvTime_H
#define RootEventData_TRecEvTime_H 1

#include "TObject.h"
#include <vector>

using namespace std;

class TRecEvTime : public TObject {

  public:
    TRecEvTime();

    ~TRecEvTime();

    //   void Clear(Option_t *option ="");

    //    void PrInt_t(Option_t *option="") const;

    // Get

    Int_t status() const { return m_status; }
    Double_t estime() const { return m_estime; }
    Double_t quality() const { return m_quality; }
    // Set
    void setTest( Double_t estime ) { m_estime = estime; }
    void setStats( Int_t status ) { m_status = status; }
    void setQuality( Double_t quality ) { m_quality = quality; }

  private:
    Int_t m_status;
    Double_t m_estime;
    Double_t m_quality;

    // vector<MucRecHit> m_vecHits;

    ClassDef( TRecEvTime, 3 )
};

#endif
