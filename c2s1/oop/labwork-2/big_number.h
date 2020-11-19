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
    BigNumber operator<< (int);

    bool operator<(const BigNumber &) const;
    bool operator<=(const BigNumber &) const;
    bool operator>(const BigNumber &) const;
    bool operator>=(const BigNumber &) const;
    bool operator==(const BigNumber &) const;
    bool operator!=(const BigNumber &) const;

    operator std::string();
    friend std::ostream& operator << (std::ostream&, BigNumber);

private:
    static const unsigned int DEFAULT_BASE = 10;
    enum Sign {
        POSITIVE = 1,
        NEGATIVE = -1
    };

    BigNumber add(BigNumber);
    BigNumber subtract(BigNumber);
    BigNumber karatsuba_multiply(BigNumber);
    BigNumber Toom_Cook(BigNumber, int);

    std::vector<int> digits; // number represents as vector
    unsigned int base;
    Sign sign;

    void shrink_to_fit();
    int exp() const;
};


#endif //LABWORK_2_BIG_NUMBER_H
