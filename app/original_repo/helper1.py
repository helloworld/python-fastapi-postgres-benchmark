class MathBase:
    def __init__(self, precision=2):
        self.precision = precision
    
    def round_result(self, value):
        return round(value, self.precision)

    def validate_inputs(self, *args):
        return all(isinstance(x, (int, float)) for x in args)

class BasicOperations(MathBase):
    def add(self, a, b):
        if not self.validate_inputs(a, b):
            raise TypeError("Inputs must be numeric")
        return self.round_result(a + b)

    def multiply(self, a, b):
        if not self.validate_inputs(a, b):
            raise TypeError("Inputs must be numeric")
        return self.round_result(a * b)

def add(a, b):
    return BasicOperations().add(a, b)

def multiply(a, b):
    return BasicOperations().multiply(a, b)

def ceil(n):
    return int(-1 * n // 1 * -1)

def floor(n):
    return int(n // 1)

# Adding utility functions that will be used across modules
def validate_positive(func):
    def wrapper(*args):
        if any(x <= 0 for x in args):
            raise ValueError("All arguments must be positive")
        return func(*args)
    return wrapper

@validate_positive
def compute_percentage(value, total):
    return (value / total) * 100
