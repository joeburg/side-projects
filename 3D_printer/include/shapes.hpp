#ifndef shapes_hpp
#define shapes_hpp

#include <fstream>
#include <vector>

class Shape
{
    private:
    unsigned int color;
    
    protected:
    /* the following protected methods were made to be helper functions;
     they really should be place in another library, but since we cannot make
     other classes, I have them here */
    double Distance(std::array<double,3> pt1,std::array<double,3> pt2);
    std::array<double,3> Vector(std::array<double,3> pt1,std::array<double,3> pt2);
    
    public:
    unsigned int GetColor(void);
    void SetColor(unsigned int color);
    virtual bool PointInside(const std::array<double,3> &point) =0;
    virtual void GetBounds(std::array<double,6> &bounds) =0;
};

class RightCircularCone: public Shape
{
    private:
    double R;
    std::array<double,3> center;
    std::array<double,3> apex;

    public:
    RightCircularCone(std::fstream& f);
    bool PointInside(const std::array<double,3> &point);
    void GetBounds(std::array<double,6> &bounds);
};

class Sphere: public Shape
{
    private:
    double R;
    std::array<double,3> center;
    
    public:
    Sphere(std::fstream& f);
    bool PointInside(const std::array<double,3> &point);
    void GetBounds(std::array<double,6> &bounds);
};

#endif /* shapes_hpp */
