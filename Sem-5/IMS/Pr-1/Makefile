TARGET = covid_simulator
CFLAGS = -Wall -Wextra
ARCHIVE = 03_xvanop01_xdudaj02

all: $(TARGET)

$(TARGET): main.cpp
	g++ $(CFLAGS) -o $(TARGET) main.cpp src/*.h src/*.cpp

run:
	./covid_simulator $(ARGS)

pack:
	tar -cvzf $(ARCHIVE).tar.gz Makefile README dokumentacia.pdf doxygen.config main.cpp src/*.h src/*.cpp

doc:
	doxygen doxygen.config

clean:
	rm -rf doc $(ARCHIVE).tar.gz $(TARGET)
