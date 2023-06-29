#include <algorithm>
#include <iostream>
#include <random>
#include <string>
#include <vector>

struct Repeat {
    int start, period, length;
    Repeat() {}
    Repeat(int start, int period, int length) : start(start),
                                                period(period),
                                                length(length) {}

    inline int end() const {
        return start + length;
    }

    friend std::ostream &operator<<(std::ostream &os, const Repeat &rep) {
        os << '[' << rep.start << ',' << rep.start + rep.length << "), period: " << rep.period;
        return os;
    }

    bool operator==(const Repeat &rep) const {
        return (start == rep.start) && (period == rep.period) && (length == rep.length);
    }

    bool operator<(const Repeat &rep) {
        if (start != rep.start)
            return (start < rep.start);
        else if (end() != rep.end())
            return end() < rep.end();
        else
            return period < rep.period;
    }
};

std::vector<Repeat> Naive(const std::string &seq) {
    int n = seq.size();
    std::vector<Repeat> repeats;
    for (int i = 0; i < n; i++) {
        for (int period = 1; period <= (n - i) / 2; period++) {

            // pick only maximal one
            if (i > 0 && seq[i - 1] == seq[i + period - 1]) continue;

            int k = 0, now = i + period;
            while (now < n && seq[now] == seq[i + k]) {
                k++, now++;
                if (k == period) k = 0;
            }

            if ((now - i) / period <= 1) continue;
            repeats.emplace_back(i, period, (now - i));
        }
    }

    return repeats;
}

void copyMaximal(
    std::vector<Repeat> &repeats,
    const std::string &seq,
    int m,
    std::vector<Repeat> &&L,
    std::vector<Repeat> &&R) {

    // Lのうち極大なもののみcopyする.
    std::copy_if(L.begin(), L.end(), std::back_inserter(repeats), [&m, &seq](const Repeat &rep) {
        int end = rep.end();
        if (end != m)
            return true;
        if (seq[end] == seq[rep.start + rep.length % rep.period])
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
        if (start > 0 && seq[start - 1] == seq[start + rep.period - 1])
            return false;
        return true;
    });
}

std::vector<Repeat> DivideConquer(const std::string &seq) {
    int n = seq.size(), m = n / 2;

    // base case
    if (n <= 1)
        return {};

    std::vector<Repeat> repeats;
    auto L = DivideConquer(seq.substr(0, m));
    auto R = DivideConquer(seq.substr(m, n - m));
    copyMaximal(repeats, seq, m, std::move(L), std::move(R));

    auto subprob = [&n, &repeats](const auto &s, int m, bool rev) {
        for (int period = 1; period <= m; period++) {

            // できるだけ左に行く.
            int left = m - period, kl = 0;
            while (left >= 0 && s[left] == s[m - period + kl]) {
                left--, kl--;
                if (kl == -1) kl = period - 1;
            }
            left++;

            // できるだけ右に行く.
            int right = m, kr = 0;
            while (right < n && s[right] == s[m - period + kr]) {
                right++, kr++;
                if (kr == period) kr = 0;
            }

            // [left,right) はtandem-repeatになっている(ちょうど周期とは限らない).
            if (right - left < 2 * period) continue;

            if (rev)
                repeats.emplace_back(n - right, period, right - left);
            else
                repeats.emplace_back(left, period, right - left);
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
    copyMaximal(repeats, seq, m, std::move(L), std::move(R));

    auto subprob = [&n, &repeats](const std::string &s, int m, bool rev) {
        auto Zl = Z_algorithm(s.rbegin() + n - m, s.rend());
        Zl.push_back(0);
        std::string t(s.begin() + m, s.end());
        std::copy(s.begin(), s.end(), std::back_inserter(t));
        auto Zr = Z_algorithm(t.begin(), t.end());

        for (int period = 1; period <= m; period++) {

            // できるだけ左に行く.
            int left = m - period - Zl[period];

            // できるだけ右に行く.
            int right = std::min(m + Zr[n - period], n);

            // [left,right) はtandem-repeatになっている(ちょうど周期とは限らない).
            if (right - left < 2 * period) continue;

            if (rev)
                repeats.emplace_back(n - right, period, right - left);
            else
                repeats.emplace_back(left, period, right - left);
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

/**
 * Random Generator
 */

template <class T>
class RandomGenerator {
  private:
    std::random_device seed_gen;
    std::mt19937 engine;
    std::uniform_int_distribution<T> rnd;
    T lower, upper;

  public:
    RandomGenerator() {}
    RandomGenerator(T lower, T upper) : engine(seed_gen()),
                                        lower(lower),
                                        upper(upper),
                                        rnd(lower, upper) {}

    T generate() {
        return rnd(engine);
    }
};

template <>
class RandomGenerator<std::string> {
    RandomGenerator<int> rg;

  public:
    RandomGenerator() : rg(0, 1) {
    }

    std::string generate(int length) {
        std::string s;
        for (int i = 0; i < length; i++)
            if (rg.generate() == 0)
                s += '0';
            else
                s += '1';
        return s;
    }
};