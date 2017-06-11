%module(docstring="CME 212 Assignment 6") pivcext

%header
%{
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>
    
#include "pivcext.h"
%}

/*---------------------------------------------------------------------*/
%typemap(in,numinputs=0) int nvalues
%{
    /* nvalues determined from input array */
%}

%typemap(in) int *a
%{
    PyArrayObject *inputarray = (PyArrayObject *)$input;
    arg1 = (int *)PyArray_DATA(inputarray);
    arg2 = PyArray_DIM(inputarray, 0);
%}

/*---------------------------------------------------------------------*/
%typemap(out) double *
%{
    if ($1 == NULL)
    {
        return Py_None;
    }
    
    npy_intp dims[2] = {arg2, arg3};
    PyObject *output = PyArray_SimpleNewFromData(2, dims, NPY_DOUBLE, (void *)$1);
    
    /* Assign ownership of the data to the Python object so memory is freed
     when the Python object is destroyed */
    
    PyArray_ENABLEFLAGS((PyArrayObject *)output, NPY_ARRAY_OWNDATA);
    
    $result = output;
%}

/*---------------------------------------------------------------------*/
// Parse pivcext.h and generate interface code
%include "pivcext.h"

%init
%{
    import_array();
%}

%feature("autodoc", "XCorr_c(double *a, double *b, int ni, int nj) -> R")
XCorr_c;
%feature("docstring")
"""
Returns an array, R, of size 2*ni-1 x 2*nj-1, that contains the overlap
values of windows a and b.
"""