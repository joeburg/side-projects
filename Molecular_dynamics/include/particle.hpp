#ifndef PARTICLE_HPP
#define PARTICLE_HPP

#include <array>
#include <cmath>

#include "operators.hpp"

template <typename T>
class particle
{
    private:
    std::array<T,3> r; // position vector
    std::array<T,3> v; // velocity vector
    std::array<T,3> a; // acceleration vector
    
    public:
    particle(void);
    std::array<T,3> GetPos(void);
    std::array<T,3> GetVel(void);
    std::array<T,3> GetAccl(void);
    void SetPos(std::array<T,3> r);
    void SetVel(std::array<T,3> v);
    void SetAccl(std::array<T,3> a);
    
    std::array<T,3> ComputeForce(particle p2, T length);
    T Distance(particle p2, T length);
    std::array<T,3> Displacement(particle p2, T length);
    std::array<T,3> PutInBox(std::array<T,3> Ri, T length);
};

template <typename T>
particle<T>::particle(void)
{
    r = {(T)0,(T)0,(T)0};
    v = {(T)0,(T)0,(T)0};
    a = {(T)0,(T)0,(T)0};
}

 
template <typename T>
std::array<T,3> particle<T>::GetPos(void)
{
    return r;
}

template <typename T>
std::array<T,3> particle<T>::GetVel(void)
{
    return v;
}
 
template <typename T>
std::array<T,3> particle<T>::GetAccl(void)
{
    return a;
}

template <typename T>
void particle<T>::SetPos(std::array<T,3> r)
{
    this->r = r;
}
 
template <typename T>
void particle<T>::SetVel(std::array<T,3> v)
{
    this->v = v;
}
 
template <typename T>
void particle<T>::SetAccl(std::array<T,3> a)
{
    this->a = a;
}

template <typename T>
std::array<T,3> particle<T>::PutInBox(std::array<T,3> R, T length)
{
    std::array<T,3> Rbc = {(T)0,(T)0,(T)0};
    for (unsigned int i=0; i < 3; i++)
        Rbc[i] = R[i] - length*std::nearbyint(R[i]/length);
    return Rbc;
}

template <typename T>
std::array<T,3> particle<T>::Displacement(particle p2, T length)
{
    return (PutInBox(r - p2.GetPos(), length));
}

template <typename T>
T particle<T>::Distance(particle p2, T length)
{
    return (norm(PutInBox(r - p2.GetPos(), length)));
}

template <typename T>
std::array<T,3> particle<T>::ComputeForce(particle p2, T length)
{
    T r = Distance(p2,length);
    std::array<T,3> R = Displacement(p2,length);
    T r2 = r*r;
    T r2i = (T)1/r2;
    T r6i = r2i*r2i*r2i;
    std::array<T,3> F = (24*r6i*r2i*(2*r6i-1))*R;
    return F;
}

#endif /* PARTICLE_HPP */

