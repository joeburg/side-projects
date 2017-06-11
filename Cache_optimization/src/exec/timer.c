#include <unistd.h>
#include <sys/time.h>

#include "timer.h"

double timer(void)
{
  double time;
  struct timeval tv;
  gettimeofday(&tv, NULL);
  time = (double)tv.tv_sec + (double)tv.tv_usec/1.e6;
  return time;
}
