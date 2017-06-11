# Find SWIG
find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})

# Find Python
find_package(PythonLibs 2.7 REQUIRED)
include_directories(${PYTHON_INCLUDE_PATH})

# Specify where to look for include directories
include_directories(${SwigExample2_SOURCE_DIR}/include)

# Set SWIG custom flags
set(CMAKE_SWIG_FLAGS "-I${SwigExample2_SOURCE_DIR}/include")

# Set standard SWIG flags, in this case enabling C++ support
set_source_files_properties(example.i PROPERTIES CPLUSPLUS ON)

# Create Python extension module called example using interface
# file example.i and source file container.cpp
swig_add_module(example python example.i container.cpp)

# Link in the Python libraries
swig_link_libraries(example ${PYTHON_LIBRARIES})

# Copy test.py to the build directory
file(COPY test.py DESTINATION ${SwigExample2_BINARY_DIR}/src)