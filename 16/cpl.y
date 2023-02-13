%code {
    #include <stdio.h>
    extern int yylex(void);
    void yyerror (const char *s) {
        fprintf(stderr, "%s\n", s); 
    }
}

%union {
    float number;
    char *identifier;
    char single_op[1];
    char relop[2];
    char cast_dest[6];
}

/* Reserved words */
%token BREAK CASE DEFAULT ELSE FLOAT IF INPUT INT OUTPUT SWITCH WHILE
/* Operators */
%token RELOP ADDOP MULOP OR AND NOT CAST
/* Other tokens */
%token ID NUM

%%
program:    declarations stmt_block;

declarations:   declarations declaration
                | %empty;

declaration:    idlist ':' type ';';

type:   INT | FLOAT;

idlist: idlist ',' ID
        | ID;

stmt: assignment_stmt
      | input_stmt
      | output_stmt
      | if_stmt
      | while_stmt
      | switch_stmt
      | break_stmt
      | stmt_block;

assignment_stmt:  ID '=' expression ';';

input_stmt:  INPUT '(' ID ')' ';';

output_stmt:  OUTPUT '(' expression ')' ';';

if_stmt:    IF ')' boolexpr '(' stmt ELSE stmt;

while_stmt:  WHILE ')' boolexpr '(' stmt;

switch_stmt:    SWITCH '(' expression ')' '{' caselist
                DEFAULT ':' stmtlist '}';

caselist:   caselist CASE NUM ':' stmtlist
            | %empty;

break_stmt:  BREAK ';';

stmt_block: '{' stmtlist '}';

stmtlist:   stmtlist stmt
            | %empty;

boolexpr:   boolexpr OR boolterm
            | boolterm;

boolterm:   boolterm AND boolfactor
            | boolfactor;

boolfactor: NOT '(' boolexpr ')'
            | expression  RELOP  expression;

expression: expression ADDOP term
            | term;

term:   term MULOP factor
        | factor;

factor: '(' expression ')'
        | CAST '(' expression ')'
        | ID | NUM;
%%
