#include "../stdlib/file_stream.c"
#include "../stdlib/file_stream.h"

#include <stdio.h>

int main() {
  int max_size = 1000;
  StreamWriter writer = file_writer("matrix_c.txt");
  char buffer[10];
  for (int i = 0; i < max_size; i = i + 1) {
    for (int j = 0; j < max_size; j = j + 1) {
      sprintf(buffer, "%d ", (i * max_size) + j);
      writer.write(writer.writer, buffer);
    }
    writer.write(writer.writer, "\n");
  }
}