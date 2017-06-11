#ifndef solverbicgstab_hpp
#define solverbicgstab_hpp

#include <algorithm>
#include <cfloat>
#include <limits>
#include <numeric>
#include <vector>

#include "macros.hpp"
#include "solveroperators.hpp"
#include "sparse.hpp"
#include "timer.h"

#include <iostream>

/* Template class for a BiConjugate Gradient STABilized (BiCGSTAB) solver */

template <typename T>
class BiCGSTABSolver
{
  private:
    int niter = -1;                             // actual number of iterations that were run
    T l2normr = std::numeric_limits<T>::max();  // l2 norm of the residual at end of iterations
    double elapsedtime = -1.;                   // elapsed solver time

  public:

    /* Method to run solver.  On entry the vector x may contain an initial guess,
       and on return will contain the solution.  Optional parameters can be specified
       to control the maximum number of iterations (defaults to the size of the
       linear system if nitermax == -1), whether to use the contents of x as the
       initial guess for the solution, and the relative threshold for determining whether
       the solution is converged. */

    bool Solve(const CSRMatrix<T> &A,
               const std::vector<T> &x,
               std::vector<T> &b,
               int nitermax = -1,
               bool use_initial_guess = false,
               double threshold = 1.e-4);

    /* Returns the actual number of iterations performed */

    int GetNumberIterations(void);

    /* Returns the l2 norm of the residual */
    
    double Getl2NormResidual(void);

    /* Get solver elapsed time */

    double GetElapsedTime(void);
};


template <typename T>
bool BiCGSTABSolver<T>::Solve(const CSRMatrix<T> &A,
                              const std::vector<T> &b,
                              std::vector<T> &x,
                              int nitermax,
                              bool use_initial_guess,
                              double threshold)
{
    double t0 = timer();
    
    if (A.GetNumberRows() != (int)b.size())
        ThrowException("ERROR: The dimensions of the input matrix and solution vector are not compatible.");
    
    if (use_initial_guess)
    {
        if (((int)x.size() != A.GetNumberRows()) or (x.size() != b.size()))
            ThrowException("ERROR: The size of the initial guess vector is not consistent with the matrix or solution vector.");
    }
    else x = std::vector<T>(b.size(), T(0)); // initialize the vector to 0 if not using initial guess
    
    if (nitermax == -1) nitermax = (int)b.size();
    
    std::vector<T> r0 = b - A*x;
    T l2normr0 = l2norm(r0);
    std::vector<T> r0h = r0;
    if (dot(r0h,r0) == 0) return true;
    
    // perfrom initializations on vectors and scalars
    T rho0 = (T)1, alpha = (T)1, omega0 = (T)1;
    std::vector<T> v0(b.size(),0), p0(b.size(),0);
    std::vector<T> v, p, s, t, r;
    T rho, omega, beta;
    niter = 0;
    while (niter < nitermax)
    {
        niter++;
        rho = dot(r0h,r0);
        beta = (rho/rho0)*(alpha/omega0);
        p = r0 + beta*(p0 - omega0*v0);
        v = A*p;
        alpha = rho/dot(r0h,v);
        s = r0 - alpha*v;
        t = A*s;
        omega = dot(t,s)/dot(t,t);
        x = x + alpha*p + omega*s;
        r = s - omega*t;
        l2normr = l2norm(r);
        if (l2normr / l2normr0 < threshold)
        {
            elapsedtime = timer() - t0;
            return true;
        }
        
        // increment variables
        rho0 = rho;
        omega0 = omega;
        p0 = p;
        v0 = v;
        r0 = r;
    }
    elapsedtime = timer() - t0;
    return false;
}


template <typename T>
int BiCGSTABSolver<T>::GetNumberIterations(void)
{
  return niter;
}


template <typename T>
double BiCGSTABSolver<T>::Getl2NormResidual(void)
{
  return l2normr;
}


template <typename T>
double BiCGSTABSolver<T>::GetElapsedTime(void)
{
  return elapsedtime;
}


#endif /* solverbicgstab_hpp */
