#include <array>
#include <cmath>
#include <fstream>
#include <iostream>
#include <vector>

#include "shapes.hpp"

/* returns the distance between two points */
double Shape::Distance(std::array<double,3> pt1,
                       std::array<double,3> pt2)
{
    double dx = pt1[0] - pt2[0];
    double dy = pt1[1] - pt2[1];
    double dz = pt1[2] - pt2[2];
    return sqrt(dx*dx + dy*dy + dz*dz);
}

/* returns a vector starting at point1 and ending at point2 */
std::array<double,3> Shape::Vector(std::array<double,3> pt1,
                            std::array<double,3> pt2)
{
    std::array<double,3> vec = {pt2[0] - pt1[0],pt2[1] - pt1[1],pt2[2] - pt1[2]};
    return vec;
}

unsigned int Shape::GetColor(void)
{
    return color;
}

void Shape::SetColor(unsigned int color)
{
    this->color = color;
}

/* concrete class RightCircularCone methods */
RightCircularCone::RightCircularCone(std::fstream& f)
{
    unsigned int clr;
    f >> clr >> R >> center[0] >> center[1] >> center[2] >> apex[0] >> apex[1] >> apex[2];
    SetColor(clr);
}

/* method to check if a point is in or on a right circular cone */
bool RightCircularCone::PointInside(const std::array<double,3> &point)
{
    /* first find the projection of the center-to-point vector onto the height vector */
    std::array<double,3> ptVec = Vector(apex,point);
    std::array<double,3> hvec = Vector(apex,center);
    double hnorm = sqrt(hvec[0]*hvec[0] + hvec[1]*hvec[1] + hvec[2]*hvec[2]);
    
    // the normalized axis vector, pointing from the apex to base
    std::array<double,3> dir = {hvec[0]/hnorm,hvec[1]/hnorm,hvec[2]/hnorm};
    double cone_dist = ptVec[0]*dir[0] + ptVec[1]*dir[1] + ptVec[2]*dir[2];
    double h = Distance(apex,center); // height of cone
    
    if ((cone_dist < 0) or (cone_dist > h)) return false;
    
    double cone_radius = (cone_dist/h)*R;  // radius at projection pt
    double orth_dist = sqrt(pow(ptVec[0]-cone_dist*dir[0],2)+pow(ptVec[1]-cone_dist*dir[1],2)+
                            pow(ptVec[2]-cone_dist*dir[2],2));
    
    /* now check distance between the c-to-pt vector and the projection vector onto the hvector
     is less than or equal to the radius of the circular conical section of the cone */
    return (orth_dist <= cone_radius);
}

/* determines a bounding box around the right circular cone object */
void RightCircularCone::GetBounds(std::array<double,6> &bounds)
{
    if (apex[0] < center[0] - R) bounds[0] = apex[0]; // x-min
    else bounds[0] = center[0] - R;
    if (apex[0] > center[0] + R) bounds[1] = apex[0]; // x-max
    else bounds[1] = center[0] + R;
    
    if (apex[1] < center[1] - R) bounds[2] = apex[1]; // y-min
    else bounds[2] = center[1] - R;
    if (apex[1] > center[1] + R) bounds[3] = apex[1]; // y-max
    else bounds[3] = center[1] + R;
    
    if (apex[2] < center[2] - R) bounds[4] = apex[2]; // z-min
    else bounds[4] = center[2] - R;
    if (apex[2] > center[2] + R) bounds[5] = apex[2]; // z-max
    else bounds[5] = center[2] + R;
}

/* concrete class sphere methods */
Sphere::Sphere(std::fstream& f)
{
    unsigned int clr;
    f >> clr >> center[0] >> center[1] >> center[2] >> R;
    SetColor(clr);
}

/* method to check if a point is in or on a sphere object */
bool Sphere::PointInside(const std::array<double,3> &point)
{
    return (Distance(center,point) <= R);
}

/* method to get the bounding box around a sphere */
void Sphere::GetBounds(std::array<double,6> &bounds)
{
    bounds[0] = center[0] - R; // x-min
    bounds[1] = center[0] + R; // x-max
    bounds[2] = center[1] - R; // y-min
    bounds[3] = center[1] + R; // y-max
    bounds[4] = center[2] - R; // z-min
    bounds[5] = center[2] + R; // z-max
}