/* Purpose: implement the CG algorithm for a linear system */

#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "CGSolver.hpp"
#include "matvecops.hpp"
#include "sparse.hpp"


/* Funtion to write the solution of the CG solver to a file */
void WriteSolution(std::vector<double> x,
                   int niter,
                   std::string soln_prefix)
{
    // create output file name
    std::ostringstream stream;
    std::string outfile;
    stream << soln_prefix << std::setw(3) << std::setfill('0') << niter << ".txt";
    outfile = stream.str();
    
    // write temp values; will add coords in python file
    std::ofstream of;
    of.open(outfile);
    if (of.is_open())
    {
        for (unsigned int i=0; i < x.size(); i++)
            of << x[i] << std::endl;
    }
    of.close();
}


int CGSolver(SparseMatrix &A,
             std::vector<double> &b,
             std::vector<double> &x,
             double              tol,
             std::string soln_prefix)

{
    //compute initial norm and initalize data    
    std::vector<double> r = vec_diff(b,A.MulVec(x));
    double L2norm0 = norm(r);
    std::vector<double> p = r;

    int niter = 0;   
    std::vector<double> r1(x.size(),0);
    double alpha=0, beta=0, L2norm=0;
    while (niter < (int)x.size())
    {
        // write out solution every 10 iterations including first and last
        if (niter == 0 or niter % 10 == 0)
            WriteSolution(x,niter,soln_prefix);
        
        niter++;
        
        alpha = vec_mult(r,r)/vec_mult(p,A.MulVec(p));
        x = vec_sum(x,scalar_mult(alpha,p));
        r1 = vec_diff(r,scalar_mult(alpha,A.MulVec(p)));
        L2norm = norm(r1);
        // check if the solution has converged to the tolerance
        if (L2norm/L2norm0 < tol) break;

        beta = vec_mult(r1,r1) / vec_mult(r,r);
        p = vec_sum(r1,scalar_mult(beta,p));
        r = r1;
        
    }
    // write out last solution
    WriteSolution(x,niter,soln_prefix);
    
    // check if the solution converged to the specified tolerance
    if (L2norm/L2norm0 < tol) return niter;
    else return -1;
}