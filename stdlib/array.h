#ifndef ARRAY_H
#define ARRAY_H

typedef struct {
    void *value;
    int size;
} Array;


void *getElement(Array x, int pos);

#endif