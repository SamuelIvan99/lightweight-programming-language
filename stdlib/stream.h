#ifndef STREAM_H
#define STREAM_H

typedef struct {
	const char *file_name;	
} StreamWriter;

StreamWriter stream_writer(const char *file_name);

int write(StreamWriter writer, const char *text);

#endif