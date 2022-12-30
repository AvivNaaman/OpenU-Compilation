%{

%}

%option noyywrap

/* yylineno WILL hold the current line number globally! */
%option yylineno

%%



 /* Skip whitespaces and new lines */
[\r\t\n ] { }

 /* Skip others */
. { return ERROR; }

%%
