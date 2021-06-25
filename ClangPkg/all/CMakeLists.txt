cmake_minimum_required(VERSION 3.13.4)
project(conanclang)

message(STATUS "Loading conan scripts for Clang dependencies...")

message(STATUS "Doing conan basic setup")
include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_subdirectory("clang")
# list(APPEND CMAKE_PROGRAM_PATH ${CONAN_BIN_DIRS})
# message(STATUS "Conan setup done. CMAKE_PROGRAM_PATH: ${CMAKE_PROGRAM_PATH}")
