#include "array.h"
#include <stdio.h>
#include <stdlib.h>

void *getElement(Array x, int pos){
    if(pos < 0 || pos >= x.size){
        printf("Index out of bounds: %d\n", pos);
        exit(1);
    }
    return x.value;
}
