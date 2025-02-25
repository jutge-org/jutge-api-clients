all: tutorial.exe

tutorial.exe: tutorial.cpp jutge_api_client.cpp httplib.h json.hpp
	g++ -I /opt/homebrew/include -L /opt/homebrew/lib -std=c++20 tutorial.cpp -l ssl -l crypto -o tutorial.exe

run: all
	./tutorial.exe

clean:
	rm *.exe *.png *.o
