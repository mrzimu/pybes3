cmake_minimum_required(VERSION 3.20)

project(pybes3-dev)

find_package(BOSS REQUIRED)

gaudi_add_executable(ExportGid
    SOURCES
        src/ExportGid.cc
    LINK
        ROOT::Core
        ROOT::Tree
        Identifier
)

gaudi_add_module(TestPybes3
    SOURCES
        src/ExportTestRawDataAlg.cc
    LINK
        Gaudi::GaudiKernel
        EventModel
        EmcRawEvent
        MdcRawEvent
        CgemRawEvent
        MucRawEvent
        TofRawEvent
        TrigEvent
)
