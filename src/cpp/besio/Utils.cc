#include <iostream>
#include <pybind11/pytypes.h>

#include "Utils.hh"

void debug_log( const std::string& file, int line, const std::string& msg ) {
    std::cout << file << ":" << line << ": " << msg << std::endl;
}

py::dict merge_dicts( const py::dict& dict1, const py::dict& dict2, bool overwrite ) {
    py::dict res;
    for ( auto item : dict1 ) { res[item.first] = item.second; }
    for ( auto item : dict2 )
    {
        if ( overwrite || !res.contains( item.first ) ) res[item.first] = item.second;
        else
            throw std::runtime_error( "Key " + std::string( py::str( item.first ) ) +
                                      " already exists in the dictionary." );
    }

    return res;
}