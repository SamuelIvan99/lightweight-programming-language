// #include <string.h>

// #define MAX_STRING_LENGTH 255

// /**
//  * @brief Struct representing a string.
//  */
// struct string
// {
//     char data[MAX_STRING_LENGTH];
//     int length; 
// };

// /**
//  * @brief Initialize a string with the given initial value.
//  * 
//  * @param str Pointer to the struct string to be initialized.
//  * @param initialValue The initial value of the string.
//  */
// void initString(struct string *str, const char *initialValue) {
//     int i;
//     for (i = 0; initialValue[i] != '\0' && i < MAX_STRING_LENGTH - 1; i++) {
//         str->data[i] = initialValue[i];
//     }
//     str->data[i] = '\0'; // Null-terminate the string
//     str->length = i;
// }

// /**
//  * Create a new string from the given initial value.
//  * 
//  * @param initialValue The initial value of the string.
//  * @return The created string.
//  */
// struct string createString(const char *initialValue) {
//     struct string result;
//     initString(&result, initialValue);

//     return result;
// }

// /**
//  * @brief Copy a string.
//  * 
//  * @param str Pointer to the struct string to be copied.
//  * @return The copied string.
//  */
// struct string copyString(const struct string *str) {
//     struct string result;
//     result.length = str->length;
//     strcpy(result.data, str->data);

//     return result;
// }

// /**
//  * @brief Combine two strings.
//  * 
//  * @param str1 Pointer to the first struct string.
//  * @param str2 Pointer to the second struct string.
//  * @return The combined string.
//  */
// struct string combineStrings(const struct string *str1, const struct string *str2) {
//     struct string result;
//     int i;

//     for (i = 0; i < str1->length && i < MAX_STRING_LENGTH - 1; i++) {
//         result.data[i] = str1->data[i];
//     }

//     for (int j = 0; j < str2->length && i < MAX_STRING_LENGTH - 1; i++, j++) {
//         result.data[i] = str2->data[j];
//     }

//     result.data[i] = '\0'; // Null-terminate the string
//     result.length = i;

//     return result;
// }

// /**
//  * @brief Reverse a string.
//  * 
//  * @param str Pointer to the struct string to be reversed.
//  * @return The reversed string.
//  */
// struct string reverseString(const struct string *str) {
//     struct string result;
//     int i;

//     for (i = 0; i < str->length; i++) {
//         result.data[i] = str->data[str->length - i - 1];
//     }

//     result.data[i] = '\0'; // Null-terminate the string
//     result.length = i;

//     return result;
// }

// /**
//  * @brief Convert a string to uppercase.
//  * 
//  * @param str Pointer to the struct string to be converted.
//  * @return The uppercase string.
//  */
// struct string toupperString(const struct string *str) {
//     struct string result;
//     int i;

//     for (i = 0; i < str->length && i < MAX_STRING_LENGTH - 1; i++) {
//         result.data[i] = toupper(str->data[i]);
//     }

//     result.data[i] = '\0'; // Null-terminate the string
//     result.length = i;

//     return result;
// }

// /**
//  * @brief Convert a string to lowercase.
//  * 
//  * @param str Pointer to the struct string to be converted.
//  * @return The lowercase string.
//  */
// struct string tolowerString(const struct string *str) {
//     struct string result;
//     int i;

//     for (i = 0; i < str->length && i < MAX_STRING_LENGTH - 1; i++) {
//         result.data[i] = tolower(str->data[i]);
//     }

//     result.data[i] = '\0'; // Null-terminate the string
//     result.length = i;

//     return result;
// }

// // The null terminator, represented by '\0', is used in C and C++ strings to indicate the end of the string. 
// // It serves as a value that marks the boundary of the string data.
// // In C and C++, string literals (sequences of characters enclosed in double quotes) 
// // are automatically null-terminated.