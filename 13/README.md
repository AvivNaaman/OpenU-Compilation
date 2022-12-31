### How to build

* Option 1: GNU Make

    Just Run: `make` in the current directory. It'll compile each *.lex to the * as an executable.
    _Note:_ You can run `make clean` to remove unused files.
* Option 2: Manual compilation

    For each lex file (e.g. q1.lex), you have to compile in 2 stages:

    1. execute: `bison --file-prefix="cpl" -v cpl.y`


You'l find the *.output file and *.tab.c files in the current directory.

#### Note: This is a partial exercise, and it wasn't commited.
I didn't have enough time, effort and need to solve all the questions, so I decided to give up on that one.