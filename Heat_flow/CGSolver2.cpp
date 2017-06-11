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
    //std::vector<double> y = A.MulVec(x);
    //std::vector<double> r = vec_diff(b,y);
    
    std::vector<double> r = vec_diff(b,A.MulVec(x));
    
    double L2norm0 = norm(r);
    std::vector<double> p = r;
    
    //std::cout << "L2norm0 = " << L2norm0 << std::endl;
    //std::cout << "r0[0] = " << r[0] << std::endl;
    //std::cout << "r0[1] = " << r[1] << std::endl;
    
    int niter = 0;
    
    std::vector<double> r1(x.size(),0);
    double alpha=0, beta=0, L2norm=0;
    
    
    //std::vector<double> y1(x.size(),0),r1(x.size(),0);
    //double alpha,scalar1,scalar2,L2norm,beta;
    
     
    while (niter < (int)x.size())
    {
        // write out solution every 10 iterations including first and last
        if (niter == 0 or niter % 10 == 0)
            WriteSolution(x,niter,soln_prefix);
        
        niter++;
        
        /*
        // compute alpha
        scalar1 = vec_mult(r,r);
        y = A.MulVec(p);
        scalar2 = vec_mult(p,y);
        alpha = scalar1/scalar2;
    
        std::cout << "rTr = " << scalar1 << std::endl;
        std::cout << "p[0]" << p[0] << std::endl;
        std::cout << "p[1]" << p[1] << std::endl;
        std::cout << "Ap[0]" << y[0] << std::endl;
        std::cout << "Ap[1]" << y[1] << std::endl;
        std::cout << "pTAp = " << scalar2 << std::endl;
        */
        
        alpha = vec_mult(r,r)/vec_mult(p,A.MulVec(p));
        
        //std::cout << "alpha0 = " << alpha << std::endl;
        
        // update x and compare norms to tolerance
        //y1 = scalar_mult(alpha,p);
        //x = vec_sum(x,y1);
    
        
        x = vec_sum(x,scalar_mult(alpha,p));
        
        //std::cout << "x1[0] = " << x[0] << std::endl;
        //std::cout << "x1[1] = " << x[1] << std::endl;
        
        
        //y1 = scalar_mult(alpha,y);
        //r1 = vec_diff(r,y1);
        
        
        r1 = vec_diff(r,scalar_mult(alpha,A.MulVec(p)));
         
        //std::cout << "r1[0] = " << r1[0] << std::endl;
        //std::cout << "r1[1] = " << r1[1] << std::endl;
        
        L2norm = norm(r1);
        if (L2norm/L2norm0 < tol) break;
        
        //std::cout << "L2norm/L2norm0 = " << L2norm/L2norm0 << std::endl;
        
        // compute beta
        beta = vec_mult(r1,r1) / vec_mult(r,r);
        
        //std::cout << "beta0 = " << beta << std::endl;
        
        
        //y1 = scalar_mult(beta,p);
        //p = vec_sum(r1,y1);
        
        
        p = vec_sum(r1,scalar_mult(beta,p));
         
        //std::cout << "p1[0] = " << p[0] << std::endl;
        //std::cout << "p1[1] = " << p[1] << std::endl;
        
        r = r1;
        
    }
    
    WriteSolution(x,niter,soln_prefix);
    
    // check if the solution converged to the specified tolerance
    if (L2norm/L2norm0 < tol) return niter;
    else return -1;
}