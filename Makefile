DEVICE  = attiny44a
F_CPU   = 1000000

CFLAGS  =  -I. -DDEBUG_LEVEL=0
OBJECTS = main.o 

COMPILE = avr-gcc -std=c99 -g -O3 -DF_CPU=$(F_CPU) $(CFLAGS) -mmcu=$(DEVICE)

main.json: json

clean:
	rm -f main.hex  main.objdump main.elf main.o main.json

.c.o:
	$(COMPILE) -c $< -o $@

main.elf: $(OBJECTS)
	$(COMPILE) -o main.elf $(OBJECTS)

mappings: main.o
	avr-objdump -dl main.o > main.objdump

json: mappings
	python objdump2json.py
