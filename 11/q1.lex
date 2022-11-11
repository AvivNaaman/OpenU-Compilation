%{

// that'll hold the current line number at each and every moment.
int line_num = 1;

/* List of roman representation of chars */
static const char *map[] = {
    "I", "II", "III", "IV", "V",
    "VI", "VII", "VIII", "IX", "X"
};

#include <stdio.h>

// that's just helpful to prevent code duplicates.
void print_current_line() {
    printf("\n%d.\t", line_num);
}

%}

%option noyywrap
%option yylineno

%%

 /* Numbers 1-9 exactly - return exactly the number. */
[1-9] { 
    int num = atoi(yytext); 
    printf("%s", map[num-1]);
}

 /* Longer, unsupported numbers */
[0-9]+ { printf("%s", yytext); } 

 /* Skip whitespaces */
[\r\t ] { putchar(*yytext); }

 /* Count & process lines - I chose to do it manually, without yylineno */
\n { 
    line_num += 1; 
    // check if odd & print line number
    if (line_num & 1) {
        print_current_line();
    }
    // no number if even.
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
            fprintf(stderr, "Failed to open file %s. Using stdin instead!", *argv);
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
        // print "1.    " for first line if such one is present.
        print_current_line();
        ungetc(c, yyin);
    }
    
    // start lexing. no return is specified, so that'll process the whole input.
    yylex();
    return 0;
}