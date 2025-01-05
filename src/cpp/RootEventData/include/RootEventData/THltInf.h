#ifndef RootEventData_THltInf_H
#define RootEventData_THltInf_H 1

#include "TObject.h"
#include <vector>

using namespace std;

class THltInf : public TObject {

  public:
    THltInf();
    ~THltInf();

    void setEventType( const Int_t i ) { m_evtType = i; }
    void setAlgProcess( const Int_t i ) { m_algProcess = i; }
    void setCriteriaTable( const Int_t i ) { m_criTable = i; }
    void setVersion( const Int_t i ) { m_verNumber = i; }
    void setTotalEnergy( const Double_t etot ) { m_eTotal = etot; }
    void setNumber( const Int_t i ) { m_subNumber = i; }
    void setNCON( const Int_t i ) { m_conNumber = i; }
    void setMdcData( const vector<Int_t>& vec ) { m_mdcData = vec; }
    void setTofData( const vector<Int_t>& vec ) { m_tofData = vec; }
    void setEmcData( const vector<Int_t>& vec ) { m_emcData = vec; }
    void setMucData( const vector<Int_t>& vec ) { m_mucData = vec; }
    void setConData( const vector<Int_t>& vec ) { m_conData = vec; }

    Int_t getEventType() const { return m_evtType; }
    Int_t getAlgProcess() const { return m_algProcess; }
    Int_t getCriteriaTable() const { return m_criTable; }
    Int_t getVersion() const { return m_verNumber; }
    Double_t getTotalEnergy() const { return m_eTotal; }
    Int_t getNumber() const { return m_subNumber; }
    Int_t getNCON() const { return m_conNumber; }
    vector<Int_t> getMdcData() const { return m_mdcData; }
    vector<Int_t> getTofData() const { return m_tofData; }
    vector<Int_t> getEmcData() const { return m_emcData; }
    vector<Int_t> getMucData() const { return m_mucData; }
    vector<Int_t> getConData() const { return m_conData; }

  private:
    Int_t m_evtType;
    Int_t m_algProcess;
    Int_t m_criTable;
    Int_t m_verNumber;
    Double_t m_eTotal;
    Int_t m_subNumber;
    Int_t m_conNumber;
    std::vector<Int_t> m_mdcData;
    std::vector<Int_t> m_tofData;
    std::vector<Int_t> m_emcData;
    std::vector<Int_t> m_mucData;
    std::vector<Int_t> m_conData;

    ClassDef( THltInf, 2 )
};

#endif // TrackRootData_THltInf_H
