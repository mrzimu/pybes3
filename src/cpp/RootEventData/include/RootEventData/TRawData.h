#ifndef DigiRootData_TRawData_H
#define DigiRootData_TRawData_H 1

#include "TObject.h"

class TRawData : public TObject {

  public:
    TRawData();

    ~TRawData();

    void initialize( UInt_t id, UInt_t time = 0, UInt_t charge = 0 );

    void Clear( Option_t* option = "" );

    void Print( Option_t* option = "" ) const;

    void setTrackIndex( const int trackIndex );

    // Get associated int id
    UInt_t getIntId() const;

    // Get time channel
    UInt_t getTimeChannel() const;

    // Get charge channel
    UInt_t getChargeChannel() const;

    // Get track index
    int getTrackIndex() const;

  private:
    UInt_t m_intId;
    UInt_t m_timeChannel;
    UInt_t m_chargeChannel;
    Int_t m_trackIndex;

    ClassDef( TRawData, 1 )
};

#endif
