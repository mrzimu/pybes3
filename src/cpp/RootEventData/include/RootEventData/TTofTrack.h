#ifndef RootEventData_TTofTrack_H
#define RootEventData_TTofTrack_H 1

#include "TObject.h"
#include <vector>

using namespace std;

class TTofTrack : public TObject {

  public:
    TTofTrack();
    ~TTofTrack();

    void setTofTrackID( Int_t tofTrackID ) { m_tofTrackID = tofTrackID; }
    void setTrackID( Int_t trackID ) { m_trackID = trackID; }
    void setTofID( Int_t tofID ) { m_tofID = tofID; }
    void setStatus( UInt_t status ) { m_status = status; }
    void setPath( Double_t path ) { m_path = path; }
    void setZrHit( Double_t zrhit ) { m_zrhit = zrhit; }
    void setPh( Double_t ph ) { m_ph = ph; }
    void setTof( Double_t tof ) { m_tof = tof; }
    void setErrTof( Double_t etof ) { m_sigma[0] = etof; }
    void setBeta( Double_t beta ) { m_beta = beta; }
    void setTexp( Double_t texp[5] ) {
        for ( Int_t i = 0; i < 5; i++ ) { m_texp[i] = texp[i]; }
    }
    void setTexpElectron( Double_t texpe ) { m_texp[0] = texpe; }
    void setTexpMuon( Double_t texpmu ) { m_texp[1] = texpmu; }
    void setTexpPion( Double_t texppi ) { m_texp[2] = texppi; }
    void setTexpKaon( Double_t texpk ) { m_texp[3] = texpk; }
    void setTexpProton( Double_t texpp ) { m_texp[4] = texpp; }
    void setToffset( Double_t toffset[6] ) {
        for ( Int_t i = 0; i < 6; i++ ) { m_toffset[i] = toffset[i]; }
    }
    void setToffsetElectron( Double_t toe ) { m_toffset[0] = toe; }
    void setToffsetMuon( Double_t tomu ) { m_toffset[1] = tomu; }
    void setToffsetPion( Double_t topi ) { m_toffset[2] = topi; }
    void setToffsetKaon( Double_t tok ) { m_toffset[3] = tok; }
    void setToffsetProton( Double_t top ) { m_toffset[4] = top; }
    void setToffsetAntiProton( Double_t topb ) { m_toffset[5] = topb; }
    void setSigma( Double_t sigma[6] ) {
        for ( Int_t i = 0; i < 6; i++ ) { m_sigma[i] = sigma[i]; }
    }
    void setSigmaElectron( Double_t se ) { m_sigma[0] = se; }
    void setSigmaMuon( Double_t smu ) { m_sigma[1] = smu; }
    void setSigmaPion( Double_t spi ) { m_sigma[2] = spi; }
    void setSigmaKaon( Double_t sk ) { m_sigma[3] = sk; }
    void setSigmaProton( Double_t sp ) { m_sigma[4] = sp; }
    void setSigmaAntiProton( Double_t spb ) { m_sigma[5] = spb; }

    void setQuality( Int_t quality ) { m_quality = quality; }

    void setT0( Double_t t0 ) { m_t0 = t0; }
    void setErrT0( Double_t errt0 ) { m_errt0 = errt0; }

    void setErrZ( Double_t errz ) { m_errz = errz; }
    void setPhi( Double_t phi ) { m_phi = phi; }
    void setErrPhi( Double_t errphi ) { m_errphi = errphi; }
    void setEnergy( Double_t energy ) { m_energy = energy; }
    void setErrEnergy( Double_t errenergy ) { m_errenergy = errenergy; }

    Int_t tofTrackID() const { return m_tofTrackID; }
    Int_t trackID() const { return m_trackID; }
    Int_t tofID() const { return m_tofID; }

    UInt_t status() const { return m_status; }

    Double_t path() const { return m_path; }
    Double_t zrhit() const { return m_zrhit; }
    Double_t ph() const { return m_ph; }
    Double_t tof() const { return m_tof; }
    Double_t errtof() const { return m_sigma[0]; }
    Double_t beta() const { return m_beta; }

    Double_t texp( Int_t i ) const { return m_texp[i]; }
    Double_t texpElectron() const { return m_texp[0]; }
    Double_t texpMuon() const { return m_texp[1]; }
    Double_t texpPion() const { return m_texp[2]; }
    Double_t texpKaon() const { return m_texp[3]; }
    Double_t texpProton() const { return m_texp[4]; }

    Double_t toffset( Int_t i ) const { return m_toffset[i]; }
    Double_t toffsetElectron() const { return m_toffset[0]; }
    Double_t toffsetMuon() const { return m_toffset[1]; }
    Double_t toffsetPion() const { return m_toffset[2]; }
    Double_t toffsetKaon() const { return m_toffset[3]; }
    Double_t toffsetProton() const { return m_toffset[4]; }
    Double_t toffsetAntiProton() const { return m_toffset[5]; }

    Double_t sigma( Int_t i ) const { return m_sigma[i]; }
    Double_t sigmaElectron() const { return m_sigma[0]; }
    Double_t sigmaMuon() const { return m_sigma[1]; }
    Double_t sigmaPion() const { return m_sigma[2]; }
    Double_t sigmaKaon() const { return m_sigma[3]; }
    Double_t sigmaProton() const { return m_sigma[4]; }
    Double_t sigmaAntiProton() const { return m_sigma[5]; }

    Int_t quality() const { return m_quality; }

    Double_t t0() const { return m_t0; }
    Double_t errt0() const { return m_errt0; }

    Double_t errz() const { return m_errz; }
    Double_t phi() const { return m_phi; }
    Double_t errphi() const { return m_errphi; }
    Double_t energy() const { return m_energy; }
    Double_t errenergy() const { return m_errenergy; }

  private:
    Int_t m_tofTrackID; // The ID of Tof Cluster reconstruction
    Int_t m_trackID;    // Track ID from MDC / Shower ID from EMC.
    Int_t m_tofID;      // Tof Counter ID.
    UInt_t m_status;    // Status.
                        // 0x0000 0000
                        //   0 0 0 0            0 0 0 0
                        //   | | | BR / 1 EC    | | | raw
                        //   | | East / 1 West  | | ReadOut Unit
                        //   No Hit             | Counter
                        //   01 1st Layer       Cluster
                        //   10 2nd Layer / 11 both Layers
                        // 0x 00 00 00 00 00(used)
                        //        |  |  counter number
                        //        |  east readout number
                        //        west readout number

    Double_t m_path;       // Distance of flight.
    Double_t m_zrhit;      // Track extrapolate Z or R Hit position.
    Double_t m_ph;         // Pulse height.
    Double_t m_tof;        // Time of flight.
    Double_t m_beta;       // Beta value of the track.
    Double_t m_texp[5];    // Expected time of flight of 5 sorts of particle.
    Double_t m_toffset[6]; // Time offset of e, mu, pi, k and p and pbar.
    Double_t m_sigma[6];   // Time resolution of 5+1 sorts of particle.
    Int_t m_quality;       // Data quality of reconstruction.
                           //  1: good charged track
                           //  2: neutral track with good hit
                           //  0: ZT-ZTDC didnot match
                           //  3: no hit in counter
                           //  4: two hits in counter
                           //  5: more than two hits in counter
                           //  6: only single end output of one layer
                           //  7: two hits in counter with bad match with ZTDC
                           // 10: initialize
                           //  ......
    Double_t m_t0;         // t0 from data set calibration.
    Double_t m_errt0;      // t0 sigma from tof calibration.

    Double_t m_errz;      // Error of zTDC(m_zrhit) for neutral track.
    Double_t m_phi;       // Angle of phi used for neutral track.
    Double_t m_errphi;    // Error of angle of phi.
    Double_t m_energy;    // Energy deposit for neutral track.
    Double_t m_errenergy; // Error of energy deposit for neutral track.

    ClassDef( TTofTrack, 2 )
};

#endif
