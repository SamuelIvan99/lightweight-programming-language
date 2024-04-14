#include "stream.h"
#include <stdio.h>
#include <stdlib.h>

StreamWriter stream_writer(const char *file_name) {
  StreamWriter write = {
    .file_name = file_name
  };
  return write;
}

int write(StreamWriter writer, const char *text) {
    FILE *file;
    int length = 0;

    file = fopen(writer.file_name, "a");
    if (file == NULL) {
        perror("Unable to open the file for writing");
        return EXIT_FAILURE;
    }

    while (text[length] != '\0') length++;

    for (int i = 0; i < length; i++) {
        if (fputc(text[i], file) == EOF) {
            perror("Failed to write to the file");
            fclose(file);
            return EXIT_FAILURE;
        }
    }

    fclose(file);

    return EXIT_SUCCESS;
}
