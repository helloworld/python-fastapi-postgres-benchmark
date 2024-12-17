import time
import re
from collections import Counter


def word_frequency(file_path, stop_words):
    """
    Reads a large text file and finds the top 10 most frequent words, excluding stop words.

    Args:
        file_path (str): Path to the text file.
        stop_words (set): A set of common stop words to exclude.

    Returns:
        list: Top 10 words with their frequencies as tuples.
    """
    start_time = time.time()

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
        words = re.findall(r"\b\w+\b", text.lower())

    clean_words = []
    for word in words:
        if word not in stop_words:
            clean_words.append(word)

    unique_words = []
    word_frequencies = []
    for word in clean_words:
        if word not in unique_words:
            unique_words.append(word)
            word_frequencies.append((word, clean_words.count(word)))

    word_frequencies.sort(key=lambda x: x[1], reverse=True)

    top_10_words = word_frequencies[:10]

    print(f"Processing time: {time.time() - start_time:.2f} seconds")
    return top_10_words


if __name__ == "__main__":
    stop_words = {"the", "and", "a", "to", "in", "of", "that", "it", "is", "was"}
    file_path = "./data/shakespeare.txt"

    print("Top 10 Words:")
    print(word_frequency(file_path, stop_words))
