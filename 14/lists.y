%code {
    #include <stdio.h>
    extern int yylex(void);
    void yyerror (const char *s) {
        fprintf(stderr, "%s\n", s); 
    }
    #define DDD ;puts("DONE");
}

%code requires {
    #include "lists.utils.h"
}

%union {
    LIST_DTYPE item_val;
    list *list_values;
}

/* Reserved words */
%nterm <item_val> s item
%nterm <list_values> l itemlist

%token <item_val> NUMBER
%token TAIL CONS MAX MIN GREATER SUM

%define parse.error verbose

%%

s:    item { if ($1 > 0) printf("%d\n", $1); } ;

l: '[' itemlist ']' { $$ = copy_list($2); } |
    TAIL '(' l ')' { $$ = tail_list($3); } |
    CONS '(' item ',' l ')' { $$ = insert_list($5, $3, 0); } |
    GREATER '(' item ',' l ')' { $$ = greater_list($5, $3); } ;

 /* Please note: I'm assuming the rules are itemlist-->itemlist,item|item!  */
itemlist: itemlist ',' item { $$ = append_list($1, $3); } |
    item { $$ = alloc_list();  append_list($$, $1); };

item: SUM '(' l ')' { $$ = sum_list($3); } |
    MAX '(' l ')' { $$ = max_list($3); } |
    MIN '(' l ')' { $$ = min_list($3); } |
    NUMBER { $$ = yylval.item_val; };

%%


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