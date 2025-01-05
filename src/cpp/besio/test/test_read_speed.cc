#include <chrono>
#include <iostream>
#include <vector>

#include "TChain.h"

#include "RootEventData/TDstEvent.h"

int main() {
    TChain chain( "Event" );

    chain.Add( "/mnt/f/08-BOSS-Compile/boss_data/01-rhopi/711/rhopi711_rec711_*.dst" );

    TDstEvent* event = new TDstEvent();
    chain.SetBranchAddress( "TDstEvent", &event );

    vector<double> vdouble;
    vector<int> vint;

    auto start = std::chrono::high_resolution_clock::now();
    for ( int i = 0; i < 100000; i++ )
    {
        chain.GetEntry( i );
        const TObjArray* obj_arr = event->getMdcTrackCol();
        for ( auto obj : *obj_arr )
        {
            const TMdcTrack* trk = static_cast<TMdcTrack*>( obj );

            vint.push_back( trk->trackId() );

            for ( int i = 0; i < 5; i++ ) vdouble.push_back( trk->helix( i ) );
            for ( int i = 0; i < 15; i++ ) vdouble.push_back( trk->err( i ) );

            vint.push_back( trk->stat() );
            vdouble.push_back( trk->chi2() );
            vint.push_back( trk->ndof() );
            vint.push_back( trk->nster() );
            vint.push_back( trk->nlayer() );
            vint.push_back( trk->firstLayer() );
            vint.push_back( trk->lastLayer() );
        }
    }
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> elapsed = end - start;
    std::cout << "Elapsed time: " << elapsed.count() << " s\n";
}