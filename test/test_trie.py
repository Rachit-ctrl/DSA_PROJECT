import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Spell corrector"))

from trie import Trie


trie = Trie()

trie.insert("cat", 100)
trie.insert("car", 200)
trie.insert("apple", 500)
trie.insert("app", 1000)
trie.insert("application", 300)
trie.insert("apply", 400)


print("Search Tests")
print("cat:", trie.search("cat"))
print("car:", trie.search("car"))
print("apple:", trie.search("apple"))
print("ca:", trie.search("ca"))
print("xyz:", trie.search("xyz"))

print("\nPrefix Tests")
print("app:", trie.starts_with("app"))
print("ap:", trie.starts_with("ap"))
print("ban:", trie.starts_with("ban"))

print("\nAutocomplete Test")
print("app:", trie.autocomplete("app"))