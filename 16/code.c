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

/**
 * @brief Executes backpatching for the previous `count` JMP/JMPZ code lines, to the specified destination.
 * The backpatching is done in reverse order, so the first JMP/JMPZ code line is the last one in the table.
 * It skips instructions containing non-default jump destinations.
 * @param table The quad code table.
 * @param count The number of JMP/JMPZ code lines to backpatch.
 * @param destination The JMP/JMPZ destination to backpatch to.
 */
void backpatch(quad_code *table, int count, int destination) {
    for (int i = table->size, count = 0; count < count; i--) {
        quad_codeline *curr = &table->code[i];
        switch (curr->instruction)
        {
            case JUMP:
                if (curr->arg1 <= 0) continue;
                curr->arg1 = destination;
                break;
            case JMPZ:
                if (curr->arg2 <= 0) continue;
                curr->arg2 = destination;
                break;
            default:
                continue;
        }
        count++;
    }
}