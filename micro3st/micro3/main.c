#include <stdio.h>
#include <uart.h>
#include <gpio.h>
#include <timer.h>
#include <leds.h>
#include "delay.h"

volatile static int seconds;
volatile static int counter;
static uint8_t AEM[5];
volatile static int period;
volatile static uint8_t temperature;
volatile static uint8_t humidity;

void timer_isr(void);
void sensor_read(void);
void sensor_init(void);
void button_press_isr(int);


void timer_isr(){
	seconds++;
}
void leds_blink(){
				while(1)
				{
					gpio_set(PB_6, 1);
					delay_ms(1000);
					gpio_set(PB_6, 0);
					delay_ms(1000);
				}
}
void button_press_isr(int status){
	counter++;
	
	if(counter == 1) {
		//timer_disable();
		period = AEM[3] + AEM[4];
		if (period == 2){
			period = 4;
			delay_ms(period *1000);
		}
		else{
			delay_ms(period * 1000);
		}
		char temp[50];
		sprintf(temp, "Changed period to %d seconds.\r\n", period);
		uart_print(temp);
		//timer_enable();
	}

	else if(counter % 2 == 1){
		//timer_disable();
		period = 3;
		delay_ms(period * 1000);
		char temp[50];
		sprintf(temp, "Changed period to %d seconds.\r\n", period);
		uart_print(temp);
		//timer_enable();
	}
	
	else if(counter % 2 == 0 && counter > 1){
		char string[60];
		sprintf(string, "Temperature: %d C | Humidity : %d rh\r\n", temperature , humidity);
		uart_print(string);
	}
}

// Sends start signal to sensor and gets the response
void sensor_init(){
  gpio_set_mode(PB_5, Output);
	gpio_set(PB_5, 0);  // pull line to LOW
	delay_ms(18);	// wait 18ms
	gpio_set(PB_5, 1); // pull line to HIGH
	delay_us(40);	// wait 40us
	gpio_set_mode(PB_5, Input); // set line as input	
	delay_us(30); // wait 30us so that you are safely in the first 80us time span
	if(gpio_get(PB_5)) uart_print("Signal is HIGH, baaad.\r\n");	// line should be LOW
	delay_us(80);	// wait 80us so that you are safely in the second 80us time span
	if(!gpio_get(PB_5)) uart_print("Signal is LOW, baaad.\r\n");	// line should be HIGH
	while(gpio_get(PB_5));	// wait for line to go LOW = ready to transmit
}

// Reads sensor and returns an array: { integral part of temperature, decimal part of temperature }
void sensor_read(){
	uint8_t rhint=0, rhdec=0, tint=0, tdec=0;
	uint8_t mask = 0x1;
	sensor_init(); // send start signal and get response
	// Get integral part of RH
	int i;
	for( i=0; i<8; i++){
		while(!gpio_get(PB_5)); // wait for line to go HIGH
		delay_us(40); // wait for 40us
		if(gpio_get(PB_5)) rhint = ((rhint << 1) | mask); // if line is HIGH, the bit is '1'
		else rhint = rhint << 1;	// otherwise, the bit is '0'
		while(gpio_get(PB_5));	// wait for line to go LOW = get next bit
	}
	// Get decimal part of RH
	for( i=0; i<8; i++){
		while(!gpio_get(PB_5)); // wait for line to go HIGH
		delay_us(40); // wait for 40us
		if(gpio_get(PB_5)) rhdec = ((rhdec << 1) | mask); // if line is HIGH, the bit is '1'
		else rhdec = rhdec << 1;	// otherwise, the bit is '0'
		while(gpio_get(PB_5));	// wait for line to go LOW = get next bit
	}
	// Get integral part of Temperature
	for( i=0; i<8; i++){
		while(!gpio_get(PB_5)); // wait for line to go HIGH
		delay_us(40); // wait for 40us
		if(gpio_get(PB_5)) tint =  ((tint << 1) | mask ); // if line is HIGH, the bit is '1'
		else tint = tint << 1;	// otherwise, the bit is '0'
		while(gpio_get(PB_5));	// wait for line to go LOW = get next bit
	}
	// Get decimal part of Temperature
	for( i=0; i<8; i++){
		while(!gpio_get(PB_5)); // wait for line to go HIGH
		delay_us(40); // wait for 40us
		if(gpio_get(PB_5)) tdec =  ((tdec << 1) | mask ); // if line is HIGH, the bit is '1'
		else tdec = tdec << 1;	// otherwise, the bit is '0'
		while(gpio_get(PB_5));	// wait for line to go LOW = get next bit
	}
	temperature = tint;
	humidity = rhint;

}


int main(void){
	// Initialize variables
	counter = 0;
	seconds = 0;
	period = 0;
	
	// Initialize leds and button, set button ISR
	//leds_init();
	//leds_set(0,0,0);
	gpio_set_mode(PB_6, Output);
	gpio_set_mode(PB_4, PullUp);	
	gpio_set_trigger(PB_4, Rising);
	gpio_set_callback(PB_4, button_press_isr);
	
	// Initialize and set UART transmission
	uart_init(9600);
	uart_enable();
	//uart_set_rx_callback(uart_rx_isr);
	
	// Initialize timer module
	timer_init(1000000);
	timer_set_callback(timer_isr);
	

	// Get AEM
	uart_print("Please insert AEM: ");
	int i;
	for(i=0; i<5; i++){
		AEM[i] = uart_rx();
		AEM[i] -= 48;
	}
	
	char text[50];
	sprintf(text, "%d%d%d%d%d\r\n", AEM[0], AEM[1], AEM[2], AEM[3], AEM[4]);
	uart_print(text);
	
	timer_enable();

	
	while(1){
		
		sensor_read();

			// LED ON if more than 25.00 degrees, OFF if less than 20.00 degrees
			if((temperature > 25) ){
				if(!gpio_get(PB_6)){
					gpio_set(PB_6, 1);}
				}
			else if((temperature < 20)){
				if(gpio_get(PB_6)) {
					gpio_set(PB_6, 0);}
			}
			// If it's between 20 and 25, change LED every second
			else{
				leds_blink();
			

		}
	}
	return 0;
}