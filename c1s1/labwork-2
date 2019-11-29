"""
This module is designed to calculate function S value with given
accuracy at given point.

Functions:
    s - return value of function S

Global arguments:
    a, b - set the domain of S
"""
from math import fabs

a = -1
b = 1


def s(x: float, eps: float) -> float:
    """Return value of S at given point x with given accuracy - eps

    Arguments:
    x - should be real number at least -1 and at most 1.
    eps - should be real number greater 0.

    Don’t check if eps is positive number. If not so, do infinite loop.
    For non relevant x the result may be inaccurate.
    """
    el = x * x / 2
    sum = 0
    k = 0
    x4 = -x * x * x * x
    while fabs(el) >= eps:
        sum += el
        el *= x4 / ((4 * k + 3) * (4 * k + 4) * (4 * k + 5) * (4 * k + 6))
        k += 1
    sum += el
    return sum


print("Variant №3", "Vladyslav Bochok", sep="\n")
print("Calculating the value of the function S with given accuracy")
try:
    x = float(input(f"Input x - real number in the range from {a} to {b}: "))
    eps = float(input("Input eps - real positive number: "))
    # Check arguments for domain, calculate S, output
    if a <= x <= b and eps > 0:
        print("***** do calculations ...", end=" ")
        result = s(x, eps)
        print("done")
        print(f"for x = {x:.6f}", f"for eps = {eps:.4E}", f"result = {result:.8f}", sep="\n")
    else:
        print("***** Error")
        # Check x ans eps for domain, print error description
        if x < a or x > b:
            print(f"if x = {x:.6f} then S is not convergence to function F")
        if eps <= 0:
            print("The calculation cannot be performed if eps is not greater than zero. ")
except ValueError or KeyboardInterrupt:
    print("***** Error", "Wrong input: x and eps should be float", sep="\n")
