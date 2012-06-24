DEVICE  = attiny44a
F_CPU   = 1000000

CFLAGS  =  -I. -DDEBUG_LEVEL=0
OBJECTS = main.o 

COMPILE = avr-gcc -std=c99 -g -O3 -DF_CPU=$(F_CPU) $(CFLAGS) -mmcu=$(DEVICE)

main.html: html 

clean:
	rm -f main.objdump main.o main.html

.c.o:
	$(COMPILE) -c $< -o $@

mappings: main.o
	avr-objdump -dl main.o > main.objdump

html: mappings 
	python objdump2html.py
