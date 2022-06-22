
PRJ=c402
#
PROGS=$(PRJ)-ad_test
CC=gcc
CFLAGS=-g -Wall -std=c99 -pedantic

all: $(PROGS)

$(PRJ)-ad_test: $(PRJ).c $(PRJ)-ad_test.c
	$(CC) $(CFLAGS) -o $@ $(PRJ).c $(PRJ)-ad_test.c -lm

clean:
	rm -f *.o *.out $(PROGS)
#
