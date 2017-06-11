run: main 
	cd src/exec; ./main 10 -o solution10.vtk; ./main 10 -i solution10.vtk -o solution20.vtk;

check: tests
	cd src/tests; ./tests

main: 
	g++ -pg -std=c++11 -Wall -Wextra -Wconversion -O3 -Iinclude src/exec/main.cpp src/utilities/timer.c src/utilities/swap.cpp -o src/exec/main

tests:
	g++ -std=c++11 -Wall -Wextra -Wconversion -O3 -Iinclude src/tests/tests.cpp src/utilities/swap.cpp -o src/tests/tests -I/opt/local/include -L/opt/local/lib -lcppunit