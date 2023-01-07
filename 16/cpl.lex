%{
#include "list.tab.h"
%}

%option noyywrap
%option yylineno

%{
#include "cpl.tab.h"
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
input { return INPUT; }
int { return INT; }
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
\|\| { return OR; }
&& { return AND; }
! { return NOT; }

 /* This would only copy the dest argument type. */ 
static_cast\<(int|float)\> { 
    int chars_to_copy = strlen(yytext)-13;
    memcpy(current_attr.cast_dest, yytext+12, chars_to_copy);
    current_attr.cast_dest[chars_to_copy] = '\0';
    return CAST;
}

 /* Additionals */
[A-Za-z][A-Za-z0-9]* { 
    // just copy the identifier as is.
    strcpy(current_attr.str_val, yytext);
    return ID;
}

[0-9]+(\.[0-9]*)? { 
    // parse to float and assign.
    current_attr.number_value = atof(yytext);
    return NUM;
}

 /* C-Style comments, will be ignored completly. */
"/*"            { BEGIN(C_COMMENT); return COMMENT; }
<C_COMMENT>"*/" { BEGIN(INITIAL); return COMMENT; }
<C_COMMENT>[\n.]   { return COMMENT; }

 /* Skip whitespaces and new lines */
[\r\t\n ] { }

 /* Skip others */
. { return ERROR; }

%%