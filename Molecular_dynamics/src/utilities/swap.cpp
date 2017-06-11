#include <cstring>

#include "swap.hpp"

void swap(int value, char *buf)
{
  union temp
  {
    int  value;
    char c[4];
  } in, out;
  in.value = value;
  out.c[0] = in.c[3];
  out.c[1] = in.c[2];
  out.c[2] = in.c[1];
  out.c[3] = in.c[0];
  memcpy(buf, out.c, 4);
}

void swap(float value, char *buf)
{
  union temp
  {
    float value;
    char  c[4];
  } in, out;
  in.value = value;
  out.c[0] = in.c[3];
  out.c[1] = in.c[2];
  out.c[2] = in.c[1];
  out.c[3] = in.c[0];
  memcpy(buf, out.c, 4);
}

void swap(double value, char *buf)
{
  union temp
  {
    double value;
    char   c[8];
  } in, out;
  in.value = value;
  out.c[0] = in.c[7];
  out.c[1] = in.c[6];
  out.c[2] = in.c[5];
  out.c[3] = in.c[4];
  out.c[4] = in.c[3];
  out.c[5] = in.c[2];
  out.c[6] = in.c[1];
  out.c[7] = in.c[0];
  memcpy(buf, out.c, 8);
}

void unswap(char *buf, int *value)
{
  union temp
  {
    int  value;
    char c[4];
  } in, out;
  memcpy(in.c, buf, 4);
  out.c[0] = in.c[3];
  out.c[1] = in.c[2];
  out.c[2] = in.c[1];
  out.c[3] = in.c[0];
  memcpy(value, &out.value, 4);
}

void unswap(char *buf, float *value)
{
  union temp
  {
    float value;
    char  c[4];
  } in, out;
  memcpy(in.c, buf, 4);
  out.c[0] = in.c[3];
  out.c[1] = in.c[2];
  out.c[2] = in.c[1];
  out.c[3] = in.c[0];
  memcpy(value, &out.value, 4);
}

void unswap(char *buf, double *value)
{
  union temp
  {
    double value;
    char   c[8];
  } in, out;
  memcpy(in.c, buf, 8);
  out.c[0] = in.c[7];
  out.c[1] = in.c[6];
  out.c[2] = in.c[5];
  out.c[3] = in.c[4];
  out.c[4] = in.c[3];
  out.c[5] = in.c[2];
  out.c[6] = in.c[1];
  out.c[7] = in.c[0];
  memcpy(value, &out.value, 8);
}
