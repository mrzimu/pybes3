#include "RootEventData/TEvtNavigator.h"
#include "TCollection.h" // Declares TIter
#include <iostream>

ClassImp( TEvtNavigator );

// Allocate the TObjArray just once

//***************************************************************
TEvtNavigator::TEvtNavigator() {}

//*****************************************************************
TEvtNavigator::~TEvtNavigator() {}

//*****************************************************************
void TEvtNavigator::Clear( Option_t* option ) {}

//*****************************************************************************
void TEvtNavigator::Print( Option_t* option ) const {
    TObject::Print( option );
    std::cout << "TEvtNavigator:  " << std::endl;
    std::cout << "    MDC MC hits " << m_mcMdcMcHits.size() << std::endl;
    std::cout << "    MDC tracks  " << m_mcMdcTracks.size() << std::endl;
    std::cout << "    EMC MC hits " << m_mcEmcMcHits.size() << std::endl;
    std::cout << "    EMC showers " << m_mcEmcRecShowers.size() << std::endl;
}
