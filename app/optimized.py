import time
import re
from collections import Counter


# Optimized function to find the top 10 most frequent words in a large dataset
def optimized_word_frequency(file_path, stop_words):
    """
    Reads a large text file and finds the top 10 most frequent words, excluding stop words.
    Optimized for performance using a single pass for counting and efficient data structures.

    Args:
        file_path (str): Path to the text file.
        stop_words (set): A set of common stop words to exclude.

    Returns:
        list: Top 10 words with their frequencies as tuples.
    """
    start_time = time.time()

    # Step 1: Read the file and tokenize words
    with open(file_path, "r", encoding="utf-8") as f:
        words = re.findall(r"\b\w+\b", f.read().lower())

    # Step 2: Count word frequencies while filtering out stop words in a single pass
    word_counter = Counter(word for word in words if word not in stop_words)

    # Step 3: Get the top 10 most frequent words
    top_10_words = word_counter.most_common(10)

    # Step 4: Print performance time
    print(f"Processing time: {time.time() - start_time:.2f} seconds")
    return top_10_words


# Example usage with stop words:
if __name__ == "__main__":
    stop_words = {"the", "and", "a", "to", "in", "of", "that", "it", "is", "was"}
    file_path = "./data/shakespeare.txt"  # Replace with the path to a large text file

    print("Top 10 Words:")
    print(optimized_word_frequency(file_path, stop_words))
