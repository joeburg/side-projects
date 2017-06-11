#include <memory>

#include "utilities.hpp"

void initmatrix(double *a, int size, int ldim)
{
     /* set each matrix value to its index in linear, contiguous memory
     and set each index in padding to 0 */
    for (int i=0; i < size; i++)
    {
        for (int j=0; j < ldim; j++)
        {
            if (j < ldim) a[j + i*ldim] = (double)(j + i*ldim);
            else a[j + i*ldim] = 0.0;
        }
    }
};