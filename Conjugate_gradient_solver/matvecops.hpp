#ifndef MATVECOPS_HPP
#define MATVECOPS_HPP

#include <vector>

/* function that returns the norm of a vector (a copy of the vector
 is passed to the function) */
double norm(std::vector<double> v);


/* a function that computes the sum of two vectors
 a copy of the vectors is passed to the fucntion */
std::vector<double> vec_sum(std::vector<double> v1,
                            std::vector<double> v2);


/* a function that computes the difference of two vectors;
 a copy of the vectors is passes to the function */
std::vector<double> vec_diff(std::vector<double> v1,
                             std::vector<double> v2);


/* a function that multiplies a vector by a scalar;
 a copy of the vector is passed to the function */
std::vector<double> scalar_mult(double scalar,
                                std::vector<double> v);

/* a function that multiplies two vectors of the form
 vT * v; it is a assumed that the the dimensions of
 the vectors match up for multipliation: (1 x n) * (n x 1);
 copies of the vectors are passed to the function */
double vec_mult(std::vector<double> v1,
                std::vector<double> v2);


/* this function multiplies a matrix in CSR form by a dense
 vector; coppies of the matrix and vector are passed to the function */
std::vector<double> vec_mat_mult(std::vector<double> val,
                                 std::vector<int> row_ptr,
                                 std::vector<int> col_idx,
                                 std::vector<double> x);

#endif /* MATVECOPS_HPP */