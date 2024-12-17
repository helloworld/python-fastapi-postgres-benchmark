import time
import unittest

from optimized import optimized_search_function
from main import search_function


class TestOptimizationStatus(unittest.TestCase):
    def setUp(self):
        self.test_file = "./app/data/shakespeare.txt"
        with open(self.test_file, "r", encoding="utf-8") as f:
            text = f.read()
        self.lines = text.splitlines()
        self.query_string = "Alice"

    def test_optimized_speed(self):
        start_time = time.time()
        for i in range(10):
            result = optimized_search_function(self.lines, self.query_string)
        end_time = time.time()
        solution = 5
        self.assertEqual(len(result), solution)
        self.assertLess(
            end_time - start_time, 2, "Optimized function took longer than 2 seconds"
        )

    def test_unoptimized_speed(self):
        start_time = time.time()
        for i in range(10):
            result = search_function(self.lines, self.query_string)
        end_time = time.time()
        solution = 5
        self.assertEqual(len(result), solution)
        self.assertLess(end_time - start_time, 60, "Optimized function took very long")


if __name__ == "__main__":
    unittest.main()
