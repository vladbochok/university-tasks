#include <iostream>
#include "big_number.h"

int main() {
    BigNumber A(200);
    BigNumber B(4000);
    BigNumber C = A * B;
    std::cout << "A = " << A << " B = " << B << "C = " << C;
}
