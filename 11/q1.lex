%{

int line_num = 1;

/* List of roman representation of chars */
static const char *map[] = {
    "I", "II", "III", "IV", "V",
    "VI", "VII", "VIII", "IX", "X"
};

#include <stdio.h>

%}
%option noyywrap
%option yylineno
%%

 /* Numbers 1-9 exactly - return exactly the number. */
[1-9] { 
    int num = atoi(yytext); 
    printf("%s", map[num-1]);
}


[0-9]+ { printf("%s", yytext); }/* Longer, unsupported numbers */

 /* Skip whitespaces */
[\r\t ] { putchar(*yytext); }

 /* Count & process lines */
\n { 
    line_num += 1; 
    if (line_num & 1) {
        printf("\n%d.\t", line_num);
    }
    else {
        printf("\n\t");
    }
}

 /* Skip others */
. { putchar(*yytext); }

%%

int main(int argc, char* argv[]) {
    ++argv, --argc;  /* skip over program name */
    if (argc > 0) {
        yyin = fopen(*argv, "r");
        if (!yyin) {
            fprintf(stderr, "Failed to open file %s. Using stdin instead.", *argv);
            yyin = stdin;
        }
    }
    else {
        yyin = stdin;
    }

    // check if file is empty.
    int c = fgetc(yyin);
    if (c == EOF) {
        exit(0);
    } else {
        printf("%s", "1.\t");
        ungetc(c, yyin);
    }

    yylex();
    return 0;
}