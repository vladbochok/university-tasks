//
// Created by Vlad on 10.11.2020.
//

#include "big_number.h"

BigNumber::BigNumber(long long number, int base) {
    this->base = base;

    // Hack to get `number_sign(number)`
    // ::std have not number_sign for primitive type
    int number_sign = (number > 0) - (number < 0);

    switch (number_sign) {
        case 1:
            this->sign = POSITIVE;
            break;
        case -1:
            this->sign = NEGATIVE;
            number *= -1;
            break;
    }

    while (number > 0) {
        digits.push_back(number % base);
        number /= base;
    }
}

BigNumber::BigNumber(std::vector<int> &digits, int base) { // TODO: add check for correctness of vector
    this->digits = digits;
    this->base = base;
    this->sign = POSITIVE;
}

BigNumber::BigNumber(long long number) : BigNumber(number, BigNumber::DEFAULT_BASE) {}

BigNumber::BigNumber() : BigNumber(0, BigNumber::DEFAULT_BASE) {}

BigNumber::BigNumber(std::vector<int> &digits) : BigNumber(digits, BigNumber::DEFAULT_BASE) {}

BigNumber BigNumber::operator+(const BigNumber &Other) {
    BigNumber Result = this->add(Other);
    return Result;
}

BigNumber BigNumber::operator+=(const BigNumber &Other) {
    *this = *this + Other;
    return *this;
}

BigNumber BigNumber::operator-() {
    BigNumber result = *this;
    if (this->sign == POSITIVE) {
        result.sign = NEGATIVE;
    } else {
        result.sign = POSITIVE;
    }

    return result;
}

BigNumber BigNumber::operator-(const BigNumber &Other) {
    BigNumber Result = this->subtract(Other);
    return Result;
}

BigNumber BigNumber::operator-=(const BigNumber &Other) {
    *this = *this - Other;
    return *this;
}

// Karatsuba
BigNumber BigNumber::operator*(const BigNumber &Other) {
    BigNumber Result = this->karatsuba_multiply(Other);
    return Result;
}

BigNumber BigNumber::operator*=(const BigNumber &Other) {
    *this = *this * Other;
    return *this;
}

bool BigNumber::operator<(const BigNumber &Other) const {
    return (*this <= Other) && (*this != Other);
}

bool BigNumber::operator<=(const BigNumber &Other) const {
    return *this == Other || !(Other >= *this);
}

bool BigNumber::operator>(const BigNumber &Other) const {
    return (*this >= Other) && (*this != Other);
}

bool BigNumber::operator>=(const BigNumber &Other) const {
    // basic checks
    if (this->sign == POSITIVE && Other.sign == NEGATIVE || this->exp() > Other.exp())
        return true;
    if (this->sign == NEGATIVE && Other.sign == POSITIVE || this->exp() < Other.exp())
        return false;

    // per digit comparison
    for (int i = (int) exp() - 1; i >= 0; --i) {
        if (digits[i] != Other.digits[i])
            return digits[i] > Other.digits[i];
    }

    // equality case
    return true;
}

bool BigNumber::operator==(const BigNumber &Other) const {
    // basic checks
    if (sign != Other.sign || exp() != Other.exp())
        return false;

    // per digit comparison
    for (size_t i = 1; i <= exp(); ++i)
        if (digits[exp() - i] != Other.digits[exp() - i])
            return false;

    // equality case
    return true;
}

bool BigNumber::operator!=(const BigNumber &Other) const {
    return !(*this == Other);
}

void BigNumber::shrink_to_fit() {
    while (this->exp() > 1 && this->digits.back() == 0)
        this->digits.pop_back();
}

int BigNumber::exp() const {
    return this->digits.size();
}

BigNumber BigNumber::add(BigNumber Other) {
    BigNumber result;
    // Remove leading zero's.
    this->shrink_to_fit();
    Other.shrink_to_fit();

    if (-Other > *this && Other.sign == NEGATIVE) {
        result = (-Other).add(-(*this));
        result = -result;
        return result;
    }

    if (-(*this) > Other && sign == NEGATIVE) {
        result = (-*this).add(-Other);
        result = -result;
        return result;
    }

    int max_exp = (int) std::max(this->exp(), Other.exp());
    // add zeros
    while (exp() != max_exp)
        this->digits.push_back(0);
    while (Other.exp() != max_exp)
        Other.digits.push_back(0);

    result.digits = std::vector<int>(1, 0);

    for (size_t i = 0; i < max_exp; ++i) {
        int s = result.digits.back() + digits[i] * sign + Other.digits[i] * Other.sign;
        result.digits.back() = (s + 2 * base) % base;
        result.digits.push_back((s + 2 * base) / base - 2);
    }

    result.base = DEFAULT_BASE;
    result.sign = POSITIVE;

    result.shrink_to_fit();

    return result;
}

BigNumber BigNumber::subtract(BigNumber Other) {
    BigNumber Result = this->add(-Other);
    return Result;
}

BigNumber BigNumber::karatsuba_multiply(BigNumber Other) {
    // Remove leading zero's.
    this->shrink_to_fit();
    Other.shrink_to_fit();

    int n = std::max(exp(), Other.exp());

    // add zeros
    while (exp() != n)
        digits.push_back(0);
    while (Other.exp() != n)
        Other.digits.push_back(0);

    // base case
    if (n == 0) {
        return BigNumber(0);
    }

    if (n == 1) {
        BigNumber A(digits[0] * Other.digits[0]);
        if (this->sign == Other.sign) {
            A.sign = POSITIVE;
        } else {
            A.sign = NEGATIVE;
        }
        return A;
    }

    // recursive calls
    int m = n / 2;
    std::vector<int> u0, u1, v0, v1;
    for (int i = 0; i < m; ++i) {
        u0.push_back(digits[i]);
        v0.push_back(Other.digits[i]);
    }
    for (int i = m; i < n; ++i) {
        u1.push_back(digits[i]);
        v1.push_back(Other.digits[i]);
    }

    BigNumber U0(u0), U1(u1), V0(v0), V1(v1);
    U0.sign = sign;
    U1.sign = sign;
    V0.sign = Other.sign;
    V1.sign = Other.sign;

    BigNumber M1 = U1 - U0, M2 = V0 - V1;

    BigNumber N1 = U1 * V1, N2 = M1 * M2, N3 = U0 * V0;

    BigNumber Result = (N1 << (2 * m)) + (N1 << m) + (N2 << m) + (N3 << m) + N3;

    // Change sign and remove leading zero's.
    Result.sign = sign == Other.sign ? POSITIVE : NEGATIVE;
    Result.shrink_to_fit();

    return Result;
}

BigNumber BigNumber::operator << (int n)
{
    BigNumber New = *this;
    for (int i = 0; i < n; ++i)
        New.digits.insert(New.digits.begin(), 0);
    return New;
}

BigNumber::operator std::string()
{
    BigNumber New = *this;
    New.shrink_to_fit();

    std::string s;
    if (New.sign == NEGATIVE)
        s = "-";

    for (int i = New.exp() - 1; i >= 0; --i)
        s+= (char)(New.digits[i] + 48);

    return s;
}

std::ostream &operator<<(std::ostream &out, BigNumber Number) {
    out << (std::string) Number;
    return out;
}