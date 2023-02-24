%code {
    #include <stdio.h>
    #include "ht.utils.h"
    #include "list.utils.h"
    #include "code.h"
    extern int yylex(void);
    void yyerror (const char *s) {
        fprintf(stderr, "%s\n", s); 
    }
    quad_code *code = new_code();
    ht *symbols = ht_alloc();
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
        union {
            int target;
        } payload;
        int begin_addr;
        int end_addr;
        int breakcount;
        bool in_while_or_switch;
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
program:  declarations stmt_block;

declarations:   declarations declaration
                | %empty;

declaration:    idlist ':' type ';' { 
    // add all the identifiers in the idlist to the symbol table
    for (node *head = $1->head; head != NULL; head = head->next) {
        // TODO: prevent aliasing!!! copy the type!!!
        if (!ht_get(symbols, head->val)) {
            // TODO: Better error message?
            fprintf(stderr, "Error: redeclaration of variable %s\n", head->val);
            continue;
        }
        ht_set(symbols, head->val, $3);
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

assignment_stmt:  ID '=' expression ';' {
    // TODO: Support float. Check typing.
    gen_2arg(code, IASN, $1, $3.target);
};

input_stmt:  INPUT '(' ID ')' ';'{
    // TODO: Support float. Check typing.
    gen_1arg(code, IINP, $3);
};

output_stmt:  OUTPUT '(' expression ')' ';' {
    // TODO: Support float. Check typing.
    gen_1arg(code, IPRT, $3.target);
};

// TODO: Backpatching for all control flow statements.
if_stmt:    IF '(' boolexpr ')' {
    gen_2arg(code, JMPZ, $3.target, 0); // that will get backpatched later.
} stmt {
    gen_1arg(code, JMP, 0);
    // backpatch the JMPZ instruction to point here.
    backpatch(code, 1, next_addr(code));
} ELSE stmt {
    // backpatch the JMP instruction to point next
    backpatch(code, 1, next_addr(code));
};

while_stmt:  WHILE '(' boolexpr ')' {
    $$.begin_addr = next_addr(code); // TODO: Implement this
    gen_2arg(code, JMPZ, $3.target, 0); // that will get backpatched later.
}
 stmt {
    gen_1arg(code, JMP, $$.begin_addr); 
    backpatch(code, $$.begin_addr, next_addr(code));
 };

 /* To allow usage of break; we'd have to store a counter of these to backpatch later */
switch_stmt:    SWITCH '(' expression ')' '{' caselist DEFAULT ':' stmtlist '}';

caselist:  caselist  CASE NUM ':' stmtlist 
            | %empty;

break_stmt:  BREAK ';';

stmt_block: {  } '{' stmtlist '}' { };

stmtlist:   { } 
                stmtlist stmt 
            | %empty { };

    /* enforcing boolfactor and boolterm having only values in {0, 1},
     a AND b can be translated to (a+b) == 2.
     a OR b can be translated to (a+b) > 0. */

boolexpr:   boolexpr OR boolterm { 
                int temp_target = newtemp();
                gen_3arg(temp_target, IADD, $$.target, $1.target, $3.target);
                $$.target = newtemp();
                gen_3arg(code, IGRT, $$.target, temp_target, 0);
 }
            | boolterm { $$.payload.target = $1.payload.target;  };

boolterm:   boolterm AND boolfactor {
    int temp_target = newtemp();
    gen_3arg(temp_target, IADD, $$.target, $1.target, $3.target);
    $$.target = newtemp();
    gen_3arg(code, IEQL, $$.target, temp_target, 2);
}
            | boolfactor { $$.payload.target = $1.payload.target; };

boolfactor: NOT '(' boolexpr ')' {
                $$.target = newtemp();
                gen_3arg(code, IEQL, $$.target, 0, $3.target);
            }
            | expression  RELOP  expression {
                $$.target = newtemp();
                // = != > < are all supported as is in quad.
                // >= is like <, but after flipping the targets. Same for <=.
                quad_instruction inst = IEQL if $2 == '==' else
                                        INQL if $2 == '!=' else
                                        ILSS if ($2 == '<' || $2 == ">=") else IGRT;
                int flip_targets = $2 == ">=" || $2 == "<=";
                int arg2 = flip_targets ? $1.target : $3.target;
                int arg3 = flip_targets ? $3.target : $1.target;
                gen_3arg(code, inst, $$.target, arg2, arg3);
            };

expression: expression ADDOP term {
                $$.target = newtemp();
                quad_instruction inst = ADD if $2 == '+' else SUB;
                gen_3arg(code, inst, $$.target, $1.target, $3.target);
            }   
            | term { $$.payload.target = $1.payload.target; };

term:   term MULOP factor {
            $$.target = newtemp();
            quad_instruction inst = MUL if $2 == '*' else DIV;
            gen_3arg(code, inst, $$.target, $1.target, $3.target);
        }
        | factor { $$.payload.target = $1.payload.target; }  ;

/* Print as is? */
factor: '(' expression ')' { $$.dtype = $2.dtype; }
        | CAST '(' expression ')' { $$.dtype = $1; }
        | ID  { ht_get(code, $1); /* TODO: Lookup for the value in table for real. Set dtype. print. */ }
        | NUM { $$.dtype = $1; /* TODO: Check if number has decimal point.*/ };
%%
