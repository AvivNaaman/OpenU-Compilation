/**
 * @file list.utils.h
 * @brief Contains header function definitions for list management.
 * @author Aviv Naaman
 * @date December 2022
*/

#include <stdlib.h>
#include <stdio.h>
#include <limits.h>

#define LIST_DTYPE int

/// @brief Represents a single node in a list.
typedef struct node {
    /// @brief The value of the current node.
    LIST_DTYPE val;
    /// @brief The next linked node in the list.
    struct node *next;
} node;

/// @brief Represents a list of items of LIST_DTYPE.
typedef struct list { node *head; } list;

/**
 * @brief Allocates a new, empty list.
 * 
 * @return list* The result list.
 */
list *alloc_list();

/**
 * @brief Prints a list nicely.
 * 
 * @param data The list to print.
 */
void print_list(list *data);

/**
 * @brief Appends to a list at it's end, and returns a deep copy of it's modified version
 * 
 * @param data The input source list (will be unchanged)
 * @param value The value to append
 * @return list* The new list
 */
list *append_list(list *data, LIST_DTYPE value);

/**
 * @brief Inserts to a list in a specific index, and returns a deep copy of the modified list.
 * 
 * @param data The input source list (will be unchanged)
 * @param value The value to insert
 * @param indx The insertion index.
 * @return list* The result list.
 */
list *insert_list(list *data, LIST_DTYPE value, size_t indx);

/**
 * @brief Makes a deep copy of a list.
 * 
 * @param data The list to copy
 * @return list* The result list.
 */
list *copy_list(list *data);

/**
 * @brief Returns a list with all the items, excluding the first one, 
 * 
 * @param data The source input list
 * @return list* The result list.
 */
list *tail_list(list *data);

/**
 * @brief Returns a new list, preserving only the items which have a value greater than the given value parameter.
 * 
 * @param data The source list (remains unchanged)
 * @param value The value to filter by
 * @return list* The filtered list.
 */
list *greater_list(list *data, LIST_DTYPE value);

/**
 * @brief Sums all the items in a list.
 * 
 * @param data The source list.
 * @return LIST_DTYPE The sum of all the lists' items
 */
LIST_DTYPE sum_list(list *data);

/**
 * @brief Finds the maximum value in a given list
 * 
 * @param data The source list
 * @return LIST_DTYPE the required maximum.
 */
LIST_DTYPE max_list(list *data);

/**
 * @brief Finds the minimum value in a given list
 * 
 * @param data The source list
 * @return LIST_DTYPE the required minimum.
 */
LIST_DTYPE min_list(list *data);

/**
 * @brief Creates a new list out of it's single item value.
 * 
 * @param item_val The item of the list
 * @return list* The result list.
 */
list *item_list(LIST_DTYPE item_val);

/**
 * @brief Frees the memory of an allocated list.
 * 
 * @param data The list to free
 */
void free_list(list *data);