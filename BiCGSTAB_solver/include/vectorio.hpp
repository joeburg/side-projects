#ifndef vectorio_hpp
#define vectorio_hpp

#include <cstdio>
#include <string>
#include <vector>

#include "mmio.h"

#include "macros.hpp"


/* Read vector using Matrix Market file format */

template <typename T>
std::vector<T> ReadMatrixMarketVector(std::string filename)
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

  int status, nrows, ncols;

  if ((status = mm_read_mtx_array_size(f, &nrows, &ncols)) != 0)
  {
    CloseFileThrowException(f, "failed to read number of rows and columns in file " + filename);
  }

  if (ncols != 1)
  {
    fclose(f);
    ThrowException("number of columns is not 1 in file " + filename);
  }

  /* Read values into vector */

  std::vector<T> v;

  int nval;
  double val;
  for (unsigned int n = 0; n < (unsigned int)nrows; n++)
  {
    nval = fscanf(f, "%lg\n", &val);
    if (nval < 1)
    {
      CloseFileThrowException(f, "failed to read dense line from file " + filename);
    }
    v.push_back((T)val);
  }

  /* Close file and return */

  fclose(f);
  return v;
}


/* Write vector using Matrix Market file format */

template <typename T>
void WriteMatrixMarketVector(std::vector<T> v, std::string filename)
{
  /* Open the file */

  FILE *f = fopen(filename.c_str(), "w");
  if (f == NULL)
  {
    ThrowException("failed to open file " + filename);
  }

  /* Setup matcode, write banner and size */

  MM_typecode matcode;

  mm_initialize_typecode(&matcode);
  mm_set_matrix(&matcode);
  mm_set_array(&matcode);
  mm_set_real(&matcode);

  mm_write_banner(f, matcode);
  mm_write_mtx_array_size(f, (int)v.size(), 1);

  for(unsigned int n = 0; n < v.size(); n++)
    fprintf(f, "%e\n", v[n]);

  /* Close file and return */

  fclose(f);
  return;
}

#endif /* vectorio_hpp */
