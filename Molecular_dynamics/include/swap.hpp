#ifndef swap_hpp
#define swap_hpp

/* Return a byte swapped version of the first agument in the
   char buffer */

void swap(int value, char *buf);

void swap(float value, char *buf);

void swap(double value, char *buf);

/* Byte swap the contents of the char buffer and return it in
   the second value. */

void unswap(char *buf, int *value);

void unswap(char *buf, float *value);

void unswap(char *buf, double *value);

#endif /* swap_hpp */
