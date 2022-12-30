LEXER_GEN=flex
PARSER_GEN=bison
CC=gcc

all: lists

# Compile all bison parsers with respective output prefixes
%.tab.c %.tab.h: %.y
	$(PARSER_GEN) --header $^

# Same for all flex
%.yy.c: %.lex
	$(LEXER_GEN) -o $@ $^

# object files
%.o: %.c
	$(CC) -c $^ -o $@

%: %.tab.o %.yy.o
	$(CC) $< -o $@


clean:
	rm *.yy.c *.tab.h *.tab.c *.o