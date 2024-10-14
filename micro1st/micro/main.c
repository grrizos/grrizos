#include <stdio.h>
#include "uart.h"
#include <string.h>
extern int hash_calculate(char* str); 
extern int sum_of_natural_numbers(int hash); 
extern int mono_digit_calculator(int n); 

#define MAX_STRING_LENGTH 100  // Define the maximum string length


void uart_receive_string(char *str, uint32_t max_length) {
    uint32_t i = 0;
    uint8_t received_char;

    while (i < max_length - 1) { // Save space for the null terminator
        received_char = uart_rx(); // Receive a single character

        if (received_char == '\r' || received_char == '\n') {
            break; 
        }

        str[i++] = received_char; 
    }

    str[i] = '\0'; 
}

int main() {
    char my_string[MAX_STRING_LENGTH];
    int hash, single_digit, result;
        char output[50];
    int exit = 0;
        uart_init(9600);
     while(exit == 0){
        uart_enable();
        
      uart_print("Enter a string: \r\n");
        //scanf("%s",my_string);
    uart_receive_string(my_string, MAX_STRING_LENGTH);
    hash = hash_calculate(my_string);
    single_digit = mono_digit_calculator(hash);
    result = sum_of_natural_numbers(single_digit);
        
    // Convert hash to string and print    
    sprintf(output, "Hash: %d\r\n", hash);
    uart_print(output);

    sprintf(output, "Single Digit: %d\r\n", single_digit);
    uart_print(output);


    sprintf(output, "Sum of natural numbers: %d\r\n", result);
    uart_print(output);
            
        if(!(strcmp(my_string,"Exit") || strcmp(my_string,"exit"))){
          exit = 1;
          uart_print("Exiting...\r\n");}
       }
    return 0;
}
