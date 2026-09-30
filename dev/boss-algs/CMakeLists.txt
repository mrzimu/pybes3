cmake_minimum_required(VERSION 3.20)

project(pybes3-dev)

find_package(BOSS REQUIRED)

add_subdirectory(NumAndGeom)
add_subdirectory(Pybes3ParticleGun)
