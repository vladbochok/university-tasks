//
// Created by Vlad on 10.11.2020.
//

#include "big_number.h"

BigNumber::BigNumber(long long number, int base) {
    this->base = base;

    // Hack to get `number_sign(number)`
    // ::std have not number_sign for primitive
    int number_sign = (number > 0) - (number < 0);

    switch (number_sign) {
        case 1:
            this->sign = POSITIVE;
            number *= -1;
            break;
        case -1:
            this->sign = NEGATIVE;
            break;
        case 0:
            this->sign = ZERO;
            digits.push_back(0);
            break;
    }

    while (number > 0)
    {
        digits.push_back(number % base);
        number /= base;
    }
}

BigNumber::BigNumber(std::vector<int> digits, int base) {
    this->digits = digits;
    this->base = base;
}

BigNumber::BigNumber(long long number): BigNumber(number, BigNumber::DEFAULT_BASE)  {}

BigNumber::BigNumber(): BigNumber(0, BigNumber::DEFAULT_BASE)  {}

BigNumber::BigNumber(std::vector<int> digits) :BigNumber(digits, BigNumber::DEFAULT_BASE)  {}
