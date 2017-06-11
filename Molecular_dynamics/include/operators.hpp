#ifndef OPERATORS_HPP
#define OPERATORS_HPP

#include <array>
#include <cmath>
#include <cstdlib> 
#include <time.h>

#include "macros.hpp"

/* operator overlaod to compute the sum of two ators */
template <typename T>
std::array<T,3> operator+ (const std::array<T,3> &a, const std::array<T,3> &b)
{
    if (a.size() != b.size()) ThrowException("ERROR: vectors are not the same size.");
    
    std::array<T,3> sum = {(T)0,(T)0,(T)0};
    for (unsigned int i=0; i < a.size(); i++)
        sum[i] = a[i]+b[i];
    return sum;
};

/* operator overload to compute the difference of two ators */
template <typename T>
std::array<T,3> operator- (const std::array<T,3> &a, const std::array<T,3> &b)
{
    if (a.size() != b.size()) ThrowException("ERROR: vectors are not the same size.");
    
    std::array<T,3> diff = {(T)0,(T)0,(T)0};
    for (unsigned int i=0; i < a.size(); i++)
        diff[i] = a[i]-b[i];
    return diff;
};


/* operator overlaod for scalar/ator mult */
template <typename T>
std::array<T,3> operator* (const T scalar, const std::array<T,3> &a)
{
    std::array<T,3> y = {(T)0,(T)0,(T)0};
    for (unsigned int i=0; i < a.size(); i++)
        y[i] = scalar*a[i];
    return y;
};

/* a function that multiplies two ators of the form vT * v;
 it is assumed that the the dimensions of the ators match up
 for multipliation: (1 x n) * (n x 1) */
template <typename T>
T dot(const std::array<T,3> &a, const std::array<T,3> &b)
{
    if (a.size() != b.size()) ThrowException("ERROR: vectors are not the same size.");
    
    T scalar=0;
    for (unsigned int i=0; i < a.size(); i++)
        scalar += a[i]*b[i];
    return scalar;
};

/* function that returns the norm of a ator */
template <typename T>
T norm(std::array<T,3> a)
{
    T normr=0;
    for (unsigned int i=0; i < a.size(); i++)
        normr += a[i]*a[i];
    normr = (T)std::sqrt(normr);
    return normr;
};

#endif /* OPERATORS_HPP */
