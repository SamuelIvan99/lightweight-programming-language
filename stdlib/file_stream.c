#include "file_stream.h"
#include <stdlib.h>

int write(void *writer, const char *text) {
    File *file_writer = (File *)writer;
    return fprintf(file_writer->file, "%s", text);
}

const char* read(StreamReader reader) {
    File *file_reader = reader.reader;
    static char res[255];
    fgets(res, 255, file_reader->file);
    return res;
}

StreamWriter file_writer(const char *file_name) {
    File *file_writer = malloc(sizeof(File));
    file_writer->file = fopen(file_name, "a");

    StreamWriter writer = {
        .writer = file_writer,
        .write = write
    };
    return writer;
}

StreamReader file_reader(const char *file_name){
    File *file_reader = malloc(sizeof(File));
    file_reader->file = fopen(file_name, "r");

    StreamReader writer = {
        .reader = file_reader
    };
    return writer;
}