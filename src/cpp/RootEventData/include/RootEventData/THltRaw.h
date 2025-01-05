#ifndef DigiRootData_THltRaw_H
#define DigiRootData_THltRaw_H 1

#include "TRawData.h"

class THltRaw : public TRawData {

  public:
    THltRaw();

    ~THltRaw();

    //   void Clear(Option_t *option ="");

    //    void Print(Option_t *option="") const;

  private:
    ClassDef( THltRaw, 2 )
};

#endif
