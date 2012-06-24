DEVICE  = attiny44a
F_CPU   = 1000000

CFLAGS  =  -I. -DDEBUG_LEVEL=0
OBJECTS = main.o 

COMPILE = avr-gcc -std=c99 -g -O3 -DF_CPU=$(F_CPU) $(CFLAGS) -mmcu=$(DEVICE)

main.json: json

clean:
	rm -f main.hex  main.objdump main.elf main.o main.html

.c.o:
	$(COMPILE) -c $< -o $@

main.elf: $(OBJECTS)
	$(COMPILE) -o main.elf $(OBJECTS)

disasm:	main.elf
	avr-objdump -CSrw main.o > main.objdump

mappings: main.o
	avr-objdump -dl main.o > main.objdump

html: disasm
	pygmentize -o main.html main.objdump
	echo "<p><link href="pygments.css" rel="stylesheet"></p>" >> main.html

json: mappings
	python objdump2json.py
