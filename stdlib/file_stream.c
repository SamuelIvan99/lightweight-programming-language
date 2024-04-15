#include "file_stream.h"
#include <stdlib.h>

int write(void *writer, const char *text) {
    FileWriter *file_writer = (FileWriter *)writer;
    return fprintf(file_writer->file, "%s", text);
}

StreamWriter file_writer(const char *file_name) {
    FileWriter *file_writer = malloc(sizeof(FileWriter));
    file_writer->file = fopen(file_name, "a");

    StreamWriter writer = {
        .writer = file_writer,
        .write = write
    };
    return writer;
}