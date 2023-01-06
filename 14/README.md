### How to build

* Option 1: GNU Make

    Just Run: `make` in the current directory. You'll get the `list` executable.
    _Note:_ You can run `make clean` to remove unused files.

* Option 2: Manual compilation
    1. lexer: `flex -o list.yy.c list.lex`
    1. parser: `bison --header list.y`
    2. final program: `gcc -o list -g list.utils.c list.yy.c list.tab.c`

### Memory Leak Test
The program uses a custom library to manage lists. 
Therefore, a memory leak test is crucial to make sure it's running  well.
You may run a memory leak test using the script `./memleak.sh`,
or customize the `valgrind` arguments to match your need.
Note - a valgrind log from assignment's final version is attached.
all the leaks are sourced from the `yy*()` functions - it has nothing to do with our lists library.
Therefore, no further effort was done for cleaning it up specifically.