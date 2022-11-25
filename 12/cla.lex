%{

#include <stdio.h>
#include <string.h>

// defines of token types
typedef enum token_type {
    // reserved words
    BREAK_T = 1, CASE_T, DEFAULT_T, 
    ELSE_T, FLOAT_T, IF_T, 
    INPUT_T, INT_T, OUTPUT_T, 
    SWITCH_T, WHILE_T,

    // symbol tokens
    RPARENT, // )
    LPARENT, // (
    RCURLY, // }
    LCURLY, // {
    COMMA, // ,
    COLON, // :
    SEMICOLON, // ;
    EQUALS, // =

    // operators
    RELOP, ADDOP, MULOP,
    OR_OP, AND_OP, NOT_OP,
    CAST_OP,

    // num & id
    IDENTIFIER, NUMBER,
    
    ERROR
} token_type;

#define STRING_MAXSZ 500
#define CAST_SZ 6

// column widths
#define TABLE_TOKEN_C_W "10"
#define TABLE_LEXEME_C_W "20"
#define TABLE_ATTRIBUTE_C_W "20"

#define ERR_OUTPUT_FILE stderr

// that's a union which holds the current payload (value) of a token.
union current_attr {
    // holds string value of identifier
    char str_val[STRING_MAXSZ];
    // holds number (float) value
    double number_value;
    // holds static_cast<T>'s T
    char cast_dest[CAST_SZ];
    // holds single-char operator
    char single_op[1];
    // holds double-char comparison operator
    char relop[2];
} current_attr;

/* type names - for the table UI */
static const char *token_names[] = {
    "", "BREAK_T", "CASE_T", "DEFAULT_T",
    "ELSE_T", "FLOAT_T", "IF_T",
    "INPUT_T", "INT_T", "OUTPUT_T",
    "SWITCH_T", "WHILE_T", "RPARENT",
    "LPARENT",  "RCURLY", "LCURLY",
    "COMMA",  "COLON", "SEMICOLON",
    "EQUALS",  "RELOP", "ADDOP",
    "MULOP",  "OR_OP", "AND_OP",
    "NOT_OP",  "CAST_OP", "IDENTIFIER",
    "NUMBER", "ERROR"
};

#define STATIC_FIELD_MEMCPY_ALL(FIELD) memcpy(FIELD, yytext, sizeof(FIELD))

%}

%option noyywrap

/* yylineno WILL hold the current line number globally! */
%option yylineno

%x C_COMMENT

%%

 /* Reserved Words */
break { return BREAK_T; }
case { return CASE_T; }
default { return DEFAULT_T; }
else { return ELSE_T; }
float { return FLOAT_T; }
if { return IF_T; }
input { return INPUT_T; }
int { return INT_T; }
output { return OUTPUT_T; }
switch { return SWITCH_T; }
while { return WHILE_T; }

 /* Symbol Tokens */
\) { return RPARENT; } 
\( { return LPARENT; }
\} { return RCURLY; }
\{ { return LCURLY; }
, { return COMMA; }
: { return COLON; }
; { return SEMICOLON; } 
= { return EQUALS; }

 /* Operators */
(=[!=])|([<>]=?) { 
    current_attr.relop[1] = '\0';
    STATIC_FIELD_MEMCPY_ALL(current_attr.relop);
    return RELOP;
}
[+-] { 
    STATIC_FIELD_MEMCPY_ALL(current_attr.single_op);
    return ADDOP;
}
[*/] { 
    STATIC_FIELD_MEMCPY_ALL(current_attr.single_op);
    return MULOP; 
}
\|\| { return OR_OP; }
&& { return AND_OP; }
! { return NOT_OP; }

 /* This would only copy the dest argument type. */ 
static_cast\<(int|float)\> { 
    int chars_to_copy = strlen(yytext)-13;
    memcpy(current_attr.cast_dest, yytext+12, chars_to_copy);
    current_attr.cast_dest[chars_to_copy] = '\0';
    return CAST_OP;
}

 /* Additionals */
[A-Za-z][A-Za-z0-9]* { 
    // just copy the identifier as is.
    strcpy(current_attr.str_val, yytext);
    return IDENTIFIER;
}

[0-9]+(\.[0-9]*)? { 
    // parse to float and assign.
    current_attr.number_value = atof(yytext);
    return NUMBER;
}

 /* C-Style comments */
"/*"            { BEGIN(C_COMMENT); }
<C_COMMENT>"*/" { BEGIN(INITIAL); }
<C_COMMENT>[\n.]   { }

 /* Skip whitespaces and new lines */
[\r\t\n ] { }

 /* Skip others */
. { return ERROR; }

%%

int main(int argc, char* argv[]) {
    // parse args - open input file and eit if missing or problematic.
    if (argc > 1) {
        if (!(yyin = fopen(argv[1], "r"))) {
            fprintf(ERR_OUTPUT_FILE, "Failed to open file '%s'! Aborting.\n", argv[1]);
            exit(1);
        }
        // add .out to original file name to get output file name:
        int firstarg_len = strlen(argv[1]);
        char *output_file_name = (char *)malloc(firstarg_len + 5);
        strcpy(output_file_name, argv[1]);
        strcpy(output_file_name + firstarg_len, ".out");
        // open output file as stdout.
        if (!(stdout = fopen(output_file_name, "wt"))) {
            fprintf(ERR_OUTPUT_FILE, "Failed to open output file %s! Aborting.\n", output_file_name);
        }
        free(output_file_name);
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
        // error
        if (token_type == ERROR) {
            fprintf(ERR_OUTPUT_FILE, "Unrecognized token '%c' (%d) @ line %d!\n", *yytext, *yytext, yylineno);
            continue;
        }

        printf("%-"TABLE_TOKEN_C_W"s\t%-"TABLE_LEXEME_C_W"s\t", token_names[token_type], yytext);

        switch (token_type) {
            case CAST_OP:
                printf("%s", current_attr.cast_dest);
                break;
            case NUMBER:
                printf("%f", current_attr.number_value);
                break;
            case IDENTIFIER:
                printf("%s", current_attr.str_val);
                break;
            case RELOP:
                printf("%c", current_attr.relop[0]);
                // print 2nd char if not zero
                if (current_attr.relop[1]) printf("%c", current_attr.relop[1]);
                break;
            case ADDOP:
            case MULOP:
                printf("%c", current_attr.relop[0]);
                break;
            default:
                break;
        }

        putchar('\n');
    }

    // final line
    fputs("Aviv Naaman\n", stderr);
    puts("Aviv Naaman");

    // close output file.
    fclose(stdout);

    return 0;
}