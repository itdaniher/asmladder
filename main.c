#include "iotn44a.h"

// overflow interrupt for TIM0
ISR( TIM0_OVF_vect ) {
	// toggle pin 1 of port A
	 PORTA ^= 1 << PINA1;
// exit interrupt
}

int main(void) {
	// set up port A pin 1 mode to output
	 DDRA = 1 << PINA1;
	// prescale timer to 1/1024th the clock rate
	TCCR0B |= (1<<CS02) | (1<<CS00);
	// enable timer overflow interrupt
	TIMSK0 |=1<<TOIE0;
	// enable interrupts
	__asm("sei");
	// do nothing, forever
	for(;;) { __asm("nop") }
}
