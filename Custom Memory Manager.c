#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define HEAP_SIZE 1024 * 1024   // 1 MB heap

typedef struct block {
    size_t size;
    int free;
    struct block *next;
} block_t;

static char heap[HEAP_SIZE];
static block_t *free_list = NULL;

/* Initialize heap */
void init_heap() {
    free_list = (block_t *)heap;
    free_list->size = HEAP_SIZE - sizeof(block_t);
    free_list->free = 1;
    free_list->next = NULL;
}

/* Split block */
void split_block(block_t *block, size_t size) {
    block_t *new_block = (block_t *)((char *)block + sizeof(block_t) + size);
    new_block->size = block->size - size - sizeof(block_t);
    new_block->free = 1;
    new_block->next = block->next;

    block->size = size;
    block->next = new_block;
}

/* First Fit allocation */
block_t *first_fit(size_t size) {
    block_t *curr = free_list;
    while (curr) {
        if (curr->free && curr->size >= size)
            return curr;
        curr = curr->next;
    }
    return NULL;
}

/* Best Fit allocation */
block_t *best_fit(size_t size) {
    block_t *curr = free_list;
    block_t *best = NULL;

    while (curr) {
        if (curr->free && curr->size >= size) {
            if (!best || curr->size < best->size)
                best = curr;
        }
        curr = curr->next;
    }
    return best;
}

/* Custom malloc */
void *my_malloc(size_t size, int use_best_fit) {
    block_t *block;

    if (!free_list)
        init_heap();

    block = use_best_fit ? best_fit(size) : first_fit(size);

    if (!block) {
        printf("Memory allocation failed\n");
        return NULL;
    }

    if (block->size > size + sizeof(block_t))
        split_block(block, size);

    block->free = 0;
    return (char *)block + sizeof(block_t);
}

/* Merge free blocks */
void coalesce() {
    block_t *curr = free_list;
    while (curr && curr->next) {
        if (curr->free && curr->next->free) {
            curr->size += sizeof(block_t) + curr->next->size;
            curr->next = curr->next->next;
        } else {
            curr = curr->next;
        }
    }
}

/* Custom free */
void my_free(void *ptr) {
    if (!ptr)
        return;

    block_t *block = (block_t *)((char *)ptr - sizeof(block_t));
    block->free = 1;
    coalesce();
}

/* Heap dump (debugging) */
void heap_dump() {
    block_t *curr = free_list;
    printf("\nHeap Status:\n");
    while (curr) {
        printf("Block size: %zu | %s\n",
               curr->size,
               curr->free ? "FREE" : "ALLOCATED");
        curr = curr->next;
    }
}

/* Memory leak detector */
void detect_leaks() {
    block_t *curr = free_list;
    int leaks = 0;

    while (curr) {
        if (!curr->free) {
            printf("Memory leak detected: %zu bytes\n", curr->size);
            leaks++;
        }
        curr = curr->next;
    }

    if (!leaks)
        printf("No memory leaks detected 🎉\n");
}

/* Test program */
int main() {
    void *a, *b, *c;

    a = my_malloc(200, 0);  // First fit
    b = my_malloc(300, 1);  // Best fit
    c = my_malloc(100, 0);

    heap_dump();

    my_free(b);
    my_free(a);

    heap_dump();

    // c is intentionally not freed (leak)
    detect_leaks();

    return 0;
}
