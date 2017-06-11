
//
//  sparse.cpp
//  
//
//  Created by Joe Burg  on 12/3/14.
//
//

#define BOOST_DISABLE_ASSERTS
#include <boost/multi_array.hpp>


#include <algorithm>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <vector>

#include "COO2CSR.hpp"
#include "sparse.hpp"

/* Method to modify sparse matrix dimensions */
void SparseMatrix::Resize(int nrows, int ncols)
{
    this->nrows = nrows;
    this->ncols = ncols;
}

/* Method to add entry to matrix in COO format */
void SparseMatrix::AddEntry(int i, int j, double val)
{
    i_idx.push_back(i);
    j_idx.push_back(j);
    a.push_back(val);
}

void SparseMatrix::PrintMatrix(void)
{
    // print out matrix
    boost::multi_array<double, 2> matrix(boost::extents[ncols][ncols]);
    for (int i=0; i < ncols; i++)
    {
        for (int j=0; j < ncols; j++)
            matrix[i][j] = 0;
    }
    
    for (unsigned int i=0; i < i_idx.size(); i++)
        matrix[i_idx[i]][j_idx[i]] = a[i];
    
    for (int i=0; i < ncols; i++)
    {
        for (int j=0; j < ncols; j++)
            std::cout << std::setw(4) << matrix[i][j] << " ";
        
        std::cout << std::endl;
    }
    
    for (unsigned int i=0; i < i_idx.size(); i++)
        std::cout << "i_idx[" << i << "] = " << i_idx[i] << std::endl;
    
    for (unsigned int i=0; i < j_idx.size(); i++)
        std::cout << "j_idx[" << i << "] = " << j_idx[i] << std::endl;
    
    //for (unsigned int i=0; i < a.size(); i++)
    //    std::cout << "val[" << i << "] = " << a[i] << std::endl;

}

/* Method to convert COO matrix to CSR format using provided function */
void SparseMatrix::ConvertToCSR(void)
{
    COO2CSR(a,i_idx,j_idx);
}

/* Method to return number of columns in matrix */
int SparseMatrix::GetCols(void)
{
    return ncols;
}

/* Method to return number of rows in matrix */
int SparseMatrix::GetRows(void)
{
    return nrows;
}

/* Method to perform sparse matrix vector multiplication using CSR formatted matrix */
std::vector<double> SparseMatrix::MulVec(const std::vector<double> vec)
{
    // initialize a vector of the same size as vec to 0
    std::vector<double> y(vec.size(),0);
    
    /* for all the non-zero elements of the sparse matrix,
     multiply the value by the corresponding index in vec */
    for (int i=0; i < (int)vec.size(); i++)
        for (int j = i_idx[i]; j < i_idx[i+1]; j++)
            y[i] += a[j]*vec[j_idx[j]];
    return y;
}




