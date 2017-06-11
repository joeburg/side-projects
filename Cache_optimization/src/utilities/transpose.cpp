#include <memory>

#include "utilities.hpp"

int SimpleTranspose(double *a, int size, int ldim)
{
    if (a == NULL) return 1; // pointer must point to something
    if (ldim < size) return 1; // can't have negative padding
    
    double val;
    for (int i=0; i < size; i++)
    {
        for (int j=i+1; j < size; j++)
        {
            val = a[j + i*ldim];
            a[j + i*ldim] = a[i + j*ldim];
            a[i + j*ldim] = val;
        }
    }
    return 0;
};


int OptimizedTranspose(double *a, int size, int ldim, int blocksize)
{
    if (a == NULL) return 1;
    if (ldim < size) return 1;
    if (size % blocksize != 0) return 2;
    
    double val;
    int baseUppr, baseLwr, Boxidx;
    for (int i=0; i < size; i+=blocksize)
    {
        SimpleTranspose(a+(i+i*ldim),blocksize,ldim);  // blocks along diag
        for (int j=i+blocksize; j < size; j+=blocksize)
        {
            baseUppr = j + i*ldim;
            baseLwr = i + j*ldim;
            
            SimpleTranspose(a+baseUppr,blocksize,ldim); // blocks above diag
            SimpleTranspose(a+baseLwr,blocksize,ldim); // blocks below diag
            
            // swap upper and lower block across diag
            for (int k=0; k < blocksize; k++)
            {
                for (int l=0; l < blocksize; l++)
                {
                    Boxidx = l + k*ldim;
                    
                    val = a[baseUppr + Boxidx];
                    a[baseUppr + Boxidx] = a[baseLwr + Boxidx];
                    a[baseLwr + Boxidx] = val;
                }
            }
        }
    }
    return 0;
};