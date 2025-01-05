#ifndef RootEventData_TRecMdcKalHelixSeg_H
#define RootEventData_TRecMdcKalHelixSeg_H 1

#include "TObject.h"
#include <vector>

using namespace std;

class TRecMdcKalHelixSeg : public TObject {

  public:
    TRecMdcKalHelixSeg();

    ~TRecMdcKalHelixSeg();

    // extractors
    Int_t getTrackId( void ) const { return m_trackid; }
    Int_t getFlagLR( void ) const { return m_lr; }
    UInt_t getMdcId() const { return m_mdcid; }
    Double_t getTdc( void ) const { return m_tdc; }
    Double_t getAdc( void ) const { return m_adc; }
    Double_t getZhit( void ) const { return m_zhit; }
    Double_t getTof( void ) const { return m_tof; }
    Double_t getDocaIncl( void ) const { return m_docaincl; }
    Double_t getDocaExcl( void ) const { return m_docaexcl; }
    Double_t getDD( void ) const { return m_dd; }
    Double_t getEntra( void ) const { return m_entra; }
    Double_t getDT( void ) const { return m_driftT; }
    //   const Int_t    getLayerId(void) const { return m_layerid; }
    //   const Double_t getDrIncl(void) const {return m_drincl; }
    //   const Double_t getFi0Incl(void) const {return m_phi0incl; }
    //   const Double_t getCpaIncl(void) const {return m_kappaincl; }
    //   const Double_t getDzIncl(void) const {return m_dzincl; }
    //   const Double_t getTanlIncl(void) const {return m_tanlincl; }
    //   const Double_t getDrExcl(void) const {return m_drexcl; }
    //   const Double_t getFi0Excl(void) const {return m_phi0excl; }
    //   const Double_t getCpaExcl(void) const {return m_kappaexcl; }
    //   const Double_t getDzExcl(void) const {return m_dzexcl; }
    //   const Double_t getTanlExcl(void) const {return m_tanlexcl; }
    Double_t getHelixIncl( Int_t i ) const { return m_helixincl[i]; }
    //   const Double_t getErrorIncl(Int_t i, Int_t j) const {return m_errorincl[i][j]; }
    Double_t getHelixExcl( Int_t i ) const { return m_helixexcl[i]; }
    //   const Double_t getErrorExcl(Int_t i, Int_t j) const {return m_errorexcl[i][j]; }

    // modifiers
    void setTrackId( Int_t trkid ) { m_trackid = trkid; }
    void setFlagLR( Int_t lr ) { m_lr = lr; }
    void setMdcId( UInt_t mdcid ) { m_mdcid = mdcid; }
    void setTdc( Double_t tdc ) { m_tdc = tdc; }
    void setAdc( Double_t adc ) { m_adc = adc; }
    void setZhit( Double_t zhit ) { m_zhit = zhit; }
    void setTof( Double_t tof ) { m_tof = tof; }
    void setDocaIncl( Double_t docaincl ) { m_docaincl = docaincl; }
    void setDocaExcl( Double_t docaexcl ) { m_docaexcl = docaexcl; }
    void setDD( Double_t dd ) { m_dd = dd; }
    void setEntra( Double_t entra ) { m_entra = entra; }
    void setDT( Double_t driftT ) { m_driftT = driftT; }
    //   void setLayerId(Int_t layerid) { m_layerid = layerid;    }
    //   void setDrIncl (Double_t drincl) { m_drincl = drincl; }
    //   void setFi0Incl (Double_t phi0incl) { m_phi0incl = phi0incl; }
    //   void setCpaIncl (Double_t kappaincl) { m_kappaincl = kappaincl; }
    //   void setDzIncl (Double_t dzincl) { m_dzincl = dzincl; }
    //   void setTanlIncl (Double_t tanlincl) { m_tanlincl = tanlincl; }
    //   void setDrExcl (Double_t drexcl) { m_drexcl = drexcl; }
    //   void setFi0Excl (Double_t phi0excl) { m_phi0excl = phi0excl; }
    //   void setCpaExcl (Double_t kappaexcl) { m_kappaexcl = kappaexcl; }
    //   void setDzExcl (Double_t dzexcl) { m_dzexcl = dzexcl; }
    //   void setTanlExcl (Double_t tanlexcl) { m_tanlexcl = tanlexcl; }
    void setHelixIncl( const Double_t helix[5] ) {
        for ( Int_t i = 0; i < 5; i++ ) m_helixincl[i] = helix[i];
    }
    void setHelixExcl( const Double_t helix[5] ) {
        for ( Int_t i = 0; i < 5; i++ ) m_helixexcl[i] = helix[i];
    }
    //   void setErrorIncl(const Double_t error[5][5]){
    //	   for (Int_t i= 0 ; i<5 ; i++)
    //		   for (Int_t j=0; j<=i; j++){
    //			   m_errorincl[i][j] = error[i][j];
    //			   m_errorincl[j][i] = error[i][j];
    //		   }
    //   }
    //   void setErrorExcl (const Double_t error[5][5]){
    //	   for(Int_t i=0; i<5; i++) {
    //		   for (Int_t j=0; j<=i; j++){
    //			   m_errorexcl[i][j] = error[i][j];
    //			   m_errorexcl[j][i] = error[i][j];
    //		   }
    //	   }
    //   }

  private:
    Int_t m_trackid; // id of track containing this hit,if this hit
    // belongs to no track, set as -1;
    Int_t m_lr;          // flag indicating left or right 0:left 1:right 2:ambig
    UInt_t m_mdcid;      // MDC identifier
    Double_t m_tdc;      // corrected TDC
    Double_t m_adc;      // corrected ADC
    Double_t m_zhit;     // z coordinate of the hit
    Double_t m_tof;      // time of flight
    Double_t m_docaincl; // distance of closesest approach for helix in the cell
    Double_t m_docaexcl;
    Double_t m_dd;     // drift distance
    Double_t m_entra;  // entrance angle in azimuth
    Double_t m_driftT; // drift time
    //  Int_t m_layerid; // layer number
    //  Double_t m_drincl;
    //  Double_t m_phi0incl;
    //  Double_t m_kappaincl;
    //  Double_t m_dzincl;
    //  Double_t m_tanlincl;
    //  Double_t m_drexcl;
    //  Double_t m_phi0excl;
    //  Double_t m_kappaexcl;
    //  Double_t m_dzexcl;
    //  Double_t m_tanlexcl;
    Double_t m_helixincl[5];
    //   Double_t m_errorincl[5][5];
    Double_t m_helixexcl[5];
    //   Double_t m_errorexcl[5][5];

    ClassDef( TRecMdcKalHelixSeg, 3 )
};

#endif
