#pragma once

#include <pybind11/pybind11.h>

/**
 * Checks if the given filepath is in BES format.
 *
 * @param filepath The filepath to check.
 * @return True if the filepath is in BES format, false otherwise.
 */
bool py_is_bes_format( const std::string& filepath );
