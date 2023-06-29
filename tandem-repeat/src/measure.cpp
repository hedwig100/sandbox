#include "algo.hpp"

double Measure(std::function<void(std::string)> f, const std::string &seq) {
    clock_t start, end;
    start = clock();
    f(seq);
    end = clock();
    return static_cast<double>(end - start) / CLOCKS_PER_SEC * 1000.0;
}

int main() {
    const int n = 10000;
    RandomGenerator<std::string> rg;
    std::string seq = rg.generate(n);

    auto t0 = Measure([](std::string s) { removeNonMaximal(Naive(s)); }, seq);
    auto t1 = Measure([](std::string s) { removeNonMaximal(DivideConquer(s)); }, seq);
    auto t2 = Measure([](std::string s) { removeNonMaximal(DivideConquerFast(s)); }, seq);

    std::cout << "n: " << n << '\n';
    std::cout << "Naive:" << t0 << "[ms], DivideConquer: " << t1 << "[ms], DivideConquerFast: " << t2 << "[ms] \n";

    return 0;
}