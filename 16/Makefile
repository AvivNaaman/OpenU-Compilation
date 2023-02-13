LEXER_GEN=flex
PARSER_GEN=bison
CC=gcc

all: cpl

# Compile all bison parsers with respective output prefixes
%.tab.c %.tab.h: %.y
	$(PARSER_GEN) --header $^

# Same for all flex
%.yy.c: %.lex
	$(LEXER_GEN) -o $@ $^

# object files
%.o: %.c
	$(CC) -g -c $^ -o $@

%.o: %.cpp
	$(CC) -g -c $^ -o $@

%: cpl.o main.o comiler.o cpl.tab.o
	$(CC) -g $^ -o $@

headers: cpl.tab.h


clean:
	rm *.yy.c *.tab.h *.tab.c *.o