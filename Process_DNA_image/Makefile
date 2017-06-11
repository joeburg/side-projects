CXX=g++
CPPFLAGS=
CXXFLAGS=-g -Wall -Wextra -Wconversion -std=c++11
LDFLAGS=-ltiff

main: main.cpp imageanalysis.hpp imageio.hpp imageio.cpp
	$(CXX) $(CXXFLAGS) main.cpp imageio.cpp $(LDFLAGS) -o main

tiffdemo: tiffdemo.c
	$(CXX) $(CXXFLAGS) tiffdemo.c $(LDFLAGS) -o tiffdemo

clean:
	rm -f main tiffdemo *~
