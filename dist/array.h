#ifndef ARRAY_H
#define ARRAY_H

#include <stdlib.h>
#include <stdio.h>

typedef struct{
    void *value;
    int size;
} Array;

void *getElement(Array x, int pos){
    if(pos >= x.size){
        printf("Index out of bounds: %d\n", pos);
        exit(1);
    }
    return x.value[pos];
}

#endif