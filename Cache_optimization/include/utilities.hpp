#ifndef utilities_hpp
#define utilities_hpp

int SimpleTranspose(double *a, int size, int ldim);

int OptimizedTranspose(double *a, int size, int ldim, int blocksize);

void initmatrix(double *a, int size, int ldim);

#endif /* utilities_hpp */
