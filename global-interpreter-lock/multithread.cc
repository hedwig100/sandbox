#include <thread>
#include <chrono>
#include <iostream>

void countdown() {
    int n = 100000000;
    while (n > 0) {
        n--;
    }
    std::cout << "Finishes\n";
}

int main() {
    auto start = std::chrono::high_resolution_clock::now();

    std::thread t1(countdown);
    std::thread t2(countdown);
    t1.join();
    t2.join();

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    std::cout << "Time: " 
              << elapsed.count()
              << "sec\n";
}