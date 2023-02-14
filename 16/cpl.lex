%{
#include "cpl.tab.h"
#define STATIC_FIELD_MEMCPY_ALL(FIELD) memcpy(FIELD, yytext, sizeof(FIELD))
%}

%option noyywrap
%option yylineno

%option noyywrap

/* yylineno WILL hold the current line number globally! */
%option yylineno

%x C_COMMENT

%%

 /* Reserved Words */
break { return BREAK; }
case { return CASE; }
default { return DEFAULT; }
else { return ELSE; }
float { return FLOAT; }
if { return IF; }
input { yylval.dtype = CPL_DTYPE_FLOAT; return INPUT; }
int { yylval.dtype = CPL_DTYPE_INT; return INT; }
output { return OUTPUT; }
switch { return SWITCH; }
while { return WHILE; }

 /* Symbol Tokens */
\) { return ')'; } 
\( { return '('; }
\} { return '}'; }
\{ { return '{'; }
, { return ','; }
: { return ':'; }
; { return ';'; } 
= { return '='; }

 /* Operators */
(=[!=])|([<>]=?) { 
    yylval.relop[1] = '\0';
    STATIC_FIELD_MEMCPY_ALL(yylval.relop);
    return RELOP;
}
[+-] { 
    STATIC_FIELD_MEMCPY_ALL(yylval.single_op);
    return ADDOP;
}
[*/] { 
    STATIC_FIELD_MEMCPY_ALL(yylval.single_op);
    return MULOP; 
}
\|\| { return OR; }
&& { return AND; }
! { return NOT; }

 /* This would only copy the dest argument type. */ 
static_cast\<(int|float)\> { 
    yylval.cast_dest[chars_to_copy] = yytext[12] == "i" ? CPL_DTYPE_INT : CPL_DTYPE_FLOAT;
    return CAST;
}

 /* Additionals */
[A-Za-z][A-Za-z0-9]* { 
    // just copy the identifier as is.
    yylval.identifier = malloc(strlen(yytext)+1);
    strcpy(yylval.identifier, yytext);
    return ID;
}

[0-9]+(\.[0-9]*)? { 
    // parse to float and assign.
    yylval.number = atof(yytext);
    return NUM;
}

 /* C-Style comments, will be ignored completly. */
"/*"            { BEGIN(C_COMMENT); }
<C_COMMENT>"*/" { BEGIN(INITIAL); }
<C_COMMENT>[\n.]   { }

 /* Skip whitespaces and new lines */
[\r\t\n ] { }

 /* Skip others */
. { fprintf(stderr, "Unexpected token %d:%s", yylineno, yytext); }

%%