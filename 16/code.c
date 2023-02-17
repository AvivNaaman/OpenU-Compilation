#include "code.h"
#include <stdio.h>

int gen_3arg(quad_code *table, quad_instructions instruction, int arg1, int arg2, int arg3) {
    if (table->size == table->capacity) {
        table->capacity *= 2;
        table->code = realloc(table->code, table->capacity * sizeof(quad_codeline));
    }
    table->code[table->size].instruction = instruction;
    table->code[table->size].arg1 = arg1;
    table->code[table->size].arg2 = arg2;
    table->code[table->size].arg3 = arg3;
    table->size++;
    return arg1;
}

int gen_2arg(quad_code *table, quad_instructions instruction, int arg1, int arg2) {
    gen_3arg(table, instruction, arg1, arg2, 0);
    return arg1;
}

void gen_1arg(quad_code *table, quad_instructions instruction, int arg1) {
    gen_3arg(table, instruction, arg1, 0, 0);
}

void gen_noarg(quad_code *table, quad_instructions instruction) {
    gen_3arg(table, instruction, 0, 0, 0);
}

void write_code(quad_code *table, FILE *out) {
    for (int i = 0; i < table->size; i++) {
        quad_codeline line = table->code[i];
        fprintf(out, "%d %d %d %d");
    }
}

quad_code *new_code() {
    quad_code *table = malloc(sizeof(quad_code));
    table->code = malloc(100 * sizeof(quad_codeline));
    table->size = 0;
    table->capacity = 100;
    table->temp_counter = 0;
    table->symbols = ht_create();
    return table;
}

int newtemp(quad_code *table) {
    table->temp_counter++;
    return table->temp_counter;
}