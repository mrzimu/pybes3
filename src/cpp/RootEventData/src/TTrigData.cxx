#include "RootEventData/TTrigData.h"

ClassImp( TTrigData );

//************************************************
//
TTrigData::TTrigData() { Clear(); }
//************************************************
//
TTrigData::~TTrigData() {}

void TTrigData::Clear( Option_t* option ) {}

void TTrigData::Print( Option_t* option ) const { TObject::Print( option ); }
