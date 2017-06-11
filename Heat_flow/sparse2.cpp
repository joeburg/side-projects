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




