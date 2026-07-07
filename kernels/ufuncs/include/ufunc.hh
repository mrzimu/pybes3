#pragma once

#define PY_SSIZE_T_CLEAN
#define NPY_TARGET_VERSION NPY_2_0_API_VERSION

#include "numpy/ndarraytypes.h"
#include "numpy/ufuncobject.h"
#include <Python.h>
#include <array>
#include <cstdint>
#include <tuple>
#include <utility>

// ===========================================================================
// function_traits
// ===========================================================================
template <typename F>
struct function_traits;

template <typename R, typename... Args>
struct function_traits<R ( * )( Args... )> {
    using args_tuple              = std::tuple<Args...>;
    static constexpr size_t nargs = sizeof...( Args );
};

template <typename R, typename... Args>
struct function_traits<R ( * )( Args... ) noexcept> {
    using args_tuple              = std::tuple<Args...>;
    static constexpr size_t nargs = sizeof...( Args );
};

template <typename T>
struct cpp_to_numpy;

template <>
struct cpp_to_numpy<double> {
    static constexpr char value = NPY_DOUBLE;
};
template <>
struct cpp_to_numpy<float> {
    static constexpr char value = NPY_FLOAT;
};
template <>
struct cpp_to_numpy<int64_t> {
    static constexpr char value = NPY_INT64;
};
template <>
struct cpp_to_numpy<int32_t> {
    static constexpr char value = NPY_INT32;
};
template <>
struct cpp_to_numpy<int16_t> {
    static constexpr char value = NPY_INT16;
};
template <>
struct cpp_to_numpy<int8_t> {
    static constexpr char value = NPY_INT8;
};
template <>
struct cpp_to_numpy<uint64_t> {
    static constexpr char value = NPY_UINT64;
};
template <>
struct cpp_to_numpy<uint32_t> {
    static constexpr char value = NPY_UINT32;
};
template <>
struct cpp_to_numpy<uint16_t> {
    static constexpr char value = NPY_UINT16;
};
template <>
struct cpp_to_numpy<uint8_t> {
    static constexpr char value = NPY_UINT8;
};
template <>
struct cpp_to_numpy<bool> {
    static constexpr char value = NPY_BOOL;
};

template <size_t NIN, size_t NOUT, auto F>
void ufunc_loop( char** args, const npy_intp* dimensions, const npy_intp* steps, void* data ) {
    npy_intp n = dimensions[0];
    char* in[NIN];
    char* out[NOUT];
    npy_intp in_step[NIN];
    npy_intp out_step[NOUT];
    for ( size_t i = 0; i < NIN; ++i )
    {
        in[i]      = args[i];
        in_step[i] = steps[i];
    }
    for ( size_t i = 0; i < NOUT; ++i )
    {
        out[i]      = args[NIN + i];
        out_step[i] = steps[NIN + i];
    }

    while ( n-- )
    {
        char* all_args[NIN + NOUT];
        for ( size_t i = 0; i < NIN; ++i ) all_args[i] = in[i];
        for ( size_t i = 0; i < NOUT; ++i ) all_args[NIN + i] = out[i];

        [&]<size_t... Is>( std::index_sequence<Is...> ) {
            using traits = function_traits<decltype( F )>;
            F( reinterpret_cast<std::tuple_element_t<Is, typename traits::args_tuple>>(
                all_args[Is] )... );
        }( std::make_index_sequence<NIN + NOUT>{} );

        for ( size_t i = 0; i < NIN; ++i ) in[i] += in_step[i];
        for ( size_t i = 0; i < NOUT; ++i ) out[i] += out_step[i];
    }
}

template <typename T>
struct remove_ptr {
    using type = T;
};
template <typename T>
struct remove_ptr<T*> {
    using type = T;
};
template <typename T>
using remove_ptr_t = typename remove_ptr<T>::type;

template <auto F>
constexpr auto make_types() {
    using traits       = function_traits<decltype( F )>;
    using args_tuple   = typename traits::args_tuple;
    constexpr size_t N = traits::nargs;

    return []<size_t... Is>( std::index_sequence<Is...> ) {
        return std::array<char, N>{
            cpp_to_numpy<remove_ptr_t<std::tuple_element_t<Is, args_tuple>>>::value... };
    }( std::make_index_sequence<N>{} );
}

template <auto... Funcs>
struct type_concat;

template <auto First, auto... Rest>
struct type_concat<First, Rest...> {
    static constexpr auto first   = make_types<First>();
    static constexpr auto rest    = type_concat<Rest...>::value;
    static constexpr size_t total = first.size() + rest.size();

    static constexpr std::array<char, total> value = []() {
        std::array<char, total> arr{};
        for ( size_t i = 0; i < first.size(); ++i ) arr[i] = first[i];
        for ( size_t i = 0; i < rest.size(); ++i ) arr[first.size() + i] = rest[i];
        return arr;
    }();
};

template <>
struct type_concat<> {
    static constexpr std::array<char, 0> value{};
};

template <size_t NIN, size_t NOUT, auto... Funcs>
void decl_ufunc( PyObject* d, const char* name, const char* doc = "" ) {
    static_assert( sizeof...( Funcs ) > 0, "At least one function is required" );

    static PyUFuncGenericFunction funcs[] = { ufunc_loop<NIN, NOUT, Funcs>... };

    static constexpr auto types = type_concat<Funcs...>::value;

    auto obj = PyUFunc_FromFuncAndData( funcs, NULL, types.data(), sizeof...( Funcs ), NIN,
                                        NOUT, PyUFunc_None, name, doc, 0 );
    if ( obj == NULL ) return;

    if ( PyDict_SetItemString( d, name, obj ) < 0 ) {
        Py_DECREF( obj );
        return;
    }
    Py_DECREF( obj );
}

template <auto... Funcs>
void decl_ufunc_11( PyObject* d, const char* name, const char* doc = "" ) {
    decl_ufunc<1, 1, Funcs...>( d, name, doc );
}

template <auto... Funcs>
void decl_ufunc_21( PyObject* d, const char* name, const char* doc = "" ) {
    decl_ufunc<2, 1, Funcs...>( d, name, doc );
}

template <auto... Funcs>
void decl_ufunc_31( PyObject* d, const char* name, const char* doc = "" ) {
    decl_ufunc<3, 1, Funcs...>( d, name, doc );
}

template <auto... Funcs>
void decl_ufunc_41( PyObject* d, const char* name, const char* doc = "" ) {
    decl_ufunc<4, 1, Funcs...>( d, name, doc );
}
