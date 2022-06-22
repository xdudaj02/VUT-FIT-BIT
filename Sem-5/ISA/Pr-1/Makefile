LDLIBS=-lcrypto -lssl

all: popcl mkdir

popcl: main.o
	g++ -o popcl main.o $(LDLIBS)

main.o: main.cpp
	g++ -c main.cpp

mkdir:
	mkdir -p ./.config
