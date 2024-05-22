#include "../stdlib/array.c"
#include "../stdlib/array.h"
#include "../stdlib/file_stream.c"
#include "../stdlib/file_stream.h"
#include "../stdlib/sfile_stream.c"
#include "../stdlib/sfile_stream.h"
#include <stdio.h>
int main() {
  int max_size = 1000;
  StreamWriter writer = file_writer("matrix_based.txt");
  Array buffer;
  buffer.size = 10;
  buffer.value = calloc(buffer.size, sizeof(char));
  for (int i = 0; i < max_size; i = i + 1) {
    for (int j = 0; j < max_size; j = j + 1) {
      sprintf(buffer.value, "%d ", (i * max_size) + j);
      writer.write(writer.writer, buffer.value);
    }
    writer.write(writer.writer, "\n");
  }
  free(buffer.value);
}