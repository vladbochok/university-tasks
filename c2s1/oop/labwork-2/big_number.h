#include <climits>
//
// Created by Vlad on 10.11.2020.
//

#ifndef LABWORK_2_BIG_NUMBER_H
#define LABWORK_2_BIG_NUMBER_H

#include <vector>

class BigNumber
{
protected:
    Static const unsigned int DEFAULT_BASE = 2;
    Static enum Sign {
        POSITIVE = 1,
        NEGATIVE = -1
    };

    std::vector <int> digits;
    unsigned int base;
    Sign sign;

    void shrink_to_fit();
    void abs();
    int exp();
public:
    BigNumber();
    BigNumber(long long); // TODO: maybe explicit?
    BigNumber(long long, int);
    BigNumber(std::vector<int>&); // TODO: maybe explicit?
    BigNumber(std::vector<int>&, int);

    BigNumber operator + (BigNumber);
    BigNumber operator - (BigNumber);
    BigNumber operator * (BigNumber);
    BigNumber operator / (BigNumber);
    BigNumber operator / (long long);
    BigNumber operator % (BigNumber);
    BigNumber operator % (long long);

    BigNumber& operator += (BigNumber&);
    BigNumber& operator -= (BigNumber&);
    BigNumber& operator *= (BigNumber&);
    BigNumber operator /= (BigNumber);
    BigNumber operator /= (long long);
    BigNumber operator %= (BigNumber);
    BigNumber operator %= (long long);

    BigNumber operator - ();

    bool operator < (BigNumber);
    bool operator <= (BigNumber);
    bool operator > (BigNumber);
    bool operator >= (BigNumber);
    bool operator == (BigNumber);
    bool operator != (BigNumber);
};


#endif //LABWORK_2_BIG_NUMBER_H
