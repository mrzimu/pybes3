#ifndef RootEventData_TJobInfo_H
#define RootEventData_TJobInfo_H 1

#include "TObject.h"
#include <string>
#include <vector>
using namespace std;

class TJobInfo : public TObject {

  public:
    TJobInfo();
    ~TJobInfo();

    string getBossVer() const { return m_bossVer; }
    vector<string> getJobOptions() const { return m_jobOptions; }
    string getDecayOptions() const { return m_decayOptions; }
    std::vector<int> getTotEvtNo() const { return m_totEvtNo; }

    void setBossVer( string ver ) { m_bossVer = ver; }
    void addJobOptions( string opt ) { m_jobOptions.push_back( opt ); }
    void setJobOptions( vector<string> opt ) { m_jobOptions = opt; }
    void setDecayOptions( string opt ) { m_decayOptions = opt; }
    void setTotEvtNo( std::vector<int> i ) { m_totEvtNo = i; }

  private:
    string m_decayOptions;
    string m_bossVer;
    vector<string> m_jobOptions;
    std::vector<int> m_totEvtNo;

    ClassDef( TJobInfo, 1 )
};

#endif // TrackRootData_TJobInfo_H
