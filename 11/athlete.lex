%{

#include <stdio.h>
#include <string.h>

// defines of token types
#define REC_NUM 1
#define PROP_NAME 2
#define DECIMAL 3
#define STRING 4
#define DATE 5
#define IGNORE 6
#define ERROR 7

#define STRING_MAXLENGTH 500

// column widths
#define TABLE_TOKEN_C_W "10"
#define TABLE_LEXEME_C_W "20"
#define TABLE_ATTRIBUTE_C_W "20"

#define ERR_OUTPUT_FILE stdout

// that's a union which holds the current payload (value) of a token.
union current_payload {
    char str_val[STRING_MAXLENGTH];
    int integer_num;
    double decimal_num;
} current_payload;

/* type names - for the table UI */
static const char *token_names[] = {
    "END", "RECORD_NUMBER", "PROP_NAME",
    "DECIMAL",  "STRING", "DATE"
};

// Removes the first & last chars of yytext, and puts it into current_payload.str_val.
void copy_parse_string2() {
    int prop_name_len = strlen(yytext) - 2;
    strcpy(current_payload.str_val, yytext+1);
    *(current_payload.str_val + prop_name_len) = '\0';
}

%}
%option noyywrap
%option yylineno
%%

 /* record indices - [NUM] */
\[[1-9][0-9]*\] { 
    copy_parse_string2();
    current_payload.integer_num = atoi(current_payload.str_val);
    return REC_NUM;
}

 /* property definition - <propertyname> */
\<[a-z]+\> { 
    // remove < and >
    copy_parse_string2();
    return PROP_NAME;
}

 /*  decimal numbers - such as 13902.53290, .9503, 1290.21 */
[0-9]?"."[0-9]+ { 
    current_payload.decimal_num = atof(yytext);
    return DECIMAL;
}

 /* just text - "gdsakjfslkd" */
\"(\\.|[^"\\])*\" { 
    // remove " at beginning & at end.
    copy_parse_string2();
    return STRING;
}

 /* date - D/DD MONTH YYYY */
(([1-3][0-9])|[1-9])" "(January|February|March|April|May|June|July|August|September|October|November|December)" "[0-9]{4} {
    strcpy(current_payload.str_val, yytext); 
    return DATE;
}

 /* Skip whitespaces and new lines */
[\r\t\n ] { return IGNORE; }

 /* Skip others */
. { return ERROR; }

%%

int main(int argc, char* argv[]) {
    // parse args - open input file and eit if missing or problematic.
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
        if (!yyin) {
            fprintf(ERR_OUTPUT_FILE, "Failed to open file '%s'! Aborting.\n", argv[1]);
            exit(1);
        }
    }
    else {
        fprintf(ERR_OUTPUT_FILE, "Missing file argument! Usage: %s filename\n", argv[0]);
        exit(1);
    }
    
    // Table Header
    printf("%-"TABLE_TOKEN_C_W"s\t%-"TABLE_LEXEME_C_W"s\t%-"TABLE_ATTRIBUTE_C_W"s\n", "TOKEN", "LEXEME", "ATTRIBUTE");

    // Tokenize & print
    int token_type = 0;
    while (token_type = yylex()) {
        // whitespace, etc.
        if (token_type == IGNORE) continue;
        // error
        if (token_type == ERROR) {
            fprintf(ERR_OUTPUT_FILE, "Unrecognized token '%c' (%d) @ line %d!\n", *yytext, *yytext, yylineno);
            continue;
        }

        printf("%-"TABLE_TOKEN_C_W"s\t%-"TABLE_LEXEME_C_W"s\t", token_names[token_type], yytext);

        switch (token_type) {
            case REC_NUM:
                printf("%-"TABLE_ATTRIBUTE_C_W"d", current_payload.integer_num);
                break;
            case DECIMAL:
                printf("%-"TABLE_ATTRIBUTE_C_W"f", current_payload.decimal_num);
                break;
            case PROP_NAME:
            case STRING:
            case DATE:
                printf("%-"TABLE_ATTRIBUTE_C_W"s", current_payload.str_val);
                break;
        }

        putchar('\n');
    }
    return 0;
}