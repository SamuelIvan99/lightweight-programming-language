#ifndef STREAM_H
#define STREAM_H

typedef struct {
    void *writer;
    int (*write)(void *writer,const char *text);
} StreamWriter;

typedef struct StreamReader{
    void *reader;
} StreamReader;



#endif
