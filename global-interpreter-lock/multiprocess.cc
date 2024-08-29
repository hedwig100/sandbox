#include <chrono>
#include <iostream>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>

void countdown() {
    int n = 100000000;
    while (n > 0) {
        n--;
    }
    std::cout << "Finishes\n";
}

int main() {
    auto start = std::chrono::high_resolution_clock::now();

    pid_t pid1, pid2;
    int status1, status2;
    if (pid1 = fork() == 0) {
        // First process
        countdown();
        exit(0);
    } else if (pid2 = fork() == 0) {
        // Second process
        countdown();
        exit(0);
    } else {
        // Parent process
        waitpid(pid1, &status1, 0);
        waitpid(pid2, &status2, 0);

        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> elapsed = end - start;
        std::cout << "Time: " 
                << elapsed.count()
                << "sec\n";
    }
}