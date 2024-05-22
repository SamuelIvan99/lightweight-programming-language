#include "../stdlib/file_stream.c"
#include "../stdlib/file_stream.h"

#include <stdio.h>

int main() {

  int max_size = 10000;
  srand(10);
  StreamWriter writer = file_writer("Texts/bubble_sort_c.txt");
  char buffer[15];
  int arrayS[10000];

    writer.write(writer.writer, "Unsorted: \n");

    for (int i = 0; i < max_size; i = i + 1) {
        arrayS[i] = rand();
        sprintf(buffer, "%d \n", arrayS[i]);
        writer.write(writer.writer, buffer);
    }

  for (int i = 0; i < max_size - 1; i = i + 1) {
      char flag = 0;
    for (int j = 0; j < max_size - i - 1; j = j + 1) {
      if(arrayS[j + 1] < arrayS[j]){
          int temp = arrayS[j];
          arrayS[j] = arrayS[j + 1];
          arrayS[j + 1] = temp;
          flag = 1;
      }
    }
    if(flag == 0){
        break;
    }
  }


  writer.write(writer.writer, "\n\n\n\n");
  writer.write(writer.writer, "Sorted: \n");

    for (int i = 0; i < max_size; i = i + 1) {
        sprintf(buffer, "%d \n", arrayS[i]);
        writer.write(writer.writer, buffer);
    }
}