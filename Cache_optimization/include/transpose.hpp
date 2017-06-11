//
//  transpose.h
//  
//
//  Created by Joe Burg on 2/8/15.
//
//

#ifndef TRANSPOSE_HPP
#define TRANSPOSE_HPP

#include <stdio.h>

int SimpleTranspose(double *a, int size, int ldim);
int OptimizedTranspose(double *a, int size, int ldim, int blocksize);

#endif /* TRANSPOSE_HPP */
