/**
 * ```
 * gcc pthread_mutex.c -lpthread -o pthread_mutex.o
 * ```
*/
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

int variable = 0;

pthread_mutex_t mut = PTHREAD_MUTEX_INITIALIZER;

void *add_variable(void *arg) {
    if (pthread_mutex_lock(&mut) != 0) {
        perror("pthread_mutex_lock"); exit(-1);
    }

    variable++;
    printf("Thread ID: %lu, variable: %d\n", pthread_self(), variable);

    if (pthread_mutex_unlock(&mut) != 0) {
        perror("pthread_mutex_unlock"); exit(-1);
    }

    return NULL;
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