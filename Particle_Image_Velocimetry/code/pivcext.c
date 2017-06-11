//
//  pivcext.c
//  
//
//  Created by Joe Burg on 3/4/15.
//
//
#include <stdlib.h>

#include "pivcext.h"

double * XCorr_c(double *a, double *b, int n1, int n2)
{
    // allocate memory for the overlap matrix
    double *R = (double *) malloc((n1*2-1)*(n2*2-1)*sizeof(double));
    
    if (R = NULL) return R;

    
    for (initialization; <#condition#>; <#increment#>) {
        statements
    }
    
    
    
    return R;
}