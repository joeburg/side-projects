%module(docstring="container c++ Extension module") containerExt
%include "std_string.i"

%{
// insert the module initialization code
#define SWIG_FILE_WITH_INIT
#include "container.hpp"
%}

// Parse these files to generate interface code
%include "container.hpp"

%template(containerFloat) container<float>;
%template(containerDouble) container<double>;