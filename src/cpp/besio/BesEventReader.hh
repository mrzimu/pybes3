#pragma once

#include <TChain.h>
#include <TFile.h>
#include <memory>
#include <pybind11/pytypes.h>
#include <set>
#include <string>
#include <vector>

#include "BesRootFieldLeaf.hpp"
#include "RootEventData/TDigiEvent.h"
#include "RootEventData/TDstEvent.h"
#include "RootEventData/TEvtHeader.h"
#include "RootEventData/TEvtRecObject.h"
#include "RootEventData/THltEvent.h"
#include "RootEventData/TMcEvent.h"
#include "RootEventData/TRecTrackEvent.h"
#include "RootEventData/TTrigEvent.h"

namespace py = pybind11;

class BesEventReader {

  public:
    BesEventReader( const std::vector<std::string> filepaths );
    ~BesEventReader();

    /* * * * * * * * * * * * * * * * * * * * * */

    const long long py_get_entries() const;

    py::list py_get_available_fields() const;

    py::dict py_arrays( const long long entry_start = 0, const long long entry_stop = -1,
                        const std::vector<std::string> field_names = {} );

    /* * * * * * * * * * * * * * * * * * * * * */
    void optimize_branch_status();

    void set_branch_status( const std::string& branch_name, bool status );

    void set_field_status( const std::string& field_name, bool status );

    /* * * * * * * * * * * * * * * * * * * * * */
    void leaves_clear();

    void leaves_i_fill();

  private:
    TChain m_chain;

    std::set<std::string> m_branch_names;
    std::map<std::string, std::unique_ptr<IBesRootField>> m_fields;

    // long long, i.e. Long64_t is the type returned by TTree::GetEntries()
    long long m_entries{ -1 };

    /* EventHeader */
    TEvtHeader* m_evt_header{ nullptr };

    /* McEvent */
    TMcEvent* m_evt_mc{ nullptr };

    /* DigiEvent */
    TDigiEvent* m_evt_digi{ nullptr };

    /* EvtRecEvent */
    TEvtRecObject* m_evt_rec{ nullptr };

    /* DstEvent */
    TDstEvent* m_evt_dst{ nullptr };

    /* TrigEvent */
    TTrigEvent* m_evt_trig{ nullptr };

    /* HltEvent */
    THltEvent* m_evt_hlt{ nullptr };

    /* TRecTrackEvent */
    TRecTrackEvent* m_rec_trk_event{ nullptr };
};
