#pragma once

#include <awkward/LayoutBuilder.h>
#include <cstddef>
#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <pybind11/stl.h>
#include <string>
#include <sys/types.h>

namespace py = pybind11;
namespace ak = awkward::LayoutBuilder;

/**
 * Debug log
 */
#ifdef DEBUG_IOCPP
#    define DEBUG_LOG( msg ) debug_log( __FILE__, __LINE__, msg )
#else
#    define DEBUG_LOG( msg )
#endif

void debug_log( const std::string& file, int line, const std::string& msg );

/**
 * Create a snapshot of the given builder, and return an `ak.Array` pyobject
 * @tparam T type of builder
 * @param builder builder
 * @return pyobject of Awkward Array
 */
template <typename T>
py::object snapshot_builder( const T& builder ) {
    // We need NumPy (to allocate arrays) and Awkward Array (ak.from_buffers).
    // pybind11 will raise a ModuleNotFoundError if they aren't installed.
    auto np = py::module::import( "numpy" );
    auto ak = py::module::import( "awkward" );

    auto dtype_u1 = np.attr( "dtype" )( "u1" );

    // How much memory to allocate?
    std::map<std::string, size_t> names_nbytes;
    builder.buffer_nbytes( names_nbytes );

    // Ask NumPy to allocate memory and get pointers to the raw buffers.
    py::dict py_container;
    std::map<std::string, void*> cpp_container;
    for ( auto name_nbytes : names_nbytes )
    {
        py::object array = np.attr( "empty" )( name_nbytes.second, dtype_u1 );

        size_t pointer = py::cast<size_t>( array.attr( "ctypes" ).attr( "data" ) );
        void* raw_data = (void*)pointer;

        py::str py_name( name_nbytes.first );
        py_container[py_name]            = array;
        cpp_container[name_nbytes.first] = raw_data;
    }

    // Write non-contiguous contents to memory.
    builder.to_buffers( cpp_container );

    // Build Python dictionary containing arrays.
    return ak.attr( "from_buffers" )( builder.form(), builder.length(), py_container );
}

/**
 * @brief A class representing a Python dictionary.
 *
 * This class provides a C++ interface to interact with Python dictionaries.
 * It allows you to manipulate and access key-value pairs in a dictionary.
 */
py::dict merge_dicts( const py::dict& dict1, const py::dict& dict2, bool overwrite = false );

/* ################################################################### */
/* ################################################################### */
/* ################################################################### */
/* ################################################################### */
/* ################################################################### */

using FieldMap = std::map<std::size_t, std::string>;

template <class... BUILDERS>
using RecordBuilder = ak::Record<FieldMap, BUILDERS...>;

template <std::size_t id, typename PRIMITIVE>
using SimpleItemField = ak::Field<id, ak::Numpy<PRIMITIVE>>;

template <std::size_t id, unsigned N, typename PRIMITIVE>
using SimpleArrayField = ak::Field<id, ak::Regular<N, ak::Numpy<PRIMITIVE>>>;

/**
 * @brief Template alias for a ragged numerical field.
 *
 * This template alias represents a ragged numerical field, which is a field
 * with a variable-length list of numerical values. It is used to define a
 * field with a specific ID and a primitive type.
 *
 * An example of array is like: [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
 *
 * @tparam id The ID of the field.
 * @tparam PRIMITIVE The primitive type of the numerical values.
 */
template <std::size_t id, typename PRIMITIVE>
using RaggedItemField = ak::Field<id, ak::ListOffset<int, ak::Numpy<PRIMITIVE>>>;

/**
 * @brief Template alias for a ragged fixed array field.
 *
 * This template alias represents a field in a data structure that stores a ragged fixed array.
 * It is used to define a field with a specific ID, number of elements, and primitive type.
 * The field is implemented using the Awkward Array library.
 *
 * An example of a 2D ragged fixed array is like (here N=3):
 * [
 *   [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
 *   [[10, 11, 12], [13, 14, 15]
 * ]
 * shape: nEntries * nElements * <N>
 *
 * @tparam id The ID of the field.
 * @tparam N The number of elements in the array.
 * @tparam PRIMITIVE The primitive type of the array elements.
 */
template <std::size_t id, unsigned N, typename PRIMITIVE>
using RaggedArrayField =
    ak::Field<id, ak::ListOffset<int, ak::Regular<N, ak::Numpy<PRIMITIVE>>>>;

/**
 * @brief Template alias for a ragged ragged field.
 *
 * This template alias represents a field with a ragged ragged structure, where the innermost
 * level of the field is a primitive type. It is used to define a field with two levels of
 * list offsets.
 *
 * An example of a ragged ragged field is like:
 * [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
 *
 * @tparam id The ID of the field.
 * @tparam PRIMITIVE The primitive type of the innermost level of the field.
 */
template <std::size_t id, typename PRIMITIVE>
using RaggedRaggedField =
    ak::Field<id, ak::ListOffset<int, ak::ListOffset<int, ak::Numpy<PRIMITIVE>>>>;

/**
 * @brief Template alias for a ragged string array field.
 *
 * This template alias represents a field in a data structure that stores a ragged array of
 * strings. The field is defined using the Field class from the ak namespace, with the template
 * parameters specifying the field ID and the types of the list offsets and strings.
 *
 * An example of a ragged string array is like:
 * [["a", "b"], ["c", "d", "e"], ["f", "g", "h", "i"]]
 *
 * @tparam id The ID of the field.
 */
template <std::size_t id>
using RaggedStringField = ak::Field<id, ak::ListOffset<int, ak::String<int>>>;

template <std::size_t id, unsigned N>
using RaggedArrayStringField =
    ak::Field<id, ak::ListOffset<int, ak::Regular<N, ak::String<int>>>>;

template <std::size_t id, unsigned N, typename PRIMITIVE>
using RaggedArrayRaggedField =
    ak::Field<id,
              ak::ListOffset<int, ak::Regular<N, ak::ListOffset<int, ak::Numpy<PRIMITIVE>>>>>;

template <std::size_t id, unsigned N>
using RaggedArrayRaggedStringField =
    ak::Field<id, ak::ListOffset<int, ak::Regular<N, ak::ListOffset<int, ak::String<int>>>>>;

template <std::size_t id, unsigned N>
using RaggedArrayRaggedStringField =
    ak::Field<id, ak::ListOffset<int, ak::Regular<N, ak::ListOffset<int, ak::String<int>>>>>;

template <std::size_t id, unsigned N, typename PRIMITIVE>
using RaggedArrayRaggedRaggedField = ak::Field<
    id,
    ak::ListOffset<
        int, ak::Regular<N, ak::ListOffset<int, ak::ListOffset<int, ak::Numpy<PRIMITIVE>>>>>>;

template <std::size_t id>
using RecExtTrackErrMatrixArrayField =
    ak::Field<id, ak::ListOffset<
                      int, ak::Regular<5, ak::Regular<6, ak::Regular<6, ak::Numpy<double>>>>>>;

template <std::size_t id, unsigned N1, unsigned N2, typename PRIMITIVE>
using RaggedArrayArrayField =
    ak::Field<id, ak::ListOffset<int, ak::Regular<N1, ak::Regular<N2, ak::Numpy<PRIMITIVE>>>>>;

template <std::size_t id, unsigned N1, unsigned N2, unsigned N3, typename PRIMITIVE>
using RaggedArrayArrayArrayField = ak::Field<
    id, ak::ListOffset<
            int, ak::Regular<N1, ak::Regular<N2, ak::Regular<N3, ak::Numpy<PRIMITIVE>>>>>>;