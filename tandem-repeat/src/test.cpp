#include "algo.hpp"

int main() {
    RandomGenerator<std::string> rg;
    std::string seq = rg.generate(300);

    auto repeats0 = removeNonMaximal(Naive(seq));
    auto repeats1 = removeNonMaximal(DivideConquer(seq));
    auto repeats2 = removeNonMaximal(DivideConquerFast(seq));

    if (std::equal(repeats0.begin(), repeats0.end(), repeats1.begin(), repeats1.end()) &&
        std::equal(repeats0.begin(), repeats0.end(), repeats2.begin(), repeats2.end()))
        std::cout << "OK\n";
    else {
        std::cout << "NO\n";
        return 1;
    }
    return 0;
}