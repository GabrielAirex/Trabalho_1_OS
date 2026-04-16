SRC    = ../src
CXX    = g++
CFLAGS = -O2 -Wall -std=c++11
LIBS   = -lpthread

all: auxiliar sequencial paralelo_threads paralelo_processos

auxiliar:
	$(CXX) $(CFLAGS) -o $(SRC)/auxiliar $(SRC)/auxiliar.cpp

sequencial:
	$(CXX) $(CFLAGS) -o $(SRC)/sequencial $(SRC)/sequencial.cpp

paralelo_threads:
	$(CXX) $(CFLAGS) -o $(SRC)/paralelo_threads $(SRC)/paralelo_threads.cpp $(LIBS)

paralelo_processos:
	$(CXX) $(CFLAGS) -o $(SRC)/paralelo_processos $(SRC)/paralelo_processos.cpp

clean:
	rm -f $(SRC)/auxiliar $(SRC)/sequencial $(SRC)/paralelo_threads $(SRC)/paralelo_processos
