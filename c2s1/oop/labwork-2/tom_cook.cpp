//
// Created by Vlad on 19.11.2020.
// Used info https://iq.opengenus.org/toom-cook-algorithm-multiplication/"

#include "big_number.h"

const int TOOM_K = 3;

BigNumber BigNumber::Toom_Cook(BigNumber N) {
    this->shrink_to_fit();
    N.shrink_to_fit();

    int max_exp = (int) std::max(exp(), N.exp());

    // base case
    if (max_exp <= 1)
        return *this * N;

    max_exp += TOOM_K - 1;
    max_exp /= TOOM_K;
    max_exp *= TOOM_K;

    // add zeros
    while (exp() != max_exp)
        digits.push_back(0);
    while (N.exp() != max_exp)
        N.digits.push_back(0);

    // divide into parts
    int t = max_exp / TOOM_K;
    std::vector<int> m(TOOM_K + 1);
    for (int i = 0; i < TOOM_K; ++i)
        m[i] = i * t;
    m[TOOM_K] = max_exp;

    std::vector<BigNumber> U(TOOM_K), V(TOOM_K);
    for (int i = 0; i < TOOM_K; ++i) {
        std::vector<int> tmp_this(digits.begin() + m[i], digits.begin() + m[i + 1]);
        std::vector<int> tmp_N(std::vector<int>(N.digits.begin() + m[i], N.digits.begin() + m[i + 1]));
        U[i] = BigNumber(tmp_this);
        V[i] = BigNumber(tmp_N);
    }

    // compute W(i), i = 0..2r-2
    std::vector<BigNumber> W(2 * TOOM_K - 1);
    for (int i = 0; i < 2 * TOOM_K - 1; ++i) {
        BigNumber P(0), Q(0);
        for (int j = 0; j < TOOM_K; ++j) {
            P += U[j] * (long long) pow(i, j);
            Q += V[j] * (long long) pow(i, j);
        }

        W[i] = P * Q;
    }

    // compute "coefficients" of W
    for (int i = 1; i < 2 * TOOM_K - 1; ++i) {
        for (int j = 2 * TOOM_K - 2; j >= i; --j) {
            W[j] -= W[j - 1];
            W[j] /= i;
        }
    }

    // compute ai
    for (int i = 2 * TOOM_K - 3; i > 0; --i)
        for (int j = i; j < 2 * TOOM_K - 2; ++j)
            W[j] -= W[j + 1] * i;

    // compute answer
    BigNumber A(0);
    for (int i = 0; i < 2 * TOOM_K - 1; ++i)
        A += (W[i]) << (i * t);

    A.shrink_to_fit();

    return A;
}