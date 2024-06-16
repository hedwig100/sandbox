#include "add.h"
#include <iostream>

int main() {
    std::cout << "Input two numbers: ";
    int a, b;
    std::cin >> a >> b;
    std::cout << "The sum is: " << arithmetic::add(a, b) << std::endl;
    return 0;
}