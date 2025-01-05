pybind11_add_module(_cpp_besio
    BesEventReader.cc
    Utils.cc
    ModuleDeclare.cc
    ModuleFunctions.cc
)

target_link_libraries(_cpp_besio
    PRIVATE
    RootEventData
    pybind11::pybind11
    ROOT::Tree
    awkward::layout-builder
)

install(TARGETS _cpp_besio
    DESTINATION ${PYBES_INSTALL_PYTHONDIR}/besio
)

if(PYBES_DEBUG)
    add_executable(io_test_read_speed
        test/test_read_speed.cc
    )

    target_link_libraries(io_test_read_speed
        PRIVATE RootEventData ROOT::Tree
    )

    install(TARGETS io_test_read_speed
        DESTINATION ${CMAKE_INSTALL_BINDIR}
    )
endif()