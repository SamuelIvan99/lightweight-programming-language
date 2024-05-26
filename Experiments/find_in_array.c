#include "../stdlib/array.c"
#include "../stdlib/array.h"
#include "../stdlib/file_stream.c"
#include "../stdlib/file_stream.h"
#include "../stdlib/generate_random.h"
#include "../stdlib/sfile_stream.c"
#include "../stdlib/sfile_stream.h"
#include <stdio.h>
int main() {
  int max_size = 10000000;
  set_random(10);
  StreamWriter writer = file_writer("Texts/find_in_array.txt");
  Array buffer;
  buffer.size = 15;
  buffer.value = calloc(buffer.size, sizeof(char));
  Array arrayS;
  arrayS.size = 10000000;
  arrayS.value = calloc(arrayS.size, sizeof(int));
  for (int i = 0; i < max_size; i = i + 1) {
    ((int *)getElement(arrayS, i))[i] = generate_random(10000);
  }
  int min = 10001;
  int max = 0;
  Array nums;
  nums.size = 2;
  nums.value = calloc(nums.size, sizeof(int));
  for (int i = 0; i < max_size; i = i + 1) {
    if (((int *)getElement(arrayS, i))[i] < min) {
      min = ((int *)getElement(arrayS, i))[i];
    }
    if (max < ((int *)getElement(arrayS, i))[i]) {
      max = ((int *)getElement(arrayS, i))[i];
    }
  }
  for (int i = 0; i < max_size; i = i + 1) {
    if (((int *)getElement(arrayS, i))[i] == min) {
      ((int *)getElement(nums, 0))[0] = ((int *)getElement(nums, 0))[0] + 1;
    }
    if (((int *)getElement(arrayS, i))[i] == max) {
      ((int *)getElement(nums, 1))[1] = ((int *)getElement(nums, 1))[1] + 1;
    }
  }
  sprintf(buffer.value, "%d \n", min);
  writer.write(writer.writer, "Min element is: ");
  writer.write(writer.writer, buffer.value);
  sprintf(buffer.value, "%d ", ((int *)getElement(nums, 0))[0]);
  writer.write(writer.writer, "Min element found: ");
  writer.write(writer.writer, buffer.value);
  writer.write(writer.writer, "times\n");
  sprintf(buffer.value, "%d \n", max);
  writer.write(writer.writer, "Max element is: ");
  writer.write(writer.writer, buffer.value);
  sprintf(buffer.value, "%d ", ((int *)getElement(nums, 1))[1]);
  writer.write(writer.writer, "Max element found: ");
  writer.write(writer.writer, buffer.value);
  writer.write(writer.writer, "times\n");
  writer.write(writer.writer, "\n\n\n\n");
  writer.write(writer.writer, "Full Array: \n");
  for (int i = 0; i < max_size; i = i + 1) {
    sprintf(buffer.value, "%d \n", ((int *)getElement(arrayS, i))[i]);
    writer.write(writer.writer, buffer.value);
  }
  free(nums.value);
  free(arrayS.value);
  free(buffer.value);
}