%{
%}

/* Reserved words */
%token tail cons greater sum max number

%%
s:    item;

l: '[' itemlist ']' |
    tail '(' l ')' |
    cons '(' item ',' l ')' |
    greater '(' item ',' l ')';

itemlist: itemlist item |
    %empty;

item: sum '(' l ')' |
    max '(' l ')' |
    number;

%%


int main() {
    printf("Hello, World!");
}