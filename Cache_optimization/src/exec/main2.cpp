#include <iomanip>
#include <iostream>
#include <memory>

#include "timer.h"
#include "utilities.hpp"

int main(void)
{
    // initialize matrix size, padding and blocksize
    int size = 4096;
    int ldim = 4096+16;
    int blocksize = 256;
    
    double *a = new double[ldim*size];
    initmatrix(a,size,ldim);

    std::cout << "Running OptimizedTranspose()" << std::endl;
    double t0 = timer();
    int val = OptimizedTranspose(a,size,ldim,blocksize);
    double elapsedtime = timer() - t0;
    
    if (val == 1)
    {
        std::cout << "The transpose operation was unsuccessful!" << std::endl;
        return 0;
    }
    else if (val == 2)
    {
        std::cout << "The block size must be a divisor of the matrix size." << std::endl;
        return 0;
    }
    else
    {
        double bandwidth = 2*size*size*(double)sizeof(double)/1.e9/elapsedtime;
        
        std::cout << "Effective bandwidth: " << std::fixed << std::setprecision(3) << bandwidth << " GB/sec" << std::endl;
    }
    delete[] a;
    return 0;
}
