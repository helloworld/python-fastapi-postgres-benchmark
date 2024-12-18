from app.original_repo.helper1 import add, multiply
from app.original_repo.helper2 import subtract, divide, ceiling
from app.original_repo.helper3 import power, modulus, floordiv


def runner():
    result_add = add(5, 3)
    result_multiply = multiply(5, 3)
    result_subtract = subtract(2, 5)
    result_power = power(5, 3)
    return {
        "add": result_add,
        "multiply": result_multiply,
        "subtract": result_subtract,
        "power": result_power,
    }
