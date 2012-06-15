#include "iotn44a.h"

ISR( TIM0_OVF_vect ) {
    PORTA ^= PIN1;
}

int main(void) {

   // Set up Port B pin 4 mode to output
    DDRA = PIN1;
 
   // prescale timer to 1/1024th the clock rate
   TCCR0B |= (1<<CS02) | (1<<CS00);
 
   // enable timer overflow interrupt
   TIMSK0 |=1<<TOIE0;

   // enable interrupts
   asm("sei");
 
   for(;;){}
}
