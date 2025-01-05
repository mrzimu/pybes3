#ifndef RootEventData_TMucTrack_H
#define RootEventData_TMucTrack_H 1

#include "TObject.h"
#include <vector>

using namespace std;

class TMucTrack : public TObject {

  public:
    TMucTrack();

    ~TMucTrack();

    //   void Clear(Option_t *option ="");

    //    void PrInt_t(Option_t *option="") const;

    // Get
    Int_t trackId() const { return m_trackId; }
    Int_t id() const { return m_id; }
    Int_t status() const { return m_status; }
    Int_t type() const { return m_type; }

    Int_t startPart() const {
        return m_startPart;
    } // start position of track locates in which part
    Int_t endPart() const {
        return m_endPart;
    } // end   position of track locates in which part
    Int_t brLastLayer() const { return m_brLastLayer; } // last layer with hits in barrel
    Int_t ecLastLayer() const { return m_ecLastLayer; } // last layer with hits in end cap
    Int_t numHits() const { return m_numHits; }         // total hits on the track
    Int_t numLayers() const { return m_numLayers; }     // number of layers with hits
    Int_t maxHitsInLayer() const { return m_maxHitsInLayer; }

    Double_t depth() const { return m_depth; } // depth of the track transport in iron
    Double_t chi2() const { return m_chi2; }
    Int_t dof() const { return m_dof; }
    Double_t rms() const { return m_rms; }

    Double_t xPos() const { return m_xPos; } // position on the start of track in muc (vertex)
    Double_t yPos() const { return m_yPos; }
    Double_t zPos() const { return m_zPos; }

    Double_t xPosSigma() const { return m_xPosSigma; }
    Double_t yPosSigma() const { return m_yPosSigma; }
    Double_t zPosSigma() const { return m_zPosSigma; }

    Double_t px() const { return m_px; } // momentum on the start of track in muc
    Double_t py() const { return m_py; }
    Double_t pz() const { return m_pz; }

    Double_t distance() const { return m_distance; }
    Double_t deltaPhi() const { return m_deltaPhi; }

    // vector<Int_t> vecHits() const { return  m_vecHits ;}
    // added by LI Chunhua 2013/02/01
    Double_t kalRechi2() const { return m_kalrechi2; }
    Int_t kaldof() const { return m_kaldof; }
    Double_t kaldepth() const { return m_kaldepth; }
    Int_t kalbrLastLayer() const { return m_kalbrLastLayer; }
    Int_t kalecLastLayer() const { return m_kalecLastLayer; }
    //**********************

    // Set
    void setTrackId( Int_t trackId ) { m_trackId = trackId; }
    void setId( Int_t id ) { m_id = id; }
    void setStatus( Int_t st ) { m_status = st; }
    void setType( Int_t type ) { m_type = type; }

    void setStartPart( Int_t part ) { m_startPart = part; }
    void setEndPart( Int_t part ) { m_endPart = part; }
    void setBrLastLayer( Int_t layer ) { m_brLastLayer = layer; }
    void setEcLastLayer( Int_t layer ) { m_ecLastLayer = layer; }
    void setNumHits( Int_t numHits ) { m_numHits = numHits; }
    void setNumLayers( Int_t numLayers ) { m_numLayers = numLayers; }
    void setMaxHitsInLayer( Int_t maxHits ) { m_maxHitsInLayer = maxHits; }

    void setDepth( Double_t depth ) { m_depth = depth; }
    void setChi2( Double_t chi2 ) { m_chi2 = chi2; }
    void setDof( Int_t dof ) { m_dof = dof; }
    void setRms( Double_t rms ) { m_rms = rms; }

    void setXPos( Double_t x ) { m_xPos = x; }
    void setYPos( Double_t y ) { m_yPos = y; }
    void setZPos( Double_t z ) { m_zPos = z; }

    void setXPosSigma( Double_t x ) { m_xPosSigma = x; }
    void setYPosSigma( Double_t y ) { m_yPosSigma = y; }
    void setZPosSigma( Double_t z ) { m_zPosSigma = z; }

    void setPx( Double_t px ) { m_px = px; }
    void setPy( Double_t py ) { m_py = py; }
    void setPz( Double_t pz ) { m_pz = pz; }

    void setDistance( double dist ) { m_distance = dist; }
    void setDeltaPhi( double dphi ) { m_deltaPhi = dphi; }

    // added by LI Chunhua
    void setkalRechi2( Double_t ch ) { m_kalrechi2 = ch; }
    void setkalDof( Int_t f ) { m_kaldof = f; }
    void setkalDepth( Double_t de ) { m_kaldepth = de; }
    void setkalbrLastLayer( Int_t br ) { m_kalbrLastLayer = br; }
    void setkalecLastLayer( Int_t ec ) { m_kalecLastLayer = ec; }
    //******************
    // void  setVecHits(vector<Int_t>& vecHits) { m_vecHits = vecHits; }

  private:
    Int_t m_trackId; // Track ID wensp Add 2005-10-19
    Int_t m_id;      // Muc Identifier
    Int_t m_status;  // Muc Status
    Int_t m_type;    // Method of judge?

    Int_t m_startPart;      // In which part does the start position of track locate
    Int_t m_endPart;        // In which part does the end   position of track locate
    Int_t m_brLastLayer;    // Last layer with hits in barrel
    Int_t m_ecLastLayer;    // Last layer with hits in endcap
    Int_t m_numHits;        // Number of hits on track
    Int_t m_numLayers;      // Number of layer with  hits
    Int_t m_maxHitsInLayer; // Max number of hits in a layer

    Double_t m_depth; // Depth of iron penetrated
    Double_t m_chi2;  // Fit parameters
    Int_t m_dof;
    Double_t m_rms;

    Double_t m_xPos; // x position of muc track vertex
    Double_t m_yPos; // y position of muc track vertex
    Double_t m_zPos; // z position of muc track vertex

    Double_t m_xPosSigma;
    Double_t m_yPosSigma;
    Double_t m_zPosSigma;

    Double_t m_px; // px on muc track vertex
    Double_t m_py; // py on muc track vertex
    Double_t m_pz; // pz on muc track vertex

    Double_t m_distance;
    Double_t m_deltaPhi;

    // vector<Int_t> m_vecHits; //// hit list of the track wensp Add 2005-10-20
    // added by LI Chunhua
    Double_t m_kalrechi2;
    Int_t m_kaldof;
    Double_t m_kaldepth;
    Int_t m_kalbrLastLayer;
    Int_t m_kalecLastLayer;

    ClassDef( TMucTrack, 3 )
};

#endif
