#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Repeat {
    int start, length, wholeLength;
    Repeat() {}
    Repeat(int start, int length, int wholeLength) : start(start),
                                                     length(length),
                                                     wholeLength(wholeLength) {}

    inline int end() const {
        return start + wholeLength;
    }

    friend std::ostream &operator<<(std::ostream &os, const Repeat &rep) {
        os << '[' << rep.start << ',' << rep.start + rep.length << "), length:" << rep.wholeLength;
        return os;
    }

    bool operator<(const Repeat &rep) {
        if (start != rep.start)
            return (start < rep.start);
        else if (end() != rep.end())
            return end() < rep.end();
        else
            return length < rep.length;
    }
};

std::vector<Repeat> Naive(const std::string &seq) {
    int n = seq.size();
    std::vector<Repeat> repeats;
    for (int i = 0; i < n; i++) {
        for (int length = 1; length <= (n - i) / 2; length++) {

            // pick only maximal one
            if (i > 0 && seq[i - 1] == seq[i + length - 1]) continue;

            int k = 0, now = i + length;
            while (now < n && seq[now] == seq[i + k]) {
                k++, now++;
                if (k == length) k = 0;
            }

            if ((now - i) / length <= 1) continue;
            repeats.emplace_back(i, length, (now - i));
        }
    }

    return repeats;
}

std::vector<Repeat> DivideConquer(const std::string &seq) {
    // std::cerr << "Seq: " << seq << '\n';
    int n = seq.size(), m = n / 2;

    // base case
    if (n <= 1)
        return {};

    std::vector<Repeat> repeats;
    auto L = DivideConquer(seq.substr(0, m));
    auto R = DivideConquer(seq.substr(m, n - m));

    // Lのうち極大なもののみcopyする.
    std::copy_if(L.begin(), L.end(), std::back_inserter(repeats), [&m, &seq](const Repeat &rep) {
        int end = rep.end();
        if (end != m)
            return true;
        if (seq[end] == seq[rep.start + rep.wholeLength % rep.length])
            return false;
        return true;
    });

    // Rのうち極大なもののみcopyする.
    std::for_each(R.begin(), R.end(), [&m](Repeat &rep) {
        return rep.start += m;
    });
    std::copy_if(R.begin(), R.end(), std::back_inserter(repeats), [&m, &seq](const Repeat &rep) {
        int start = rep.start;
        if (start != m)
            return true;
        if (start > 0 && seq[start - 1] == seq[start + rep.length - 1])
            return false;
        return true;
    });

    auto subprob = [&n, &repeats](const auto &s, int m, bool rev) {
        for (int length = 1; length <= m; length++) {

            // できるだけ左に行く.
            int left = m - length, kl = 0;
            while (left >= 0 && s[left] == s[m - length + kl]) {
                left--, kl--;
                if (kl == -1) kl = length - 1;
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

            // std::cout << "length: " << length << '\n'
            //           << "rev: " << rev << '\n'
            //           << "n: " << n << '\n'
            //           << "left: " << left << '\n'
            //           << "right: " << right << "\n\n";
            if (rev)
                repeats.emplace_back(n - right, length, right - left);
            else
                repeats.emplace_back(left, length, right - left);
        }
    };

    subprob(seq.begin(), m, false);
    subprob(seq.rbegin(), n - 1 - m, true);

    return repeats;
}

template <typename T>
std::vector<int> Z_algorithm(const T &s, const T &send) {
    int l = (int)(send - s);
    if (l == 0)
        return {};
    std::vector<int> Z(l);
    Z[0]  = l;
    int i = 1, j = 0;
    while (i < l) {
        while (i + j < l && s[j] == s[i + j])
            j++;
        Z[i] = j;

        if (j == 0) {
            i++;
            continue;
        }
        int k = 1;
        while (k < j && k + Z[k] < j) {
            Z[i + k] = Z[k];
            k++;
        }
        i += k;
        j -= k;
    }

    return Z;
}

std::vector<Repeat> DivideConquerFast(std::string seq) {
    // std::cerr << "Seq: " << seq << '\n';
    int n = seq.size(), m = n / 2;

    // base case
    if (n <= 1)
        return {};

    std::vector<Repeat> repeats;
    auto L = DivideConquerFast(seq.substr(0, m));
    auto R = DivideConquerFast(seq.substr(m, n - m));

    // Lのうち極大なもののみcopyする.
    std::copy_if(L.begin(), L.end(), std::back_inserter(repeats), [&m, &seq](const Repeat &rep) {
        int end = rep.end();
        if (end != m)
            return true;
        if (seq[end] == seq[rep.start + rep.wholeLength % rep.length])
            return false;
        return true;
    });

    // Rのうち極大なもののみcopyする.
    std::for_each(R.begin(), R.end(), [&m](Repeat &rep) {
        return rep.start += m;
    });
    std::copy_if(R.begin(), R.end(), std::back_inserter(repeats), [&m, &seq](const Repeat &rep) {
        int start = rep.start;
        if (start != m)
            return true;
        if (start > 0 && seq[start - 1] == seq[start + rep.length - 1])
            return false;
        return true;
    });

    auto subprob = [&n, &repeats](const std::string &s, int m, bool rev) {
        auto Zl = Z_algorithm(s.rbegin() + n - m, s.rend());
        Zl.push_back(0);
        std::string t(s.begin() + m, s.end());
        std::copy(s.begin(), s.end(), std::back_inserter(t));
        auto Zr = Z_algorithm(t.begin(), t.end());

        for (int length = 1; length <= m; length++) {

            // できるだけ左に行く.
            int left = m - length - Zl[length];

            // できるだけ右に行く.
            int right = std::min(m + Zr[n - length], n);

            // [left,right) はtandem-repeatになっている(ちょうど周期とは限らない).
            if (right - left < 2 * length) continue;

            // std::cout << "length: " << length << '\n'
            //           << "n: " << n << '\n'
            //           << "left: " << left << '\n'
            //           << "right: " << right << '\n';
            if (rev)
                repeats.emplace_back(n - right, length, right - left);
            else
                repeats.emplace_back(left, length, right - left);
        }
    };

    subprob(seq, m, false);
    std::reverse(seq.begin(), seq.end());
    subprob(seq, n - 1 - m, true);

    return repeats;
}

std::vector<Repeat> removeNonMaximal(std::vector<Repeat> repeats) {
    std::sort(repeats.begin(), repeats.end());
    std::vector<Repeat> answer;
    for (const auto &rep : repeats) {
        if (answer.size() > 0 && answer.back().start == rep.start && answer.back().end() == rep.end())
            continue;
        answer.push_back(rep);
    }
    return answer;
}

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