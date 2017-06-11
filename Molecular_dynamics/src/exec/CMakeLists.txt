# Find SWIG
find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})

# Find Python
find_package(PythonLibs 2.7 REQUIRED)
include_directories(${PYTHON_INCLUDE_PATH})

# Specify where to look for include directories
include_directories(${FinalProject_SOURCE_DIR}/include)

# Set SWIG custom flags
set(CMAKE_SWIG_FLAGS "-I${FinalProject_SOURCE_DIR}/include")

# Set standard SWIG flags, in this case enabling C++ support
set_source_files_properties(containerExt.i PROPERTIES CPLUSPLUS ON)

# Create Python extension module called containerExt using interface
# file containerExt.i and source file container.cpp
swig_add_module(containerExt python containerExt.i)

# Link in the Python libraries and utilities library
swig_link_libraries(containerExt ${PYTHON_LIBRARIES} utilities)

# Copy other Python files to the build directory
file(COPY main.py DESTINATION ${FinalProject_BINARY_DIR}/src/exec)


