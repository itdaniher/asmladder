DEVICE  = attiny44a
F_CPU   = 8000000

CFLAGS  =  -I. -DDEBUG_LEVEL=0
OBJECTS = main.o 

COMPILE = avr-gcc -g -Wall -O0 -DF_CPU=$(F_CPU) $(CFLAGS) -mmcu=$(DEVICE)

main.html: html

clean:
	rm -f main.hex  main.objdump main.elf main.o main.html

.c.o:
	$(COMPILE) -c $< -o $@

main.elf: $(OBJECTS)
	$(COMPILE) -o main.elf $(OBJECTS)

main.hex: main.elf
	rm -f main.hex main.eep.hex
	avr-objcopy -j .text -j .data -O ihex main.elf main.hex
	avr-size main.hex

disasm:	main.elf
	avr-objdump -CSr main.o > main.objdump

html: disasm
	pygmentize -o main.html main.objdump
	echo "<p><link href="pygments.css" rel="stylesheet"></p>" >> main.html
