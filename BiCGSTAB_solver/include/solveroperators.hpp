#include <cmath>
#include <vector>

#ifndef solveroperators_hpp
#define solveroperators_hpp

/* operator overlaod to compute the sum of two vectors */
template <typename T>
std::vector<T> operator+ (const std::vector<T> &vec1, const std::vector<T> &vec2)
{
    if (vec1.size() != vec2.size()) ThrowException("ERROR: Vectors are not the same size.");
    
    std::vector<T> sum(vec1.size(),0);
    for (unsigned int i=0; i < vec1.size(); i++)
        sum[i] = vec1[i]+vec2[i];
    return sum;
};

/* operator overload to compute the difference of two vectors */
template <typename T>
std::vector<T> operator- (const std::vector<T> &vec1, const std::vector<T> &vec2)
{
    if (vec1.size() != vec2.size()) ThrowException("ERROR: Vectors are not the same size.");
    
    std::vector<T> diff(vec1.size(),0);
    for (unsigned int i=0; i < vec1.size(); i++)
        diff[i] = vec1[i]-vec2[i];
    return diff;
};


/* operator overlaod for scalar/vector mult */
template <typename T>
std::vector<T> operator* (const T scalar, const std::vector<T> &vec)
{
    std::vector<T> y(vec.size(),0);
    for (unsigned int i=0; i < vec.size(); i++)
        y[i] = scalar*vec[i];
        return y;
};

/* a function that multiplies two vectors of the form vT * v;
 it is assumed that the the dimensions of the vectors match up
 for multipliation: (1 x n) * (n x 1) */
template <typename T>
T dot(const std::vector<T> &vec1, const std::vector<T> &vec2)
{
    if (vec1.size() != vec2.size()) ThrowException("ERROR: Vectors are not the same size.");
    
    T scalar=0;
    for (unsigned int i=0; i < vec1.size(); i++)
        scalar += vec1[i]*vec2[i];
    return scalar;
};

/* function that returns the norm of a vector */
template <typename T>
T l2norm(std::vector<T> vec)
{
    T l2normr=0;
    for (unsigned int i=0; i < vec.size(); i++)
        l2normr += vec[i]*vec[i];
    l2normr = (T)sqrt(l2normr);
    return l2normr;
};


#endif /* solveroperators_hpp */