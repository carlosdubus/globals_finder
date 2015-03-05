#### Install
	pip install pycparser
	git clone https://github.com/carlosdubus/globals_finder.git
	
#### Usage
	python globals_finder.py <dir> <expression>

#### Example
	python globals_finder.py . "*.[c|h]"
	
#### Output:
	./example.c:2:declaration:myArray
	./example.c:18:usage:other
	./example.c:18:usage:another
	./example.c:22:usage:A
	./example.h:1:declaration:A
	./example.h:2:declaration:B