
all: mfcalc.o

mfcalc.o: parser.tab.c
	gcc parser.tab.c -o mfcalc.o -lm

parser.tab.c: parser.y
	bison parser.y

# calc.o: calc.c
# 	gcc -o calc.o -c calc.c -lm