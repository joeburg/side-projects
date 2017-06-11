#include <iomanip>
#include <iostream>
#include <memory>

#include "timer.h"
#include "utilities.hpp"

int main(void)
{
    int size = 4096;
    int ldim = 4096;

    double *a = new double[ldim*size];
    initmatrix(a,size,ldim);
    
    std::cout << "Running SimpleTranspose()" << std::endl;
    double t0 = timer();
    int val = SimpleTranspose(a,size,ldim);
    double elapsedtime = timer() - t0;
    
    if (val)
    {
        std::cout << "The transpose operation was unsuccessful!" << std::endl;
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