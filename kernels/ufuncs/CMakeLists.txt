find_package(Python COMPONENTS Interpreter Development.Module NumPy REQUIRED)

python_add_library(_ufuncs MODULE WITH_SOABI
    src/mod.cc
    src/helix.cc
    src/identifier.cc
    src/detectors/cgem.cc
    src/detectors/emc.cc
    src/detectors/mdc.cc
    src/detectors/tof.cc
)

target_include_directories(_ufuncs PRIVATE ${CMAKE_CURRENT_LIST_DIR}/include)
target_link_libraries(_ufuncs PRIVATE Python::NumPy)

install(TARGETS _ufuncs DESTINATION ${SKBUILD_PROJECT_NAME}/_kernels/)
