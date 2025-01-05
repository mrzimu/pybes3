#ifndef RootEventData_TRecEmcHit_H
#define RootEventData_TRecEmcHit_H 1

#include "TObject.h"
#include <iostream>

using namespace std;

class TRecEmcHit : public TObject {

  public:
    TRecEmcHit();
    ~TRecEmcHit();

    // Get
    Int_t cellId() const { return m_cellId; }
    Double_t energy() const { return m_energy; }
    Double_t time() const { return m_time; }

    // Set
    void setCellId( const Int_t id ) { m_cellId = id; }
    void setEnergy( const Double_t e ) { m_energy = e; }
    void setTime( const Double_t time ) { m_time = time; }

  private:
    Int_t m_cellId;
    Double_t m_energy;
    Double_t m_time;

    ClassDef( TRecEmcHit, 2 )
};

#endif // TrackRootData_TRecEmcHit_H
