#include <climits>
//
// Created by Vlad on 10.11.2020.
//

#ifndef LABWORK_2_BIG_NUMBER_H
#define LABWORK_2_BIG_NUMBER_H

#include <vector>
#include <string>
#include <iostream>

class BigNumber {
public:
    BigNumber();

    BigNumber(long long); // TODO: maybe explicit?
    BigNumber(std::vector<int> &); // TODO: maybe explicit?

    BigNumber(long long, int);

    BigNumber(std::vector<int> &, int);

    BigNumber operator+(const BigNumber &);
    BigNumber operator-(const BigNumber &);
    BigNumber operator*(const BigNumber &);

    BigNumber operator+=(const BigNumber &);
    BigNumber operator-=(const BigNumber &);
    BigNumber operator*=(const BigNumber &);

    BigNumber operator-();

    bool operator<(const BigNumber &) const;
    bool operator<=(const BigNumber &) const;
    bool operator>(const BigNumber &) const;
    bool operator>=(const BigNumber &) const;
    bool operator==(const BigNumber &) const;
    bool operator!=(const BigNumber &) const;

private:
    static const unsigned int DEFAULT_BASE = 2;
    static enum Sign {
        POSITIVE = 1,
        NEGATIVE = -1
    };

    BigNumber add(BigNumber);
    BigNumber subtract(BigNumber);
    BigNumber karatsuba_multiply(BigNumber);

    std::vector<int> digits; // number represents as vector
    unsigned int base;
    Sign sign;

    void shrink_to_fit();
    int exp() const;
};


#endif //LABWORK_2_BIG_NUMBER_H
