cmake_minimum_required(VERSION 2.8)
project(FinalProject)

if (NOT CMAKE_BUILD_TYPE)
  message(STATUS "No build type selected, default to Release")
  set(CMAKE_BUILD_TYPE "Release")
endif()

# enable test running via ‘make test’ command
enable_testing()

add_subdirectory(src/exec)
add_subdirectory(src/tests)
add_subdirectory(src/utilities)
