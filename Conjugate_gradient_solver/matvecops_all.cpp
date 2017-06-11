/* purpose: matrix and vector operations */

#include <vector> 
#include <math.h>

#include "matvecops.hpp"

/* function that returns the norm of a vector (a copy of the vector 
 is passed to the function) */
double norm(std::vector<double> v)
{
    double L2norm;
    for (int i=0; i < v.size(); i++)
        L2norm += v[i]*v[i];
    L2norm = sqrt(L2norm);
    return L2norm;
}

/* a function that computes the transpose of a vector;
 a copy of the vector is passed to the function */
//std::vector<double> transpose(std::vector<double> v)
//{
//    std::vector<double> vT;
//    for (int i=0; i < v.size(); i++)
//        vT[i]
//    }
//}


/* a function that computes the sum of two vectors
 a copy of the vectors is passed to the fucntion */
std::vector<double> vec_sum(std::vector<double> v1,
                            std::vector<double> v2)
{
    std::vector<double> sum;
    for (int i=0; i < v1.size(); i++)
        sum.push_back(v1[i]+v2[i]);
    return sum;
}


/* a function that computes the difference of two vectors; 
 a copy of the vectors is passes to the function */
std::vector<double> vec_diff(std::vector<double> v1,
                             std::vector<double> v2)
{
    std::vector<double> diff,
    for (int i=0; i < v1.size(); i++)
        diff.push_back(v1[i]-v2[i]);
    return diff;
}


/* a function that multiplies a vector by a scalar; 
 a copy of the vector is passed to the function */
std::vector<double> scalar_mult(double scalar,
                                std::vector<double> v)
{
    std::vector<double> y;
    for (int i=0; i < v.size(); i++)
        y.push_back(scalar*v[i]);
    return y;
}

/* a function that multiplies two vectors of the form 
 vT * v; it is a assumed that the the dimensions of 
 the vectors match up for multipliation: (1 x n) * (n x 1);
 copies of the vectors are passed to the function */
double vec_mult(std::vector<double> v1,
                std::vector<double> v2)
{
    double scalar;
    for (int i=0; i < v1.size(); i++)
        scalar += v1[i]*v2[i];
    return scalar;
}

void scalar_product(std::vector<double> &v,
                    double scalar)
{
    for (int i=0; i < v.size(); i++)
        scalar += v[i]*v[i];
}


/* this function multiplies a matrix in CSR form by a dense
 vector; coppies of the matrix and vector are passed to the function */
std::vector<double> vec_mat_mult(std::vector<double> val,
                                 std::vector<int> row_ptr,
                                 std::vector<int col_idx,
                                 std::vector<double> x)
{
    // initialize a vector of the same size as x to 0
    std::vector<double> y;
    for (int i=0; i < x.size(); i++)
        y.push_back(0);
    
    /* for all the non-zero elements of the sparse matrix,
     multiply the value by the corresponding index in x */
    for (int i=0; i < val.size(); i++)
        for (int j = row_ptr[i]; j < row_ptr[i+1]; j++)
            y[i] = val[j]*x[col_idx[j]];
    return y;
}

