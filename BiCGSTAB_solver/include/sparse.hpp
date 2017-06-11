#ifndef sparse_hpp
#define sparse_hpp

#include <cstdio>
#include <string>
#include <vector>

#include "mmio.h"

#include "macros.hpp"


/* Bubble sorting function for sparse matrix format conversion,
   used to sort the entries in one row of the matrix. */

template <typename T>
void SortRow(int *col_idx, T *a, int start, int end)
{
  for (int i = end - 1; i > start; i--)
  {
    for(int j = start; j < i; j++)
    {
      if (col_idx[j] > col_idx[j+1])
      {
        /* Swap the value and the column index */
	if (a)
        {
	  T dt = a[j]; 
	  a[j] = a[j+1]; 
	  a[j+1] = dt;
        }
	int it = col_idx[j]; 
	col_idx[j] = col_idx[j+1]; 
	col_idx[j+1] = it;
      }
    }
  }
}


/* In place conversion of square matrix from COO to CSR format */

template <typename T>
void COO2CSR(int n, int nz, T *a, int *i_idx, int *j_idx)
{
  int *row_start = new int[n+1];
  for (int i = 0; i <= n; i++)
  {
    row_start[i] = 0;
  }

  /* Determine row lengths */

  for (int i = 0; i < nz; i++) row_start[i_idx[i]+1]++;
  for (int i = 0; i < n; i++) row_start[i+1] += row_start[i];

  for (int init = 0; init < nz; )
  {
    T dt = a[init];
    int i = i_idx[init];
    int j = j_idx[init];
    i_idx[init] = -1;

    while (true)
    {
      int i_pos = row_start[i];
      T a_next = a[i_pos];
      int i_next = i_idx[i_pos];
      int j_next = j_idx[i_pos];

      a[i_pos] = dt;
      j_idx[i_pos] = j;
      i_idx[i_pos] = -1;
      row_start[i]++;

      if (i_next < 0) break;

      dt = a_next;
      i = i_next;
      j = j_next;
    }
    init++;

    while ((init < nz) and (i_idx[init] < 0))
    {
      init++;
    }
  }

  /* Copy row pointer */

  for (int i = 0; i < n; i++)
  {
    i_idx[i+1] = row_start[i];
  }
  i_idx[0] = 0;

  /* Sort each row */

  for (int i = 0; i < n; i++)
  {
    SortRow(j_idx, a, i_idx[i], i_idx[i+1]);
  }

  delete[] row_start;
}


/* Template class for a sparse matrix in CSR format */

template <typename T>
class CSRMatrix
{
  private:
    /* Memory for CSR storage of a matrix (using int for compatibility with Matrix Market IO). */
    T *val = NULL;
    int *col_ind = NULL;
    int *row_ptr = NULL;
    /* Size of matrix and number of nonzero entries */
    int nrows = 0;
    int ncols = 0;
    int nnonzeros = 0;

  public:
    int GetNumberRows (void) const;
    int GetNumberCols (void) const;
    int GetNumberNonZeros (void) const;
    void ReadMatrixMarketFile(std::string filename);
    std::vector<T> operator* (const std::vector<T> &x) const;
    ~CSRMatrix();
};

/* operator overload to multiply a matrix in CSR form by a dense vector */
template <typename T>
std::vector<T> CSRMatrix<T>::operator* (const std::vector<T> &x) const
{
    if (ncols != (int)x.size()) ThrowException("The matrix and vector are not compatible for multiplication.");
    
    // initialize a vector of the same size as x to 0
    std::vector<T> y(x.size(),0);
    
    /* for all the non-zero elements of the sparse matrix,
     multiply the value by the corresponding index in x */
    for (unsigned int i=0; i < x.size(); i++)
        for (unsigned int j = row_ptr[i]; j < row_ptr[i+1]; j++)
            y[i] += val[j]*x[col_ind[j]];
    return y;
}

template <typename T>
int CSRMatrix<T>::GetNumberRows(void) const
{
  return nrows;
}


template <typename T>
int CSRMatrix<T>::GetNumberCols(void) const
{
  return ncols;
}


template <typename T>
int CSRMatrix<T>::GetNumberNonZeros(void) const
{
  return nnonzeros;
}


template <typename T>
void CSRMatrix<T>::ReadMatrixMarketFile(std::string filename)
{
  /* Open the file */

  FILE *f = fopen(filename.c_str(), "r");
  if (f == NULL)
  {
    ThrowException("failed to open file " + filename);
  }

  /* Read the banner */

  MM_typecode matcode;
  if (mm_read_banner(f, &matcode) != 0)
  {
    CloseFileThrowException(f, "failed to read banner in file " + filename);
  }

  /* Determine the size */

  int status;

  if (mm_is_sparse(matcode))
  {
    if ((status = mm_read_mtx_crd_size(f, &nrows, &ncols, &nnonzeros)) != 0)
    {
      CloseFileThrowException(f, "failed to read coordinate size in file " + filename);
    }
  }
  else
  {
    CloseFileThrowException(f, "matrix in file " + filename + " is not sparse");
  }

  /* Allocate memory for data in COO format */

  if (mm_is_symmetric(matcode))
  {
    val = new T[2*nnonzeros];
    col_ind = new int[2*nnonzeros];
    row_ptr = new int[2*nnonzeros];
  }
  else
  {
    val = new T[nnonzeros];
    col_ind = new int[nnonzeros];
    row_ptr = new int[nnonzeros];
  }

  /* Read values from file */

  int i, j, nval, nn = 0, ndiag = 0;
  double value;
  for (int n = 0; n < nnonzeros; n++)
  {
    nval = fscanf(f, "%d %d %lg\n", &i, &j, &value);
    if (nval < 3)
    {
      CloseFileThrowException(f, "failed to read 3 values from sparse line in file " + filename);
    }
    // Keep track of non-zero entries on the diagonal
    if (i == j) ndiag++;
    // Store the value, Matrix Market uses 1 based indexing so subtract 1
    val[nn] = (T)value;
    col_ind[nn] = j - 1;
    row_ptr[nn] = i - 1;
    nn++;
    if (mm_is_symmetric(matcode) and i != j)
    {
      val[nn] = (T)value;
      col_ind[nn] = i - 1;
      row_ptr[nn] = j - 1;
      nn++;
    }
  }

  /* Recompute the number of nonzeros for symmetric case */
  
  if (mm_is_symmetric(matcode))
  {
    nnonzeros = 2*nnonzeros - ndiag;
  }

  /* Close file */

  fclose(f);

  /* Convert COO to CSR format */

  if (nrows != ncols)
  {
    ThrowException("no support for converting non-square COO matrix to CSR format");
  }

  COO2CSR(nrows, nnonzeros, val, row_ptr, col_ind);

}


template <typename T>
CSRMatrix<T>::~CSRMatrix()
{
  /* Free heap memory */
  if (val)     delete[] val;     val = NULL;
  if (col_ind) delete[] col_ind; col_ind = NULL;
  if (row_ptr) delete[] row_ptr, row_ptr = NULL;
}

#endif /* sparse_hpp */
