cmake_minimum_required(VERSION 3.20)

project(pybes3-dev)

find_package(BOSS REQUIRED)

gaudi_add_executable(ExportIdx
    SOURCES
        src/ExportIdx.cc
    LINK
        ROOT::Core
        ROOT::Tree
        Identifier
)

gaudi_add_module(TestPybes3
    SOURCES
        src/ExportTestRawDataAlg.cc
        src/ExportTofHitStatusAlg.cc
    LINK
        Gaudi::GaudiKernel
        EventModel
        EmcRawEvent
        MdcRawEvent
        CgemRawEvent
        MucRawEvent
        TofRawEvent
        TrigEvent
        DstEvent
)
