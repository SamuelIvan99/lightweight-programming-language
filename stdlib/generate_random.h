#ifndef GENERATE_RANDOM_H
#define GENERATE_RANDOM_H
#include <stdlib.h>

void set_random(int seed){
    srand(seed);
}

int generate_random(int max){
    return rand() % max;
}

#endif