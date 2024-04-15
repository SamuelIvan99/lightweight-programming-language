#ifndef FILE_STREAM_H
#define FILE_STREAM_H

#include "stream.h"
#include <stdio.h>

typedef struct {
    FILE *file;
} FileWriter;

StreamWriter file_writer(const char *file_name);

#endif
