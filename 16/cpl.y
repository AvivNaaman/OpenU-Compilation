%code {
    #include <stdio.h>
    #include "ht.utils.h"
    #include "list.utils.h"
    extern int yylex(void);
    void yyerror (const char *s) {
        fprintf(stderr, "%s\n", s); 
    }
}

%union {
    // for terminals
    float number;
    char *identifier;
    cpl_dtype dtype;
    char single_op[1];
    char relop[2];
    cpl_dtype cast_dest;
    // for non-terminals
    struct {
        int length;
        union {
            int target_variable;
        } payload;
        *quad_code code;
    } var_value;
    list *idlist_vals;
}

/* Reserved words */
%token BREAK CASE DEFAULT ELSE IF INPUT OUTPUT SWITCH WHILE
/* Operators */
%token <relop> RELOP
%token <single_op> ADDOP MULOP
%token OR AND NOT
%token <cast_dest> CAST
/* Other tokens */
%token <identifier> ID
%token <number> NUM
%token <dtype> INT FLOAT

%nterm <var_value> program declarations declaration stmt assignment_stmt input_stmt output_stmt if_stmt while_stmt switch_stmt caselist break_stmt stmt_block stmtlist boolexpr boolterm boolfactor expression term factor
%nterm <dtype> type
%nterm <idlist_vals> idlist

%define parse.error verbose

%%
program:    declarations stmt_block;

declarations:   declarations declaration
                | %empty;

declaration:    idlist ':' type ';' { 
    // add all the identifiers in the idlist to the symbol table
    for (node *head = $1->head; head != NULL; head = head->next) {
        // TODO: prevent aliasing!!! copy the type!!!
        if (!ht_get($$.symbols, head->val)) {
            // TODO: Better error message?
            fprintf(stderr, "Error: redeclaration of variable %s\n", head->val);
            continue;
        }
        ht_set($$.symbols, head->val, $3);
    }
    // list is no longer needed.
    free_list($1);
};

type:   INT | FLOAT { $$ = $1; };

idlist: idlist ',' ID { append_list_no_copy($1, $3); }
        | ID { $$ = alloc_list(); append_list_no_copy($$, $1); };

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

if_stmt:    IF '(' boolexpr ')' stmt ELSE stmt;

while_stmt:  WHILE '(' boolexpr ')' stmt;

switch_stmt:    SWITCH '(' expression ')' '{' caselist
                DEFAULT ':' stmtlist '}';

caselist:   caselist CASE NUM ':' stmtlist
            | %empty;

break_stmt:  BREAK ';';

stmt_block: { $2.code = $$.code; } '{' stmtlist '}' { $$.length = $2.length; };

stmtlist:   { $1.code = $$.code; $2 = $$.code; } 
                stmtlist stmt 
                { $$.length = $1.length + $2.length; }
            | %empty { $$.length = 0; };

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

/* Print as is? */
factor: '(' expression ')' { $$.dtype = $2.dtype; }
        | CAST '(' expression ')' { $$.dtype = $1; }
        | ID  { ht_get($$.code, $1); /* TODO: Lookup for the value in table for real. Set dtype. print. */ }
        | NUM { $$.dtype = $1; /* TODO: Check if number has decimal point.*/ };
%%
