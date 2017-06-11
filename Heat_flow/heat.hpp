#ifndef HEAT_HPP
#define HEAT_HPP

#include <string>
#include <vector>

#include "sparse.hpp"

class HeatEquation2D
{
  private:
    SparseMatrix A;
    std::vector<double> b, x;
    double length, width, h;
    double T_c, T_h;
    int nx, ny;

    /* Method to populate matrix with values from interior nodes */
    void SetInterior(void);

    /* Method to populate matrix with values from boundary nodes */
    void SetBoundaries(void);

    /* Helper method to compute lower isothermal boundary temperatures */
    double TemperatureDist(double x);

  public:
    /* Method to setup Ax=b system */
    int Setup(std::string inputfile);

    /* Method to solve system using CGsolver */
    int Solve(std::string soln_prefix);

};

#endif /* HEAT_HPP */
