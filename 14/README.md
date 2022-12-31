### How to build

* Option 1: GNU Make

    Just Run: `make` in the current directory. It'll compile each *.lex to the * as an executable.
    _Note:_ You can run `make clean` to remove unused files.
* Option 2: Manual compilation
    1. lexer: `flex -o list.yy.c list.lex`
    1. parser: `bison --header list.y`
    2. final program: `gcc -o list -g list.utils.c list.yy.c list.tab.c`


You'l find the executables in the current directory, with the respecitve name.