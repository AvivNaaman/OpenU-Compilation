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

/// @brief a node is also a list.
typedef struct list { node *head; } list;

void append_list(list *data, LIST_DTYPE value);

void insert_list(list *data, LIST_DTYPE value, size_t indx);

list *alloc_list();

list *tail_list(list *data);

list *greater_list(list *data, LIST_DTYPE value);

LIST_DTYPE sum_list(list *data);

LIST_DTYPE max_list(list *data);

void free_list(list *data);