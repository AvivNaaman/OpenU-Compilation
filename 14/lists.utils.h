/*
This file contains utilities for manging lists.
Every ptr of list is a deep copy of the previous one.
*/

#include <stdlib.h>
#include <stdio.h>
#include <limits.h>

#define LIST_DTYPE int

/// @brief Represents a single node in a list.
typedef struct node {
    LIST_DTYPE val;
    struct node *next;
} node;

/// @brief Represents a list of items of LIST_DTYPE.
typedef struct list { node *head; } list;

list *alloc_list();

void print_list(list *data);

list *append_list(list *data, LIST_DTYPE value);

list *insert_list(list *data, LIST_DTYPE value, size_t indx);

list *copy_list(list *data);

list *tail_list(list *data);

list *greater_list(list *data, LIST_DTYPE value);

LIST_DTYPE sum_list(list *data);

LIST_DTYPE max_list(list *data);

LIST_DTYPE min_list(list *data);

list *item_list(LIST_DTYPE item_val);

void free_list(list *data);