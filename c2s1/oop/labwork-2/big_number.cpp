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
            number *= -1;
            break;
        case -1:
            this->sign = NEGATIVE;
            break;
    }

    while (number > 0)
    {
        digits.push_back(number % base);
        number /= base;
    }
}

BigNumber::BigNumber(std::vector<int> &digits, int base) {
    this->digits = digits;
    this->base = base;
    this->sign = POSITIVE;
}

BigNumber::BigNumber(long long number): BigNumber(number, BigNumber::DEFAULT_BASE)  {}

BigNumber::BigNumber(): BigNumber(0, BigNumber::DEFAULT_BASE)  {}

BigNumber::BigNumber(std::vector<int> &digits) :BigNumber(digits, BigNumber::DEFAULT_BASE)  {}

BigNumber BigNumber::operator + (BigNumber other)
{
    BigNumber result;
    // Remove leading zero's.
    this->shrink_to_fit();
    other.shrink_to_fit();

    if (-other > *this && other.sign < 0)
    {
        result = (-other) + (-(*this));
        result = -result;
        return result;
    }

    if (-(*this) > other && sign < 0)
    {
        result = (-*this) + (-other);
        result = -result;
        return result;
    }

    // add zeros
    int n = (int)std::max(this->exp(), other.exp());
    while (exp() != n)
        digits.push_back(0);
    while (other.exp() != n)
        other.digits.push_back(0);

    result.digits = std::vector<int>(1,0);

    for (size_t i = 0; i < n; ++i)
    {
        int s = result.digits.back() + digits[i] * sign + other.digits[i] * other.sign;
        result.digits.back() = (s + 2 * base) % base;
        result.digits.push_back((s + 2 * base) / base - 2);
    }

    result.base = DEFAULT_BASE;
    result.sign = POSITIVE;

    result.shrink_to_fit();

    return result;
}

BigNumber& BigNumber::operator += (BigNumber& other)
{
    *this = *this + other;
    return *this;
}

BigNumber& BigNumber::operator - ()
{
    if(this->sign == POSITIVE) {
        result.sign = NEGATIVE;
    } else {
        result.sign = POSITIVE;
    }

    return result;
}

BigNumber BigNumber::operator - (BigNumber other)
{
    return *this + (-other);
}

BigNumber BigNumber::operator -= (BigNumber other)
{
    BigNumber result = *this - other;
    *this = result;
    return *this;
}

// Karatsuba
BigNumber BigNumber::operator * (BigNumber other)
{
    // Remove leading zero's.
    this->shrink_to_fit();
    other.shrink_to_fit();

    int n = std::max(exp(), other.exp());

    // add zeros
    while (exp() != n)
        digits.push_back(0);
    while (other.exp() != n)
        other.digits.push_back(0);

    // base case
    if (n == 0)
    {
        return BigNumber(0);
    }

    if (n == 1)
    {
        BigNumber A(digits[0] * other.digits[0]);
        if(this->sign == other.sign)
        {
            A.sign = POSITIVE;
        }
        else {
            A.sign = NEGATIVE;
        }
        return A;
    }

    // recursive calls
    int m = n / 2;
    std::vector<int> u0, u1, v0, v1;
    for (int i = 0; i < m; ++i)
    {
        u0.push_back(digits[i]);
        v0.push_back(other.digits[i]);
    }
    for (int i = m; i < n; ++i)
    {
        u1.push_back(digits[i]);
        v1.push_back(other.digits[i]);
    }

    BigNumber U0(u0), U1(u1), V0(v0), V1(v1);
    U0.sign = sign; U1.sign = sign; V0.sign = other.sign; V1.sign = other.sign;

    BigNumber M1 = U1 - U0, M2 = V0 - V1;

    BigNumber N1 = U1 * V1, N2 = M1 * M2, N3 = U0 * V0;

    BigNumber A = (N1 << (2 * m)) + (N1 << m) + (N2 << m) + (N3 << m) + N3;

    // Change sign and remove leading zero's.
    A.sign = A.sign == POSITIVE? NEGATIVE: POSITIVE;
    A.shrink_to_fit();

    return A;
}

BigNumber& BigNumber::operator *= (BigNumber& other)
{
    *this = *this * other;
    return *this;
}

BigNumber BigNumber::operator / (long long n)
{
    BigNumber result = *this;
    for (int i = (int)result.exp() - 1; i > 0; --i)
    {
        int s = result.digits[i];
        result.digits[i] /= n;
        result.digits[i - 1] += base * (s - other * result.digits[i]);
    }
    result.digits[0] /= n;

    return result;
}

BigNumber BigNumber::operator /= (long long n)
{
    *this = *this / n;
    return *this;
}

BigNumber BigNumber::operator / (BigNumber N)
{
    int other = N.exp();
    lreal T = lreal(*this) >> n;
    lreal R = lreal(N) >> n;
    lreal A = T / R;
    A = strip(A);
    return BigNumber(A.digits, A.decimal_point);
}

BigNumber BigNumber::operator /= (BigNumber N)
{
    BigNumber result = *this / N;
    *this = result;
    return *this;
}

BigNumber BigNumber::operator % (BigNumber N)
{
    return (*this - (*this / N) * N);
}

BigNumber BigNumber::operator %= (BigNumber N)
{
    *this -= (*this / N) * N;
    return *this;
}

BigNumber BigNumber::operator % (long long n)
{
    return (*this - (*this / n) * n);
}

BigNumber BigNumber::operator %= (long long n)
{
    *this -= (*this / n) * BigNumber(n);
    return *this;
}

BigNumber BigNumber::operator << (int n)
{
    BigNumber result = *this;
    for (int i = 0; i < n; ++i)
        result.digits.insert(result.digits.begin(), 0);
    return result;
}

BigNumber BigNumber::operator <<= (int n)
{
    *this = *this << n;
    return *this;
}

BigNumber BigNumber::operator >> (int n)
{
    BigNumber result = *this;
    for (int i = 0; i < n; ++i)
        result.digits.erase(result.digits.begin());
    return result;
}

BigNumber BigNumber::operator >>= (int n)
{
    *this = *this >> n;
    return *this;
}

bool BigNumber::operator < (BigNumber N)
{
    return (*this <= N) && (*this != N);
}

bool BigNumber::operator <= (BigNumber N)
{
    return *this == other || ! (N >= *this);
}

bool BigNumber::operator > (BigNumber N)
{
    return (*this >= N) && (*this != N);
}

bool BigNumber::operator >= (BigNumber N)
{
    // strip
    *this = strip(*this);
    other = strip(N);

    // basic checks
    if (sign > N.sign)
        return true;
    if (sign < N.sign)
        return false;
    if (exp() > N.exp())
        return true;
    if (exp() < N.exp())
        return false;

    // per digit comparison
    for (int i = (int)exp() - 1; i >= 0; --i)
    {
        if (digits[i] > N.digits[i])
            return true;
        if (digits[i] < N.digits[i])
            return false;
    }

    // equality case
    return true;
}

bool BigNumber::operator == (BigNumber N)
{
    *this = strip(*this);
    other = strip(N);

    // basic checks
    if (sign != N.sign)
        return false;
    if (exp() != N.exp())
        return false;

    // per digit comparison
    for (int i = 1; i <= exp(); ++i)
        if (digits[exp() - i] != N.digits[exp() - i])
            return false;

    // equality case
    return true;
}

bool BigNumber::operator != (BigNumber N)
{
    return !(*this == N);
}

void BigNumber::shrink_to_fit(BigNumber &) {

}

BigNumber::operator string()
{
    BigNumber result = strip(*this);

    string s = "";
    for (int i = 0; i < result.exp(); ++i)
        s = (char)(result.digits[i] + 48) + s;
    if (result.sign == -1)
        s = '-' + s;

    return s;
}

BigNumber abs(BigNumber N)
{
    BigNumber result = N;
    result.sign = 1;
    return result;
}

BigNumber strip(BigNumber N)
{
    BigNumber result = N;
    while (result.exp() > 1 && result.digits.back() == 0)
        result.digits.pop_back();
    return result;
}


ostream& operator << (ostream& out, BigNumber N)
{
    out << (string)N;
    return out;
}