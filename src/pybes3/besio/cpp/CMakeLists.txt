pybind11_add_module(besio_cpp
    besio_cpp.cc
    raw_io.cc
)

target_link_libraries(besio_cpp PRIVATE uproot-custom)

install(TARGETS besio_cpp LIBRARY DESTINATION ${SKBUILD_PROJECT_NAME}/besio)
