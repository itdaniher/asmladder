#include "io.h"

// overflow interrupt for TCC0
ISR(TCC0_OVF_vect){ 
// toggle pin 1 of port A
	PORTA.OUTTGL = PIN1_bm;
// exit interrupt
}

int main(void) {
	// set up port A pin 1 mode to output
	PORTA.DIRSET = PIN1_bm;
	// prescale timer to 1/8th the clock rate
    TCC0.CTRLA = TC_CLKSEL_DIV8_gc;
	// interrupt on timer overflow
	TCC0.INTCTRLA = TC_OVFINTLVL_LO_gc;
	// set timer period to full 16b
	TCC0.PER = 0xFFFF;
	// initalize timer count at 0
    TCC0.CNT = 0;
	// enable interrupts
	__asm("sei");
	// do nothing, forever
	for(;;) { __asm("nop"); } 
}
