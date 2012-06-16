DEVICE  = attiny44a
F_CPU   = 1000000

CFLAGS  =  -I. -DDEBUG_LEVEL=0
OBJECTS = main.o 

COMPILE = avr-gcc -g -Wall -O5 -DF_CPU=$(F_CPU) $(CFLAGS) -mmcu=$(DEVICE)

main.html: html

clean:
	rm -f main.hex  main.objdump main.elf main.o main.html

.c.o:
	$(COMPILE) -c $< -o $@

main.elf: $(OBJECTS)
	$(COMPILE) -o main.elf $(OBJECTS)

disasm:	main.elf
	avr-objdump -CSrw main.o > main.objdump

mappings: main.elf
	avr-objdump -dl main.o > main.objdump

html: disasm
	pygmentize -o main.html main.objdump
	echo "<p><link href="pygments.css" rel="stylesheet"></p>" >> main.html
