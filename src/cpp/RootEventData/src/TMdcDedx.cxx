#include "RootEventData/TMdcDedx.h"
#include <cstdlib>
#include <iostream>

ClassImp( TMdcDedx );

//************************************************
//
TMdcDedx::TMdcDedx() { Clear(); }
//************************************************
//
TMdcDedx::~TMdcDedx() { Clear(); }

Double_t TMdcDedx::chi( int i ) const {
    double chi_ret = 0;
    switch ( i )
    {
    case 0: chi_ret = m_chiE; break;
    case 1: chi_ret = m_chiMu; break;
    case 2: chi_ret = m_chiPi; break;
    case 3: chi_ret = m_chiK; break;
    case 4: chi_ret = m_chiP; break;
    default:
        std::cerr << " TMdcDedx::chi: i= " << i << " - out of range" << std::endl;
        exit( 1 );
    }

    return chi_ret;
}
