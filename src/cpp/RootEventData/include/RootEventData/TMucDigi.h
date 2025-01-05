#ifndef DigiRootData_TMucDigi_H
#define DigiRootData_TMucDigi_H 1

#include "TRawData.h"

class TMucDigi : public TRawData {

  public:
    TMucDigi();

    ~TMucDigi();

  private:
    ClassDef( TMucDigi, 4 )
};

#endif
