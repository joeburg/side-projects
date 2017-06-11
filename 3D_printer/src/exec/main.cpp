#include <iomanip>
#include <iostream>
#include <map>
#include <string>

#include "part.hpp"
#include "shapes.hpp"



int main(int argc, char *argv[])
{
    if (argc < 4)
    {
        std::cout << "Usage:" << std::endl;
        std::cout << "  " << argv[0] << " <part file> <axis = x, y, or z> <distance along axis>" << std::endl;
        return 0;
    }
    std::string partfile = argv[1];
    std::string axis = argv[2];
    double dist;
    sscanf(argv[3],"%lf",&dist);
    
    /* initialize unit normal based on given axis */
    std::array<double,3> unitnormal;
    std::array<double,3> point;
    if (axis == "x")
    {
        unitnormal = {1.,0.,0.};
        point = {dist,0.,0.};
    }
    else if (axis == "y")
    {
        unitnormal = {0.,1.,0.};
        point = {0.,dist,0.};
    }
    else if (axis == "z")
    {
        unitnormal = {0.,0.,1.};
        point = {0.,0.,dist};
    }
    
    std::array<double,3> discretization = {0.01,0.01,0.01};
    
    try
    {
        Part part;
        part.ReadPartFile(partfile);
        std::map<unsigned int,double> data = part.SliceVolume(unitnormal,point,discretization);
        
        // print out volume of each color
        unsigned int Nshapes = part.GetNumShapes();
        unsigned int Ncolors = part.GetNumColors();
        std::cout << "Loaded part from file " << partfile << " with a total of " << Nshapes << " shapes and " << Ncolors << " colors." << std::endl;
        std::cout << "Material volume requirements for slice through " << axis << " = " << dist << ":" << std::endl;
        std::cout << "  color      volume" << std::endl;
        for (auto &idx : data)
            std::cout << "  " << std::setw(5) << idx.first << "     " << std::setw(7) << std::fixed << std::setprecision(3) << idx.second << std::endl;
    }
    catch (std::exception &e)
    {
        std::cerr << e.what() << std::endl;
    }
    return 0;
}