cmake_minimum_required(VERSION 3.20)

if(CMAKE_VERSION VERSION_GREATER_EQUAL 3.27)
    cmake_policy(SET CMP0148 NEW)
endif()

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_STANDARD 17)

project(${SKBUILD_PROJECT_NAME}
    VERSION ${SKBUILD_PROJECT_VERSION}
    LANGUAGES CXX
)

set(PYBIND11_NEWPYTHON ON)
find_package(pybind11 REQUIRED)

add_subdirectory(src/pybes3/besio/cpp)
