#ifndef DigiRootData_TMdcDigi_H
#define DigiRootData_TMdcDigi_H 1

#include "TRawData.h"

class TMdcDigi : public TRawData {

  public:
    TMdcDigi();

    ~TMdcDigi();

    //   void Clear(Option_t *option ="");

    //    void Print(Option_t *option="") const;

    void setOverflow( const UInt_t overflow );

    // Get
    UInt_t getOverflow() const;

  private:
    UInt_t m_overflow;

    ClassDef( TMdcDigi, 2 )
};

#endif
