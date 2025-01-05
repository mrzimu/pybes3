#ifndef RootEventData_TRecMdcDedxHit_H
#define RootEventData_TRecMdcDedxHit_H 1

#include "TObject.h"

using namespace std;
class TRecMdcDedxHit : public TObject {

  public:
    TRecMdcDedxHit();

    ~TRecMdcDedxHit();
    // is this hit grouped to any track?
    Bool_t isGrouped( void ) { return m_isGrouped; }

    //   void Clear(Option_t *option ="")
    //   void PrInt_t(Option_t *option="")
    // get

    Int_t mdcHitId() { return m_mdcHitId; }
    Int_t mdcKalHelixSegId() { return m_mdcKalHelixSegId; }
    Int_t trkId( void ) const { return m_trkid; }
    Int_t flagLR( void ) const { return m_lr; }
    UInt_t mdcId() const { return m_mdcid; }
    Double_t pathLength( void ) const { return m_pathlength; }

    Double_t getDedx( void ) const { return m_dedx; }

    // set
    void setMdcHitId( const int mdcHitId ) { m_mdcHitId = mdcHitId; }
    void setMdcKalHelixSegId( const int mdcKalHelixSegId ) {
        m_mdcKalHelixSegId = mdcKalHelixSegId;
    }
    void setDedx( double dedx ) { m_dedx = dedx; }
    void setIsGrouped( Bool_t isGrouped ) { m_isGrouped = isGrouped; }
    void setTrkId( Int_t trkid ) { m_trkid = trkid; }
    void setFlagLR( Int_t lr ) { m_lr = lr; }
    void setMdcId( UInt_t mdcid ) { m_mdcid = mdcid; }
    void setPathLength( double pathlength ) { m_pathlength = pathlength; }

  private:
    Bool_t m_isGrouped;
    Int_t m_trkid; // id of track containing this hit,if this hit belongs to no track, set as
                   // -1;
    Int_t m_mdcHitId;         // dE/dx hit reference to MdcHit;
    Int_t m_mdcKalHelixSegId; // dE/dx hit reference to MdcKalHelixSeg;
    Int_t m_lr;               // flag indicating left or right 0:left 1:right 2:ambig
    UInt_t m_mdcid;           // MDC identifier
    Double_t m_pathlength;
    double m_dedx;

    ClassDef( TRecMdcDedxHit, 5 )
};

#endif
