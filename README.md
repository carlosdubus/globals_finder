#### Install
	pip install pycparser
	git clone https://github.com/carlosdubus/globals_finder.git
	
#### Run
	python globals_finder.py example.c
	
#### Output:
	example.c:1:declaration:myArray
	example.c:2:declaration:A
	example.c:17:usage:other
	example.c:21:usage:A