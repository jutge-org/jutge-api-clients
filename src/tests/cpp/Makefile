all: tests.exe

tests.exe: tests.cpp jutge_api_client.cpp httplib.h json.hpp
	g++ -I /opt/homebrew/include -L /opt/homebrew/lib -std=c++20 tests.cpp catch_amalgamated.cpp -l ssl -l crypto -o tests.exe

test:
	./tests.exe

clean:
	rm *.exe *.png *.o
