#include "iotn44a.h"

ISR( TIM0_OVF_vect ) {
	 PORTA ^= 1 << PINA1;
}

int main(void) {
	// Set up port A pin 1 mode to output
	 DDRA = 1 << PINA1;
	// prescale timer to 1/1024th the clock rate
	TCCR0B |= (1<<CS02) | (1<<CS00);
	// enable timer overflow interrupt
	TIMSK0 |=1<<TOIE0;
	// enable interrupts
	__asm("sei");
	for(;;) {
		__asm("nop");
	}
}
