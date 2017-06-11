#include <array>
#include <cmath>
#include <fstream>
#include <iostream> 
#include <map>
#include <memory>
#include <sstream>
#include <string>
#include <vector>

#include "part.hpp"

unsigned int Part::GetNumShapes(void)
{
    return (unsigned int)shapes.size();
}

unsigned int Part::GetNumColors(void)
{
    return (unsigned int)data.size();
}

/* method to get the boundary around all the shape objects */
void Part::GetBoundary(void)
{
    // initialize bounardy with first shape
    shapes[0]->GetBounds(bounds);
    std::array<double,6> bound;
    unsigned int clr;
    /* for each shape object, compare max/min values to intialized bounds
     and update accordingly */
    for (auto shape : shapes)
    {
        shape->GetBounds(bound);
        if (bound[0] < bounds[0]) bounds[0] = bound[0]; // x-min
        if (bound[1] > bounds[1]) bounds[1] = bound[1]; // x-max
        
        if (bound[2] < bounds[2]) bounds[2] = bound[2]; // y-min
        if (bound[3] > bounds[3]) bounds[3] = bound[3]; // y-max
        
        if (bound[4] < bounds[4]) bounds[4] = bound[4]; // z-min
        if (bound[5] > bounds[5]) bounds[5] = bound[5]; // z-max
        
        // initialze color:volume map
        clr = shape->GetColor();
        data[clr] = 0.;
    }
}

/* method to read a part file */
void Part::ReadPartFile(std::string partfile)
{
    std::fstream f;
    f.open(partfile, std::ios::in);
    if (f.is_open())
    {
        while (f >> type)
        {
            if (type == "sphere") shapes.push_back(std::make_shared<Sphere>(f));
            else if (type == "rccone") shapes.push_back(std::make_shared<RightCircularCone>(f));
            else
            {
                // not allowed type, so throw exception
                std::stringstream s;
                s << "ERROR: Invalid part, " << type << " is not a supported shape.";
                throw std::runtime_error(s.str());
            }
        }
        f.close();
    }
    else
    {
        // raise exception about file not opening properly
        std::stringstream s;
        s << "ERROR: Reading file " << partfile << " failed!";
        throw std::runtime_error(s.str());
    }
}

/* method to compute the volume occupied by each color given a slicing plane */
std::map<unsigned int,double> Part::SliceVolume(const std::array<double,3> &unitnormal,
                                               const std::array<double,3> &point,
                                               const std::array<double,3> &discretization)
{
    GetBoundary();
    
    double epsilon = 0.000001;
    
    /* check that the unitnormal is in fact within epsilon of length 1 and the vector
    components sum to within epsilon of 1 */
    double norm = sqrt(pow(unitnormal[0],2)*pow(unitnormal[0],2)*pow(unitnormal[0],2));
    double sum = unitnormal[0]+unitnormal[1]+unitnormal[2];
    
    if (not(abs(norm - 1.) < epsilon) and not(abs(sum - 1.) < epsilon))
    {
        std::stringstream s;
        s << "ERROR: Invalid slicing plane: (" << unitnormal[0] << "," << unitnormal[1] << "," << unitnormal[2] << "). Only planes normal to the x, y or z axes are supported.";
        throw std::runtime_error(s.str());
    }
    
    /* maximum value of vector will be the slicing plane axis */
    unsigned int idx = 0;
    for (unsigned int i=1; i < unitnormal.size(); i++)
    {
        if (unitnormal[i] > unitnormal[idx]) idx = i;
    }
    
    // fix bounds at point corresponding to axes
    if (idx == 0)
    {
        bounds[0] = point[0]; // set x-min to point value
        bounds[1] = point[0]+discretization[0]; // set x-max to point value + dx
    }
    else if (idx == 1)
    {
        bounds[2] = point[1]; // set y-min to point value
        bounds[3] = point[1]+discretization[1]; // set y-max to point value + dy
    }
    else if (idx == 2)
    {
        bounds[4] = point[2]; // set z-min to point value
        bounds[5] = point[2]+discretization[2]; // set z-max to point value + dz
    }
    
    /* for each point in the grid, check if the point lies within a shape */
    std::array<double,3> pt;
    unsigned int mincolor,color;
    bool ptInside;
    for (double i = bounds[0]; i < bounds[1]; i += discretization[0])
    {
        for (double j = bounds[2]; j < bounds[3]; j += discretization[1])
        {
            for (double k = bounds[4]; k < bounds[5]; k += discretization[2])
            {
                pt = {i,j,k};
                // to use the smallest color, set mincolor to the last key since the map is sorted
                mincolor = data.rbegin()->first;
                ptInside = false;
                for (auto &shape : shapes)
                {
                    if (shape->PointInside(pt))
                    {
                        ptInside = true;
                        color = shape->GetColor();
                        if (color < mincolor) mincolor = color;
                    }
                }
                
                if (ptInside) data[mincolor] += discretization[0]*discretization[1]*discretization[2];
            }
        }
    }
    return data;
}

