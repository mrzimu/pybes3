if(CMAKE_VERSION VERSION_GREATER_EQUAL 3.24)
    cmake_policy(SET CMP0135 NEW)
endif()

if(CMAKE_VERSION VERSION_GREATER_EQUAL 3.27)
    cmake_policy(SET CMP0148 NEW)
endif()

find_package(ROOT COMPONENTS Core Physics Tree REQUIRED)
find_package(pybind11 REQUIRED)

include(FetchContent)
set(AWKWARD_VERSION "v2.7.2")

FetchContent_Declare(
    awkward-headers
    URL      ${CMAKE_SOURCE_DIR}/external/awkward-header-only-${AWKWARD_VERSION}.zip
)
# Instead of using `FetchContent_MakeAvailable(awkward-headers)`, we manually load the target so
# that we can EXCLUDE_FROM_ALL
FetchContent_GetProperties(awkward-headers)
if(NOT awkward-headers_POPULATED)
    FetchContent_Populate(awkward-headers)
    add_subdirectory(${awkward-headers_SOURCE_DIR} ${awkward-headers_BINARY_DIR} EXCLUDE_FROM_ALL)
endif()
