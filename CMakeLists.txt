cmake_minimum_required(VERSION 3.20)

project(pybes VERSION 0.1.0)

include(GNUInstallDirs)

if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    set(CMAKE_INSTALL_PREFIX ${CMAKE_BINARY_DIR}/install CACHE PATH "Install Prefix" FORCE)
endif()

set(PYBES_INSTALL_PYTHONDIR ${CMAKE_INSTALL_PREFIX}/python/${PROJECT_NAME}
    CACHE PATH "Installation directory for python module" FORCE
)

include(cmake/pybes-dependencies.cmake)

add_subdirectory(src)

install(FILES cmake/setup-pybes.sh
    DESTINATION ${CMAKE_INSTALL_PREFIX}/bin
)

install(FILES
    test/test_besio.py
    test/test_besio1.rtraw
    test/test_besio2.rtraw
    DESTINATION ${CMAKE_INSTALL_PREFIX}/test
)