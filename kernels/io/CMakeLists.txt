find_package(Python COMPONENTS Interpreter Development.Module NumPy REQUIRED)

pybind11_add_module(_io
    src/mod.cc
    src/raw_io.cc
)

target_link_libraries(_io PRIVATE uproot-custom Python::NumPy)

install(TARGETS _io LIBRARY DESTINATION ${SKBUILD_PROJECT_NAME}/kernels/)
