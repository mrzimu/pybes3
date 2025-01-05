cmake_minimum_required(VERSION 3.20)

if(CMAKE_VERSION VERSION_GREATER_EQUAL 3.27)
    cmake_policy(SET CMP0148 NEW)
endif()

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)


project(${SKBUILD_PROJECT_NAME}
    VERSION ${SKBUILD_PROJECT_VERSION}
    LANGUAGES CXX
)

set(PYBIND11_NEWPYTHON ON)
find_package(pybind11 REQUIRED)

pybind11_add_module(besio_cpp src/pybes/besio/besio_cpp.cc)
target_compile_definitions(besio_cpp PRIVATE
    SAFETY_PARSE # PRINT_DEBUG_INFO
)

install(TARGETS besio_cpp LIBRARY DESTINATION ${SKBUILD_PROJECT_NAME}/besio)
