import time
import unittest
from optimized import optimized_word_frequency


class TestOptimizationStatus(unittest.TestCase):
    def setUp(self):
        self.test_file = "./app/data/shakespeare.txt"
        self.stop_words = {
            "the",
            "and",
            "a",
            "to",
            "in",
            "of",
            "that",
            "it",
            "is",
            "was",
        }

    def test_optimized_speed(self):
        start_time = time.time()
        result = optimized_word_frequency(self.test_file, self.stop_words)
        end_time = time.time()
        solution = [
            ("i", 10555),
            ("you", 6514),
            ("my", 6031),
            ("not", 4036),
            ("with", 3858),
            ("s", 3760),
            ("his", 3717),
            ("for", 3709),
            ("me", 3623),
            ("he", 3447),
        ]
        self.assertEqual(result, solution)
        self.assertLess(
            end_time - start_time, 1, "Optimized function took longer than 1 second"
        )


if __name__ == "__main__":
    unittest.main()
