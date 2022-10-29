### How to build

* Option 1: GNU Make

    Just Run: `make` in the current directory. It'll compile each *.lex to the * as an executable.
    _Note:_ You can run `make clean` to remove unused files.
* Option 2: Manual compilation

    For each lex file (e.g. q1.lex), you have to compile in 2 stages:

    1. execute: `flex q1.lex`
    2. execute: `gcc -o q1 lex.yy.c`


You'l find the executables in the current directory, with the respecitve name.