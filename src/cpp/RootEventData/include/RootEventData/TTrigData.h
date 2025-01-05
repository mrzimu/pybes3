#ifndef RootEventData_TTrigData_H
#define RootEventData_TTrigData_H 1

#include "TObject.h"

using namespace std;

class TTrigData : public TObject {

  public:
    TTrigData();
    virtual ~TTrigData();

    void Clear( Option_t* option = "" );

    void Print( Option_t* option = "" ) const;

    // Set
    void setTrigCondition( int i, int j ) { m_trigcond[i] = j; }
    void setTrigCondition( const int* cond ) {
        for ( int i = 0; i < 48; i++ ) m_trigcond[i] = cond[i];
    }
    void setTrigChannel( int i, int j ) { m_trigChan[i] = j; }
    void setTrigChannel( const int* chan ) {
        for ( int i = 0; i < 16; i++ ) m_trigChan[i] = chan[i];
    }
    void setTimeWindow( int i ) { m_timeWindow = i; }
    void setTimingType( int i ) { m_Timing = i; }
    void setPreScale( bool i ) { m_preScale = i; }

    // Get
    int getTrigCondition( int i ) const { return m_trigcond[i]; }
    const int* getTrigCondition() const { return m_trigcond; }
    int getTrigChannel( int i ) const { return m_trigChan[i]; }
    const int* getTrigChannel() const { return m_trigChan; }
    int getTimeWindow() const { return m_timeWindow; }
    int getTimingType() const { return m_Timing; }
    bool getPreScale() const { return m_preScale; }

  private:
    Bool_t m_preScale;    // PreScale for bhabha events
    Int_t m_trigcond[48]; // Trigger conditions from 0 to 47
    Int_t m_trigChan[16]; // Trigger channel from 0 to 15
    Int_t m_timeWindow;   // The time window of trigger system
    Int_t m_Timing;       // Time type, 0: No timing 1: TOF 2: MDC 3: EMC

    ClassDef( TTrigData, 2 )
};

#endif // TrackRootData_TTrigData_H
