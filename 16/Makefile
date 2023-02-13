LEXER_GEN=flex
PARSER_GEN=bison
CC=gcc

cpq: cpq.o cpl.tab.o cpl.yy.o
	$(CC) -g $^ -o $@

# object files
%.o: %.c cpl.tab.h
	$(CC) -g -c $^

# Compile all bison parsers with respective output prefixes
cpl.tab.c cpl.tab.h: cpl.y
	$(PARSER_GEN) --header $^

# Same for all flex
%.yy.c: %.lex
	$(LEXER_GEN) -o $@ $^



clean:
	rm *.yy.c *.tab.* *.o