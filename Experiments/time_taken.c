#include <time.h>


clock_t start = clock();

  clock_t end = clock();

  double time_taken = (double)(end - start)/CLOCKS_PER_SEC;
  printf("%lf\n", time_taken);