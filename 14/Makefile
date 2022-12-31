LEXER_GEN=flex
PARSER_GEN=bison
CC=gcc

all: list

# Compile all bison parsers with respective output prefixes
%.tab.c %.tab.h: %.y
	$(PARSER_GEN) --header $^

# Same for all flex
%.yy.c: %.lex
	$(LEXER_GEN) -o $@ $^

# object files
%.o: %.c 
	$(CC) -g -c $^ -o $@

%: %.tab.o %.yy.o %.utils.o
	$(CC) -g $^ -o $@


clean:
	rm *.yy.c *.tab.h *.tab.c *.o