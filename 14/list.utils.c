#include <stdlib.h>
#include <stdio.h>
#include <limits.h>
#include "list.utils.h"

void *malloc_safe(size_t bytes) {
    void *result;
    if (!(result = malloc(bytes))) {
        perror("Memory allocation failed!");
        exit(1);
    }
    return result;
}

void append_list(list *data, LIST_DTYPE value) {
    if (data->head == NULL) {
       data->head = (node*)malloc_safe(sizeof(node));
       data->head->val = value;
       data->head->next = NULL;
       return;
    }

    node *curr = data->head;
    while (curr->next) {
        curr = curr->next;
    }

    curr->next = (node*)malloc_safe(sizeof(node));
    curr->next->val = value;
    curr->next->next = NULL;
}

void insert_list(list *data, LIST_DTYPE value, size_t indx) {
    if (data->head == NULL) {
       data->head = (node*)malloc_safe(sizeof(node));
       data->head->val = value;
       data->head->next = NULL;
       return;
    }

    size_t curr_indx = 0;

    node *curr = data->head;
    while (curr->next) {
        if (curr_indx == indx) {
            node *old_next = curr->next;
            curr->next = (node*)malloc_safe(sizeof(node));
            curr->next->val = value;
            curr->next->next = old_next;
        }
        curr = curr->next;
        curr_indx += 1;
    }

}

list *alloc_list() {
    list *result = (list*)malloc_safe(sizeof(list));
    result->head = NULL;
    return result;
}

list *tail_list(list *data) {
    list *result = alloc_list();
    if (!data->head) return result; // empty if empty

    node *curr = data->head->next;
    while (curr) {
        append_list(result, curr->val);
        curr = curr->next;
    }
    return result;
}

list *greater_list(list *data, LIST_DTYPE value) {
    list *result = alloc_list();
    if (!data->head) return result; // empty if empty

    node *curr = data->head->next;
    while (curr) {
        if (curr->val > value)
            append_list(result, curr->val);

        curr = curr->next;
    }
    return result;
}

LIST_DTYPE sum_list(list *data) {
    node *curr = data->head->next;
    LIST_DTYPE result = 0;
    while (curr) {
        result += curr->val;
        curr = curr->next;
    }
    return result;
}

LIST_DTYPE max_list(list *data) {
    node *curr = data->head->next;
    LIST_DTYPE result = 0;
    LIST_DTYPE curr_max = INT_MIN;
    while (curr) {
        curr_max = result <= curr_max ? curr_max : result;
        curr = curr->next;
    }
    return result;
}

void free_list(list *data) {
    free(data);
}