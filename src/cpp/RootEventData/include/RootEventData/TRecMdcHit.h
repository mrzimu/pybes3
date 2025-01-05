#ifndef RootEventData_TRecMdcHit_H
#define RootEventData_TRecMdcHit_H 1

#include "TObject.h"
#include <vector>

using namespace std;

class TRecMdcHit : public TObject {

  public:
    TRecMdcHit();

    ~TRecMdcHit();

    // is this hit grouped to any track?
    Bool_t isGrouped( void ) const { return m_isGrouped; }
    // extractors
    Int_t getId( void ) const { return m_id; }
    Int_t getTrkId( void ) const { return m_trkid; }
    Double_t getDriftDistLeft( void ) const { return m_ddl; }
    Double_t getDriftDistRight( void ) const { return m_ddr; }
    Double_t getErrDriftDistLeft( void ) const { return m_erddl; }
    Double_t getErrDriftDistRight( void ) const { return m_erddr; }
    Double_t getChisqAdd( void ) const { return m_pChisq; }
    Int_t getFlagLR( void ) const { return m_lr; }
    Int_t getStat( void ) const { return m_stat; }
    UInt_t getMdcId() const { return m_mdcid; }
    Double_t getTdc( void ) const { return m_tdc; }
    Double_t getAdc( void ) const { return m_adc; }
    Double_t getDriftT( void ) const { return m_driftT; }
    Double_t getDoca( void ) const { return m_doca; }
    Double_t getEntra( void ) const { return m_entra; }
    Double_t getZhit( void ) const { return m_zhit; }
    Double_t getFltLen( void ) const { return m_fltLen; }

    // modifiers
    void setIsGrouped( Bool_t isGrouped ) { m_isGrouped = isGrouped; }
    void setId( Int_t id ) { m_id = id; }
    void setTrkId( Int_t trkid ) { m_trkid = trkid; }
    void setDriftDistLeft( Double_t ddl ) { m_ddl = ddl; }
    void setDriftDistRight( Double_t ddr ) { m_ddr = ddr; }
    void setErrDriftDistLeft( Double_t erddl ) { m_erddl = erddl; }
    void setErrDriftDistRight( Double_t erddr ) { m_erddr = erddr; }
    void setChisqAdd( Double_t pChisq ) { m_pChisq = pChisq; }
    void setFlagLR( Int_t lr ) { m_lr = lr; }
    void setStat( Int_t stat ) { m_stat = stat; }
    void setMdcId( UInt_t mdcid ) { m_mdcid = mdcid; }
    void setTdc( Double_t tdc ) { m_tdc = tdc; }
    void setAdc( Double_t adc ) { m_adc = adc; }
    void setDriftT( Double_t driftT ) { m_driftT = driftT; }
    void setDoca( Double_t doca ) { m_doca = doca; }
    void setEntra( Double_t entra ) { m_entra = entra; }
    void setZhit( Double_t zhit ) { m_zhit = zhit; }
    void setFltLen( Double_t fltLen ) { m_fltLen = fltLen; }
    void setTRecMdcHit( const TRecMdcHit* mdchit ) {
        m_isGrouped = mdchit->isGrouped();
        m_id        = mdchit->getId();
        m_trkid     = mdchit->getTrkId();
        m_ddl       = mdchit->getDriftDistLeft();
        m_ddr       = mdchit->getDriftDistRight();
        m_erddl     = mdchit->getErrDriftDistLeft();
        m_erddr     = mdchit->getErrDriftDistRight();
        m_pChisq    = mdchit->getChisqAdd();
        m_lr        = mdchit->getFlagLR();
        m_stat      = mdchit->getStat();
        m_mdcid     = mdchit->getMdcId();
        m_tdc       = mdchit->getTdc();
        m_adc       = mdchit->getAdc();
        m_driftT    = mdchit->getDriftT();
        m_doca      = mdchit->getDoca();
        m_entra     = mdchit->getEntra();
        m_zhit      = mdchit->getZhit();
        m_fltLen    = mdchit->getFltLen();
    }

  private:
    Bool_t m_isGrouped;
    Int_t m_id;
    Int_t m_trkid;     // id of track containing this hit,if this hit
                       // belongs to no track, set as -1;
    Double_t m_ddl;    // drift distance left
    Double_t m_ddr;    // drift distance right
    Double_t m_erddl;  // error of drift distance left
    Double_t m_erddr;  //  error of drift distance right
    Double_t m_pChisq; // contribution to chisquare
    Int_t m_lr;        // flag indicating left or right 0:left 1:right 2:ambig
    Int_t m_stat;      // status flag
    UInt_t m_mdcid;    // MDC identifier
    Double_t m_tdc;    // corrected TDC
    Double_t m_adc;    // corrected ADC
    Double_t m_driftT; // drift time
    Double_t m_doca;   // distance of closesest approach for helix in the cell
    Double_t m_entra;  // entrance angle in azimuth
    Double_t m_zhit;   // z coordinate of the hit
    Double_t m_fltLen; // flight length of this hit

    ClassDef( TRecMdcHit, 3 )
};

#endif
