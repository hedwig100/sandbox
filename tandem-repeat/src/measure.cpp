#include "algo.hpp"

double Measure(std::function<void(std::string)> f, const std::string &seq) {
    clock_t start, end;
    start = clock();
    f(seq);
    end = clock();
    return (end - start) / CLOCKS_PER_SEC;
}

int main() {
    RandomGenerator<std::string> rg;
    std::string seq = rg.generate(3000);

    auto t0 = Measure([](std::string s) { removeNonMaximal(Naive(s)); }, seq);
    auto t1 = Measure([](std::string s) { removeNonMaximal(DivideConquer(s)); }, seq);
    auto t2 = Measure([](std::string s) { removeNonMaximal(DivideConquerFast(s)); }, seq);

    std::cout << "Naive:" << t0 << "s, DivideConquer: " << t1 << "s, DivideConquerFast: " << t2 << "s \n";

    return 0;
}