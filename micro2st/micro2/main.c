#include "platform.h"
#include <stdio.h>
#include <stdint.h>
#include "uart.h"
#include <string.h>
#include "queue.h"
#include "gpio.h"
volatile int static counter;
char static counterstring[50];
int c=0;
volatile int leds = 0;
#define BUFF_SIZE 128 //read buffer length

Queue rx_queue; // Queue for storing received characters


// Interrupt Service Routine for UART receive
void uart_rx_isr(uint8_t rx) {
	// Check if the received character is a printable ASCII character
	if (rx >= 0x0 && rx <= 0x7F ) {
		// Store the received character
		queue_enqueue(&rx_queue, rx);
	if (rx ==  '\r'){
				if( c%2 ==1 ) 
				{
					
				 timer_enable();
				 leds_set(1,1,1);
			    timer_init(50000000);
					leds_set(0,0,0);
					
				}
				else if ( c%2 ==0 )
				{
				  timer_disable();

        if (!gpio_get(P_LED_R)) 
					{
            leds_set(1,1,1);
          } 
					else 
						{
             leds_set(0,0,0);
             }
					 }
			
					 }
}
}

void button_press_isr(int status){
	// If LED is OFF, turn it ON
	if(!gpio_get(P_LED_G)){
		leds_set(1,1,1);
		uart_print("\n The LED was switched on.");		
	}
	// If LED is ON, turn it OFF
	else{
		leds_set(0,0,0);
		uart_print("\n The LED was switched off.");
	}
	
	counter++;
	sprintf(counterstring, "\n The button has been pressed %d times.", counter);
	uart_print(counterstring);		
}



int main() {
		

	uint8_t rx_char = 0;
	char buff[BUFF_SIZE]; // The UART read string will be stored here
	uint32_t buff_index;
	uart_init(9600);
	uart_enable(); // Enable UART module
	leds_init();
	leds_set(0, 0, 0);
	


	uart_set_rx_callback(uart_rx_isr); // Set the UART receive callback function

	counter = 0;

	gpio_set_mode(P_LED_G, Output);
	gpio_set_mode(P_SW, PullUp);
	
	uart_print("\r\n");// Print newline
	gpio_set_trigger(P_SW, Rising);
	gpio_set_callback(P_SW, button_press_isr);
	queue_init(&rx_queue, 7);
	// Repeatedly ask for AEM and await signals
	uart_print("\n Please insert AEM: ");
	
	while(1) {

		// Prompt the user to enter their full name

		buff_index = 0; // Reset buffer index
		
		do {
			// Wait until a character is received in the queue
			while (!queue_dequeue(&rx_queue, &rx_char))
				__WFI(); // Wait for Interrupt

			if (rx_char == 0x7F) { // Handle backspace character
				if (buff_index > 0) {
					buff_index--; // Move buffer index back
					uart_tx(rx_char); // Send backspace character to erase on terminal
				}
			} else {
			
				// Store and echo the received character back
				buff[buff_index++] = (char)rx_char; // Store character in buffer
				uart_tx(rx_char); // Echo character back to terminal
					c= buff[buff_index-1];
			}
		} while (rx_char != '\r' && buff_index < BUFF_SIZE); // Continue until Enter key or buffer full
		
		// Replace the last character with null terminator to make it a valid C string
		buff[buff_index - 1] = '\0';
		uart_print("\r\n"); // Print newline
		
		// Check if buffer overflow occurred
		if (buff_index > BUFF_SIZE) {
			uart_print("Stop trying to overflow my buffer! I resent that!\r\n");
		}
		
	}
}
