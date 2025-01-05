#ifndef DigiRootData_TLumiDigi_H
#define DigiRootData_TLumiDigi_H 1

#include "TRawData.h"

class TLumiDigi : public TRawData {

  public:
    TLumiDigi();

    ~TLumiDigi();

    void setOverflow( const UInt_t overflow );

    // Get
    UInt_t getOverflow() const;

  private:
    UInt_t m_overflow;

    ClassDef( TLumiDigi, 1 )
};

#endif
