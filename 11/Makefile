LEXER = flex
LEX_EXT = lex
LEX_OUT_EXT = yy.c
CC = gcc

all: q1 q2

%: %.$(LEX_EXT)
	$(LEXER) -o $@.$(LEX_OUT_EXT) $@.$(LEX_EXT)
	$(CC) $@.$(LEX_OUT_EXT) -o $@
