import logging
from typing import List, Tuple, Union
from functools import lru_cache
import numpy as np
from app.original_repo.helper1 import MathBase, validate_positive, compute_percentage
from app.original_repo.helper2 import AdvancedOperations

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StatisticalOperations(MathBase):
    def __init__(self, precision=2):
        super().__init__(precision)
        self._advanced_ops = AdvancedOperations()
        self._cache = {}

    def _memoize(self, key, calculation_func):
        if key not in self._cache:
            self._cache[key] = calculation_func()
        return self._cache[key]

    def power(self, a: float, b: float) -> float:
        """Enhanced power function with validation and logging"""
        logger.debug(f"Computing power: {a}^{b}")
        try:
            result = self.round_result(a**b)
            return result
        except OverflowError:
            logger.error(f"Overflow error for {a}^{b}")
            raise ValueError("Result too large to compute")

    def modulus(self, a: float, b: float) -> float:
        """Modulus with input validation"""
        if not self.validate_inputs(a, b):
            raise TypeError("Inputs must be numeric")
        if b == 0:
            raise ValueError("Modulus by zero")
        return self.round_result(a % b)

    def geometric_mean(self, values: List[float]) -> float:
        """Calculate geometric mean using power and nth root"""
        if not values:
            raise ValueError("Empty input list")
        n = len(values)
        product = 1.0
        for v in values:
            if v <= 0:
                raise ValueError("Geometric mean requires positive values")
            product = self._advanced_ops.multiply(product, v)
        return self.power(product, 1 / n)

    @lru_cache(maxsize=32)
    def fibonacci_power_sum(self, n: int, power: int) -> float:
        """Calculate sum of first n Fibonacci numbers raised to given power"""
        if n < 0 or power < 0:
            raise ValueError("Requires non-negative inputs")

        def fib(k):
            if k <= 1:
                return k
            return fib(k - 1) + fib(k - 2)

        total = 0
        for i in range(n):
            fib_num = fib(i)
            total += self.power(fib_num, power)
        return total

    def squareboth(self, a: float, b: float) -> Tuple[float, float]:
        """Enhanced square both function with validation"""
        if not self.validate_inputs(a, b):
            raise TypeError("Inputs must be numeric")
        return (self.power(a, 2), self.power(b, 2))

    def calculate_statistics(self, values: List[float]) -> dict:
        """Calculate comprehensive statistics for a list of values"""
        if not values:
            raise ValueError("Empty input list")

        def calc_stats():
            n = len(values)
            sorted_vals = sorted(values)
            mean = sum(values) / n
            median = (
                sorted_vals[n // 2]
                if n % 2
                else (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2
            )
            variance = sum((x - mean) ** 2 for x in values) / n

            return {
                "mean": self.round_result(mean),
                "median": self.round_result(median),
                "variance": self.round_result(variance),
                "std_dev": self.round_result(self.power(variance, 0.5)),
                "geometric_mean": self.geometric_mean(values),
            }

        return self._memoize(tuple(values), calc_stats)


# Module-level interface
_stats = StatisticalOperations()


def power(a: float, b: float) -> float:
    return _stats.power(a, b)


def modulus(a: float, b: float) -> float:
    return _stats.modulus(a, b)


def squareboth(a: float, b: float) -> Tuple[float, float]:
    return _stats.squareboth(a, b)


def calculate_statistics(values: List[float]) -> dict:
    return _stats.calculate_statistics(values)


def fibonacci_power_sum(n: int, power: int) -> float:
    return _stats.fibonacci_power_sum(n, power)
