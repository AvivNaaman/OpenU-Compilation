LEXER = flex
LEX_EXT = lex
LEX_OUT_EXT = yy.c
CC = gcc

# If you need to compile more single-lex executables, just add their prefix here, before clean.
all: cla clean_inter

# Template for 2-stage flex-gcc compilations
%: %.$(LEX_EXT)
	$(LEXER) -o $@.$(LEX_OUT_EXT) $@.$(LEX_EXT)
	$(CC) $@.$(LEX_OUT_EXT) -o $@

# Remove temporary .yy.c files from flex.
clean_inter:
	rm -f *.$(LEX_OUT_EXT)
