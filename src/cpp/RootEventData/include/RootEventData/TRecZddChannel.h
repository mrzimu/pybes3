#ifndef RootEventData_TRecZddChannel_H
#define RootEventData_TRecZddChannel_H

#include "TObject.h"
#include <memory> //std::pair
#include <vector>

class TRecZddChannel : public TObject {
  public:
    TRecZddChannel();
    virtual ~TRecZddChannel();

    typedef std::vector<std::pair<Int_t, Float_t>> Fragments;

    Int_t channelId() const { return m_chId; }
    Int_t scanCode() const { return m_scanCode; }
    Int_t baseLine() const { return m_baseLine; }
    Int_t phase() const { return m_phase; }
    const Fragments& fragments() const { return m_frags; }

    void setChannelId( int chId ) { m_chId = chId; }
    void setScanCode( int scanCode ) { m_scanCode = scanCode; }
    void setBaseLine( int baseLine ) { m_baseLine = baseLine; }
    void setPhase( int phase ) { m_phase = phase; }
    void setFragments( const Fragments& frags ) { m_frags = frags; }

  private:
    Int_t m_chId;
    Int_t m_scanCode;
    Int_t m_baseLine;
    Int_t m_phase;
    std::vector<std::pair<Int_t, Float_t>> m_frags;

    ClassDef( TRecZddChannel, 1 )
};

#endif
