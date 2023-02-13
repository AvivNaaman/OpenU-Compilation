#include <stdio.h>
#include "cpl.tab.h"
extern int yylex(void);
void yyerror (const char *s) {
    fprintf(stderr, "%s\n", s); 
}

int main(int argc, char *argv[]) {
    extern FILE *yyin;
    if (argc != 2) {
        fprintf(stderr, "Invalid arguments: Missing input file name!\nUsage\n\t%s <filename>\n\n", argv[0]);
        return 1;
    }

    yyin = fopen(argv[1], "r");
    if (!yyin) {
        fprintf(stderr, "Failed to open input file %s! Aborting.\n", argv[1]);
        return 1;
    }

    return yyparse();
}