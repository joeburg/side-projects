/* purpose: main program that loads array, invokes a CG solver,
 and writes solution to file */

#include <fstream>
#include <iostream>
#include <vector>

#include "CGSolver.hpp"
#include "COO2CSR.hpp"
#include "matvecops.hpp"

int main(int argc, char *argv[])
{
    if (argc < 3)
    {
        std::cout << "Usage:" << std::endl;
        std::cout << "  " << argv[0] << " <matrix file> <solution file>" << std::endl;
        return 0;
    }
    
    std::string filename = argv[1];
    std::string ofilename = argv[2];
    
    // Initialize vectors to read the matrix file in COO format
    std::vector<int> i_idx,j_idx;
    std::vector<double> val;
    
    // Read the values from matrix file
    std::ifstream f(filename);
    int ni, nj;
    if (f.is_open())
    {
        //the first line is the size of the array
        f >> ni >> nj;
        
        // Read the data and populate the vectors
        int i, j;
        double value;
        while (f >> i >> j >> value)
        {
            i_idx.push_back(i);
            j_idx.push_back(j);
            val.push_back(value);
        }
    }
    f.close();


    // call the COO2CSR() function to convert the vectors to CSR format
    COO2CSR(val,i_idx,j_idx); // note: i_idx is now row_ptr and j_idx is col_idx
    
    // invoke the CG solver to solve the system
    // inialize b vector to 0's and x to 1's
    std::vector<double> b(ni,0),x(ni,1);
    double  tol = 1.e-5;
    
    int niter = CGSolver(val,i_idx,j_idx,b,x,tol);
    
    if (niter == -1)
        std::cout << "Failure: CG solver did not converge" << std::endl;
    else
        std::cout << "SUCCESS: CG solver converged in " << niter << " iterations." << std::endl;
    
    // write solution to file
    std::ofstream of;
    of.setf(std::ios::scientific, std::ios::floatfield);
    of.precision(4);
    of.open(ofilename);
    if (of.is_open())
    {
        for (int i=0; i < ni; i++)
            of << x[i] << std::endl;
    }
    of.close();
    return 0;
}