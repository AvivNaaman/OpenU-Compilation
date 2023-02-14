#include "defs.h"
#include "hash_table.h"

typedef struct quad_codeline {
    quad_instructions instruction;
    int arg1;
    int arg2;
    int arg3;
} quad_codeline;

typedef struct quad_code {
    quad_codeline *code;
    int size;
    int capacity;
    int temp_counter;
    ht *symbols;
} quad_code;