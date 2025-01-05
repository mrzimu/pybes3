#ifndef RootEventData_TEvtRecPi0_H
#define RootEventData_TEvtRecPi0_H

#include "TObject.h"
#include <vector>

class TEvtRecPi0 : public TObject {

  public:
    TEvtRecPi0();
    ~TEvtRecPi0();

    Double_t unconMass() const { return m_unconMass; }
    Double_t chisq() const { return m_chisq; }

    Double_t hiPxfit() const { return m_hiPx; }
    Double_t hiPyfit() const { return m_hiPy; }
    Double_t hiPzfit() const { return m_hiPz; }
    Double_t hiPefit() const { return m_hiPe; }

    Double_t loPxfit() const { return m_loPx; }
    Double_t loPyfit() const { return m_loPy; }
    Double_t loPzfit() const { return m_loPz; }
    Double_t loPefit() const { return m_loPe; }

    Int_t hiEnGamma() const { return m_hiEnGamma; }
    Int_t loEnGamma() const { return m_loEnGamma; }

    // setters
    void setUnconMass( Double_t unconMass ) { m_unconMass = unconMass; }
    void setChisq( Double_t chisq ) { m_chisq = chisq; }

    void setHiPxfit( Double_t hiPx ) { m_hiPx = hiPx; }
    void setHiPyfit( Double_t hiPy ) { m_hiPy = hiPy; }
    void setHiPzfit( Double_t hiPz ) { m_hiPz = hiPz; }
    void setHiPefit( Double_t hiPe ) { m_hiPe = hiPe; }

    void setLoPxfit( Double_t loPx ) { m_loPx = loPx; }
    void setLoPyfit( Double_t loPy ) { m_loPy = loPy; }
    void setLoPzfit( Double_t loPz ) { m_loPz = loPz; }
    void setLoPefit( Double_t loPe ) { m_loPe = loPe; }

    void setHiEnGamma( Int_t hiEnGamma ) { m_hiEnGamma = hiEnGamma; }
    void setLoEnGamma( Int_t loEnGamma ) { m_loEnGamma = loEnGamma; }

  private:
    Double_t m_unconMass;
    Double_t m_chisq;

    Double_t m_hiPx;
    Double_t m_hiPy;
    Double_t m_hiPz;
    Double_t m_hiPe;

    Double_t m_loPx;
    Double_t m_loPy;
    Double_t m_loPz;
    Double_t m_loPe;

    Int_t m_hiEnGamma;
    Int_t m_loEnGamma;

    ClassDef( TEvtRecPi0, 1 )
};
#endif
