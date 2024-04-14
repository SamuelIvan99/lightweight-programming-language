#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *file;
    char data[] = "Hello, world!";
    int length = sizeof(data) / sizeof(data[0]);

    // Open the file for writing
    file = fopen("example.txt", "w");
    if (file == NULL) {
        perror("Unable to open the file for writing");
        return EXIT_FAILURE;
    }

    // Write each byte from 'data' to the file
    for (int i = 0; i < length - 1; i++) { // Exclude the null terminator
        if (fputc(data[i], file) == EOF) {
            perror("Failed to write to the file");
            fclose(file);
            return EXIT_FAILURE;
        }
    }

    // Close the file
    fclose(file);

    return EXIT_SUCCESS;
}
