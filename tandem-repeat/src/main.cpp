#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Repeat {
    int start, length, n_repeat;
    Repeat() {}
    Repeat(int start, int length, int n_repeat) : start(start),
                                                  length(length),
                                                  n_repeat(n_repeat) {}

    friend std::ostream &operator<<(std::ostream &os, const Repeat &rep) {
        os << '[' << rep.start << ',' << rep.start + rep.length << ")*" << rep.n_repeat;
        return os;
    }
};

std::vector<Repeat> Naive(const std::string &seq) {
    int n = seq.size();
    std::vector<Repeat> repeats;
    for (int i = 0; i < n; i++) {
        for (int length = 1; length <= (n - i) / 2; length++) {

            int k = 0, now = i + length;
            while (now < n) {
                if (seq[now] != seq[i + k]) break;
                k++, now++;
                if (k == length) k = 0;
            }

            if ((now - i) / length <= 1) continue;

            // pick only maximal one
            if (i - length >= 0 && std::equal(
                                       seq.begin() + i - length, seq.begin() + i,
                                       seq.begin() + i, seq.begin() + i + length)) continue;
            repeats.emplace_back(i, length, (now - i) / length);
        }
    }
    return repeats;
}

std::vector<Repeat> DivideConquer(const std::string &seq) {
    std::cerr << "Seq: " << seq << '\n';
    int n = seq.size(), m = n / 2;

    // base case
    if (n <= 1)
        return {};

    std::vector<Repeat> repeats;
    auto L = DivideConquer(seq.substr(0, m));
    auto R = DivideConquer(seq.substr(m, n - m));
    repeats.resize(L.size() + R.size());
    std::copy(L.begin(), L.end(), std::back_inserter(repeats));
    std::transform(
        R.begin(), R.end(), std::back_inserter(repeats), [&m](Repeat &rep) {
            rep.start += m;
            return rep;
        });

    auto subprob = [&n, &repeats](const auto &s, int m, bool rev) {
        for (int length = 1; length <= m; length++) {

            // できるだけ左に行く.
            int left = m - length, kl = 0;
            while (left >= 0 && s[left] == s[m - length + kl]) {
                left--, kl++;
                if (kl == length) kl = 0;
            }
            left++;

            // できるだけ右に行く.
            int right = m, kr = 0;
            while (right < n && s[right] == s[m - length + kr]) {
                right++, kr++;
                if (kr == length) kr = 0;
            }

            // [left,right) はtandem-repeatになっている(ちょうど周期とは限らない).
            if (right - left < 2 * length) continue;

            std::cout << "length: " << length << '\n'
                      << "n: " << n << '\n'
                      << "left: " << left << '\n'
                      << "right: " << right << '\n';
            if (rev)
                repeats.emplace_back(n - right, length, (right - left) / length);
            else
                repeats.emplace_back(left, length, (right - left) / length);
        }
    };

    subprob(seq.begin(), m, false);
    subprob(seq.rbegin(), n - 1 - m, true);

    return repeats;
}

int main() {
    std::cout << "Input String:\n";
    std::string seq;
    std::cin >> seq;

    std::cout << "Naive:\n";
    auto repeats = Naive(seq);
    for (const auto &rep : repeats)
        std::cout << rep << '\n';

    std::cout << "DivideConquer:\n";
    repeats = DivideConquer(seq);
    for (const auto &rep : repeats)
        std::cout << rep << '\n';
    return 0;
}