import time
import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Spell corrector"))

from trie import Trie
from dictionary import Dictionary


dictionary = Dictionary()

trie = Trie()

start_time = time.perf_counter()

trie.build_from_dictionary(dictionary)

build_time = time.perf_counter() - start_time

print("\nDictionary loaded.")
print(f"Trie build time: {build_time:.4f} seconds")
print("Total words in Trie:", trie.word_count)

print("\nSearch tests:")

print("the:", trie.search("the"))
print("hello:", trie.search("hello"))
print("xyzabc:", trie.search("xyzabc"))

print("\nSearch Performance")

start_time = time.perf_counter()
trie.search("the")
search_time = time.perf_counter() - start_time

print(f"Search time for 'the': {search_time:.8f} seconds")

print("\nAutocomplete Performance")

start_time = time.perf_counter()
suggestions = trie.autocomplete("app")
autocomplete_time = time.perf_counter() - start_time

print("Suggestions:", suggestions)
print(f"Autocomplete time for 'app': {autocomplete_time:.8f} seconds")

print("\nPrefix Performance")

prefixes = ["a", "ap", "app", "z", "xyz"]

for prefix in prefixes:
    start_time = time.perf_counter()

    suggestions = trie.autocomplete(prefix)

    elapsed = time.perf_counter() - start_time

    print(
        f"'{prefix}' -> "
        f"{len(suggestions)} suggestions returned "
        f"in {elapsed:.8f} seconds"
    )

print("\nNumber of Words by Prefix")

prefixes = ["a", "ap", "app", "z", "xyz"]

for prefix in prefixes:
    count = trie.count_words_with_prefix(prefix)
    print(f"'{prefix}' -> {count} words")
