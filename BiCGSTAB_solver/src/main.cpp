#include <iostream>
#include <string>
#include <vector>

#include "solverbicgstab.hpp"
#include "sparse.hpp"
#include "vectorio.hpp"


int main(int argc, char *argv[])
{
  /* Gather command line arguments */

  if (argc < 4)
  {
    std::cout << "Usage:" << std::endl;
    std::cout << "  " << argv[0] << " <matrix> <rhs> <soln> [nitermax]" << std::endl;
    return 0;
  }
  std::string matrix = argv[1];
  std::string rhs = argv[2];
  std::string soln = argv[3];

  int nitermax = -1;
  if (argc == 5)
  {
    nitermax = std::stoi(argv[4]);
  }

  /* Read the matrix and rhs */

  CSRMatrix<double> A;
  A.ReadMatrixMarketFile(matrix);
  auto b = ReadMatrixMarketVector<double>(rhs);

  /* Setup solution vector and run the solver */

  std::vector<double> x;
  BiCGSTABSolver<double> BiCGSTAB;
  bool converged = BiCGSTAB.Solve(A, b, x, nitermax);

  std::cout << "Ran " << BiCGSTAB.GetNumberIterations() << " iterations" << std::endl;
  std::cout << "Elapsed solver time " << BiCGSTAB.GetElapsedTime() << " seconds" << std::endl;
  std::cout << "l2 norm of the residual " << BiCGSTAB.Getl2NormResidual() << std::endl;

  if (converged)
  {
    WriteMatrixMarketVector(x, soln);
    std::cout << "Converged solution written to " << soln << std::endl;
  }
  else
  {
    std::cout << "Solver failed to converge!" << std::endl;
  }

  return 0;
}
