import math
 

def domain(x: float) -> bool:
    """Perform validation of the value range.

    Arguments:
    x - should be float.

    For non real the result may be unpredictable.
    """
    return x >= -14 and x != 6 and x != -7


def f(x: float) -> float:
    """Calculate expression value.

    Arguments:
    x should be real number greater or equal to -14, not equal 6, -7.

    For non relevant x the result may be unpredictable.
    """
    return math.tan(25 / 69) - 23 * math.pi + 650 * math.e / ((x - 6) * (x + 7)) + 13 * math.sin(x - 15) \
        - math.sqrt(x + 14)


def f_total(x: float) -> (bool, float):
    """Сheck the belonging of x to the area of allowable value and calculate the result of expression.

    Arguments:
    x - should be float.

    For non float the result may be unpredictable.
    For non relevant the result be (False, None).
    """
    if domain(x):
        return True, f(x)
    else:
        return False, None


print("Variant №3", "Expression calculation", "Vladyslav Bochok", "Print x", sep="\n")
try:
    x = float(input())
    print("***** do calculations ...", end=" ")

    isRelevant, result = f_total(x)
    print("done", f"for x = {x:.6f}", "result =", sep="\n", end=" ")

    if isRelevant:
        print(f"{result:.6f}")
    else:
        print("undefined")
except ValueError:
    print("wrong input")
