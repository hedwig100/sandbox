/**
 * ```
 * gcc sync.c -lpthread -o sync.o
 * ```
*/
#include <stdint.h>
#include <stdbool.h>
#include <pthread.h>
#include <stdio.h>

// If *p is val, set p as newval and return true. Otherwise, return false.
bool compare_and_swap(uint64_t *p, uint64_t val, uint64_t newval) {
    return __sync_bool_compare_and_swap(p, val, newval);
}

// If *p is true, return true. Otherwise, return false and set p as true.
bool test_and_set(volatile bool *p) {
    return __sync_lock_test_and_set(p, 1);
}

// Set *p as false.
void tas_release(volatile bool *p) {
    return __sync_lock_release(p);
}

// Spinlock functions are used like
// ```
// bool lock = false;
//
// void some_func() {
//     spinlock_acquire(&lock);
//     // critical section
//     spinlock_release(&lock);
// }
// ```
void spinlock_acquire(volatile bool *lock) {
    for (;;) {
        while (*lock);
        if (!test_and_set(lock))
            break;
    }
}

void spinlock_release(bool *lock) {
    tas_release(lock);
}


int variable = 0;
bool lock = false;

void *add_variable(void *arg) {
    spinlock_acquire(&lock);
    variable++;
    printf("Thread Id: %lu, Variable: %d\n", pthread_self(), variable);
    spinlock_release(&lock);
}

int main() {
    const int kNumThreads = 10;
    pthread_t threads[kNumThreads];

    for (int t = 0;t < kNumThreads; t++) {
        if (pthread_create(&threads[t], NULL, add_variable, NULL) != 0) {
            perror("thread create failed"); return -1;
        }
    }

    for (int t = 0;t < kNumThreads; t++) {
        if (pthread_join(threads[t], NULL) != 0) {
            perror("thread join failed"); return -1;
        }
    }

    printf("Last Variable: %d\n", variable);
    return 0;
}

