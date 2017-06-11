//
//  find_size.cpp
//  
//
//  Created by Joe Burg on 12/4/14.
//
//

#include <stdio.h>


// sort the column inidices so they can be compared
std::vector<int> j_idx_sort = j_idx;
std::sort(j_idx_sort.begin(), j_idx_sort.end());

int N =1;
for (int i=1; i < (int)j_idx.size(); i++)
{
    // compare each column index to previous, if different then add 1
    if (j_idx_sort[i] != j_idx_sort[i-1])
        N++;
}
nrows = N;

// sort the column inidices so they can be compared
std::vector<int> i_idx_sort = i_idx;
std::sort(i_idx_sort.begin(), i_idx_sort.end());

int N = 1;
for (int i=1; i < (int)i_idx.size(); i++)
{
    // compare each column index to previous, if different then add 1
    if (i_idx_sort[i] != i_idx_sort[i-1])
        N++;
}
ncols = N;

// no ordering needed
std::vector<unsigned int> v;