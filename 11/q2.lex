%{

#include <stdio.h>
#include <string.h>

#define REC_NUM 1
#define PROP_NAME 2
#define DECIMAL 3
#define STRING 4
#define DATE 5
#define OTHER 6

#define STRING_MAXLENGTH 500

union current_payload {
    char text[STRING_MAXLENGTH];
    int integer_num;
    double decimal_num;
} current_payload;

/* type names - for the table UI */
static const char *token_names[] = {
    "END", "RECORD_NUMBER", "PROP_NAME",
    "DECIMAL",  "STRING", "DATE", "OTHER"
};

// Removes the first & last chars of yytext, and puts it into current_payload.text.
void copy_parse_string2() {
    int prop_name_len = strlen(yytext) - 2;
    strcpy(current_payload.text, yytext+1);
    *(current_payload.text + prop_name_len) = '\0';
}

%}
%option noyywrap
%option yylineno
%%

 /* [NUM] */
\[[1-9][0-9]*\] { 
    copy_parse_string2();
    current_payload.integer_num = atoi(current_payload.text);
    return REC_NUM;
}

 /* <propertyname> */
\<[a-z]+\> { 
    // remove < and >
    copy_parse_string2();
    return PROP_NAME;
}

 /*  13902.53290, .9503, 1290.21 */
[0-9]?"."[0-9]+ { 
    current_payload.decimal_num = atof(yytext);
    return DECIMAL;
}

 /* "gdsakjfslkd" */
\"(\\.|[^"\\])*\" { 
    // remove " at beginning & at end.
    copy_parse_string2();
    return STRING;
}

 /* 1 June 1999 */
(([1-3][0-9])|[1-9])" "(January|February|March|April|May|June|July|August|September|October|November|December)" "[0-9]{4} {
    strcpy(current_payload.text, yytext); 
    return DATE;
}

 /* Skip whitespaces and new lines */
[\r\t\n ] { return OTHER; }



 /* Skip others */
. { fprintf(stderr, "Unrecognized token '%c' (%d) @ line %d! \n", *yytext, *yytext, yylineno); return OTHER; }

%%

int main(int argc, char* argv[])
{
    ++argv, --argc;  /* skip over program name */
    if (argc > 0)
        yyin = fopen( argv[0], "r" );
    else
        yyin = stdin;
    int token_type = 0;

    // Header
    printf("%-10s\t%-20s\t%-20s\n", "TOKEN", "LEXEME", "ATTRIBUTE");

    while (token_type = yylex()) {
        if (token_type == OTHER) continue;

        printf("%-10s\t%-20s\t", token_names[token_type], yytext);

        switch (token_type) {
            case REC_NUM:
                printf("%-20d", current_payload.integer_num);
                break;
            case DECIMAL:
                printf("%-20f", current_payload.decimal_num);
                break;
            case PROP_NAME:
            case STRING:
            case DATE:
                printf("%-20s", current_payload.text);
                break;
        }

        putchar('\n');
    }
    return 0;
}