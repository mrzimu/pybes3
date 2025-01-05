#ifndef DigiRootData_TTofDigi_H
#define DigiRootData_TTofDigi_H 1

#include "TRawData.h"

class TTofDigi : public TRawData {

  public:
    TTofDigi();

    ~TTofDigi();

    //   void Clear(Option_t *option ="");

    //    void Print(Option_t *option="") const;

    void setOverflow( const UInt_t overflow );

    // Get
    UInt_t getOverflow() const;

  private:
    UInt_t m_overflow;

    ClassDef( TTofDigi, 1 )
};

#endif
