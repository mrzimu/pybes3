pybind11_add_module(besio_cpp
    besio_cpp.cc
    root_io.cc
    raw_io.cc
)
target_compile_definitions(besio_cpp PRIVATE
    SAFETY_PARSE # PRINT_DEBUG_INFO
)

install(TARGETS besio_cpp LIBRARY DESTINATION ${SKBUILD_PROJECT_NAME}/besio)
