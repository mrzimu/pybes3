#ifndef RootEventData_TEmcTrack_H
#define RootEventData_TEmcTrack_H 1

#include "TObject.h"
#include <cmath>

class TEmcTrack : public TObject {

  public:
    TEmcTrack();
    ~TEmcTrack();

    //   void Clear(Option_t *option ="");

    //   void PrInt_t(Option_t *option="") const;
    // Get
    Int_t trackId() const { return m_trackId; }
    Int_t numHits() const { return m_numHits; }
    Int_t status() const { return m_status; }
    Int_t cellId() const { return m_cellId; }
    Int_t module() const { return m_module; }
    Double_t x() const { return m_x; }
    Double_t y() const { return m_y; }
    Double_t z() const { return m_z; }
    Double_t theta() const {
        return ( m_x == 0.0 && m_y == 0.0 && m_z == 0.0 )
                   ? 0.0
                   : std::atan2( std::sqrt( m_x * m_x + m_y * m_y ), m_z );
    }
    Double_t phi() const {
        return ( m_x == 0.0 && m_y == 0.0 ) ? 0.0 : std::atan2( m_y, m_x );
    }
    Double_t dx() const;
    Double_t dy() const;
    Double_t dz() const;
    Double_t dtheta() const { return m_dTheta; }
    Double_t dphi() const { return m_dPhi; }
    Double_t energy() const { return m_energy; }
    Double_t dE() const { return m_dE; }
    Double_t eSeed() const { return m_eSeed; }
    Double_t e3x3() const { return m_e3x3; }
    Double_t e5x5() const { return m_e5x5; }
    Double_t time() const { return m_time; }
    Double_t secondMoment() const { return m_secondMoment; }
    Double_t latMoment() const { return m_latMoment; }
    Double_t a20Moment() const { return m_a20Moment; }
    Double_t a42Moment() const { return m_a42Moment; }
    Double_t err( Int_t i ) const { return m_err[i]; }

    // Set
    void setTrackId( const Int_t trackId ) { m_trackId = trackId; }
    void setNumHits( const Int_t hit ) { m_numHits = hit; }
    void setStatus( const Int_t st ) { m_status = st; }
    void setCellId( const Int_t id ) { m_cellId = id; }
    void setModule( const Int_t mod ) { m_module = mod; }
    void setX( const Double_t x ) { m_x = x; }
    void setY( const Double_t y ) { m_y = y; }
    void setZ( const Double_t z ) { m_z = z; }
    void setEnergy( const Double_t e ) { m_energy = e; }
    void setDE( const Double_t de ) { m_dE = de; }
    void setDtheta( const Double_t dt ) { m_dTheta = dt; }
    void setDphi( const Double_t dpi ) { m_dPhi = dpi; }
    void setESeed( const Double_t eSeed ) { m_eSeed = eSeed; }
    void setE3x3( const Double_t e3x3 ) { m_e3x3 = e3x3; }
    void setE5x5( const Double_t e5x5 ) { m_e5x5 = e5x5; }
    void setTime( const Double_t time ) { m_time = time; }
    void setSecondMoment( const Double_t secondMoment ) { m_secondMoment = secondMoment; }
    void setLatMoment( const Double_t latMoment ) { m_latMoment = latMoment; }
    void setA20Moment( const Double_t a20Moment ) { m_a20Moment = a20Moment; }
    void setA42Moment( const Double_t a42Moment ) { m_a42Moment = a42Moment; }
    void setErr( const Double_t err[6] );

  private:
    Int_t m_trackId; // Track Id wensp Add 2005-10-19
    Int_t m_numHits; // Total number of hits
    Int_t m_status;  // Status
    Int_t m_cellId;  // Cell ID
    Int_t m_module;  // Module
    Double_t m_x;    //  Shower coordinates and errors
    Double_t m_y;
    Double_t m_z;
    Double_t m_dTheta;
    Double_t m_dPhi;
    Double_t m_energy; // Total energy observed in Emc
    Double_t m_dE;
    Double_t m_eSeed;        //// Energy of seed, only one
    Double_t m_e3x3;         // Energy of 3x3 crystals, totally 9 ones
    Double_t m_e5x5;         // Energy of 5x5 crystals, totally 25 ones
    Double_t m_time;         // Time measurement
    Double_t m_secondMoment; // add 2006-07-03
    Double_t m_latMoment;    // Lateral moment
    Double_t m_a20Moment;    // Zernike moment
    Double_t m_a42Moment;
    Double_t m_err[6]; // Error Matrix: 0:dxx, 1:dyy, 2:dzz
                       //               3:dxy, 4:dxz, 5:dyz

    ClassDef( TEmcTrack, 2 )
};

#endif // TrackRootData_TEmcTrack_H
