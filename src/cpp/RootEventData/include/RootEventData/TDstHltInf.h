#ifndef RootEventData_TDstHltInf_H
#define RootEventData_TDstHltInf_H 1

#include "TObject.h"
#include <vector>

// using namespace std;

class TDstHltInf : public TObject {

  public:
    TDstHltInf();
    ~TDstHltInf();

    void setEventType( const Int_t i ) { m_evtType = i; }
    void setAlgProcess( const Int_t i ) { m_algProcess = i; }
    void setCriteriaTable( const Int_t i ) { m_criTable = i; }
    void setVersion( const Int_t i ) { m_verNumber = i; }
    void setTotalEnergy( const Double_t etot ) { m_eTotal = etot; }
    void setNumber( const Int_t i ) { m_subNumber = i; }
    void setNCON( const Int_t i ) { m_conNumber = i; }

    Int_t getEventType() const { return m_evtType; }
    Int_t getAlgProcess() const { return m_algProcess; }
    Int_t getCriteriaTable() const { return m_criTable; }
    Int_t getVersion() const { return m_verNumber; }
    Double_t getTotalEnergy() const { return m_eTotal; }
    Int_t getNumber() const { return m_subNumber; }
    Int_t getNCON() const { return m_conNumber; }

  private:
    Int_t m_evtType;
    Int_t m_algProcess;
    Int_t m_criTable;
    Int_t m_verNumber;
    Double_t m_eTotal;
    Int_t m_subNumber;
    Int_t m_conNumber;

    ClassDef( TDstHltInf, 2 )
};

#endif // TrackRootData_TDstHltInf_H
