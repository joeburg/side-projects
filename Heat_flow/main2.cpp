//
//  main2.cpp
//  
//
//  Created by Joe Burg  on 12/5/14.
//
//

#include <stdio.h>
#include <iostream>
#include <string>

#include "CGSolver.hpp"
#include "COO2CSR.hpp"
#include "heat.hpp"
#include "sparse.hpp"

int main(int argc, char *argv[])
{
    /* Get command line arguments */
    if (argc != 3)
    {
        std::cout << "Usage:" << std::endl;
        std::cout << "  " << argv[0] << " <input file> <soln prefix>" << std::endl;
        return 0;
    }
    std::string inputfile   = argv[1];
    std::string soln_prefix   = argv[2];
    
    /* Setup 2D heat equation system */
    HeatEquation2D sys;
    int status = sys.Setup(inputfile);
    if (status)
    {
        std::cerr << "ERROR: System setup was unsuccessful!" << std::endl;
        return 1;
    }
    return 0;
}
