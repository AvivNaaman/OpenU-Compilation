%{
#include "list.tab.h"
%}

%option noyywrap
%option yylineno

%%

[0-9]+ { yylval.item_val = atoi(yytext); return NUMBER; }   

TAIL { return TAIL; }
CONS { return CONS; }
GREATER { return GREATER; }
MAX { return MAX; }
MIN { return MIN; }
SUM { return SUM; }

\, { return ','; }
\[ { return '['; }
\] { return ']'; }

\( { return '('; }
\) { return ')'; }

 /* Skip whitespaces and new lines */
[\r\t\n ] { }

 /* Skip others */
. { fprintf(stderr, "Unexpected token `%s`", yytext); }

%%
