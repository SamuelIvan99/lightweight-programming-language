#include "../stdlib/file_stream.c"
#include "../stdlib/file_stream.h"

#include <stdio.h>
#include <time.h>


int main() {

    clock_t start = clock();

  int max_size = 10000000;
  srand(10);
  StreamWriter writer = file_writer("Texts/find_in_array_c.txt");
  char buffer[200];
  int *arrayS = calloc(10000000, sizeof(int));

    for (int i = 0; i < max_size; i = i + 1) {
        arrayS[i] = rand() % 10000;
    }

    int min = 10001;
    int max = 0;

    int nums[2] = {0,0};

    for(int i = 0; i < max_size; i = i + 1){
        if(arrayS[i] < min){
            min = arrayS[i];
        }
        if(max < arrayS[i]){
            max = arrayS[i];
        }
    }

    for(int i = 0; i < max_size; i = i + 1){
        if(arrayS[i] == min){
            nums[0] = nums[0] + 1;
        }
        if(arrayS[i] == max ){
            nums[1] = nums[1] + 1;
        }
    }



    sprintf(buffer, "Min element is: %d \n", min);
    writer.write(writer.writer, buffer);
    sprintf(buffer, "Min element found: %d times\n", nums[0]);
    writer.write(writer.writer, buffer);
    sprintf(buffer, "Max element is: %d \n", max);
    writer.write(writer.writer, buffer);
    sprintf(buffer, "Max element found: %d times\n", nums[1]);
    writer.write(writer.writer, buffer);
    writer.write(writer.writer, "\n\n\n\n");
    writer.write(writer.writer, "Full Array: \n");

    for (int i = 0; i < max_size; i = i + 1) {
        sprintf(buffer, "%d \n", arrayS[i]);
        writer.write(writer.writer, buffer);
    }

    clock_t end = clock();

    double time_taken = (double)(end - start)/CLOCKS_PER_SEC;
     printf("%lf\n", time_taken);
}