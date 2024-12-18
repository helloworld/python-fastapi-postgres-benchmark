from app.original_repo.helper1 import MathBase, validate_positive, compute_percentage
from functools import lru_cache

class AdvancedOperations(MathBase):
    def __init__(self, cache_size=128):
        super().__init__()
        self.cache_size = cache_size
        
    @lru_cache(maxsize=128)
    def divide(self, a, b):
        if not self.validate_inputs(a, b):
            raise TypeError("Inputs must be numeric")
        if b == 0:
            raise ValueError("Division by zero")
        return self.round_result(a / b)
    
    def subtract(self, a, b):
        if not self.validate_inputs(a, b):
            raise TypeError("Inputs must be numeric")
        return self.round_result(a - b)
    
    @validate_positive
    def calculate_ratio(self, a, b):
        """Calculate ratio as percentage and cache result"""
        raw_ratio = self.divide(a, b)
        return compute_percentage(raw_ratio, 1)

def subtract(a, b):
    return AdvancedOperations().subtract(a, b)

def divide(a, b):
    return AdvancedOperations().divide(a, b)

@lru_cache(maxsize=64)
def ceiling(a):
    """Cached ceiling implementation"""
    if not isinstance(a, (int, float)):
        raise TypeError("Input must be numeric")
    return int(-1 * a // 1 * -1)

def floordiv(a, b):
    """Floor division with validation"""
    ops = AdvancedOperations()
    if not ops.validate_inputs(a, b):
        raise TypeError("Inputs must be numeric")
    if b == 0:
        raise ValueError("Division by zero")
    return int(ops.divide(a, b))

def calculate_percentage_change(old_value, new_value):
    """Calculate percentage change between two values"""
    ops = AdvancedOperations()
    change = ops.subtract(new_value, old_value)
    return compute_percentage(change, abs(old_value))
