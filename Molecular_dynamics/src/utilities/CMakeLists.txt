# Specify where to look for include directories
include_directories(${FinalProject_SOURCE_DIR}/include)

# define a variable utilities_source_files containing a list of the source files for the io library
set(utilities_source_files swap.cpp timer.c)

# create a library called utilities which includes the source files defined in utilities_source_files
add_library(utilities SHARED ${utilities_source_files})