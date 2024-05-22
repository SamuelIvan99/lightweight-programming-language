#include "../stdlib/array.c"
#include "../stdlib/array.h"
#include "../stdlib/file_stream.c"
#include "../stdlib/file_stream.h"
#include "../stdlib/sfile_stream.c"
#include "../stdlib/sfile_stream.h"
#include <stdio.h>
int main() {

  int max_size = 10000;
  srand(10);
  StreamWriter writer = file_writer("Texts/bubble_sort_based.txt");
  Array buffer;
  buffer.size = 15;
  buffer.value = calloc(buffer.size, sizeof(char));
  Array arrayS;
  arrayS.size = 10000;
  arrayS.value = calloc(arrayS.size, sizeof(int));
  writer.write(writer.writer, "Unsorted: \n");
  for (int i = 0; i < max_size; i = i + 1) {
    ((int *)getElement(arrayS, i))[i] = rand();
    sprintf(buffer.value, "%d \n", ((int *)getElement(arrayS, i))[i]);
    writer.write(writer.writer, buffer.value);
  }
  writer.write(writer.writer, "\n");
  for (int i = 0; i < max_size - 1; i = i + 1) {
    for (int j = 0; j < max_size - i - 1; j = j + 1) {
      if (((int *)getElement(arrayS, j + 1))[j + 1] <
          ((int *)getElement(arrayS, j))[j]) {
        int temp = ((int *)getElement(arrayS, j))[j];
        ((int *)getElement(arrayS, j))[j] =
            ((int *)getElement(arrayS, j + 1))[j + 1];
        ((int *)getElement(arrayS, j + 1))[j + 1] = temp;
      }
    }
  }
  writer.write(writer.writer, "\n\n\n\n");
  writer.write(writer.writer, "Sorted: \n");
  for (int i = 0; i < max_size; i = i + 1) {
    sprintf(buffer.value, "%d \n", ((int *)getElement(arrayS, i))[i]);
    writer.write(writer.writer, buffer.value);
  }
  free(arrayS.value);
  free(buffer.value);
}