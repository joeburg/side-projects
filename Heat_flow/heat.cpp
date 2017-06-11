//
//  heat.cpp
//  
//
//  Created by Joe Burg  on 12/3/14.
//
//

#define BOOST_DISABLE_ASSERTS
#include <boost/multi_array.hpp>

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
    
    
    
    //A.AddEntry(0,0,4.);
    //A.AddEntry(0,1,1.);
    //A.AddEntry(1,0,1.);
    //A.AddEntry(1,1,3.);
    
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
            b[i] = -TemperatureDist(h*i);
        else if (i > ncols - nx - 1)
            b[i] = T_h;
        else
            b[i] = 0.0;
    }
     
    //int ncols = A.GetCols();
    //b.assign(ncols,0.0);
    
    
    
    //b.push_back(1);
    //b.push_back(2);
    
     
    // print b vector
    //for (unsigned int i=0; i < b.size(); i++)
    //    std::cout << "b[" << i << "] = " << b[i] << std::endl;
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
    
    std::cout << "nx = " << nx << std::endl;
    std::cout << "ny = " << ny << std::endl;
    std::cout << "N = " << N << std::endl;
    
    A.Resize(N,N);
    
    SetInterior();
    SetBoundaries();
    
    //A.PrintMatrix();
    
    A.ConvertToCSR();
    
    //A.PrintMatrix();
    
    return 0;
}

/* Method to solve system using CGsolver */
int HeatEquation2D::Solve(std::string soln_prefix)
{
    
    int ncols = A.GetCols();
    x.assign(ncols,0.);
    
     
    
    //x.push_back(2);
    //x.push_back(1);
    
    /*
    // print x vector
    for (unsigned int i=0; i < x.size(); i++)
        std::cout << "x[" << i << "] = " << x[i] << std::endl;
    */
     
    int niter = CGSolver(A,b,x,1.e-5,soln_prefix);
    
    if (niter == -1)
        return 1;
    else
    {
        std::cout << "SUCCESS: GG solver converged in " << niter << " iterations." << std::endl;
        return 0;
    }
}