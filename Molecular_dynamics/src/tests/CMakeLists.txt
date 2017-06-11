set( CMAKE_MODULE_PATH
 ${FinalProject_SOURCE_DIR}/src/tests)

find_package( CPPUnit REQUIRED )

# Specify where to look for include directories
include_directories(${FinalProject_SOURCE_DIR}/include ${CPPUNIT_INCLUDE_DIRS})

# Directories to look for libraries
link_directories(${MyProject_BINARY_DIR}/src/utilities)

# Compile tests from tests.cpp
add_executable(tests tests.cpp)

# tests should link to the utilities libraries
target_link_libraries(tests ${CPPUNIT_LIBRARIES} utilities)

# copy the data files used for the test to the test build
file(COPY solution0.dat solution10_ref.dat DESTINATION ${FinalProject_BINARY_DIR}/src/tests)

# Tests to run
add_test(BasicTests tests)