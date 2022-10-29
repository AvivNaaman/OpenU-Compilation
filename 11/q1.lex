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

int main(int argc, char* argv[])
{
    ++argv, --argc;  /* skip over program name */
    if (argc > 0)
        yyin = fopen( argv[0], "r" );
    else
        yyin = stdin;

    if (!feof(yyin)) {  
        printf("1.\t");
    }

    yylex();
    return 0;
}