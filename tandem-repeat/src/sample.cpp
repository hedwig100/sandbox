#include "algo.hpp"

int main() {
    std::cout << "Input String:\n";
    std::string seq;
    std::cin >> seq;

    std::cout << "Naive:\n";
    auto repeats = removeNonMaximal(Naive(seq));
    for (const auto &rep : repeats)
        std::cout << rep << '\n';

    std::cout << "DivideConquer:\n";
    repeats = removeNonMaximal(DivideConquer(seq));
    for (const auto &rep : repeats)
        std::cout << rep << '\n';

    std::cout << "DivideConquerFast:\n";
    repeats = removeNonMaximal(DivideConquerFast(seq));
    for (const auto &rep : repeats)
        std::cout << rep << '\n';
    return 0;
}