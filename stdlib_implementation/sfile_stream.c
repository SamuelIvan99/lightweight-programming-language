#include "sfile_stream.h"
#include <stdlib.h>

int swrite(void *writer, const char *text) {
    SFile *file_writer = (SFile *)writer;
    int sum = 0;
    for(int i = 0; pass[i] != 0; ++i){
        sum+= pass[i];
    }
    sum = sum % 200;
    
    char* new_msg = (char*)malloc(strlen(text));

    for(int i = 0; text[i] != 0; ++i){
        new_msg[i] = text[i] - sum;
    }
    int res = fprintf(file_writer->file, "%s\n", new_msg);
    free(new_msg);
    return res;
}

const char* sread(StreamReader reader) {
    SFile *file_reader = reader.reader;
    static char res[255];
    int sum = 0;
    int i;
    for(i = 0; pass[i] != 0; ++i){
        sum+= pass[i];
    }
    sum = sum % 200;

    fgets(res, 255, file_reader->file);

    for(i = 0; res[i] != 0; ++i){
        res[i] = res[i] + sum;
    }
    res[i-1] = '\0';
    return res;
}

StreamWriter sfile_writer(const char *file_name) {
    SFile *sfile_writer = malloc(sizeof(SFile));
    sfile_writer->file = fopen(file_name, "a");

    StreamWriter writer = {
        .writer = sfile_writer,
        .write = swrite
    };
    return writer;
}

StreamReader sfile_reader(const char *file_name) {
    SFile *sfile_reader = malloc(sizeof(SFile));
    sfile_reader->file = fopen(file_name, "r");

    StreamReader writer = {
        .reader = sfile_reader
    };
    return writer;
}
