#include <stdlib.h>
#include <stdio.h>
#include <limits.h>
#include "list.utils.h"

void print_list(list *data)
{
    node *curr = data->head;
    if (!curr)
    {
        puts("Empty List.");
        return;
    }

    while (curr)
    {
        printf("%d ", curr->val);
        curr = curr->next;
    }
    puts("");
}

void *malloc_safe(size_t bytes)
{
    void *result;
    if (!(result = malloc(bytes)))
    {
        perror("Memory allocation failed!");
        exit(1);
    }
    return result;
}

list *alloc_list()
{
    list *result = (list *)malloc_safe(sizeof(list));
    result->head = NULL;
    return result;
}

void append_list_no_copy(list *data, LIST_DTYPE value)
{
    if (data->head == NULL)
    {
        data->head = (node *)malloc_safe(sizeof(node));
        data->head->val = value;
        data->head->next = NULL;
        return;
    }

    node *curr = data->head;
    while (curr->next)
    {
        curr = curr->next;
    }

    curr->next = (node *)malloc_safe(sizeof(node));
    curr->next->val = value;
    curr->next->next = NULL;
}

list *append_list(list *src, LIST_DTYPE value)
{
    list *data = copy_list(src);
    append_list_no_copy(data, value);
    return data;
}

list *insert_list(list *src, LIST_DTYPE value, size_t indx)
{
    list *data = copy_list(src);
    // empty list - insert as a first node anyway.
    node *old_head = data->head;
    if (old_head == NULL || indx == 0)
    {
        data->head = (node *)malloc_safe(sizeof(node));
        data->head->val = value;
        data->head->next = old_head;
        return data;
    }

    size_t curr_indx = 0;

    node *curr = data->head;

    while (curr->next)
    {
        print_list(data);

        if (curr_indx == indx)
        {
            node *old_head = curr->next;
            curr->next = (node *)malloc_safe(sizeof(node));
            curr->next->val = value;
            curr->next->next = old_head;
        }
    }

    return data;
}

list *copy_list(list *src)
{
    list *result = alloc_list();

    node *curr = src->head;
    while (curr)
    {
        append_list_no_copy(result, curr->val);

        curr = curr->next;
    }
    return result;
}

list *tail_list(list *data)
{
    list *result = alloc_list();
    if (!data->head)
        return result; // empty if empty

    node *curr = data->head;
    while (curr)
    {
        append_list_no_copy(result, curr->val);
        curr = curr->next;
    }
    return result;
}

list *greater_list(list *data, LIST_DTYPE value)
{
    list *result = alloc_list();
    if (!data->head)
        return result; // empty if empty

    node *curr = data->head;
    while (curr)
    {
        if (curr->val > value)
            append_list_no_copy(result, curr->val);

        curr = curr->next;
    }
    return result;
}

LIST_DTYPE sum_list(list *data)
{
    node *curr = data->head;
    LIST_DTYPE result = 0;
    while (curr)
    {
        result += curr->val;
        curr = curr->next;
    }
    return result;
}

LIST_DTYPE max_list(list *data)
{
    if (!data->head)
    {
        return INT_MIN;
    }

    LIST_DTYPE curr_max = data->head->val;
    node *curr = data->head;
    while (curr)
    {
        curr_max = curr->val <= curr_max ? curr_max : curr->val;
        curr = curr->next;
    }
    return curr_max;
}

LIST_DTYPE min_list(list *data)
{
    if (!data->head)
    {
        return INT_MAX;
    }

    LIST_DTYPE curr_min = data->head->val;
    node *curr = data->head;
    while (curr)
    {
        curr_min = curr->val >= curr_min ? curr_min : curr->val;
        curr = curr->next;
    }
    return curr_min;
}

list *item_list(LIST_DTYPE item_val)
{
    list *to_return = alloc_list();
    append_list_no_copy(to_return, item_val);
    return to_return;
}

void free_list(list *data)
{
    free(data);
}