#ifndef SFILE_STREAM_H
#define SFILE_STREAM_H

#include "stream.h"
#include <stdio.h>
#include <string.h>

char* pass = "default";

typedef struct {
    FILE *file;
} SFile;

StreamWriter sfile_writer(const char *file_name);
StreamReader sfile_reader(const char *file_name);

void set_pass(char *password){
    pass = password;
}

#endif
