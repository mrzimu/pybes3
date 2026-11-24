#include <TFile.h>
#include <TTree.h>

#include <cstddef>
#include <exception>
#include <iostream>
#include <string>

#include <RootEventData/TDstEvent.h>

constexpr int kPrintFreq = 10000;

// The collections are stored in sub-branches of TDstEvent (TDstEvent.m_mdcTrackCol, ...).
constexpr const char* kDstBranches[] = { "m_mdcTrackCol", "m_mdcKalTrackCol", "m_mdcDedxCol",
                                         "m_extTrackCol", "m_tofTrackCol",    "m_emcTrackCol",
                                         "m_mucTrackCol" };

static int usage( const char* prog ) {
    std::cerr << "Usage: " << prog << " <input-file> <n-evt>" << std::endl;
    return 1;
}

int main( int argc, char** argv ) {
    if ( argc != 3 ) return usage( argv[0] );

    const char* input_file = argv[1];

    long long n_evt = 0;
    try
    {
        std::size_t parsed = 0;
        n_evt              = std::stoll( argv[2], &parsed );
        if ( argv[2][parsed] != '\0' || n_evt < 0 )
        {
            std::cerr << "Invalid number of events: " << argv[2] << std::endl;
            return 1;
        }
    } catch ( const std::exception& error )
    {
        std::cerr << "Invalid number of events '" << argv[2] << "': " << error.what()
                  << std::endl;
        return 1;
    }

    TFile file( input_file, "READ" );
    if ( !file.IsOpen() )
    {
        std::cerr << "Failed to open input file: " << input_file << std::endl;
        return 1;
    }

    TTree* tree = dynamic_cast<TTree*>( file.Get( "Event" ) );
    if ( !tree )
    {
        std::cerr << "Failed to get TTree 'Event' from file: " << input_file << std::endl;
        return 1;
    }

    tree->SetBranchStatus( "*", false );
    tree->SetBranchStatus( "TDstEvent", true );

    // SetBranchStatus only matches the top level branch names, so the wildcards "TDstEvent*"
    // and "TDstEvent.*" do not reach the sub-branches, and every collection has to be enabled
    // by its full name. Without this the entries are skipped and GetEntry() never touches the
    // event data, which turns the benchmark into a file-open measurement. The `found` counter
    // is the check that every name did match: a typo would otherwise be ignored silently.
    for ( const char* name : kDstBranches )
    {
        const std::string full_name = std::string( "TDstEvent." ) + name;

        UInt_t found = 0;
        tree->SetBranchStatus( full_name.c_str(), true, &found );
        if ( found == 0 )
        {
            std::cerr << "No branch '" << full_name << "' in tree 'Event'" << std::endl;
            return 1;
        }
    }

    // ROOT wants the address of a pointer and reuses the object it points to. The object is
    // intentionally never released: once TBranchElement has filled it, the collections belong
    // to the branch, and `TDstEvent::~TDstEvent()` double-frees them, so destroying a filled
    // event segfaults. A process-wide object is the usage BOSS itself relies on.
    TDstEvent* event = new TDstEvent;
    tree->SetBranchAddress( "TDstEvent", &event );

    const Long64_t n_entries = tree->GetEntries();
    if ( n_evt > n_entries )
    {
        std::cerr << "Requested number of events (" << n_evt << ") exceeds available entries ("
                  << n_entries << ")" << std::endl;
        return 1;
    }

    for ( Long64_t i = 0; i < n_evt; ++i )
    {
        if ( tree->GetEntry( i ) <= 0 )
        {
            std::cerr << "Failed to read entry " << i << std::endl;
            return 1;
        }

        if ( ( i + 1 ) % kPrintFreq == 0 )
            std::cout << "Processed " << i + 1 << " events" << std::endl;
    }

    file.Close();

    return 0;
}
