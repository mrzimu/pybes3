#ifndef DigiRootData_TEmcDigi_H
#define DigiRootData_TEmcDigi_H 1

#include "TRawData.h"

class TEmcDigi : public TRawData {

  public:
    TEmcDigi();
    ~TEmcDigi();

    //   void Clear(Option_t *option ="");

    //   void Print(Option_t *option="") const;

    // Set Measure Word
    void setMeasure( const UInt_t measure );

    // Get Measure Word
    UInt_t getMeasure() const;

  private:
    UInt_t m_measure;

    ClassDef( TEmcDigi, 2 )
};

#endif // DigiRootData_TEmcDigi_H
