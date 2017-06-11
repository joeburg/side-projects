/* Purpose: implement the CG algorithm for a linear system */

#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "CGSolver.hpp"
#include "matvecops.hpp"

int CGSolver(std::vector<double> &val,
             std::vector<int>    &row_ptr,
             std::vector<int>    &col_idx,
             std::vector<double> &b,
             std::vector<double> &x,
             double              tol)

{
    //compute initial norm and initalize data
    std::vector<double> y = vec_mat_mult(val,row_ptr,col_idx,x);
    std::vector<double> r = vec_diff(b,y);
    double L2norm0 = norm(r);
    std::vector<double> p = r;
    
    int niter = 0;
    std::vector<double> y1(x.size(),0),r1(x.size(),0);
    double alpha,scalar1,scalar2,L2norm,beta;
    while (niter < (int)row_ptr.size()-1)
    {
        niter++;
    
        // compute alpha
        scalar1 = vec_mult(r,r);
        y = vec_mat_mult(val,row_ptr,col_idx,p);
        scalar2 = vec_mult(p,y);
        alpha = scalar1/scalar2;
        
        // update x and compare norms to tolerance
        y1 = scalar_mult(alpha,p);
        x = vec_sum(x,y1);
        y1 = scalar_mult(alpha,y);
        r1 = vec_diff(r,y1);
        L2norm = norm(r1);
        if (L2norm/L2norm0 < tol) break;
        
        // compute beta
        beta = vec_mult(r1,r1) / vec_mult(r,r);
        y1 = scalar_mult(beta,p);
        p = vec_sum(r1,y1);
        r = r1;
    }
    
    // check if the solution converged to the specified tolerance
    if (L2norm/L2norm0 < tol) return niter;
    else return -1;
}