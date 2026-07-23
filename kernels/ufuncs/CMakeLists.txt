find_package(Python COMPONENTS Interpreter Development.Module NumPy REQUIRED)

python_add_library(ufuncs MODULE WITH_SOABI
    src/mod.cc
    src/helix.cc
    src/identifier.cc
    src/cgem.cc
    src/emc.cc
    src/mdc.cc
    src/tof.cc
)

target_include_directories(ufuncs PRIVATE ${CMAKE_CURRENT_LIST_DIR}/include)
target_link_libraries(ufuncs PRIVATE Python::NumPy)

install(TARGETS ufuncs DESTINATION ${SKBUILD_PROJECT_NAME}/kernels/)
