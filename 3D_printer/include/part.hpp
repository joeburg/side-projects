#ifndef part_hpp
#define part_hpp

#include <memory>
#include <string>
#include <vector>

#include "shapes.hpp"

class Part
{
    private:
    std::string type;
    std::vector<std::shared_ptr<Shape>> shapes; // pointers to shape objects
    std::array<double,6> bounds; // boundaries around all shape objects
    std::map<unsigned int,double> data; // color-volume key pair
    void GetBoundary(void);
    
    public:
    unsigned int GetNumColors(void);
    unsigned int GetNumShapes(void);
    void ReadPartFile(std::string partfile);
    std::map<unsigned int,double> SliceVolume(const std::array<double,3> &unitnormal,
                                              const std::array<double,3> &point,
                                              const std::array<double,3> &discretization);
    
};

#endif /* part_hpp */
