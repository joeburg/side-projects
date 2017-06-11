#include <fstream>
#include <iostream>
#include <math.h>
#include <string>

#include "CGSolver.hpp"
#include "heat.hpp"
#include "sparse.hpp"

/* Method to populate matrix with values from interior nodes */
void HeatEquation2D::SetInterior(void)
{
    
    int row=0;
    for (int y=0; y < ny; y++)
    {
        for (int x=0; x < nx; x++)
        {
            A.AddEntry(row, x + (y*nx), 4);
            
            // consider periodic boundaries in x direction
            if (x == 0)
                A.AddEntry(row, (nx-2)+(y*nx), -1);
            else
                A.AddEntry(row, (x-1)+(y*nx), -1);
            
            if (x == nx -1)
                A.AddEntry(row, 1+(y*nx), -1);
            else
                A.AddEntry(row, (x+1)+(y*nx), -1);
            
            // ensure that the y stensile does not hit boundary
            if (y != 0)
                A.AddEntry(row, x+(y-1)*nx, -1);
            
            if (y != ny -1)
                A.AddEntry(row, x+(y+1)*nx, -1);
            
            row++;
        }
    }
}

/* Method to populate matrix with values from boundary nodes */
void HeatEquation2D::SetBoundaries(void)
{
    int ncols = A.GetCols();
    b.assign(ncols,0.0);
    
    // assign - values since -A(u) = -b is solved
    for (int i=0; i < ncols; i++)
    {
        // matrix is filled L to R, bottom to top, so first
        // nx values are lower boundary and last nx values./
        // are upper boundary
        if (i < nx)
            b[i] = TemperatureDist(h*i);
        else if (i > ncols - nx - 1)
            b[i] = T_h;
        else
            b[i] = 0.0;
    }
}

/* Helper method to compute lower isothermal boundary temperatures */
double HeatEquation2D::TemperatureDist(double x)
{
    double T_x = -T_c * (exp(-10 * pow(x - length/2, 2)) - 2);
    return T_x;
}

/* Method to setup Ax=b system */
int HeatEquation2D::Setup(std::string inputfile)
{
    // read input file
    std::ifstream f(inputfile);
    if (f.is_open())
    {
        f >> length >> width >> h;
        f >> T_c >> T_h;
    }
    f.close();
    
    nx = (int)(length/h + 1.0);
    ny = (int)(width/h - 1.0);
    int N = nx*ny;    
    A.Resize(N,N);
    
    SetInterior();
    SetBoundaries();
    
    // check if the system was setup property
    if (A.GetCols() != A.GetRows())
    	return 1;
    else if ((int)b.size() != A.GetCols())
    	return 1;

    A.ConvertToCSR();    
    return 0;
}

/* Method to solve system using CGsolver */
int HeatEquation2D::Solve(std::string soln_prefix)
{  
    int ncols = A.GetCols();
    x.assign(ncols,0.);
     
    int niter = CGSolver(A,b,x,1.e-5,soln_prefix);
    
    if (niter == -1)
        return 1;
    else
    {
        std::cout << "SUCCESS: GG solver converged in " << niter << " iterations." << std::endl;
        return 0;
    }
}